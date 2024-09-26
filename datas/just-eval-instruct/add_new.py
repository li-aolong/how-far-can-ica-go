import json 
from datasets import load_dataset
import random 
import jsonlines

random.seed(42)
  
jsonl_file_path = 'test_486.jsonl'

with jsonlines.open(jsonl_file_path, 'r') as reader:
    just_eval_data = [item for item in reader]

print(len(just_eval_data))

just_eval_data = [x for x in just_eval_data if x["dataset"]!="lima"]
ae_dataset = list(load_dataset("tatsu-lab/alpaca_eval", "alpaca_eval", split="eval"))
lima_dataset = list(load_dataset("GAIR/lima", split="test"))
mt_dataset = list(load_dataset("HuggingFaceH4/mt_bench_prompts", split="train"))

all_inputs = [x["instruction"] for x in just_eval_data]

cnt = 0 
just_eval_data_new = []
for ind, item in enumerate(ae_dataset):
    if item["instruction"] in all_inputs:
        just_eval_data_new.append(dict(id=len(just_eval_data_new), instruction=item["instruction"], source_id=f"alpaca_eval-{ind}", dataset=item["dataset"], category="regular", output="N/A", generator=None))  
        continue
    if ind < 150:
        continue
    if len(item["instruction"].split()) >= 30:
        continue
    if random.uniform(0, 1) < 0.5:
        continue
    just_eval_data_new.append(dict(id=len(just_eval_data_new), instruction=item["instruction"], source_id=f"alpaca_eval-{ind}", dataset=item["dataset"], category="regular", output="N/A", generator=None))  
    cnt += 1
    # just_eval_data.append(dict(id=len(just_eval_data), instruction=item["instruction"], source_id=f"alpaca_eval-{len(just_eval_data)}", dataset=item["dataset"], category="regular", output="N/A", generator=None))
    if len(just_eval_data_new) == 420:
        break 
    
print(len(just_eval_data_new))

for ind, item in enumerate(lima_dataset):  
    just_eval_data_new.append(dict(id=len(just_eval_data_new), instruction=item["conversations"][0], source_id=f"lima-{ind}", dataset="lima", category="regular", output="N/A", generator=None))

print(len(just_eval_data_new))
    
for ind, item in enumerate(mt_dataset):  
    just_eval_data_new.append(dict(id=len(just_eval_data_new), instruction=item["prompt"][0], source_id=f"mt-{item['prompt_id']}-{item['category']}", dataset="mt", category="regular", output="N/A", generator=None))

print(len(just_eval_data_new))

with jsonlines.open('test_regular.jsonl', mode='w') as writer:
    writer.write_all(just_eval_data_new)