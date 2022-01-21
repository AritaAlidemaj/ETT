import helpers

fiek = helpers.getFiek()
rooms = helpers.getRooms()
periods = helpers.getPeriods()


def RoomPeriodConstraints():
    roomPeriod = []

    for room in rooms:
        column = []
        for period in periods:
            result = 0
            for constraint in fiek["Constraints"]:
                if (constraint["Type"] == "RoomPeriodConstraint"
                        and constraint["Level"] == "Preferred"):
                    result = 2
                elif (constraint["Type"] == "RoomPeriodConstraint"
                      and constraint["Level"] == "Forbidden"):
                    result = -1
                elif (constraint["Type"] == "RoomPeriodConstraint"
                      and constraint["Level"] == "Undesired"):
                    result = 10
            column.append(result)
        roomPeriod.append(column)

    file = open("dzn instance/fiek.dzn", "a")

    for index, lists in enumerate(roomPeriod):
        if index == 0:
            new_list = str(lists)[
                0:-1].replace("[", "RoomPeriodConstraints = [|")
        elif index == len(roomPeriod)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()
