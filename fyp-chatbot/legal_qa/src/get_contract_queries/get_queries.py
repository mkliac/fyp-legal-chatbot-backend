# coding: utf-8

import os
import json

# generate queries from the output of aggregate_and_clean.py

class QueryGenerator:
    def __init__(self):
        self.ety_kwd_patterns = ['what is {}', 'what is {} in a contract']
        self.vo_patterns = ['what does it mean to {} {}', 'what does it mean to {} {} in a contract']
        pass

    def get_ety_kwd_queries(self, item_list):
        output = []
        for item in item_list:
            for pt in self.ety_kwd_patterns:
                output.append(pt.format(item))
        return output
    
    def get_svo_queries(self, item_list):
        output = []
        for s, v, o in item_list:
            for pt in self.vo_patterns:
                output.append(pt.format(v, o))
            for pt in self.ety_kwd_patterns:
                output.append(pt.format(s))
                output.append(pt.format(o))
        return output

    def generate(self, info_fn):
        ''' Generate queries & half-complete queries based on the given information contained in info_fn. '''
        with open(info_fn) as f:
            info = json.loads(f.read())
        
        queries = self.get_ety_kwd_queries(info['ety'])
        queries.extend(self.get_ety_kwd_queries(info['kwd']))
        queries.extend(self.get_svo_queries(info['svo']))

        queries = list(set(list(queries)))
        
        return queries
    
    def save(self, data, output_fn='queries_from_contract.json'):
        with open(output_fn, 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False))
    


if __name__ == '__main__':
    info_fn = '/home/data/jchengaj/law/CUAD/CUAD_v1/contract_svo_kwd_ety/ety_kwd_svo.json'
    output_fn = 'queries_from_contract.json'

    query_generator = QueryGenerator()

    queries = query_generator.generate(info_fn)
    print('Queries #:', len(queries))

    query_generator.save(queries, output_fn)