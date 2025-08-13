import json
import os
from retry import retry
from openai import OpenAI
import re

@retry()
def generate(data):
    if os.path.isfile(data["output_file"]):
        with open(data["output_file"]) as f:
            for i in f.readlines():
                i = json.loads(i)
                if i['id'] == data["id"]:
                    return i["output"]
    
    if 'llama' in data['model']:
        client = OpenAI(api_key=os.getenv('LLAMA_API_KEY'), base_url=os.getenv('LLAMA_BASE_URL'), timeout=60)
    elif 'claude' in data['model']:
        client = OpenAI(api_key=os.getenv('CLAUDE_API_KEY'), base_url=os.getenv('CLAUDE_BASE_URL'), timeout=60)
    else:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), timeout=60)

    if "generation_config" in data:
        if 'claude' in data['model']:
            n = data['generation_config']["n"]
            stream = client.chat.completions.create(
                model=data["model"],
                messages=data["messages"],
                **data["generation_config"]
            ).to_dict()
            for _ in range(n-1):
                this_stream = client.chat.completions.create(
                    model=data["model"],
                    messages=data["messages"],
                    **data["generation_config"]
                ).to_dict()
                stream["choices"].append(this_stream["choices"][0])
        else:
            stream = client.chat.completions.create(
                model=data["model"],
                messages=data["messages"],
                **data["generation_config"]
            ).to_dict()
    else:
        stream = client.chat.completions.create(
            model=data["model"],
            messages=data["messages"],
        ).to_dict()
    
    output_data = {
        "id": data["id"],
        "output": stream,
        "input": data
    }
    write_jsonl(file_path=data["output_file"], single_data=output_data)
    
    return output_data["output"]

def read_json(file_path):
    if not os.path.isfile(file_path):
        return None
    with open(file_path) as f:
        return json.load(f)

def read_jsonl(file_path):
    if not os.path.isfile(file_path):
        return None
    with open(file_path) as f:
        result = [json.loads(line) for line in f.readlines()]
    result = sorted(result, key=lambda x: x['id'])
    return result

def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def write_jsonl(file_path, single_data):
    with open(file_path, 'a') as f:
        f.write(json.dumps(single_data, ensure_ascii=False)+'\n')


def find_value(input_string):
    pattern = r'\(\s*(0(\.\d+)?|1(\.0+)?)\s*\|\s*(.+?)\s*\)'
    matches = re.findall(pattern, input_string)

    values, evals = [], []
    for m in matches:
        pattern = re.compile(r'\-?\d+\.\d+|\-?\d+')
        tmp_score = pattern.findall(m[0])
        value = float(tmp_score[0])
        values.append(value)
        
        text = '|'.join(input_string.split('|')[1:])
        text = ')'.join(text.split(')')[:-1]).strip()

        evals.append(text)
    return values, evals