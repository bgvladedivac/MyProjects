const socket = io()
let username = prompt("Enter your username")

socket.emit('newuser', { data: username})

// on submit emit the msg + un
document.querySelector('#message-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const newMessage = document.querySelector('#user-message').value
    const objWrapperMsgUn = {
        "message" : newMessage,
        "username" : username
    }
    socket.emit('newMessageToServer', { text: objWrapperMsgUn})
} )

// listens for messages that need to be broadcasted.
// update the dom with current time + un + msg
socket.on('messageToClients', (msg) => {
    console.log("Giving u the wrapper object")
    console.log(msg["text"]["username"])
    
    let currentDate = new Date().toLocaleTimeString(); 
    document.querySelector("#messages")
        .innerHTML += `<li>${currentDate} ${msg["text"]["username"]} : ${msg["text"]["message"]} </li>`
})

// update the dom with all active users
socket.on('activeUsersPropagation', (msg) => {

    // get the current active users and compare them
    // with the users in msg, find the ones who are 
    // not metd in msg, and display them
    let listValues = document.getElementById("loggedUser").getElementsByTagName("li")
    
    // for some reason the below code won't give me the values
    for(let i = 0; i < listValues.length; i++) {
        console.log(listValues[i])
    }

    
    msg['data'].forEach((el) => {
        document.querySelector("#loggedUser").innerHTML += `<li>${el}</li>`
    })
  
})

 


