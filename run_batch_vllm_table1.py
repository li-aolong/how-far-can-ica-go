import os
import subprocess

model_names = ['llama2-7b', 'llama2-13b', 'llama2-70b']
model_paths = ['/home/liyinghao/models/llama-2-7b', '/home/liyinghao/models/modelscope/Llama-2-13b-ms/modelscope/Llama-2-13b-ms', '/home/liyinghao/share/yhli/models/Llama-2-70B-GPTQ']
icl_names = ['0_0_0', '0_0_urial', '0_urial_0', '0_urial_urial', 'md_0_0', 'md_0_urial', 'md_urial_0']
icl_path = '/home/liyinghao/papers/how_far_ica_go/prompts/table1'

command_template = '''dataset="just-eval-instruct"
model_name={model_name}
model_path={model_path}
icl_name={icl_name}
icl_path={icl_path}
stop="{stop}"
max_tokens=2048
batch_size=1

output_path=outputs/just-eval-instruct/{model_name}/table1_{icl_name}
echo ------------$output_path------------
mkdir -p $output_path
cp run_vllm.py $output_path
cp run_batch_vllm_table1.py $output_path
log_file=outputs/just-eval-instruct/{model_name}/table1_{icl_name}/safe_100_table1.log

CUDA_VISIBLE_DEVICES=0 batch_size=$batch_size icl_path=$icl_path max_tokens=$max_tokens icl_name=$icl_name dataset=$dataset model_name=$model_name stop=$stop output_path=$output_path model_path=$model_path python run_vllm.py 2>&1 | tee $log_file'''

count = 0
for i, model_name in enumerate(model_names):
    if '70b' not in model_name.lower():
        continue
    model_path = model_paths[i]
    for icl_name in icl_names:
        icl_format = icl_name.split('_')[0]

        if icl_format == 'md':
            stop = "['\`\`\`']"

        if icl_format == 'chatml':
            stop = "['<|im_end|>', 'im_end']"
        
        if icl_format == '0':
            stop = "['Query:']"

        print(f'当前进度：{model_name}, {icl_name}')
        
        command = command_template.format(model_name=model_name, model_path=model_path, icl_name=icl_name, icl_path=icl_path, stop=stop)

        print('-----------command-----------')
        print(command)
        print('-----------command-----------')

        # count += 1

        # if count == 2:
        #     exit()

        subprocess.run(["bash", "-c", command], check=True)
        os.system('wait')
        print(f'======={model_name}=======end===={icl_name}========')