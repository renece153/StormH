document.getElementById('sendMessageButton1').addEventListener('click', sendMessage);
document.getElementById('inputuser1').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    let userMessage = document.getElementById('inputuser1').value.trim();

    if (userMessage === '') {
        return; 
    }

  
    addMessageToChat('user', userMessage);
    document.getElementById('inputuser1').value = ''; 
    
    const Key_API = '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'; 

   
    try {
        let response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${Key_API}` 
            },
            body: JSON.stringify({
                "model": "gpt-3.5-turbo-1106",
                "messages": [
                  {"role": "system", "content": "You are a helpful assistant and Explain it in a friendly, simple sentence, and if it's about jobs,location, IDs, locations, or documents, provide 10 lists."},
                  {"role": "user", "content": userMessage}
                ]
              })
        });
    
        let data = await response.json();
        console.log('API Response:', data);  
    
        if (data.choices && data.choices.length > 0) {
            let botMessage = data.choices[0].message.content;
            addMessageToChat('bot', botMessage);
        } else {
            addMessageToChat('bot', 'Sorry, I could not process your request.');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('bot', 'Sorry, something went wrong. Please try again later.');
    }
    
}

function addMessageToChat(sender, message) {
    let chatBody = document.getElementById('chtbdy');
    let bubbleClass = sender === 'user' ? 'chtbl1 user' : 'chtbl1 bot';
    let messageBubble = `<div class="${bubbleClass}">${message}</div>`;
    chatBody.innerHTML += messageBubble;
    chatBody.scrollTop = chatBody.scrollHeight;
}
