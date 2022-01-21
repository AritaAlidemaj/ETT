import helpers

rooms = helpers.getRooms()


def RoomsetOverlap():
    roomsetOverlap = []

    for room1 in rooms:
        column = []
        for room2 in rooms:
            result = 0
            secondRoomList = room2["Name"].split('/')
            firstRoomList = room1["Name"].split('/')
            if (room1["Name"] == room2["Name"]
                    and room1["Name"] != "No room needed"):
                column.append(1)
            elif ((room1["Name"] in secondRoomList
                    or room2["Name"] in firstRoomList)
                  and room1["Name"] != "No room needed"):
                column.append(1)
            elif (firstRoomList in secondRoomList
                  or secondRoomList in firstRoomList):
                column.append(1)
            elif len(secondRoomList) == 2 and len(firstRoomList) == 2:
                for room in secondRoomList:
                    if room in room1["Name"]:
                        result = 1
                        break
                column.append(result)
            else:
                column.append(0)
        roomsetOverlap.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(roomsetOverlap):
        if index == 0:
            new_list = str(lists)[0:-1].replace("[", "RoomsetOverlap = [|")
        elif index == len(roomsetOverlap)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()