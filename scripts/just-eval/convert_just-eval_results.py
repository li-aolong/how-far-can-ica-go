import json
from transformers import AutoTokenizer
import os

model_path = '/home/liyinghao/models/llama-2-7b'

# file = '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-7b/table1_md_0_0/output_safe_100.jsonl'
path = '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/md_urial_gpt4web-3'
file_name = 'output_safe_100.jsonl'
count = 0

def remove_repeated_text(text, split_token='\n'):
    lines = text.split(split_token)
    seen = set()
    result = []
    for line in lines:
        # 排除两个类似\n连在一起的情况
        if not line.strip():
            result.append(line)
            continue

        line_content = line

        # 处理序号增加，但内容不变的文本
        parts = line.split('. ', 1)
        if len(parts) == 2 and parts[0].isdigit():
            line_content = parts[1]          

        # 处理分割后的重复文本
        if line_content not in seen:
            result.append(line)
            seen.add(line_content)
        else:
            # 被split_token切开并留下的第一个重复字符串需要把split_token加上
            result[-1] = result[-1] + split_token
            # If we see the same line again, stop processing further lines
            break
        
    return split_token.join(result)

def process_single_file(path):
    file_path = os.path.join(path, file_name)
    if not os.path.exists(file_path):
        return

    new_file_path = file_path.replace('.jsonl', '_evaluation.json')
    if os.path.exists(new_file_path):
        return
    print(new_file_path)

    icl_name_splits = file_path.split('/')[-2].split('_')
    stop_token = ''
    if len(icl_name_splits) >= 3:
        format_type = icl_name_splits[-3]
        if format_type == 'chatml':
            stop_token = '<|im_end|>'
        elif format_type == 'md':
            stop_token = '```'
        elif format_type == '0':
            stop_token = 'Query:'

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    datas = []
    for i, line in enumerate(open(file_path)):
        # print(i)

        data = json.loads(line)

        output = data['output']
        if output.endswith(stop_token):
            finish_type = 'stop_token'
        else:
            finish_type = 'max_length'
            
        output = output.rstrip(stop_token).strip()

        # 去重
        output = remove_repeated_text(output, '\n').strip()
        output = remove_repeated_text(output, '. ').strip()
        output = remove_repeated_text(output, ', ').strip()
        output = remove_repeated_text(output, '.\n').strip()

        prompt_length = len(tokenizer.tokenize(data['prompt']))
        output_length = len(tokenizer.tokenize(output))
        
        data.update({
            'output': output,
            'prompt_length': prompt_length,
            'output_length': output_length,
            'finish_type': finish_type
        })
        datas.append(data)

    json.dump(datas, open(new_file_path, 'w'), indent=2, ensure_ascii=False)

    print('finish')

    
for root, dirs, files in os.walk(path):

    process_single_file(root)

    for n, dire in enumerate(dirs):
        path = os.path.join(root, dire)
        process_single_file(path)
        count += 1
        print(f'{count}---{dire}')

    break