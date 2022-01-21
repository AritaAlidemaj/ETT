import helpers

fiek = helpers.getFiek()
periods = helpers.getPeriods()
events = helpers.getExams()


def EventPeriodConstraints():
    eventPeriod = []

    for event in events:
        column = []
        for period in periods:
            periodID = period["Id"]
            result = 0
            for constraint in fiek["Constraints"]:
                if (constraint["Course"] == event["Name"]
                        and constraint["Period"] == periodID
                        and constraint["Type"] == "EventPeriodConstraint"):
                    result = 2
                    break
                elif ("Written" in event["Name"]
                        and constraint["Course"] == event["Name"].split("(")[0].rstrip()
                        and constraint["Period"] == periodID and constraint["Type"] == "EventPeriodConstraint"):
                    result = 2
                    break
            column.append(result)
        eventPeriod.append(column)

    file = open('dzn instance/fiek.dzn', 'a')

    for index, lists in enumerate(eventPeriod):
        if index == 0:
            new_list = str(lists)[
                0:-1].replace("[", "EventPeriodConstraints = [|")
        elif index == len(eventPeriod)-1:
            new_list = str(lists)[0:-1].replace(str(lists)[0:-1],
                                                str(lists)[0:-1] + "|];").replace('[', "|")
        else:
            new_list = str(lists)[0:-1].replace("[", "|")

        line = new_list + "\n"
        file.write(line)

    file.close()

