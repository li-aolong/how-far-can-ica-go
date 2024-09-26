import json

file = '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_urial_0/output_100.jsonl'

# json
# for data in json.load(open(file)):
#     print(data['prompt'])
#     print('-------\n')

#     print(data['output'])
    
#     break

# jsonl
for i, line in enumerate(open(file)):
    data = json.loads(line)

    if i < 2:
        continue

    print(data['prompt'])
    print('-------\n')

    print(data['output'])
    
    break