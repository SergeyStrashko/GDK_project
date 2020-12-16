const express = require('express')
const fetch = require("node-fetch");
const db = require('./queries');

const app = express()
const port = 3000

app.use(express.json())

app.post('/students', db.addStudent);
app.post('/lessons-evaluation', db.addLesson);
app.post('/lecturers-evaluation', db.addLecturer);
app.post('/evaluations-info', db.addEvaluationInfo);
app.get('/schedule', db.getSchedule);
app.get('/lecturers-evaluation', db.getLecturerEvaluation);
app.get('/lessons-evaluation',db.getLessonEvaluation);
app.get('/credentials', db.getCredentials);

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
