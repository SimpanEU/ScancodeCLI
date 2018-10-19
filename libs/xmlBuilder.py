import xml.etree.ElementTree as et
import datetime

def create_wakeup_xml():

    root = et.Element("Task", attrib={"version": "1.2", "xmlns": "http://schemas.microsoft.com/windows/2004/02/mit/task"})

    element = []
    task = ["RegistrationInfo", "Triggers", "Principals", "Settings", "Actions"]
    reginfo = ["Date", "Author", "URI"]
    triggers = ["TimeTrigger"]
    principals = ["Principal"]
    actions = ["Exec"]
    settings = ["MultipleInstancesPolicy", "DisallowStartIfOnBatteries", "StopIfGoingOnBatteries", "AllowHardTerminate",
                        "StartWhenAvailable", "RunOnlyIfNetworkAvailable", "IdleSettings", "AllowStartOnDemand", "Enabled", "Hidden",
                        "RunOnlyIfIdle", "WakeToRun", "ExecutionTimeLimit", "Priority"]

    for name in task:
        if name == "Actions": element.append(et.SubElement(root, name, attrib = {'Context': 'Author'}))
        else: element.append(et.SubElement(root, name))

    for name in reginfo:
        element.append(et.SubElement(element[0], name))

    for name in triggers:
        element.append(et.SubElement(element[1], name))

    for name in principals:
        if name == "Principal": element.append(et.SubElement(element[2], name, attrib={'id': 'Author'}))
        else: element.append(et.SubElement(element[2], name))

    for name in settings:
        element.append(et.SubElement(element[3], name))

    for name in actions:
        element.append(et.SubElement(element[4], name))

    #triggers>timetrigger children
    element.append(et.SubElement(element[8], 'Repetition'))
    element.append(et.SubElement(element[8], 'StartBoundary'))
    element.append(et.SubElement(element[8], 'Enabled'))

    #timetrigger>repetition children
    element.append(et.SubElement(element[25], 'Interval'))
    element.append(et.SubElement(element[25], 'Duration'))
    element.append(et.SubElement(element[25], 'StopAtDurationEnd'))

    #principals>principal children
    element.append(et.SubElement(element[9], 'UserId'))
    element.append(et.SubElement(element[9], 'LogonType'))
    element.append(et.SubElement(element[9], 'RunLevel'))

    #settings>idlesettings children
    element.append(et.SubElement(element[16], 'StopOnIdleEnd'))
    element.append(et.SubElement(element[16], 'RestartOnIdle'))

    #actions>exec children
    element.append(et.SubElement(element[24], 'Command'))

    currentTime = str(datetime.datetime.now())
    currentTime = currentTime[:10]+'T'+currentTime[11:19]
    print(currentTime)

    values = ["", "", "", "", "", currentTime, "SimonN", "\WakeUp", "", "", "IgnoreNew", "false", "false", "true", "false",
              "false", "", "true", "true", "false", "false", "true", "PT72H", "7", "", "", currentTime, "true", "PT1M", "PT30M", "false",
              "S-1-5-21-714594801-1865861827-2143135371-1001", "Password", "HighestAvailable", "true", "false", "C:\\WakeUp.bat"]

    for num, value in enumerate(values):
        element[num].text = value

    for num, name in enumerate(element):
        print(num, name)

    xml = et.tostring(root)
    with open('C:\WakeUpTask.xml', 'wb') as f:
        f.write(xml)

def main():
    create_wakeup_xml()
if __name__ == "__main__":
    main()