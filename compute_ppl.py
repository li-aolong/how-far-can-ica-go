import torch, os, json, math
from transformers import AutoTokenizer, AutoModelForCausalLM
from vllm import LLM, SamplingParams

# /home/liyinghao/models/llama-2-7b
# /home/liyinghao/models/modelscope/Llama-2-13b-ms/modelscope/Llama-2-13b-ms
# /home/liyinghao/share/yhli/models/Llama-2-70B-GPTQ
model_path = '/home/liyinghao/share/yhli/models/Llama-2-70B-GPTQ'

tokenizer = AutoTokenizer.from_pretrained(model_path)
if '70B' not in model_path:
    # hf
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map=f'auto', torch_dtype=torch.float16)
    model.eval()
else:
    # vllm
    sampling_params = SamplingParams(
        temperature=0, 
        max_tokens=1,
        include_stop_str_in_output=False,
        prompt_logprobs=1
    )
    llm = LLM(
        model=model_path,
        tokenizer=model_path,
        gpu_memory_utilization=0.99,
        max_num_seqs=1,
        enforce_eager=True,
    )

def hf_ppl(text):
    # 将输入文本编码为模型输入
    inputs = tokenizer(text, return_tensors='pt').to('cuda')
    input_ids = inputs['input_ids']

    with torch.no_grad():
        # 获取模型输出
        outputs = model(input_ids, labels=input_ids)
        loss = outputs.loss
    
    # 计算困惑度
    perplexity = torch.exp(loss)
    return perplexity.item()

def vllm_ppl(text):
    if len(tokenizer.tokenize(text)) > 500:
        text = text[:int(len(text)/3)]
    output = llm.generate(text, sampling_params, use_tqdm=False)
    # print(text[:int(len(text)/5)])
    # exit()

    logprobs = [list(prompt_logprob.values())[0].logprob for prompt_logprob in output[0].prompt_logprobs if prompt_logprob]
    ppl = math.exp(- (sum(logprobs) / len(logprobs)))
    # print(ppl)
    # exit()

    return ppl

def average_perplexity(texts):
    # 计算每个文本的困惑度
    if '70B' not in model_path:
        perplexities = [hf_ppl(text) for text in texts]
    else:
        perplexities = [vllm_ppl(text) for text in texts]

    # 计算平均困惑度
    avg_perplexity = sum(perplexities) / len(perplexities)
    return perplexities, avg_perplexity
    
paths = [
    # '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_0_0',
    # '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_0_0-2',
    # '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_0_0-3',
    '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_urial_0',
    # '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_urial_0-2',
    # '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_urial_0-3',
    # '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_urial_urial',
    # '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_urial_urial-2'
]

all_ppls = {}

for path in paths:
    file = os.path.join(path, 'output_100_evaluation.json')
    datas = json.load(open(file))

    texts = [data['prompt'] + data['output'] for data in datas]
    # texts = [data['output'] for data in datas]
    # texts = [f"[INST] {data['prompt'] + data['output']} [/INST]" for data in datas]

    ppls, avg_ppl = average_perplexity(texts)
    print(f"{path.split('/')[-1]} Average Perplexity: {avg_ppl:.2f}")

    all_ppls = {index: value for index, value in enumerate(ppls)}

    json.dump(all_ppls, open(os.path.join(path, '[70B-model]_all_query-output_ppls.json'), 'w'), indent=2, ensure_ascii=False)
    open(os.path.join(path, '[70B-model]_avg_query-output_ppl.txt'), 'w').write(str(avg_ppl))