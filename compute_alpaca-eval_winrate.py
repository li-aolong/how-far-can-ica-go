import json

result_file = '/home/liyinghao/papers/how_far_ica_go/outputs/alpaca-eval/base/[llama2-13b]_[urial_urial_urial]/weighted_alpaca_eval_gpt4_turbo/annotations.json'

datas = json.load(open(result_file))

print(len(datas))

# for data in datas:
#     if data['raw_completion']['text'] not in ['m', 'M']:
#         print(data)
#         exit()
results = [data['raw_completion']['logprobs']['content'][0]['top_logprobs'][0]['token'] for data in datas]
switchs = [data['is_switched_outputs'] for data in datas]

wins = [1 if (switch and result == 'm') or (not switch and result == 'M') else 0 for result, switch in zip(results, switchs)]

print(sum(wins) / len(wins))