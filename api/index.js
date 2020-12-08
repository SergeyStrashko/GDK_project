const express = require('express')
const fetch = require("node-fetch");

const app = express()
const port = 3000

app.use(express.json())

app.post('/study-schedule-current-day', (req, res) => {
  (async () => {
    const rawResponse = await fetch('http://localhost:5000/get-schedule-current-day', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: req
    });
    const content = await rawResponse.json();

    res.send(content)
  })();
})

app.listen(port, (err) => {
    if (err) {
        return console.log('something bad happened', err)
    }
    console.log(`server is listening on ${port}`)
})
