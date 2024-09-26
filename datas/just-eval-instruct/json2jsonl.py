import json
import jsonlines
import sys, os


folder_path = "judgements/score_multi_gpt4"

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    filename = folder_path+"//"+ filename
    if not filename.endswith(".json"):
        continue
    # Input JSON file path
    input_json_file = filename

    # Output JSONL file path
    output_jsonl_file = filename.replace(".json", ".jsonl")

    # Read the JSON file and load its content
    with open(input_json_file, "r") as json_file:
        print(json_file.name)
        data = json.load(json_file)
        for item in data:
            for d in item["parsed_result"]:
                item["parsed_result"][d]["score"] = str(item["parsed_result"][d]["score"])

    # Open the JSONL file for writing
    with jsonlines.open(output_jsonl_file, "w") as jsonl_file:
        # Iterate through the list of dictionaries and write each dictionary as a JSON line
        # for item in data:
        jsonl_file.write_all(data)
