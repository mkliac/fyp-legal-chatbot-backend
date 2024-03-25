from transformers import pipeline

class ExtractiveQA:
    def __init__(self):
        self.model_path = "extractive-qa-model"
        self.question_answerer = pipeline("question-answering", 
                                    model=self.model_path+'/model', 
                                    tokenizer=self.model_path+'/tokenizer')

    def getResponse(self, question, context):
        results = self.question_answerer(question = question, context = context)

        return results

# Testing 
if __name__ == "__main__":
    model = ExtractiveQA()
    question = "How old are you?"
    context = "I'm 16 years old."
    results = model.getResponse(question , context)

    print(results)

    
