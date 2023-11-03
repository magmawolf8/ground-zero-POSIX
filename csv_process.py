import csv

with open("lit_clock_annotated.csv", newline='', encoding="utf8") as lit_clock_full:
    lit_clock_reader = csv.reader(lit_clock_full, delimiter='|')
    try:
        while True:
            lit_clock_time=next(lit_clock_reader)
            lit_clock_time[0] = lit_clock_time[0][:2]+lit_clock_time[0][3:]
            print(str(lit_clock_time[0]))
            f=open("C:/Users/hyang/Desktop/meow/times/" + lit_clock_time[0] + ".csv", "a", newline='', encoding="utf8")
            f.write(lit_clock_time[0] + "|" + lit_clock_time[1] + "|" + lit_clock_time[2] + "\n")
            f.close()

    except StopIteration:
        print("bye")
        