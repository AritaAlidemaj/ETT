import json
from flask import Flask, render_template, request
import pymzn

app = Flask(__name__)

app.config["ALLOWED_FILES_EXTENSION"] = ["DZN"]

headings = ["Teacher", "Subject", "Period", "Room"]
eventPeriod = []
eventRoom = []
rooms = []


def allowed_files(filename):

    if not "." in filename:
        return False

    extension = filename.rsplit(".", 1)[1]

    if extension.upper() in app.config["ALLOWED_FILES_EXTENSION"]:
        return True
    else:
        return False


def getTeachers():
    teachers = open('app/teachers.json')
    return json.load(teachers)


def getExams():
    exams = open('app/events.json')
    return json.load(exams)


def getRooms():
    rooms = open('app/rooms.json')
    return json.load(rooms)


def getPeriods():
    periods = open('app/periods.json', encoding='utf-8')
    return json.load(periods)


def getRoomById(id, roomsData=None):
    roomsList = getRooms() if roomsData is None else roomsData
    for room in roomsList:
        if room['Id'] == id:
            return room
    return None


def getTeacherById(id, teachersData=None):
    teachers = getTeachers() if teachersData is None else teachersData
    for teacher in teachers:
        if teacher['Id'] == id:
            return teacher
    return None


def getPeriodById(id, periodsData=None):
    periodsList = getRooms() if periodsData is None else periodsData
    for period in periodsList:
        if period['Id'] == id:
            return period
    return None


def getTable(eventPeriods, eventRooms):
    exams = getExams()
    teachers = getTeachers()
    rooms = getRooms()
    periods = getPeriods()
    table = []

    for examIndex, exam in enumerate(exams):
        row = {
            "ExamId": exam['Id'],
            "Exam": exam['Name'],
            "Teachers": []
        }
        for examTeachersIndex, teacherId in enumerate(exam['Teachers']):
            teacher = getTeacherById(teacherId, teachers)
            if teacher is not None:
                row["Teachers"].append(teacher)

        room = getRoomById(eventRooms[examIndex] if len(
            eventRooms) > examIndex else 0, rooms)
        row["Room"] = room["Name"] if room is not None else "Unknown"

        period = getPeriodById(eventPeriods[examIndex]-1 if len(
            eventPeriods) > examIndex else 0, periods)
        row["Periods"] = period["Name"] if period is not None else "Unknown"

        table.append(row)

    return table


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload", methods=['POST'])
def upload():
    response = {}
    solutions = None
    if request.files:
        dznFile = request.files["dznFile"]
        if allowed_files(dznFile.filename):
            solver = pymzn.Chuffed(solver_id='chuffed')
            dznFileData = dznFile.read().decode('utf-8')
            solutions = pymzn.minizinc(
                'exam_tt.mzn', data=dznFileData, output_mode='json', solver=solver)
            if (len(solutions) <= 0):
                response['error'] = "No solutions"
                return response

    if solutions is None:
        response['error'] = "No solutions"
        return response

    solution = json.loads(str(solutions[0]))
    eventPeriod = solution['EventPeriod']
    eventRoom = solution['EventRoom']
    response['data'] = getTable(eventPeriod, eventRoom)
    return response

if __name__ == "__main__":
    app.run(debug=True)
