import psycopg2

from dotenv import load_dotenv

load_dotenv()

CREATE_STUDENTS_TABLE = """CREATE TABLE IF NOT EXISTS students(
	student_id SERIAL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	login TEXT NOT NULL,
	faculty VARCHAR(25) NOT NULL,
	group_name TEXT NOT NULL,
	email VARCHAR(100) NOT NULL,
	password TEXT NOT NULL
);"""

INSERT_STUDENT = "INSERT INTO students (first_name, last_name, login, faculty, group_name, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s);"

CREATE_LECTURERS_EVALUATION = """CREATE TABLE IF NOT EXISTS lecturers_evaluation(
	lecturer_id SERIAL PRIMARY KEY,
	full_name TEXT NOT NULL,
	overall_grade FLOAT,
	grade_1 INTEGER,
	grade_2 INTEGER,
	grade_3 INTEGER,
	grade_4 INTEGER,
	grade_5 INTEGER,
	grade_6 INTEGER,
	lecturer_feedbacks TEXT []
);"""

INSERT_LECTURER = "INSERT INTO lecturers_evaluation (full_name, overall_grade, grade_1, grade_2, grade_3, grade_4, grade_5, grade_6, lecturer_feedbacks) VALUES (%s, %s, %s, %s, %s, %s);"

CREATE_LESSONS_EVALUATION = """CREATE TABLE IF NOT EXISTS lessons_evaluation(
	lesson_id SERIAL PRIMARY KEY,
	lesson_name TEXT NOT NULL,
	lesson_type TEXT,
	lesson_number INTEGER NOT NULL,
	# lesson_room TEXT,
	# faculty_name TEXT,
	group_name TEXT NOT NULL,
	day_number INTEGER NOT NULL, 
	day_name TEXT,
	week_number BOOL NOT NULL,
	# semester INTEGER NOT NULL,
	# academic_year TEXT,
	# date_start DATA,
	# date_finish DATA,
	overall_grade FLOAT NOT NULL,
	lesson_feedbacks TEXT [],
	# rate FLOAT,
	# time_start TEXT NOT NULL, 
	# time_end TEXT NOT NULL,
	lecturer_id INTEGER REFERENCES lecturers_evaluation (lecturer_id) 
);"""

