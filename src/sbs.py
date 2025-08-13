import json
import os
from .mapping import STR_TO_MODEL_NAME_MAP
from .prompt import NEW_PROMPTS
from .utils import generate, find_value

def behavior_prediction(student, test_index):
    this_test, this_retrieval, summarize_kc = student.test[test_index], student.retrieval[test_index], student.summarize_kc

    os.makedirs(f'{student.result_dir}/ours', exist_ok=True)
    mid_file = f'{student.result_dir}/ours/predict.json'

    retrieved_question = this_retrieval["text_units_section_list"][1][1]
    retrieved_messages = []
    for i in this_retrieval['results'][:5]:
        this_kc = i['entity_name']
        this_desc = summarize_kc[this_kc]
        retrieved_messages.append(this_kc + '\n\n' + this_desc)
    retrieved_messages = '\n-----------------\n'.join(retrieved_messages)

    content = NEW_PROMPTS['generate_error_desc'].format(summarize_kc=retrieved_messages, case=retrieved_question, problem=this_test['question'], subject=student.subject)
    
    request = {
        "id": this_test['problem_id'],
        "model": STR_TO_MODEL_NAME_MAP[student.model],
        "messages": [{"role": "user", "content": content}],
        "output_file": mid_file,
    }
    output = generate(request)['choices'][0]['message']['content']

    eval_file = f"{student.result_dir}/ours/error_eval.json"
    acc, score = eval_behavior_prediction(this_test, output, eval_file, student.subject)

    return acc, score, output

def eval_behavior_prediction(this_test, output, eval_file, subject):
    judge_correct = False if 'Yes' in output.split('\n')[0] else True
    gt_correct = True if this_test['error_desc'] == "No error." else False

    acc = int(judge_correct == gt_correct)

    if judge_correct:
        output = "No error."
    
    content = NEW_PROMPTS['eval_error_desc'].format(question=this_test['question'], gt_code=this_test['program'], error_desc=this_test['error_desc'], new_error_desc=output, subject=subject)

    request = {
        "id": this_test['problem_id'],
        "model": "o1-mini",
        "messages": [{"role": "user", "content": content}],
        "output_file": eval_file,
    }
    score_string = generate(request)['choices'][0]['message']['content']
    score = int(score_string.split('|')[0].split('(')[-1].strip())
    
    return acc, score


def evaluate(mid_file, question, code, error_desc, iter, answer_idx, used_model, subject):
    content = NEW_PROMPTS['evaluate_1'].format(question=question, code=code, error_desc=error_desc, subject=subject)
    data = {
        "id": f"iter_{iter}_answer_{answer_idx}_value_1",
        "model": used_model,
        "messages": [{"role": "user", "content": content}],
        "output_file": mid_file,
    }
    output = generate(data)['choices'][0]['message']['content']

    content2 = NEW_PROMPTS['evaluate_2'].format(error_desc=error_desc)
    data = {
        "id": f"iter_{iter}_answer_{answer_idx}_value_2",
        "model": used_model,
        "messages": [{"role": "user", "content": content},
                        {"role": "assistant", "content": output},
                        {"role": "user", "content": content2}],
        "output_file": mid_file,
    }
    while True:
        output2 = generate(data)['choices'][0]['message']['content']
        values, evals = find_value(output2)
        if len(values)>=1:
            break
        else:
            output2 = output2 + ')'
            values, evals = find_value(output2)
            if len(values)==1:
                break
            print(output2)
            tmp = []
            with open(mid_file) as f:
                for i in f.readlines():
                    i = json.loads(i)
                    if i['id'] != f"iter_{iter}_answer_{answer_idx}_value_2":
                        tmp.append(i)
            with open(mid_file, 'w') as f:
                for i in tmp:
                    line = json.dumps(i, ensure_ascii=False)
                    f.write(line+'\n')

    return values[0], evals[0]


def solution_simulation(student, test_index, description, max_iter=3, max_beam=2):
    #### get example
    this_test, this_retrieval = student.test[test_index], student.retrieval[test_index]

    retrieved_question = this_retrieval["text_units_section_list"][1][1]
    example_code = retrieved_question.split('Student Program:\n')[1].split('Error Description:\n')[0].strip()
    example_question = retrieved_question.split('Question:\n')[1].split('Description:\n')[0].strip()


    mid_dir = f'{student.result_dir}/ours_ours/depth_{max_iter}_beam_{max_beam}'
    os.makedirs(mid_dir, exist_ok=True)
    mid_file = f'{mid_dir}/{this_test["problem_id"]}.json'
    content = NEW_PROMPTS['generate_initial_code'].format(eg_question=example_question, eg_code=example_code, question=this_test['question'], subject=student.subject)
    data = {
        "id": "iter_0_generate_code",
        "model": STR_TO_MODEL_NAME_MAP[student.model],
        "messages": [{"role": "user", "content": content}],
        "output_file": mid_file,
    }
    output = generate(data)

    answer = output['choices'][0]['message']['content']

    value, eval = evaluate(mid_file=mid_file, question=this_test['question'], code=answer, error_desc=description, iter=0, answer_idx=0, used_model=STR_TO_MODEL_NAME_MAP[student.model], subject=student.subject)

    current_value, current_answer, current_eval = value, answer, eval

    for i in range(max_iter):
        if current_value >= 0.9:
            break
        content = NEW_PROMPTS["refine"].format(eg_code=example_code, question=this_test['question'], error_desc=description, code=current_answer, evaluation=current_eval, subject=student.subject)
        data = {
            "id": f"iter_{i+1}_refine",
            "model": STR_TO_MODEL_NAME_MAP[student.model],
            "messages": [{"role": "user", "content": content}],
            "output_file": mid_file,
            "generation_config": {"n": max_beam}
        }
        output = generate(data)

        refined_code = [j['message']['content'] for j in output['choices']]
        assert len(refined_code)==max_beam

        nodes = []
        for j, c in enumerate(refined_code):
            value, eval = evaluate(mid_file=mid_file, question=this_test['question'], code=c, error_desc=description, iter=i+1, answer_idx=j, used_model=STR_TO_MODEL_NAME_MAP[student.model], subject=student.subject)
            if value > current_value:
                current_value, current_answer, current_eval = value, c, eval

    eval_file = f'{mid_dir}/code_eval.json'
    score = eval_solution_simulation(this_test, current_answer, description, eval_file, student.subject)

    return score, current_answer

def eval_solution_simulation(this_test, answer, description, eval_file, subject):
    content = NEW_PROMPTS['eval_code'].format(question=this_test['question'], gt_code=this_test['program'], error_desc=description, code=answer, subject=subject)

    request = {
        "id": this_test['problem_id'],
        "model": "o1-mini",
        "messages": [{"role": "user", "content": content}],
        "output_file": eval_file,
    }
    
    score_string = generate(request)['choices'][0]['message']['content']
    score = int(score_string.split('|')[0].split('(')[-1].strip())

    return score