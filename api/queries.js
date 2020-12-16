const Pool = require('pg').Pool
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'student',
  password: 'group_ip74',
  port: 5432,
})

module.exports.addStudent = (request, response) => {
  const {first_name, last_name, login, faculty, group_name, email, password} = request.body;
  pool.query(`INSERT INTO students (first_name, last_name, login, faculty, group_name, email, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s);`,[first_name, last_name, login, faculty, group_name, email, password], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

module.exports.addLesson = (request, response) => {
  const {lesson_name, lesson_type, lesson_number, group_name, day_number, day_name, week_number, overall_grade , lesson_feedbacks, lecturer_id} = request.body;
  pool.query(`INSERT INTO lessons_evaluation(
    lesson_name,
    lesson_type,
    lesson_number,
    group_name,
    day_number,
    day_name,
    week_number,
    overall_grade ,
    lesson_feedbacks,
    lecturer_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);`,[lesson_name, lesson_type, lesson_number, group_name, day_number, day_name, week_number, overall_grade , lesson_feedbacks, lecturer_id], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

module.exports.addLecturer = (request, response) => {
  const {full_name, overall_grade, grade_1, grade_2, grade_3, grade_4, grade_5, grade_6, lecturer_feedbacks} = request.body;

  pool.query(`INSERT INTO lecturers_evaluation (full_name, overall_grade, grade_1, grade_2, grade_3, grade_4, grade_5, grade_6, lecturer_feedbacks)
    VALUES (%s, %s, %s, %s, %s, %s);`, [full_name, overall_grade, grade_1, grade_2, grade_3, grade_4, grade_5, grade_6, lecturer_feedbacks], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

module.exports.addEvaluationInfo = (request, response) => {
  const {students_id, lesson_id, lecturer_id } = request.body

  pool.query(`INSERT INTO evaluations_info (students_id, lesson_id, lecturer_id)
    VALUES (%s, %s, %s);`, [students_id, lesson_id, lecturer_id], (error, results) => {
    if (error) {
      throw error
    }
    response.status(201).send(`User added with ID: ${result.insertId}`)
  })
}

module.exports.getSchedule = (request, response) => {
  const {day_number, week_number, group_number} = request.query;
  pool.query(`SELECT *
  FROM schedule
  INNER JOIN lessons_evaluation ON schedule.lesson_id = lessons_evaluation.lesson_id
  WHERE lessons_evaluation.day_number = %s
  AND lessons_evaluation.week_number = %s
  AND lessons_evaluation.group_number = %s;`,[day_number, week_number, group_number], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

module.exports.getLecturerEvaluation = (request, response) => {
  const {day_number, week_number, group_number} = request.query;
  pool.query(`SELECT *
  FROM (lecturers_evaluation
  INNER JOIN lessons_evaluation ON lecturers_evaluation.lecturer_id = lessons_evaluation.lesson_id
  WHERE lessons_evaluation.day_number = %s
  AND lessons_evaluation.week_number = %s
  AND lessons_evaluation.group_number = %s);`,[day_number, week_number, group_number], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}


module.exports.getLessonEvaluation = (request, response) => {
  const {lesson_number, day_number, week_number, group_number} = request.query;
  pool.query(`SELECT lessons_evaluation.overall_grade, lessons_evaluation.lesson_feedbacks, lessons_evaluation.lesson_number, lessons_evaluation.lesson_name
  FROM lessons_evaluation
  WHERE lessons_evaluation.lesson_number = %s
  AND lessons_evaluation.day_number = %s
  AND lessons_evaluation.week_number = %s
  AND lessons_evaluation.group_number = %s;`, [lesson_number, day_number, week_number, group_number], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows);
  })
}

module.exports.getCredentials = (request, response) => {
  const {login, password} = request.query;
  pool.query(`SELECT students.login, students.password 
    FROM students WHERE students.login = %s AND students.password = %s`, [login, password], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows);
  })
}



