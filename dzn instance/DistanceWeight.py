import helpers

events = helpers.getExams()
courses = helpers.getCourses()


def DistanceWeight():
    distanceWeight = []

    for event1 in events:
        column = []
        for event2 in events:
            result = 0
            column.append(result)
        distanceWeight.append(column)
    # for event1 in events:
    #     column = []
    #     for event2 in events:
    #         result = 0
    #         for curricula in courses["Curricula"]:
    #             if (event1["Name"] != event2["Name"]
    #                 and event1["Name"] in curricula["PrimaryCourses"]
    #                     and event2["Name"] in curricula["PrimaryCourses"]):
    #                 if ("Written" in event1["Name"]
    #                     and "Oral" in event2["Name"]
    #                         and event1["Name"].split('(')[0].rstrip() == event2["Name"].split('(')[0].rstrip()):
    #                     result = 5
    #                     break
    #                 elif ("Oral" in event1["Name"]
    #                       and "Written" in event2["Name"]
    #                       and event1["Name"].split('(')[0].rstrip() == event2["Name"].split('(')[0].rstrip()):
    #                     result = 0
    #                     break
    #                 else:
    #                     result = 5
    #             elif (event1["Name"] != event2["Name"]
    #                   and event1["Name"] in curricula["PrimaryCourses"]
    #                   and event2["Name"] in curricula["SecondaryCourses"]):
    #                 if ("Written" in event1["Name"]
    #                     and "Oral" in event2["Name"]
    #                         and event1["Name"].split('(')[0].rstrip() == event2["Name"].split('(')[0].rstrip()):
    #                     result = 2
    #                     break
    #                 elif ("Oral" in event1["Name"]
    #                       and "Written" in event2["Name"]
    #                       and event1["Name"].split('(')[0].rstrip() == event2["Name"].split('(')[0].rstrip()):
    #                     result = 0
    #                     break
    #                 else:
    #                     result = 2
    #         column.append(result)
    #     distanceWeight.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(distanceWeight):
        if index == 0:
            new_list = str(lists)[
                0:-1].replace("[", "DistanceWeight = [|")
        elif index == len(distanceWeight)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()
