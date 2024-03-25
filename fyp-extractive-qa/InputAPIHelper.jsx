class InputAPIHelper {
    static  extractContract = async (docURL) => {
        const contractPromise = new Promise(async (resolve,reject)=>{
            try{
              const url = 'http://127.0.0.1:5005/';
              const queryData = { fileURL: docURL}
              const fetch = require("node-fetch");
              const response = await fetch(url+'extract', {
                method: 'POST',
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(queryData)
              });
              const result = await response.json();
              const contract = result.context;
              resolve(contract);
              
            }catch(error){
                reject(error);
            }
        })
        const contractResult = await contractPromise;
        return contractResult;
        //setData(responseData);   
      }

      
    static  chatbotResponse = async (userQuestion,contract) => {
    const chatResponse = new Promise(async (resolve,reject)=>{
        try {
          const url = 'http://127.0.0.1:5005/';
          const queryData = { question:userQuestion,context:contract}
          const fetch = require("node-fetch");
          const response = await fetch(url+'getResponse', {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(queryData)
          });
          const result = await response.json();
          const chatResult = result["answer"].answer;
          resolve(chatResult);
          

        }catch(error){
            console.log(error);
            reject(error);
        }
    })
    const chatBotResult = await chatResponse;
    return chatBotResult;
    }


    static generalQAResponse = async (data) =>{
      const chatResponse = new Promise(async (resolve,reject)=>{
        try{
          // const url = 'http://127.0.0.1:5005/';
          const url = " https://songcpu1.cse.ust.hk/cs-fyp/chatbot/";
          //const queryData = { fileURL: docURL}
          const fetch = require("node-fetch");
          const response = await fetch(url + 'getChatbotResponse', {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(data)
          });
          const result = await response.json();
         console.log("Success:",result);
          
        }catch(error){
          console.error("Error:",error)
            reject(error);
        }
    })
    const chatBotResult = await chatResponse;   
    return chatBotResult;

    }
    
}
generalQAResponse({"question":"what is NDA","n_retrieved_docs":"5"})
export default InputAPIHelper;