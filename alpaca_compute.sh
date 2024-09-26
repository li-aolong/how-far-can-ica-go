

alpaca_eval --model_outputs '/home/liyinghao/codes/alpaca_eval/results/llama-2-70b-chat-hf/model_outputs.json' \
            --precomputed_leaderboard '/home/liyinghao/codes/alpaca_eval/results/llama-2-70b-chat-hf/weighted_alpaca_eval_gpt4_turbo/leaderboard.csv' \
            --is_recompute_metrics_only \
            --output_path '/home/liyinghao/codes/alpaca_eval/results/llama-2-70b-chat-hf' \
            --is_overwrite_leaderboard True \
            # --precomputed_leaderboard None \
            # --max_instances 2 
            # --leaderboard_mode_to_print verified \