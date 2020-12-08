#!/usr/bin/env bash

python -m pip install -r ./api/study_schedule/requirements.txt --user

gnome-terminal -- python ./api/study_schedule/study_schedule_parser.py
gnome-terminal -- node ./api/index.js
