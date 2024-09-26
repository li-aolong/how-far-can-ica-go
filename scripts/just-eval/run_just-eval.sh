result_file="/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/llama2-70b/md_urial_gpt4web-3/output_safe_100_evaluation.json"
# gpt-4o-2024-05-13  gpt-3.5-turbo-0125
gpt_model="gpt-4o-2024-05-13"
output_file=${result_file/.json/.${gpt_model}.json}
log_file=${result_file/.json/.${gpt_model}.log}
# score_multi, score_safety
mode="score_safety"

just_eval \
    --mode $mode \
    --gpt_model ${gpt_model} \
    --model_output_file $result_file \
    --eval_output_file $output_file 2>&1 | tee $log_file

just_eval \
    --report_only \
    --mode $mode \
    --eval_output_file $output_file  2>&1 | tee -a $log_file