import json
from transformers import AutoTokenizer
import os

model_path = '/home/liyinghao/models/llama-2-7b'
tokenizer = AutoTokenizer.from_pretrained(model_path)


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

def process_path_files(path, file_name):
    count = 0

    for root, dirs, files in os.walk(path):
        for n, dir in enumerate(dirs):
            file_path = os.path.join(root, dir, file_name)
            if not os.path.exists(file_path):
                continue

            new_file_path = file_path.replace('.jsonl', '_evaluation.json')
            if os.path.exists(new_file_path):
                continue
        
            process_single_file(file_path, new_file_path)
            count += 1
            print(f'{count}---{dir}')

def process_single_file(file_path, new_file_path=''):
    stop_token = None

    if new_file_path == '':
        new_file_path = file_path.replace('.jsonl', '_evaluation.json')
        
    icl_name_splits = file_path.split('/')[-2].split('_')
    if len(icl_name_splits) >= 3:
        format_type = icl_name_splits[-3]
        if format_type == 'chatml':
            stop_token = '<|im_end|>'
        if format_type == 'md':
            stop_token = '```'
        if format_type == '0':
            stop_token = 'Query:'

    datas = []
    for i, line in enumerate(open(file_path)):
        # print(i)

        data = json.loads(line)

        output = data['output']
        if stop_token and (output.endswith(stop_token) or output.endswith('</s>')):
            finish_type = 'stop_token'
        else:
            finish_type = 'max_length'
        
            
        output = output.rstrip(stop_token).rstrip('</s>').strip()

        # 去重
        output = remove_repeated_text(output, '.\n').strip()
        output = remove_repeated_text(output, '\n').strip()
        output = remove_repeated_text(output, '. ').strip()
        output = remove_repeated_text(output, ', ').strip()

        prompt_word_length = len(data['prompt'].split())
        output_word_length = len(output.split())
        prompt_token_length = len(tokenizer.tokenize(data['prompt']))
        output_token_length = len(tokenizer.tokenize(output))
        
        data.update({
            'output': output,
            'prompt_word_length': prompt_word_length,
            'output_word_length': output_word_length,
            'prompt_token_length': prompt_token_length,
            'output_token_length': output_token_length,
            # 'finish_type': finish_type
        })
        datas.append(data)

    json.dump(datas, open(new_file_path, 'w'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    file_path = '/home/liyinghao/papers/how_far_ica_go/outputs/if-eval/llama2-70b/base/outputs.jsonl'
    process_single_file(file_path)
    print('finish')

    # path = '/home/liyinghao/papers/how_far_ica_go/outputs/if-eval'
    # file_name = 'outputs.jsonl'
    # process_path_files(path, file_name)
