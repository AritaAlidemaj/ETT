import Conflicts
import DistanceWeight
import EventPeriodConstraints
import EventRoomConstraints
import MaxDistance
import MinDistance
import Precedence
import RoomedEvents
import RoomPeriodConstraints
import RoomsetOverlap
import helpers


def main():
    events = 'Events = ' + str(len(helpers.getExams())) + ';\n'
    periods = 'Periods = ' + str(len(helpers.getPeriods())) + ';\n'
    rooms = 'Rooms = ' + str(len(helpers.getRooms())) + ';\n'

    list = [events, periods, rooms]

    file = open('dzn instance/fiek.dzn', 'a')
    for variable in list:
        file.write(variable)
    file.close()

    RoomedEvents.RoomedEvents()
    Conflicts.Conflicts()
    DistanceWeight.DistanceWeight()
    MinDistance.MinDistance()
    MaxDistance.MaxDistance()
    Precedence.Precedence()
    EventPeriodConstraints.EventPeriodConstraints()
    RoomPeriodConstraints.RoomPeriodConstraints()
    EventRoomConstraints.EventRoomConstraints()
    RoomsetOverlap.RoomsetOverlap()

    return file


f = open('dzn instance/fiek.dzn',  "w+")
if f.read() != None:
    f.write('')
    main()
else:
    main()
