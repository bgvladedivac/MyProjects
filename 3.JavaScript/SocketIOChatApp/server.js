const express = require('express')
const app = express()
const socketio = require('socket.io')

app.use(express.static(__dirname  + '/public'))

const expressServer = app.listen(9000)
const io = socketio(expressServer)

io.on('connection', (socket) => {

    socket.on('newuser', (username) => {
        insertActiveUser(username)
        getActiveUsers()
    })
     
    socket.on('newMessageToServer', (msg) => {
        io.emit('messageToClients', {text: msg.text})      
    })

    // This needs to be improved, how to get the username who is 
    // being disconnected and then update the dom
    socket.on('disconnect', function() {
        io.emit('user disconnected')
        console.log('user got disconnected')
    })
})

var MongoClient = require('mongodb').MongoClient

function insertActiveUser(username) {
    MongoClient.connect('mongodb://db:27017/', function (err, client) {
         if (err) throw err
         let db = client.db('chatpp')
         db.collection('activeusers').insertOne( {
            'username' : username
        })
    })
}

 function getActiveUsers() {
    MongoClient.connect('mongodb://db:27017/', function (err, client) {
       
         if (err) throw err
         
         let db = client.db('chatpp')

       
            let resultSet = db.collection('activeusers').find({}).toArray(function(err, result) {
                if (err) throw err;
                
                var noReocuringUsers = []

                result.forEach((el) => {
                    let currentUserName = el["username"]["data"]

                    if (!noReocuringUsers.includes(currentUserName)) {
                        noReocuringUsers.push(currentUserName)
                    }
                })
                 io.emit('activeUsersPropagation', { data : noReocuringUsers})
            })
        })
       
}


// improvements

// 1. make sure that when a new user joins
// the already joined users are not being updated
// with all the usernames, just with the new joiner.
 
