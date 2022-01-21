import helpers

rooms = helpers.getRooms()
periods = helpers.getPeriods()
exams = helpers.getExams()
eventRoom = helpers.getEventRoom()


def GetExamRoomProperties(examId):
    exam = helpers.getExamById(examId)
    if exam is None:
        return None

    examRoom = helpers.getExamRoom(exam['Name'])
    if examRoom is None:
        return None

    properties = {
        'IsComposite': False,
        'Type': "Dummy",
        'CompositeType': None
    }

    if (examRoom['NumberOfExams'] == 0):
        return properties

    if (examRoom['RoomsRequested']['Number'] == 1):
        properties['IsComposite'] = False
    elif (examRoom['RoomsRequested']['Number'] == 2):
        properties["IsComposite"] = True

    properties['CompositeType'] = examRoom['RoomsRequested']['Type']
    properties['Type'] = examRoom['RoomsRequested']['Type']

    return properties


def EventRoomConstraints():
    conf = []
    forbidden = -1
    allowed = 0
    for exam in exams:
        column = []
        examRoomProperties = GetExamRoomProperties(exam['Id'])
        for room in rooms:
            if (examRoomProperties is None):
                column.append(forbidden)
                continue

            examRoomIsComposite = examRoomProperties['IsComposite']
            examRoomCompositeType = examRoomProperties['CompositeType']
            examRoomType = examRoomProperties['Type']

            roomIsComposite = room['IsComposite']
            roomCompositeType = room['CompositeType']
            roomType = room['Type']

            if (roomIsComposite):
                if (examRoomIsComposite == roomIsComposite
                        and examRoomCompositeType == roomCompositeType):
                    column.append(allowed)
                else:
                    column.append(forbidden)
            else:
                if (examRoomIsComposite == roomIsComposite
                        and roomType == examRoomType):
                    column.append(allowed)
                else:
                    column.append(forbidden)

        conf.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(conf):
        if index == 0:
            new_list = str(lists)[
                0:-1].replace("[", "EventRoomConstraints = [|")
        elif index == len(eventRoom)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()

