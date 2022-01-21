import helpers

exams = helpers.getExams()
fiek = helpers.getFiek()
courses = helpers.getCourses()


def Conflicts():
    conflicts = []

    for exam1 in exams:
        column = []
        for exam2 in exams:
            result = 0
            for curricula in courses["Curricula"]:
                for teacher1 in exam1["Teachers"]:
                    for teacher2 in exam2["Teachers"]:
                        if (exam1["Name"] != exam2["Name"]
                                and teacher1 == teacher2):
                            result = -1
                            break
                        elif (exam1["Name"] != exam2["Name"]
                              and exam1["Name"] in curricula["PrimaryCourses"]
                              and exam2["Name"] in curricula["PrimaryCourses"]):
                            result = -1
                            break
                        elif (exam1["Name"] != exam2["Name"]
                              and exam1["Name"] in curricula["PrimaryCourses"]
                              and exam2["Name"] in curricula["SecondaryCourses"]):
                            result = 5
                            break
                        elif (exam1["Name"] != exam2["Name"]
                              and exam2["Name"] in curricula["PrimaryCourses"]
                              and exam1["Name"] in curricula["SecondaryCourses"]):
                            result = 5
                            break
                        elif (exam1["Name"] != exam2["Name"]
                              and exam1["Name"] in curricula["SecondaryCourses"]
                              and exam2["Name"] in curricula["SecondaryCourses"]):
                            result = 1
                            break
            column.append(result)
        conflicts.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(conflicts):
        if index == 0:
            new_list = str(lists)[0:-1].replace("[", "Conflicts = [|")
        elif index == len(conflicts)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()
