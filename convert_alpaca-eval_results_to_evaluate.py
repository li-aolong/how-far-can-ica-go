import json

file = '/home/liyinghao/codes/alpaca_eval/results/gpt4_1106_preview/model_outputs.json'
# generator = '[llama2-13b]_[urial_urial_urial]'

new_datas = []

# for i, line in enumerate(open(file)):
for i, line in enumerate(json.load(open(file))):

    if i >= 100:
        break
    # data = json.loads(line)
    data = line

    new_data = {
        'instruction': data['instruction'],
        'output': data['output'].strip('```').strip('<|im_end|>').strip(),
        'generator': data['generator'],
        'dataset': data['dataset'],
    }
    new_datas.append(new_data)

new_file = file.replace('model_outputs.json', 'output_eval_100.json')
json.dump(new_datas, open(new_file, 'w'), indent=2, ensure_ascii=False)

print('finish')