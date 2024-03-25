import requests

"""
After hosting the server, run this file to test.
"""
print("running")
#testing extract API
# url = 'http://songcpu1.cse.ust.hk/cs-fyp/extractive-qa/'
# url = "http://127.0.0.1:5005/"
url = "http://123.203.88.20:80/"
file = {"file":open('./Extraction-test-files/testFile2.pdf', 'rb')}
resp = requests.post(url=url + "extract", files=file) 
print(resp.json())

#testing getResponse API
question = "How old are you?"
context = "I'm 16 years old."
resp = requests.post(url=url + "getResponse",json={
    "question": question,
    "context": context
})
print(resp.json())
