import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import Union
from pipeline import LegalQA

class ChatbotQuery(BaseModel):
    question: str
    n_retrieved_docs: int = 1

    # class Config:
    #     validate_assignment = True

    # @validator('n_retrieved_docs')
    # def set_n_retrieved_docs(cls, n_retrieved_docs):
    #     return n_retrieved_docs or 5

app = FastAPI()

@app.post('/getChatbotResponse/', response_class=JSONResponse)
def enter_QA_session(query: ChatbotQuery):
    try:
        print(f'n_docs={query.n_retrieved_docs}')
        top_n_questions, answer = lqa(query=query.question, n_docs=query.n_retrieved_docs, muted=False)
        top_n_questions = [question[9:] for question in top_n_questions]
        answer = answer[0]['generated_text']
    except Exception as e:
        print(e)
        answer = ''
        top_n_questions = []
    finally:
        return {'answer': answer,
                'top_n_questions': top_n_questions}

print('Loading legal QA model into memory ...')
lqa = LegalQA(tfidf_path='models/legal_qa_retriever/base-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz',
                db_path='models/legal_qa_retriever/base.db',
                LM_checkpoint_path='models/checkpoints/GenQA-BART-large/checkpoint-151000/')
