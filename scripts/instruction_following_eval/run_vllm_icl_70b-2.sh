# /home/liyinghao/models/llama-2-7b
# /home/liyinghao/models/llama-2-7b-chat
# /home/liyinghao/models/modelscope/Llama-2-13b-ms/modelscope/Llama-2-13b-ms
# /home/liyinghao/models/modelscope/Llama-2-13b-chat-ms/modelscope/Llama-2-13b-chat-ms
# /home/liyinghao/share/yhli/models/Llama-2-70B-GPTQ
# /home/liyinghao/share/yhli/models/Llama-2-70B-Chat-GPTQ

dataset="if-eval"
model_name="llama2-70b"
model_path="/home/liyinghao/share/yhli/models/Llama-2-70B-GPTQ"
icl_name="chatml_urial_gpt4web"
icl_path="/home/liyinghao/papers/how_far_ica_go/prompts/table2"
stop="['<|im_end|>']"
output_file_name="outputs"
max_tokens=2048
batch_size=1

output_path=outputs/${dataset}/${model_name}/${icl_name}
echo "output_path: $output_path"
mkdir -p $output_path
cp /home/liyinghao/papers/how_far_ica_go/scripts/instruction_following_eval/run_vllm_icl_70b.sh $output_path
cp run_vllm.py $output_path
log_file=${output_path}/log.txt

CUDA_VISIBLE_DEVICES=0,1 output_file_name=$output_file_name batch_size=$batch_size icl_path=$icl_path max_tokens=$max_tokens icl_name=$icl_name dataset=$dataset model_name=$model_name stop=$stop output_path=$output_path model_path=$model_path python run_vllm.py 2>&1 | tee $log_file
