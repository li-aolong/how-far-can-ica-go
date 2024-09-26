import json 
import jsonlines

# Load test_all.jsonl
with jsonlines.open('legacy/test_all.jsonl') as reader:
    data = [obj for obj in reader]

# Load tags_list.json

with open('legacy/tags_list.json') as f:
    tags_list = json.load(f)
    
for data_item, tag_item in zip(data, tags_list):
    data_item['task'] = tag_item["task_types"]
    data_item['topic'] = tag_item["topics"]
    data_item["difficulty"] = "N/A"
    del data_item["output"]
    del data_item["generator"]

with open('test_all_with_tags.jsonl', 'w') as outfile:
    jsonlines.Writer(outfile).write_all(data)
