import csv
from datetime import datetime
import random
import os
import antigravity


def get_random_entry(h, m):
    time_csv = (str(h) if h >= 10 else "0" + str(h)) + (str(m) if m >= 10 else "0" + str(m))
    lit_clock_selected = [time_csv, print_words(h, m), print_words(h, m)]
    path = os.path.join(os.getenv("HOME"), "Desktop/meow/times", time_csv + ".csv")

    try:
        with open(path, newline='', encoding="utf8") as lit_clock_time:
            lit_clock_reader = csv.reader(lit_clock_time, delimiter='|')
            try:
                lit_clock_selected = next(lit_clock_reader)
                num = 1
                while True:
                    lit_clock_entry = next(lit_clock_reader)
                    num += 1
                    if random.uniform(0, 1) < 1/num:
                        lit_clock_selected = lit_clock_entry
            except StopIteration:
                pass
    except FileNotFoundError as e:
        print("file not found: " + str(e))
        pass

    return lit_clock_selected


def print_words(h, m):
    nums = ["zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen",
            "fourteen", "fifteen", "sixteen", 
            "seventeen", "eighteen", "nineteen", 
            "twenty", "twenty one", "twenty two", 
            "twenty three", "twenty four", 
            "twenty five", "twenty six", "twenty seven",
            "twenty eight", "twenty nine"]
  
    if (m == 0):
        return nums[h] + " o' clock"
  
    elif (m == 1):
        return "one minute past" + " " + nums[h]
  
    elif (m == 59):
        return "one minute to" + " " + nums[(h % 12) + 1]
  
    elif (m == 15):
        return "quarter past" + " " + nums[h]
  
    elif (m == 30):
        return "half past" + " " + nums[h]
  
    elif (m == 45):
        return "quarter to" + " " + (nums[(h % 12) + 1])
  
    elif (m <= 30):
        return nums[m] + " minutes past" + " " + nums[h]
  
    elif (m > 30):
        return nums[60 - m] + " minutes to" + " " + nums[(h % 12) + 1]
        

def get_prime_factors(num):
    num_left=num

    prime_factors={1}

    i=2

    while i <= num/2:
        if num_left % i == 0:
            prime_factors.add(int(i))
            # print(num_left)

        while num_left  % i == 0:
            num_left  /= i
        
        i+=1

    # print(prime_factors)
    return prime_factors
        
        

def change_window():
    # POSIX systems do not have native functions to manipulate terminal windows
    import subprocess
    subprocess.run(["clear"], shell=True) 



def main():

    output_path = os.path.join("output.txt")
    trace_path = os.path.join("traces", datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt')

    with open(output_path, 'w') as file: file.write('')
    change_window()

    rn = datetime.now()
    lit_data = get_random_entry(int(rn.hour), int(rn.minute))

    print(lit_data[2])

    print("\n\nWhat's on your mind?")

    returns = 0

    i=0

    with open(trace_path, 'a') as file:
        while returns < 2:
            #print(temp_prime_set)
            idea_in = input(": ")
            if idea_in == " ":
                returns += 1
            else:
                returns = 0
                i+=1
                file.write(str(i) + ". " + idea_in + "\n")

    # then, have the user prime factorize the time.
    time_num=rn.hour*100+rn.minute
    temp_prime_set=get_prime_factors(time_num)
    print("\n\nWhat are the distinct prime factors of \"" + lit_data[1] + "\"?")

    while len(temp_prime_set) > 0:
        #print(temp_prime_set)
        try:
            prime_in = int(input(": "))
            #print(temp_prime_set)
            temp_prime_set.remove(prime_in)
        except (KeyError, ValueError):
            print("++++++++++++++++++++++++++++++++ NOT DISTINCT PRIME FACTOR OF " + lit_data[1] + " RESET ++++++++++++++++++++++++++++++++")
            temp_prime_set=get_prime_factors(time_num)

    with open(output_path, 'w') as file: file.write('bye')
    print("bye")


if __name__ == '__main__':
    # open("./times/" + "2328" + ".csv", newline='', encoding="utf8")
    # get_prime_factors(14)
    main()

# make the user find the prime factorization of the number formed by concatenating the hour and the minute. no tabbing out!

# then, exit python program to the batch file. then, do the "press any key to continue" thing
