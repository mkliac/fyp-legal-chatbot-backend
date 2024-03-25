# coding: utf-8

''' This code sets up database and pre-compute necessary files (like tf-idf model files) for the retriever. '''

import os
from crawler.postprocess import to_DrQA_fmt

if __name__ == '__main__':
    ''' The directory saving all the _output folders, each containing a all.txt data file. '''
    data_dir = '/home/data/jchengaj/crawled_question_answers'
    ''' The output dir, model retriever files will be written to this directory. '''
    output_dir = '/home/data/jchengaj/legal_qa_retriever'


    # process the crawled data into format understandable to DrQA modules
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    processed_fn = os.path.join(output_dir, 'source.txt')
    db_fn = os.path.join(output_dir, 'base.db')

    input_file_list = {os.path.join(data_dir, fn, 'all.txt'): 'iter-'+fn[-8] for fn in os.listdir(data_dir) if fn.endswith('_output')}
    to_DrQA_fmt(input_file_list, processed_fn)

    # setup database
    assert not os.path.exists(db_fn)
    os.system(f'python3 build_db.py {processed_fn} {db_fn}')

    # train retriever
    os.system(f'python3 build_tfidf.py {db_fn} {output_dir}')

    print('Finished. \nOutput directory:', output_dir)
