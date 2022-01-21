import helpers

courses = helpers.getCourses()
fiek = helpers.getFiek()
exams = helpers.getExams()


def MinDistance():
    minDistance = []

    for exam1 in exams:
        examID = exam1["Id"]
        column = []
        for exam2 in exams:
            exam2ID = exam2["Id"]
            result = 0
            for curricula in courses["Curricula"]:
                if (examID != exam2ID
                    and exam1["Name"] in curricula["PrimaryCourses"]
                        and exam2["Name"] in curricula["PrimaryCourses"]):
                    if ("Oral" in exam1["Name"]
                        and "Written" in exam2["Name"]
                            and examID > exam2ID):
                        for distance in fiek["Courses"]:
                            if (distance["ExamType"] == "WrittenAndOral"
                                and distance["Course"] == exam1["Name"].split('(')[0].rstrip()
                                    and distance["Course"] == exam2["Name"].split('(')[0].rstrip()):
                                result = 0
                                break
                    else:
                        result = 4
                        break
                elif ("Written" in exam1["Name"]
                      and "Oral" in exam2["Name"]
                      and examID < exam2ID):
                    for distance in fiek["Courses"]:
                        if (distance["ExamType"] == "WrittenAndOral"
                            and distance["Course"] == exam1["Name"].split('(')[0].rstrip()
                            and distance["Course"] == exam2["Name"].split('(')[0].rstrip()):
                            result = distance["WrittenOralSpecs"]["MinDistance"]
                            break

            column.append(result)
        minDistance.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(minDistance):
        if index == 0:
            new_list = str(lists)[0:-1].replace("[", "MinDistance = [|")
        elif index == len(minDistance)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()