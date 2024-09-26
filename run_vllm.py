import os
from vllm import LLM, SamplingParams
import json, csv
from tqdm import tqdm
from transformers import AutoTokenizer, LlamaForCausalLM
from datasets import load_dataset
import time
from outlines import models, generate
# os.environ['TOKENIZERS_PARALLELISM'] = 'false'

dataset = os.environ['dataset']
model_path = os.environ['model_path']
output_path = os.environ['output_path']
model_name = os.environ['model_name']
icl_name = os.environ['icl_name']
icl_path = os.environ['icl_path']
max_tokens = eval(os.environ['max_tokens'])
if 'min_tokens' in os.environ:
    min_tokens = eval(os.environ['min_tokens'])
else:
    min_tokens = 0
generator = f'[{model_name}]_[{icl_name}]'
batch_size = eval(os.environ['batch_size'])
output_file_name = os.environ['output_file_name']
gpu_num = len(os.environ['CUDA_VISIBLE_DEVICES'].split(','))

if os.environ['stop']:
    stop = eval(os.environ['stop'])
    if stop == [""]:
        stop = None
else:
    stop = None

print('stop符号为：', stop)
if 'use_json' in os.environ:
    use_json = eval(os.environ['use_json'])
    json_schema = """
{
    "type": "object",
    "properties": {
        "completion_code": {"type": "string"}
    }
}
"""
    print('use_json', use_json)
# exit()

if icl_name:
    prefix = open(os.path.join(icl_path, icl_name+'.txt')).read()

output_file = os.path.join(output_path, f'{output_file_name}.jsonl')
print('output_file', output_file)

tokenizer = AutoTokenizer.from_pretrained(model_path)

print(f'--- finish loading tokenizer: {model_path} ---')


def make_datas(dataset):
    datas = []

    def add_prompt_column(example, key_name="instruction"):
        instruction = example[key_name]
        example['prompt'] = prefix.format(query=instruction)
        return example

    # instruction
    if dataset == 'just-eval-instruct':
        datas = load_dataset("datas/just-eval-instruct", split="test")
        if icl_name:    # ICA
            datas = datas.map(add_prompt_column).to_list()
        else:   # chat模型
            datas = datas.to_list()
        datas = datas[-100:]
    
    # question
    if dataset == 'nq':
        with open('datas/nq/nq-test.qa.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                assert len(row) == 2
                question = row[0].capitalize()
                if question[-1] not in '.,?!;:':
                    question += '?'
                answers = eval(row[1])
                datas.append({'question': question, 'answer': answers, 'prompt': prefix.format(query=question)})

    # prompt
    if dataset == 'if-eval':
        datas = [json.loads(line) for line in open('datas/instruction_following_eval/input_data.jsonl')]

        for i, data in enumerate(datas):
            data['instruction'] = data['prompt']
            data['prompt'] = prefix.format(query=data['prompt'])

    if dataset == 'human-eval':
        datas = [json.loads(line) for line in open(f'datas/{dataset}/data.jsonl')]
        for i, data in enumerate(datas):
            datas[i]['prompt'] = prefix.format(query=data['prompt'])
    
    print('---------example------')
    for query_name in ['instruction', 'question', 'input']:
        if query_name in datas[0]:
            print(f'{query_name}:\n{datas[0][query_name]}')
    print('--'*5)
    print('Prompt:')
    print(datas[0]['prompt'])
    return datas



def run(llm, datas, output_file, sampling_params):
    for cur_id in tqdm(range(0, len(datas), batch_size)):
        batch_datas = datas[cur_id :cur_id + batch_size]
        batch_prompts = [data['prompt'] for data in batch_datas]

        if 'use_json' in os.environ and use_json:
            model_generator = generate.json(llm, json_schema)
            batch_outputs = model_generator(batch_prompts, sampling_params=sampling_params)
            print(batch_outputs)
            exit()
        else:
            batch_outputs = llm.generate(batch_prompts, sampling_params, use_tqdm=False)
            
        batch_outputs = [o.outputs[0].text for o in batch_outputs]

        with open(output_file, 'a') as f:
            for i, data in enumerate(batch_datas):
                data.update({'output': batch_outputs[i], 'generator': generator})
                f.write(json.dumps(data, ensure_ascii=False) + '\n')


if __name__ == '__main__':

    datas = make_datas(dataset)

    # exit()

    print('---finish load data---')

    # 跳过已经计算过的结果
    if os.path.exists(output_file):
        cur_datas = []
        for line in open(output_file):
            cur_datas.append(json.loads(line))

        print(f'已有{len(cur_datas)}个结果，计算剩余的{len(datas)-len(cur_datas)}个。')
        datas = datas[len(cur_datas):]

    print(f'开始计算{len(datas)}个数据。')

    sampling_params = SamplingParams(
        temperature=0, 
        max_tokens=max_tokens,
        stop=stop,
        include_stop_str_in_output=True,
        min_tokens=min_tokens
    )
    
    llm = LLM(
        model=model_path,
        tokenizer=model_path,
        gpu_memory_utilization=0.95,
        max_num_seqs=1,
        tensor_parallel_size=gpu_num,
        enforce_eager=True,
        trust_remote_code=True
    )
    
    if 'use_json' in os.environ and use_json:
        llm = models.VLLM(llm)

    # llm = None

    start = time.time()
    run(llm, datas, output_file, sampling_params)

    print(f'||||||||||||single exp time: {(time.time() - start)/3600}h')