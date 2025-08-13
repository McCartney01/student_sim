import json
from .utils import read_json, write_json, generate
from .mapping import MODEL_FUNC_MAP, STR_TO_MODEL_NAME_MAP
from .nano_graphrag import GraphRAG, QueryParam
from .prompt import NEW_PROMPTS
from .nano_graphrag.prompt import GRAPH_FIELD_SEP
from concurrent.futures import ThreadPoolExecutor, as_completed

class StudentProfile:
    def __init__(self, student_id, model, dataset_dir="dataset", result_dir="results"):
        self.student_id = student_id
        self.dataset_dir = dataset_dir + '/' + student_id
        self.result_dir = result_dir + '/' + model + '/' + student_id
        self.model = model
        self.subject = student_id.split('_')[0]

        self.train = read_json(f'{self.dataset_dir}/train.json')
        self.test = read_json(f'{self.dataset_dir}/test.json')

    def insert(self):
        input_string = []
        for i in self.train:
            this_d = NEW_PROMPTS['get_library'].format(question=i['question'], desc=i['desc'], program=i['program'], error_desc=i['error_desc'])
            input_string.append(this_d)

        connect_str = "-"*10000
        input_string = connect_str.join(input_string)
        tmp = input_string.split(connect_str)
        assert len(tmp)==len(self.train)
        self.graph_func.insert(input_string)
    
    def generate_desc_for_every_kc(self, working_dir):
        graph = self.graph_func.chunk_entity_relation_graph._graph
        node = graph.nodes

        messages = []
        mid_file = f'{working_dir}/summarize_kc.json'
        for i in node.data():
            node_name = i[0]
            node_desc = i[1]['description'].split(GRAPH_FIELD_SEP)
            good_cnt, bad_cnt = 0, 0
            for j in node_desc:
                if 'Good' in j or 'GOOD' in j:
                    good_cnt += 1
                elif 'Bad' in j or 'BAD' in j:
                    bad_cnt += 1
            content = NEW_PROMPTS['summarize_kc'].format(kc_name=node_name, good_cnt=good_cnt, bad_cnt=bad_cnt, desc='\n'.join(node_desc))
            messages.append({
                "id": node_name,
                "model": STR_TO_MODEL_NAME_MAP[self.model],
                "messages": [{"role": "user", "content": content}],
                "output_file": mid_file,
            })
        futures = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            for message in messages:
                futures.append(executor.submit(lambda p: generate(*p), [message]))

            for job in as_completed(futures):
                job.result(timeout=None)

        self.summarize_kc = {}
        with open(f'{working_dir}/summarize_kc.json') as f:
            for i in f.readlines():
                i = json.loads(i)
                self.summarize_kc[i['id']] = i['output']['choices'][0]['message']['content']

    def retrieve(self):
        self.retrieval = []

        for i in self.test:
            this_d = NEW_PROMPTS['retrieve'].format(question=i['question'], desc=i['desc'])
            a = self.graph_func.query(this_d, param=QueryParam(mode="local", only_need_context=True))
            self.retrieval.append(a)
        
        write_json(f'{self.result_dir}/retrieve.json', self.retrieval)

    def prototype_construction(self):
        retrieval_file_path = f'{self.result_dir}/retrieve.json'
        self.retrieval = read_json(retrieval_file_path)

        if self.retrieval is None:
            working_dir = f'{self.result_dir}/graph'

            model_func = MODEL_FUNC_MAP[self.model]
            self.graph_func = GraphRAG(working_dir=working_dir, best_model_func=model_func, cheap_model_func=model_func)

            self.insert()
            self.generate_desc_for_every_kc(working_dir)
            self.retrieve()
        else:
            self.summarize_kc = {}
            with open(f'{self.result_dir}/graph/summarize_kc.json') as f:
                for i in f.readlines():
                    i = json.loads(i)
                    self.summarize_kc[i['id']] = i['output']['choices'][0]['message']['content']