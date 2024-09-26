import json
import re
import sys
sys.path.append('/home/liyinghao/papers/how_far_ica_go/scripts/human-eval')

from utils import read_problems, write_jsonl


def humaneval_postprocess(text: str) -> str:
    # text = text.rstrip('```\n\n')
    # 去掉第一句话
    text = '\n\n'.join(text.split('\n\n')[1:])
    # text = '\n'.join(text.split('\n')[1:])
    
    if '```' in text:
        blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
        if len(blocks) == 0:
            text = text.split('```')[1]  # fall back to default strategy
        else:
            text = blocks[0]  # fetch the first code block
            if not text.startswith('\n'):  # in case starting with ```python
                text = text[max(text.find('\n') + 1, 0):]
    if text.strip().startswith('from') or text.strip().startswith('import'):
        def_idx = text.find('def')
        if def_idx != -1:
            text = text[max(text.find('\n', def_idx) + 1, 0):]
    text = text.split('\n\n')[0]
    if text.strip().startswith('def'):
        text = '\n'.join(text.split('\n')[1:])
    if not text.startswith('    '):
        if text.startswith(' '):
            text = '    ' + text.lstrip()
        else:
            text = '\n'.join(['    ' + line for line in text.split('\n')])
    return text

problems_file = '/home/liyinghao/papers/how_far_ica_go/datas/human-eval/HumanEval.jsonl'
predictions_file = '/home/liyinghao/papers/how_far_ica_go/outputs/human-eval/llama2-70b-chat/llama2-chat-2/outputs.jsonl'

problems = read_problems(problems_file)


completions = [json.loads(line)['output'].rstrip('</s>').strip() for line in open(predictions_file)]
# completions = [value["prediction"] for value in json.load(open(predictions_file)).values()]

# print(completions[2])
# print(humaneval_postprocess(completions[0]))
# exit()

assert len(problems) == len(completions)

samples = [
    dict(task_id=task_id, completion=humaneval_postprocess(completion)) for task_id, completion in zip(problems, completions)
]
write_jsonl(predictions_file.replace('.jsonl', '_completions.json'), samples)
print('finish')