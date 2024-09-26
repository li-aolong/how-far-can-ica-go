import os
import subprocess

model_names = ['llama2-7b-chat', 'llama2-13b-chat', 'llama2-70b-chat']
model_paths = ['/home/liyinghao/models/llama-2-7b-chat', '/home/liyinghao/models/modelscope/Llama-2-13b-chat-ms/modelscope/Llama-2-13b-chat-ms', '/home/liyinghao/share/yhli/models/Llama-2-70B-Chat-GPTQ']
icl_names = ['llama2-chat', 'llama2-chat-system']
icl_path = '/home/liyinghao/papers/how_far_ica_go/prompts'

command_template = '''dataset="just-eval-instruct"
model_name={model_name}
model_path={model_path}
icl_name={icl_name}
icl_path={icl_path}
stop="{stop}"
output_file_name="output_safe_100"
max_tokens=2048
batch_size=1

output_path=outputs/just-eval-instruct/{model_name}/{icl_name}
echo ------------$output_path------------
mkdir -p $output_path
cp run_vllm.py $output_path
cp run_batch_vllm_chat-model.py $output_path
log_file=outputs/just-eval-instruct/{model_name}/{icl_name}/help_100.log

CUDA_VISIBLE_DEVICES=0 output_file_name=$output_file_name batch_size=$batch_size icl_path=$icl_path max_tokens=$max_tokens icl_name=$icl_name dataset=$dataset model_name=$model_name stop=$stop output_path=$output_path model_path=$model_path python run_vllm.py 2>&1 | tee $log_file'''

count = 0
for i, model_name in enumerate(model_names):
    model_path = model_paths[i]
    for icl_name in icl_names:
        icl_format = icl_name.split('_')[0]

        if icl_format == 'md':
            stop = "['\`\`\`']"

        elif icl_format == 'chatml':
            stop = "['<|im_end|>']"
        
        elif icl_format == '0':
            stop = "['Query:']"
        
        else:   # chat模型
            stop = "['']"

        print(f'当前进度：{model_name}, {icl_name}')
        
        command = command_template.format(model_name=model_name, model_path=model_path, icl_name=icl_name, icl_path=icl_path, stop=stop)

        print('-----------command-----------')
        print(command)
        print('-----------command-----------')

        # count += 1

        # if count == 2:
        #     exit()

        subprocess.run(["bash", "-c", command], check=True)
        # os.system(command)
        os.system('wait')
        print(f'======={model_name}=======end===={icl_name}========')
        # exit()