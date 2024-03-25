# coding: utf-8

import os
import json


def aggregate_single_dir(dir='.', output_fn='all.txt'):
    ''' Aggregate all the crawled data files within a directory and output to file 'output_fn'. '''
    dir_fns = os.listdir(dir)
    output_f = open(os.path.join(dir, output_fn), 'w')

    for fn in dir_fns:
        if fn.isdigit():
            print('Current processing file: ', fn, end='\r')
            with open(os.path.join(dir, fn)) as f:
                file_data = json.loads(f.read())
                for item in file_data:
                    output_f.write(json.dumps(item, ensure_ascii=False, sort_keys=True)+'\n')
    print()

    output_f.close()


def aggregate_all(dir='.', output_dir='output', sub_output_fn='all.txt'):
    ''' Aggregate all the data files from different servers. Also, aggregate the future url lists and crawled url lists. '''
    sub_dirs = [os.path.join(dir, sub) for sub in os.listdir(dir)]

    # sub_data_fns = [os.path.join(sub_dir, sub_output_fn) for sub_dir in sub_dirs]
    sub_future_fns = [os.path.join(dir, sub_dir, 'future.json') for sub_dir in sub_dirs]
    sub_crawled_fns = [os.path.join(dir, sub_dir, 'crawled.json') for sub_dir in sub_dirs]

    if not os.path.exists(os.path.join(dir, output_dir)): os.mkdir(os.path.join(dir, output_dir))

    futures = {}
    for fn in sub_future_fns:
        with open(fn) as f:
            futures.update(json.loads(f.read()))
    with open(os.path.join(dir, output_dir, 'future.json'), 'w') as f:
        f.write(json.dumps(futures, ensure_ascii=False, indent=4, separators=(',', ':'), sort_keys=True))
    
    crawled = {}
    for fn in sub_crawled_fns:
        with open(fn) as f:
            crawled.update(json.loads(f.read()))
    with open(os.path.join(dir, output_dir, 'crawled.json'), 'w') as f:
        f.write(json.dumps(crawled, ensure_ascii=False, indent=4, separators=(',', ':'), sort_keys=True))


    # aggregate all the data into one file, and no repetition is kept
    output_f = open(os.path.join(dir, output_dir, 'all.txt'), 'w')
    tmp_record = set()
    for sub_dir in sub_dirs:
        # aggregate sub dir data
        if not os.path.exists(os.path.join(sub_dir, sub_output_fn)): 
            aggregate_single_dir(sub_dir, output_fn=sub_output_fn)
        with open(os.path.join(sub_dir, sub_output_fn)) as f:
            for line in f:
                if line.strip() != '':  # the last line
                    d = json.loads(line)
                    if d['question'] not in tmp_record:
                        tmp_record.add(d['question'])
                        output_f.write(line)
        
    
    output_f.close()

        

def generate_tocrawl_list(in_folders, out_fn='future_list.json'):
    ''' Generate to-crawl list for later crawling. 

    in_folders <list of str>: a list of folder names, each folder contains a crawled.json file and a future.json file.
    out_fn <str>: the output filename with which the output stuffs will be saved.
    '''
    crawled_fns = [os.path.join(dir, 'crawled.json') for dir in in_folders]
    future_fns = [os.path.join(dir, 'future.json') for dir in in_folders]

    crawled = {}
    for fn in crawled_fns:
        with open(fn) as f:
            crawled.update(json.loads(f.read()))
    future = {}
    for fn in future_fns:
        with open(fn) as f:
            future.update(json.loads(f.read()))
    
    output_list = []
    for item in future:
        if item not in crawled:
            output_list.append(item)
    
    with open(out_fn, 'w') as f:
        f.write(json.dumps(output_list, ensure_ascii=False))



def to_DrQA_fmt(input_file_list, output_filename):
    ''' Load input files (all.txt), transform to output DrQA format for retrieval.
    '''
    output_f = open(output_filename, 'w')
    print('outputing to file:', output_filename)
    ct = 0
    for fn in input_file_list:
        print('processing: '+fn)
        iter_name = input_file_list[fn]

        with open(fn) as f:
            for line in f:
                if line.strip() != '':
                    print(ct, end='\r')

                    pack = json.loads(line)

                    if pack['result']['featured_snippet'] is None: continue

                    Q = pack['question']
                    FS = pack['result']['featured_snippet']['text']
                    SA = pack['result']['featured_snippet']['short_answer'] or ''

                    

                    item_id = '['+iter_name+']:'+pack['question']
                    # Q:question, FS:featured snippet, SA:short answer
                    item_text = '<Q>'+Q+'<FS>'+FS+'<SA>'+SA

                    item = {'id':item_id, 'text':item_text}

                    output_f.write(json.dumps(item, ensure_ascii=False)+'\n')
                    ct += 1
        print()

    



if __name__ == '__main__':
    ''' aggregate the crawled data within a single directory'''
    # aggregate_single_dir(dir='/home/data/jchengaj/crawled_question_answers/crawled_question_answers_test', output_fn='all.txt')

    ''' aggregate all data within directories inside the given directory '''
    aggregate_all(dir='/home/data/jchengaj/crawled_question_answers/contract_iter3_raw')
    exit()

    ''' generate the next iteration crawling filenames from the current future list files '''
    # generate_tocrawl_list(['/home/data/jchengaj/crawled_question_answers/'+'iter{}_output'.format(i) for i in range(1, 4)], \
    #                     '/home/data/jchengaj/crawled_question_answers/iter3_output/future_list.json')

    ''' transform files inside the given name list to the DrQA retriever format and output to target file '''
    input_file_list = {'/home/data/jchengaj/crawled_question_answers/iter{}_output/all.txt'.format(i): 'iter-'+str(i) for i in range(1, 5)}
    output_filename = '/home/data/jchengaj/crawled_question_answers/legal_google_drqa.txt'
    to_DrQA_fmt(input_file_list, output_filename)
