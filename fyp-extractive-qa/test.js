const fetch = require("node-fetch");

async function postJSON(data) {
    try {
const url = "https://songcpu1.cse.ust.hk/cs-fyp/chatbot/getChatbotResponse"
        // const url = "http://127.0.0.1:5005/getResponse"
      const response = await fetch(url, {
        method: "POST", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
  
      const result = await response.json();
      console.log("Success:", result);
    } catch (error) {
      console.error("Error:", error);
    }
  }
  
  const data = { question: "penalty of murdering", n_retrieved_docs: "5"};
  postJSON(data);