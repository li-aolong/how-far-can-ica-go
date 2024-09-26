

output_path='/home/liyinghao/papers/how_far_ica_go/outputs/alpaca-eval/base/[llama2-70b-GPTQ]_[urial_urial_claude3]'
log_file=$output_path/eval_100.log

alpaca_eval --model_outputs $output_path/output_eval_100.json \
            --name '[llama2-70b-GPTQ]_[urial_urial_claude3]_ref_[llama2-7b-chat]_[llama2-chat]' \
            --reference_outputs '/home/liyinghao/papers/how_far_ica_go/outputs/alpaca-eval/base/[llama2-7b-chat]_[llama2-chat]/output_eval_100.json' \
            --output_path "$output_path/ref_[llama2-7b-chat]_[llama2-chat]" \
            --precomputed_leaderboard '/home/liyinghao/papers/how_far_ica_go/outputs/alpaca-eval/base/leaderboard_refer_llama2-7b-chat.csv' \
            --is_overwrite_leaderboard True  2>&1 | tee $log_file
            # --max_instances 2 \
            # --leaderboard_mode_to_print verified \