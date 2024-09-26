from datasets import load_dataset
import random
import jsonlines 

random.seed(1337)

dataset = load_dataset("Anthropic/hh-rlhf", data_dir="red-team-attempts")
def filter(x):
  if "What is an offensive" in x["task_description"]:
    return False 
  if "the assistant" in x["task_description"]:
    return False
  return x["rating"]>=4.0 and x["task_description"].endswith("?") and x["min_harmlessness_score_transcript"] < -1.0

filtered_data = [(x, x["min_harmlessness_score_transcript"]) for x in dataset["train"] if filter(x)]
filtered_data.sort(key=lambda x: x[1])
print(len(filtered_data))
# sampled_data = random.sample(filtered_data[:200], k=100)
sampled_data = filtered_data[:100]



red_team_data = []
for idx, (x, _) in enumerate(sampled_data):
    # print(x)
    # exit()
    item = {"id": 800+len(red_team_data), 
            "instruction": x["task_description"], 
            "source_id": f"red_team-{idx}", 
            "dataset": "hh-rlhf/red-team-attempts", "category": "safety", "output": "N/A", "generator": None}
    red_team_data.append(item)

with open("legacy/MaliciousInstruct.txt", "r") as f:
    lines = f.readlines()
    for idx, l in enumerate(lines):
        item = {"id": 800+len(red_team_data), 
                "instruction": l.strip(),
                "source_id": f"MaliciousInstruct-{idx}",
                "dataset": "MaliciousInstruct", "category": "safety", "output": "N/A", "generator": None}
        red_team_data.append(item)


with jsonlines.open('test_red.jsonl', mode='w') as writer:
    writer.write_all(red_team_data)
    
# from huggingface_hub import HfApi
# api = HfApi() 
# api.upload_file(
#     path_or_fileobj=f"src/red_team/test.jsonl",
#     path_in_repo=f"test.jsonl",
#     repo_id="yuchenlin/just-eval-redteam",
#     repo_type="dataset", 
#     # create_pr=1
# )