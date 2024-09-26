# Content of `--input_response_data` should be like:
# {"prompt": "Write a 300+ word summary ...", "response": "PUT YOUR MODEL RESPONSE HERE"}
# {"prompt": "I am planning a trip to ...", "response": "PUT YOUR MODEL RESPONSE HERE"}
# ...

python3 -m instruction_following_eval.evaluation_main \
  --input_data=/home/liyinghao/papers/how_far_ica_go/datas/instruction_following_eval/input_data.jsonl \
  --input_response_data="/home/liyinghao/papers/how_far_ica_go/outputs/if-eval/llama2-7b/base/outputs_evaluation.json"
  # --output_dir=/home/liyinghao/papers/how_far_ica_go/outputs/if-eval/llama2-7b/0_urial_urial

exit 0