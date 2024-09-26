import json, re, os

def general_postprocess(text: str) -> str:
    # Cut off the first newline, period, or comma
    truncated_text = re.split(r'[\n.,]', text, 1)[0]

    # Remove punctuation
    no_punctuation = re.sub(r'[^\w\s]', '', truncated_text)

    # Remove article
    no_articles = re.sub(r'\b(a|an|the)\b',
                         '',
                         no_punctuation,
                         flags=re.IGNORECASE)

    # Remove duplicated blank spaces
    cleaned_text = re.sub(r'\s+', ' ', no_articles).strip()

    return cleaned_text

def score(predictions, references):
    if len(predictions) != len(references):
        return {
            'error': 'predictions and references have different '
            'length'
        }
    processed_predictions = []
    for prediction in predictions:
        processed_prediction = prediction.strip().split('\n')[0].lower()
        if 'answer is:' in processed_prediction:
            processed_prediction = processed_prediction.split('answer is:')[-1]
        elif 'answer is' in processed_prediction:
                processed_prediction = processed_prediction.split('answer is')[-1]
        processed_prediction = general_postprocess(processed_prediction)
        processed_predictions.append(processed_prediction)
    processed_answers = [[general_postprocess(j).lower() for j in i]
                            for i in references]

    details = []
    cnt_strict = cnt_standard = cnt_loose = 0
    for pred, processed_pred, cand_ans in zip(predictions, processed_predictions, processed_answers):
        pred = pred.lower()
        detail = {
            'pred': pred, 
            'processed_pred': processed_pred, 
            'answer': cand_ans, 
            'correct_strict': False,
            'correct_standard': False,
            'correct_loose': False
        }
        is_correct_strict = any([cand == processed_pred for cand in cand_ans])
        is_correct_standard = any([cand in processed_pred for cand in cand_ans])
        is_correct_loose = any([cand in pred for cand in cand_ans])
        cnt_strict += int(is_correct_strict)
        cnt_standard += int(is_correct_standard)
        cnt_loose += int(is_correct_loose)
        detail['correct_strict'] = is_correct_strict
        detail['correct_standard'] = is_correct_standard
        detail['correct_loose'] = is_correct_loose
        details.append(detail)
    score_strict = cnt_strict / len(predictions) * 100
    score_standard = cnt_standard / len(predictions) * 100
    score_loose = cnt_loose / len(predictions) * 100

    return {'score_strict': score_strict, 'score_standard': score_standard, 'score_loose': score_loose, 'details': details}

def eval_path_files(path, file_name):
    count = 0

    for root, dirs, files in os.walk(path):
        for n, dir in enumerate(dirs):
            file_path = os.path.join(root, dir, file_name)
            if not os.path.exists(file_path):
                continue

            new_file_path = file_path.replace('.json', '_result.json')
            if os.path.exists(new_file_path):
                continue
        
            eval_single_file(file_path, new_file_path)
            count += 1
            print(f'{count}---{dir}')

def eval_single_file(file_path, new_file_path=''):
    if new_file_path == '':
        new_file_path = file_path.replace('.json', '_result.json')

    datas = json.load(open(file_path))
    predictions = [data['output'] for data in datas]
    references = [data['answer'] for data in datas]

    results = score(predictions, references)

    json.dump(results, open(new_file_path, 'w'), indent=2, ensure_ascii=False)
     
if __name__ == '__main__':
    file_path = '/home/liyinghao/papers/how_far_ica_go/outputs/nq/llama2-7b-chat/llama2-chat-system-2/output_100_evaluation.json'
    eval_single_file(file_path)
    print('finish')

    # path = '/home/liyinghao/papers/how_far_ica_go/outputs/nq/llama2-70b'
    # file_name = 'outputs_evaluation.json'
    # eval_path_files(path, file_name)