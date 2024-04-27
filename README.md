# SYQ1-FYP
## fyp-chatbot
Installation Guide:

1. Download files and unzip it

2. Prepare Conda environment
```
conda create -n fyp-chatbot python=3.9 -y
conda activate fyp-chatbot
```

3. Navigate to `fyp-chatbot/legal_qa/src/` and stay inside the folder
```
cd <YOUR TARGET DIRECTORY>/fyp-chatbot/legal_qa/src/
```

4. Follow instructions on PyTorch website (https://pytorch.org/get-started/locally/) to install PyTorch on the targeting computing platform (I deleted torchvision torchaudio)![image](https://user-images.githubusercontent.com/41886378/212022373-773f2086-13c7-4f5f-bd36-f105d4e1aa44.png), and other necessary packages

```
conda install pytorch pytorch-cuda=11.7 -c pytorch -c nvidia -y
pip install fastapi uvicorn transformers pexpect scipy scikit-learn elasticsearch
```

5. Start the chatbot server with this (Change to any other ports that you want)
```
uvicorn server:app --reload --host=127.0.0.1 --port=5005
```

6. Verify by sending a POST request to http://localhost:5005 ![image](https://user-images.githubusercontent.com/41886378/212052304-4a1536ef-b845-4232-87db-906ec12f1ee4.png)

## fyp-extractive-qa
1. Follow below links to download and config PyTesseract
https://wellsr.com/python/convert-image-to-string-with-python-pytesseract-ocr/  
https://github.com/Belval/pdf2image  

2. Import all the libraries  
