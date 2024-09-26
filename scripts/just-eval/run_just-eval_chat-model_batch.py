import os
import subprocess

models = ['llama2-13b-chat']
icl_names = ['llama2-chat', 'llama2-chat-system']

command_template = '''result_file="/home/liyinghao/papers/how_far_ica_go/outputs/just-eval-instruct/{model}/{icl_name}/output_help_100_evaluation.json"
output_file=${{result_file/.json/.gpt-4o-2024-05-13.json}}
log_file=${{result_file/.json/.gpt-4o-2024-05-13.log}}
mode="score_multi"

just_eval \
    --mode $mode \
    --gpt_model "gpt-4o-2024-05-13" \
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