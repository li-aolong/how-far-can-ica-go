import os
import subprocess

models = ['llama2-70b']
icl_names = ['0_0_0', '0_0_urial', '0_urial_0', '0_urial_urial', 'md_0_0', 'md_0_urial', 'md_urial_0']

command_template = '''result_file="/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/{model}/table1_{icl_name}/output_safe_100_evaluation.json"
output_file=${{result_file/.json/.gpt-3.5-turbo-0125.json}}
log_file=${{result_file/.json/.gpt-3.5-turbo-0125.log}}
mode="score_safety"

just_eval \
    --mode $mode \
    --gpt_model "gpt-3.5-turbo-0125" \
    --model_output_file $result_file \
    --eval_output_file $output_file 2>&1 | tee $log_file

just_eval \
    --report_only \
    --mode $mode \
    --eval_output_file $output_file  2>&1 | tee -a $log_file'''

for model in models:
    for icl_name in icl_names:
        print(f'-------{model} - {icl_name}-----')

        command = command_template.format(model=model, icl_name=icl_name)
        subprocess.run(["bash", "-c", command], check=True)
        os.system('wait')
        print(f'======={model}=======end======{icl_name}======')