INSERT_LESSON = """INSERT INTO lessons_evaluation(
	lesson_name, 
	lesson_type, 
	lesson_number, 
	# lesson_room, 
	# faculty_name, 
	group_name, 
	day_number, 
	day_name, 
	week_number, 
	# semester, 
	# academic_year,
	# date_start,
	# date_finish,
	overall_grade ,
	lesson_feedbacks,
	# rate,
	# time_start,
	# time_end,
	lecturer_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

CREATE_SCHEDULES = """CREATE TABLE IF NOT EXISTS schedules(
	schedule_id SERIAL PRIMARY KEY,
	lesson_id INTEGER REFERENCES lesson_evaluation (lesson_id),
	lecturer_id INTEGER REFERENCES lecturers_evaluation (lecturer_id),
	full_date DATE
	rate FLOAT,
	time_start TEXT NOT NULL, 
	time_end TEXT NOT NULL,
	semester INTEGER NOT NULL,
	academic_year TEXT,
	date_start DATA,
	date_finish DATA,
	lesson_room TEXT,
	faculty_name TEXT,
	group_name TEXT NOT NULL,
	lesson_type TEXT
);"""

INSERT_SCHEDULE = "INSERT INTO schedules (lesson_id, lecturer_id, full_date, rate, time_start, time_end, semester, academic_year , date_start, date_finish, lesson_room, faculty_name,group_name, lesson_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

# to store info who has voted
CREATE_EVALUATIONS_INFO = """CREATE TABLE IF NOT EXISTS evaluations_info(
	id SERIAL PRIMARY KEY,
	students_id INTEGER REFERENCES students (student_id),
	lesson_id INTEGER REFERENCES lesson_evaluation (lesson_id),
	lecturer_id INTEGER REFERENCES lecturers_evaluation (lecturer_id),
);"""

INSERT_EVALUATION_INFO = "INSERT INTO evaluations_info (students_id, lesson_id, lecturer_id) VALUES (%s, %s, %s);"

GET_SCHEDULE = """SELECT * 
	FROM schedule 
	INNER JOIN lessons_evaluation ON schedule.lesson_id = lessons_evaluation.lesson_id 
	WHERE lessons_evaluation.day_number = %s
	AND lessons_evaluation.week_number = %s
	AND lessons_evaluation.group_number = %s;"""

GET_LECTURER_EVALUATION = """SELECT *
	FROM (lecturers_evaluation
	INNER JOIN lessons_evaluation ON lecturers_evaluation.lecturer_id = lessons_evaluation.lesson_id 
	WHERE lessons_evaluation.day_number = %s
	AND lessons_evaluation.week_number = %s
	AND lessons_evaluation.group_number = %s);"""

GET_LESSON_EVALUATION = """SELECT lessons_evaluation.overall_grade, lessons_evaluation.lesson_feedbacks, lessons_evaluation.lesson_number, lessons_evaluation.lesson_name
	FROM lessons_evaluation 
	WHERE lessons_evaluation.lesson_number = %s 
	AND lessons_evaluation.day_number = %s
	AND lessons_evaluation.week_number = %s
	AND lessons_evaluation.group_number = %s;"""

GET_CREDENTIALS = """SELECT students.login, students.password FROM students WHERE students.login = %s AND students.password = %s"""
#connect to the db
connection = psycopg2.connect(
	host="localhost",
	database="student",
	user="postgres",
	password="group_ip74",
	port=5432)

def create_tables():
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(CREATE_STUDENTS_TABLE)
			cursor.execute(CREATE_LECTURERS_EVALUATION)
			cursor.execute(CREATE_LESSONS_EVALUATION)
			cursor.execute(CREATE_SCHEDULES)
			cursor.execute(CREATE_EVALUATIONS_INFO)

def add_student(first_name, last_name, login, faculty, group_name, email, password):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(INSERT_STUDENT, (first_name, last_name, login, faculty, group_name, email, password))

def add_lesson(
		lesson_name,
		lesson_type,
		lesson_number,
		# lesson_room,
		# faculty_name,
		group_name,
		day_number,
		day_name,
		week_number,
		# semester,
		# academic_year,
		# date_start,
		# date_finish,
		overall_grade ,
		lesson_feedbacks,
		rate,
		time_start,
		time_end,
		lecturer_id):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(INSERT_LESSON, (
				lesson_name,
				lesson_type,
				lesson_number,
				# lesson_room,
				# faculty_name,
				group_name,
				day_number,
				day_name,
				week_number,
				# semester,
				# academic_year,
				# date_start,
				# date_finish,
				overall_grade ,
				lesson_feedbacks,
				lecturer_id)
			)

def add_lecturer(full_name, overall_grade, grade_1, grade_2, grade_3, grade_4, grade_5, grade_6, lecturer_feedbacks):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(INSERT_LECTURER, (full_name, overall_grade, grade_1, grade_2, grade_3, grade_4, grade_5, grade_6, lecturer_feedbacks))

def add_schedule(lesson_id, lecturer_id, full_date, rate, time_start, time_end, semester, academic_year , date_start, date_finish, lesson_room, faculty_name,group_name, lesson_type):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(INSERT_SCHEDULE, (lesson_id, lecturer_id, full_date, rate, time_start, time_end, semester, academic_year , date_start, date_finish, lesson_room, faculty_name,group_name, lesson_type))

def add_evaluation_info(students_id, lesson_id, lecturer_id):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(INSERT_EVALUATION_INFO, (students_id, lesson_id, lecturer_id))

def get_schedule(day_number, week_number, group_number):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(GET_SCHEDULE, (day_number, week_number, group_number))
		return cursor.fetchall()

def get_lecturer_evaluation(day_number, week_number, group_number):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(GET_LECTURER_EVALUATION, (day_number, week_number, group_number))
		return cursor.fetchone()

def get_lesson_evaluation(lesson_number, day_number, week_number, group_number):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(GET_LESSON_EVALUATION, (lesson_number, day_number, week_number, group_number))
		return cursor.fetchone()

def get_lesson_evaluation(login, password):
	with connection:
		with connection.cursor() as cursor:
			cursor.execute(GET_CREDENTIALS, (login, password))
		return cursor.fetchone()