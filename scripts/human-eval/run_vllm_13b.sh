# /home/liyinghao/models/llama-2-7b
# /home/liyinghao/models/llama-2-7b-chat
# /home/liyinghao/models/modelscope/Llama-2-13b-ms/modelscope/Llama-2-13b-ms
# /home/liyinghao/models/modelscope/Llama-2-13b-chat-ms/modelscope/Llama-2-13b-chat-ms
# /home/liyinghao/share/yhli/models/Llama-2-70B-GPTQ
# /home/liyinghao/share/yhli/models/Llama-2-70B-Chat-GPTQ

dataset="human-eval"
model_name="llama2-13b-chat"
model_path="/home/liyinghao/models/modelscope/Llama-2-13b-chat-ms/modelscope/Llama-2-13b-chat-ms"
icl_name="llama2-chat-system"
icl_path="/home/liyinghao/papers/how_far_ica_go/prompts"
stop="['']"
output_file_name="outputs"
max_tokens=2048
batch_size=1

output_path=outputs/${dataset}/${model_name}/${icl_name}
echo "output_path: $output_path"
mkdir -p $output_path
cp /home/liyinghao/papers/how_far_ica_go/scripts/human-eval/run_vllm_13b.sh $output_path
cp run_vllm.py $output_path
log_file=${output_path}/log.txt

CUDA_VISIBLE_DEVICES=0 output_file_name=$output_file_name batch_size=$batch_size icl_path=$icl_path max_tokens=$max_tokens icl_name=$icl_name dataset=$dataset model_name=$model_name stop=$stop output_path=$output_path model_path=$model_path python run_vllm.py 2>&1 | tee $log_file
