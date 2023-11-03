with open("triggers.txt", "w") as w:
    h=0
    m=0
    for t in range(0, 1440, 40):
        h = int(t / 60)
        m = int(t % 60)
        s = int(60 * (t % 1))
        w.write("<CalendarTrigger>\n<StartBoundary>2023-07-07T" + (str(h) if h >= 10 else "0" + str(h)) + ":" + (str(m) if m >= 10 else "0" + str(m)) + ":" + (str(s) if s >= 10 else "0" + str(s)) + "</StartBoundary>\n<RandomDelay>PT30M</RandomDelay>\n<Enabled>true</Enabled>\n<ScheduleByDay>\n<DaysInterval>1</DaysInterval>\n</ScheduleByDay>\n</CalendarTrigger>\n")