import helpers

fiek = helpers.getFiek()


def RoomedEvents():
    RoomedEvent = []

    for exam in fiek["Courses"]:
        if exam["ExamType"] == "Written":
            if exam["NumberOfExams"] != 0:
                RoomedEvent.append(1)
            else:
                RoomedEvent.append(0)
        elif exam["ExamType"] == "WrittenAndOral":
            if exam["NumberOfExams"] != 0:
                RoomedEvent.append(1)
                if exam["WrittenOralSpecs"]["RoomForOral"] == True:
                    RoomedEvent.append(1)
                else:
                    RoomedEvent.append(0)
            else:
                RoomedEvent.append(0)

    file = open('dzn instance/fiek.dzn', 'a')
    line = 'RoomedEvent = {};\n'.format(RoomedEvent)
    file.write(line)
    file.close()
