urial="inst_1k_v4" # urial prompt name -->  `urial_prompts/{urial}.txt`
output_dir="result_dirs/just_eval/vllm_urial=${urial}"  

mkdir -p $output_dir

CUDA_VISIBLE_DEVICES=0 python /home/liyinghao/codes/URIAL/src/unified_infer.py \
    --urial $urial \
    --engine vllm \
    --model_name "/home/liyinghao/models/llama-2-7b" \
    --tensor_parallel_size 1 \
    --dtype 'auto' \
    --data_name "just_eval" \
    --top_p 1.0 --temperature 0 --repetition_penalty 1.0 \
    --batch_size 1 --max_tokens 2048 \
    --end_index 1 \
    --output_folder $output_dir 2>&1 | tee ${output_dir}/log.txt