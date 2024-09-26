import json
import os
import numpy as np

model = 'llama2-70b'
icl = '0-urial-0'

help_path = '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/md_urial_gpt4web-2/output_safe_100_evaluation.json'
safe_path = '/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/table1_0_urial_0/output_safe_100_evaluation.json'
# safe_path = help_path.replace('help', 'safe')

assert 'evaluation' in help_path and 'evaluation' in safe_path

datas = json.load(open(help_path))
# safe_datas = json.load(open(safe_path))
# datas.extend(safe_datas)

input_lengths = [len(data['prompt'].split()) for data in datas]
output_lengths = [len(data['output'].split()) for data in datas]
input_avg_length = np.mean(input_lengths)
output_avg_length = np.mean(output_lengths)

# assert len(output_lengths) == 200

# open('/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/all_word_avg_length.txt', 'a').write(f"{model} {icl} {round(input_avg_length)} {round(output_avg_length)} \n")
print(round(input_avg_length), round(output_avg_length))