import json
# data = json.load(open('/home/liyinghao/codes/alpaca_eval/src/alpaca_eval/evaluators_configs/weighted_alpaca_eval_gpt4_turbo/annotations_seed0_configs.json'))
# print(len(data))
# print(data[-1])
# exit()
file = '/home/liyinghao/codes/alpaca_eval/results/llama-2-7b-chat-hf/model_outputs.json'

datas = json.load(open(file))[:100]

print(datas[0].keys())
# exit()

# for i in range(len(datas)):
#     if i > 99:
#         break
#     origin_datas.append({
#         'instruction': datas[i]['instruction'],
#         'output_1': datas[i]['output_1'],
#         'output_2': datas[i]['output_2'],
#         'annotator': datas[i]['annotator'],
#         'preference': datas[i]['preference'],
#         'price_per_example': datas[i]['price_per_example'],
#         'raw_completion': datas[i]['raw_completion'],
#         'time_per_example': datas[i]['time_per_example'],
#     })

new_file = '/home/liyinghao/papers/how_far_ica_go/alpaca-eval_outputs/llama2-7b-chat/model_outputs.json'
json.dump(datas, open(new_file, 'w'), indent=2, ensure_ascii=False)
print('finish')