# coding: utf-8

''' Interactive interface for the legal QA agent. '''

import code
from pipeline import LegalQA

print('Loading legal QA model into memory ...')
lqa = LegalQA(tfidf_path='../../../base-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz',
                db_path='../../../base.db',
                LM_checkpoint_path='../../../GenQA-BART-large/checkpoint-151000')

def enter_QA_session(n_retrieved_docs=5):
    print('Entering Question Answering session ...\nType "exit" to exit this mode.')
    input_text = input('Type below:\n')
    while input_text != 'exit':
        lqa(input_text, n_retrieved_docs, muted=False)
        input_text = input('Type below:\n')
    print('Exiting from QA session ...')
    print(banner)

banner = """
Interactive legal QA agent
>> enter_QA_session(n_retrieved_docs=5)
>> usage()
"""

def usage():
    print(banner)

code.interact(banner=banner, local=locals())
