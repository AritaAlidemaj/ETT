import helpers


fiek = helpers.getFiek()
exams = helpers.getExams()
periods = helpers.getPeriods()


def MaxDistance():
    maxDistance = []

    for exam1 in exams:
        examID = exam1["Id"]
        column = []
        for exam2 in exams:
            exam2ID = exam2["Id"]
            result = len(periods)
            for course in fiek["Courses"]:
                if (exam1["Name"].split("(")[0] == exam2["Name"].split("(")[0]
                    and examID < exam2ID
                    and course["ExamType"] == "WrittenAndOral"):
                    result = course["WrittenOralSpecs"]["MaxDistance"]
            column.append(result)
        maxDistance.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(maxDistance):
        if index == 0:
            new_list = str(lists)[0:-1].replace("[", "MaxDistance = [|")
        elif index == len(maxDistance)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()