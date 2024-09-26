import os, time
import subprocess

model_names = ['llama2-7b', 'llama2-13b', 'llama2-70b']
model_paths = ['/home/liyinghao/models/llama-2-7b', '/home/liyinghao/models/modelscope/Llama-2-13b-ms/modelscope/Llama-2-13b-ms', '/home/liyinghao/share/yhli/models/Llama-2-70B-GPTQ']
icl_names = ['md_urial_urial', 'md_urial_urial-2', 'md_urial_urial-3', 'base']
icl_path = '/home/liyinghao/papers/how_far_ica_go/prompts/nq'

command_template = '''dataset="nq"
model_name={model_name}
model_path={model_path}
icl_name={icl_name}
icl_path={icl_path}
stop="{stop}"
max_tokens=2048
batch_size=1

output_path=/home/liyinghao/papers/how_far_ica_go/outputs/nq/{model_name}/{icl_name}
mkdir -p $output_path
cp /home/liyinghao/papers/how_far_ica_go/run_vllm.py $output_path
cp /home/liyinghao/papers/how_far_ica_go/scripts/nq/0_run_batch_vllm_nq-2.py $output_path
log_file=/home/liyinghao/papers/how_far_ica_go/outputs/nq/{model_name}/{icl_name}/nq.log

CUDA_VISIBLE_DEVICES=0 batch_size=$batch_size icl_path=$icl_path max_tokens=$max_tokens icl_name=$icl_name dataset=$dataset model_name=$model_name stop=$stop output_path=$output_path model_path=$model_path python /home/liyinghao/papers/how_far_ica_go/run_vllm.py 2>&1 | tee $log_file'''

start = time.time()
count = 0
for i, model_name in enumerate(model_names):
    model_path = model_paths[i]
    for icl_name in icl_names:
        icl_name_splits = icl_name.split('_')
        
        if len(icl_name_splits) >= 3:
            icl_format = icl_name_splits[0].lower()

            if icl_format == 'md':
                stop = "['\`\`\`']"

            if icl_format == 'chatml':
                stop = "['<|im_end|>']"
            
            if icl_format == '0':
                stop = "['Query:']"
        else:
            stop = "['Question:']"

        # 给stop添加换行
        stop = stop.replace("[", "['\\n', ")
        print(f'当前进度：{model_name}, {icl_name}')
        
        command = command_template.format(model_name=model_name, model_path=model_path, icl_name=icl_name, icl_path=icl_path, stop=stop)

        # print('-----------command-----------')
        # print(command)
        # print('-----------command-----------')

        # count += 1

        # if count == 2:
        #     exit()

        subprocess.run(["bash", "-c", command], check=True)
        os.system('wait')
        print(f'====end=====\n\n')

        # exit()

print(f'all exp time: {(time.time() - start)/3600}h')