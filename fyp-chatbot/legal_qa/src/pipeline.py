# coding: utf-8

# using DrQA retriever and database settings + Finetuned BART-large genQA model
# to fulfill Legal-QA task

# DEFAULTS = {
#     'tokenizer': CoreNLPTokenizer,
#     'ranker': TfidfDocRanker,
#     'db': DocDB,
#     'reader_model': os.path.join(DATA_DIR, 'reader/multitask.mdl'),
# }
import re
from answer_generator import AnswerGenerator
from DrQA.drqa.pipeline import TfidfDocRanker, DocDB

class LegalQA:
    def __init__(self, tfidf_path='', db_path='', LM_checkpoint_path=''):
        ''' Initialize retriever and document reader. 
        For retriever:
            We follow the general setup from DrQA, like its database, tf-idf based ranker.
        
        For document reader:
            Following Alexa's ACL 2021 findings paper "Answer Generation for Retrieval-based Question Answering Systems", we finetuned BART-large on the MSMARCO dataset and use the saved parameters to conduct answer generation based on the retrieved passages as well as the user-input query. The answer is generated (abstracted) instead of extracted from passages.
        '''
        self.ranker = TfidfDocRanker(tfidf_path=tfidf_path)
        self.db = DocDB(db_path=db_path)
        self.pats = (re.compile(r'<FS>(.*)<SA>'), re.compile(r'<FS>(.*)'))

        self.genQA = AnswerGenerator(LM_checkpoint_path)

    def __call__(self, query, n_docs=5, muted=True):
        ''' 
        n_docs is by default set to 5, which is the same as number of passages used in the finetuning of GenQA model.
        '''
        if not muted:
            print('----QUERY----')
            print(query)

        # retrieval
        questions, passages = self._retrieve(query, n_docs=n_docs, muted=muted)

        # generate results based on the query and retrieved passages
        gen_result = self._generate(query, passages)

        if not muted:
            print('----GENERATED_ANSWER----')
            print(gen_result)

        return questions, gen_result

    def _retrieve(self, query, n_docs=5, muted=True):
        def _process_doc(input_doc):
            for pat in self.pats:
                found = pat.findall(input_doc)
                if len(found) > 0:
                    return found[0]

        all_docids, all_doc_scores = self.ranker.closest_docs(query, k=n_docs)
        
        docs = [self.db.get_doc_text(doc_id) for doc_id in all_docids]
        docs = [_process_doc(doci) for doci in docs]
        
        if not muted:
            for id_, score, doc in zip(all_docids, all_doc_scores, docs):
                print(id_)
                print(score)
                print(doc)
                print()
        return all_docids, docs

    def _generate(self, query, passages):
        input_text = '\n'.join(['<question>', query, '<passages>']+passages)
        return self.genQA(input_text)



if __name__ == '__main__':
    # lqa = LegalQA(tfidf_path='/home/data/jchengaj/crawled_question_answers/retrieval_model/legal_google_drqa_db-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz', 
    #             db_path='/home/data/jchengaj/crawled_question_answers/legal_google_drqa_db.db',
    #             LM_checkpoint_path='/data/jchengaj/gen-qa-summarization/checkpoint-151000/')

    lqa = LegalQA(tfidf_path='/home/data/jchengaj/legal_qa_retriever/base-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz',
                    db_path='/home/data/jchengaj/legal_qa_retriever/base.db',
                    LM_checkpoint_path='/data/jchengaj/gen-qa-summarization/checkpoint-151000/')
    Queries = ['what is attorney', 'what is contract', 'what does it mean to kill someone']
    for q in Queries:
        print(q)
        lqa(q)
        print('-------')
