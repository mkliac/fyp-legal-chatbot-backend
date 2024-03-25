const fetch = require("node-fetch");

const fetchData = async () => {
    const url = 'http://127.0.0.1:5005/';
    const data = { question: "How old are you?",context: "I am 16 years old."}
    const response = await fetch(url+'getResponse', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data)
    }).then(response=>console.log(response.json)).catch((err)=>console.log(err));
    console.log(response);

    
    //setData(responseData);
    
  }

  fetchData();