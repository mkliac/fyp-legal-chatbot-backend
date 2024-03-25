# coding: utf-8

# This code is for transforming the MS MARCO dataset to the format to be read by BART/UnifiedQA-T5

import os
import csv
import json

def read_file(fn):
    if fn.endswith('2.1.json'):
        with open(fn) as f:
            return json.loads(f.read())
    elif fn.endswith('1.1.json'):
        with open(fn) as f:
            ret = {'passages': {},
                    'query': {},
                    'answers': {},
                    'query_type': {},
                }
            query_ids = []
            for line in f:
                if line.strip() == '':
                    break
                datum = json.loads(line)
                query_id = datum['query_id']
                query_ids.append(query_id)
                for key in ret:
                    ret[key][query_id] = datum[key]
            ret['query_id'] = query_ids
                
            return ret

def transform_single_file(input_fn, output_fn='out.csv', truncate_n=-1):
    ''' Reformat the data file. & Filter out items without answers presented.
    When truncate_n is set to a positive number, only output the previous truncate_n items to file. This could be useful when generating a small subset of dataset.
    '''
    print('Processing file {}, output to {} with truncation number {}...'.format(input_fn, output_fn, truncate_n))

    data = read_file(input_fn)
    print('Original # items:', len(data['query_id']))
    # we format our training data as a standard sequence-to-sequence/text-to-text task, where the source text is the question concatenated with the top five answer candidates, (q, Sk=5), joined by newlines.
    def compose_source_target(data, key_id):
        # return the source and target for a given item
        # specifically, return None when the answer is not present
        passage_texts = [item['passage_text'] for item in data['passages'][key_id]]
        query = data['query'][key_id]

        # top-5 answers, as instructed in the paper
        source = '\n'.join(['<question>', query, '<passages>']+passage_texts[:5])

        if len(data['answers'][key_id]) == 0: 
            return None
        target = data['answers'][key_id][0]
        if target == 'No Answer Present.':
            if len(data['answers'][key_id]) == 1:
                return None
            else:
                target = data['answers'][key_id][1]
        
        return source, target
    
    all_processed = []
    for key_id in data['query_id']:
        tmp = compose_source_target(data, key_id)
        if tmp is not None:
            all_processed.append(tmp)
    
    print('Lengths after processing:', len(all_processed))
    # output to file
    with open(output_fn, 'w') as f:
        # csv_writer = csv.writer(f)
        # csv_writer.writerow(['text', 'summary'])  # header

        if truncate_n >= 0:
            gen_len = min(truncate_n, len(all_processed))
        else:
            gen_len = len(all_processed)

        to_write = [json.dumps({'text':item[0], 'summary':item[1]}, ensure_ascii=False) for item in all_processed[:gen_len]]
        f.write('\n'.join(to_write))
        # csv_writer.writerows(all_processed[:gen_len])
        print('Total output lines:', gen_len)




if __name__ == '__main__':
    ''' Transform v2.1 dataset '''
    transform_single_file('/home/data/jchengaj/MSMARCO/dev_v2.1.json', 
                            output_fn='/home/data/jchengaj/MSMARCO_processed/dev_v2.1.json')

    transform_single_file('/home/data/jchengaj/MSMARCO/train_v2.1.json', 
                            output_fn='/home/data/jchengaj/MSMARCO_processed/train_v2.1.json')

    # ''' Transform v1.1 dataset '''
    # transform_single_file('/home/data/jchengaj/MSMARCO/dev_v1.1.json', 
    #                         output_fn='/home/data/jchengaj/MSMARCO_processed/dev_v1.1.json')

    # transform_single_file('/home/data/jchengaj/MSMARCO/train_v1.1.json', 
    #                         output_fn='/home/data/jchengaj/MSMARCO_processed/train_v1.1.json')


    # ''' Get small dataset sample for preliminary exp. '''
    # transform_single_file('/home/data/jchengaj/MSMARCO/dev_v1.1.json', 
    #                         output_fn='/home/data/jchengaj/MSMARCO_processed/dev_v1.1_small.json',
    #                         truncate_n=100)

    # transform_single_file('/home/data/jchengaj/MSMARCO/train_v1.1.json', 
    #                         output_fn='/home/data/jchengaj/MSMARCO_processed/train_v1.1_small.json',
    #                         truncate_n=1000)