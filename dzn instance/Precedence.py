import helpers

exams = helpers.getExams()


def Precedence():
    precedence = []

    for exam1 in exams:
        examID = exam1["Id"]
        column = []
        for exam2 in exams:
            exam2ID = exam2["Id"]
            if (examID < exam2ID
                and exam1["Name"] != exam2["Name"]
                and exam1["Name"].split("(")[0] == exam2["Name"].split("(")[0]):
                column.append(1)
            else:
                column.append(0)
        precedence.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(precedence):
        if index == 0:
            new_list = str(lists)[0:-1].replace("[", "Precedence = [|")
        elif index == len(precedence)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()
