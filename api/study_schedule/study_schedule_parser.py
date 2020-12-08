import urllib3
import json
import sys
from lxml import html
from flask import Flask, request, jsonify

url = 'http://api.rozklad.org.ua/v2/groups/{}/lessons'
current_study_week_req = 'https://api.rozklad.org.ua/v2/weeks'

app = Flask(__name__)

def get_study_schedule(url, group_name):
    http = urllib3.PoolManager()
    req = http.request('GET', url.format(group_name))
    return json.loads(req.data.decode('utf-8', errors='ignore'))


def get_current_study_week():
    http = urllib3.PoolManager()
    req = http.request('GET', current_study_week_req)
    return json.loads(req.data.decode('utf-8', errors='ignore'))['data']


def get_current_day_study_schedule(study_schedule, current_study_week, current_day):
    all_lessons = study_schedule['data']
    lessons = []
    for lesson in all_lessons:
        if (lesson['day_number'] == str(current_day) and lesson['lesson_week'] == str(current_study_week)):
            lessons.append(lesson)
    return lessons

@app.route("/get-schedule-current-day", methods=['POST'])
def analyse_sentiment():
    group_name = request.get_json()['group_name']
    day_number = request.get_json()['day_number']

    current_study_week = get_current_study_week()

    study_schedule = get_study_schedule(url, group_name)
    current_day_study_schedule = get_current_day_study_schedule(study_schedule, current_study_week, day_number)

    return jsonify(
        group_name=group_name,
        day_number=day_number,
        current_study_week=current_study_week,
        study_schedule=current_day_study_schedule
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
