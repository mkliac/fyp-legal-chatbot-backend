from fastapi import FastAPI
from fastapi import File, UploadFile
from Extraction import Extractor
from extractiveQA import ExtractiveQA
from pydantic import BaseModel
import os

app = FastAPI()

@app.post("/extract")
def extract(file: UploadFile = File(...)):
    print("Received a request with filename: ", file.filename)
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        text = extractor.extract(file.filename)
        os.remove(file.filename)
    except Exception as e:
        print(e)
        text = ""
    finally:
        file.file.close()

    return {"context": text}

class ExtractiveQAQuery(BaseModel):
    question: str
    context: str

@app.post("/getResponse")
def getResponse(query: ExtractiveQAQuery):
    try:
        answer = model.getResponse(query.question, query.context)
    except Exception as e:
        print(e)
        answer = ""
    finally:
        return {'answer': answer}

extractor = Extractor()
model = ExtractiveQA()