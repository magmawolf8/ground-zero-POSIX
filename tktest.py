import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from datetime import datetime

import csv
import random
import re


class Marquee(tk.Canvas):
    def __init__(self, parent, margin=2, borderwidth=1, c1="white", c2="black"):
        super().__init__(parent, borderwidth=borderwidth, bg=c2, highlightthickness=1, highlightbackground=c1)

        self.fps = 60
        self.margin = margin
        self.borderwidth=borderwidth
        self.c1=c1
        self.c2=c2
        
        # start by drawing the text off screen, then asking the canvas
        # how much space we need. Use that to compute the initial size
        # of the canvas. 
        rn=datetime.now()
        self.displayed_min=int(rn.minute)

        text = self.create_text(0, -1000, text=self.get_random_entry(int(rn.hour), int(rn.minute))[2], anchor="w", tags=("text",), font=("Courier", 20), fill=self.c1)
        (x0, y0, x1, y1) = self.bbox("text")
        self.width = (x1 - x0) + (2*margin) + (2*borderwidth)
        self.height = (y1 - y0) + (2*margin) + (2*borderwidth)
        self.configure(width=self.width, height=self.height)

        

        # start the animation
        self.animate()

    def animate(self):
        (x0, y0, x1, y1) = self.bbox("text")
        if x1 < 0 or y0 < 0:
            # everything is off the screen; reset the X
            rn=datetime.now()
            if rn.minute != self.displayed_min:
                self.get_random_entry(int(rn.hour), int(rn.minute))
                self.displayed_min=int(rn.minute)

                self.delete("text")
                text = self.create_text(0, -1000, text=self.get_random_entry(int(rn.hour), int(rn.minute))[2], anchor="w", tags=("text",), font=("Courier", 20), fill=self.c1)
                (x0, y0, x1, y1) = self.bbox("text")
                self.width = (x1 - x0) + (2*self.margin) + (2*self.borderwidth)
                self.height = (y1 - y0) + (2*self.margin) + (2*self.borderwidth)
                self.configure(width=self.width, height=self.height)

            # to be just past the right margin
            x0 = self.winfo_width()
            y0 = int(self.winfo_height()/2)
            self.coords("text", x0, y0)
        else:
            self.move("text", -3, 0)

        # do again in a few milliseconds
        self.after_id = self.after(int(1000/self.fps), self.animate)

    def get_random_entry(self, h, m):

        time_csv=(str(h) if h >= 10 else "0" + str(h)) + (str(m) if m >= 10 else "0" + str(m))
        lit_clock_selected = [time_csv, self.print_words(h, m), self.print_words(h, m)]

        try:
            with open("./times/" + time_csv + ".csv", newline='', encoding="utf8") as lit_clock_time:
                lit_clock_reader = csv.reader(lit_clock_time, delimiter='|')
                try:
                    lit_clock_selected=next(lit_clock_reader)
                    num=1
                    while True:
                        lit_clock_entry = next(lit_clock_reader)
                        num+=1

                        if random.uniform(0, 1) < 1/num:
                            lit_clock_selected=lit_clock_entry
                except StopIteration:
                    pass
        except FileNotFoundError as e:
            print("file not found: " + str(e))
            pass

        return lit_clock_selected


    def print_words(self, h, m):
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
        
    def get_displayedmin(self):
        return self.displayed_min
        



class ProgressClock(tk.Frame):
    def __init__(self, parent, width, c2="black", c1="white"):
        super().__init__(parent, width=width, bg=c2, highlightthickness=1, highlightbackground=c1)

        # Composite frame for hour progress bar and label
        self.hour_frame = tk.Frame(self, width=width, bg=c2)
        #self.hour_frame.pack_propagate(False)  # Prevent resizing of frame by children
        self.hour_progress = ttk.Progressbar(self.hour_frame, style="Horizontal.TProgressbar", orient="horizontal", mode="determinate", maximum=23)
        self.hour_progress.pack(fill=tk.BOTH, expand=True)
        self.hour_label = tk.Label(self.hour_frame, text="24HOUR: 00", font=("Courier", 8), fg=c1, bg=c2)
        self.hour_label.place(relx=0.5, rely=0.42, anchor='center')

        # Composite frame for minute progress bar and label
        self.minute_frame = tk.Frame(self, width=width, bg=c2)
        #self.minute_frame.pack_propagate(False)
        self.minute_progress = ttk.Progressbar(self.minute_frame, style="Horizontal.TProgressbar", orient="horizontal", mode="determinate", maximum=59)
        self.minute_progress.pack(fill=tk.BOTH, expand=True)
        self.minute_label = tk.Label(self.minute_frame, text="MINUTE: 00", font=("Courier", 8), fg=c1, bg=c2)
        self.minute_label.place(relx=0.5, rely=0.42, anchor='center')

        # Composite frame for second progress bar and label
        self.second_frame = tk.Frame(self, width=width, bg=c2)
        #self.second_frame.pack_propagate(False)
        self.second_progress = ttk.Progressbar(self.second_frame, style="Horizontal.TProgressbar", orient="horizontal", mode="determinate", maximum=59)
        self.second_progress.pack(fill=tk.BOTH, expand=True)
        self.second_label = tk.Label(self.second_frame, text="SECOND: 00", font=("Courier", 8), fg=c1, bg=c2)
        self.second_label.place(relx=0.5, rely=0.42, anchor='center')

        # Pack the frames
        self.hour_frame.pack(fill=tk.X, expand=True)
        self.minute_frame.pack(fill=tk.X, expand=True)
        self.second_frame.pack(fill=tk.X, expand=True)

        # Start the animation
        self.animate()

    def animate(self):
        rn = datetime.now()
        self.hour_label['text'] = f"TFHOUR: {rn.hour}"
        self.hour_progress['value'] = rn.hour
        self.minute_label['text'] = f"MINUTE: {rn.minute}"
        self.minute_progress['value'] = rn.minute
        self.second_label['text'] = f"SECOND: {rn.second}"
        self.second_progress['value'] = rn.second

        # Calculate remaining milliseconds until the next second
        millisec_until_next_sec = (1000 - rn.microsecond // 1000) if (1000 - rn.microsecond // 1000) < 1000 else 1000 

        # self.rainbows(abs((rn.microsecond // 1000)-500)*4/5 + 380)

        # Schedule the next update at the beginning of the next second
        self.after(millisec_until_next_sec, self.animate)

    
    def rainbows(self, wavelength):
        gamma = 0.80
        intensity_max = 255

        if 380 <= wavelength <= 440:
            attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
            R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
            G = 0.0
            B = (1.0 * attenuation) ** gamma
        elif 440 <= wavelength <= 490:
            R = 0.0
            G = ((wavelength - 440) / (490 - 440)) ** gamma
            B = 1.0
        elif 490 <= wavelength <= 510:
            R = 0.0
            G = 1.0
            B = (-(wavelength - 510) / (510 - 490)) ** gamma
        elif 510 <= wavelength <= 580:
            R = ((wavelength - 510) / (580 - 510)) ** gamma
            G = 1.0
            B = 0.0
        elif 580 <= wavelength <= 645:
            R = 1.0
            G = (-(wavelength - 645) / (645 - 580)) ** gamma
            B = 0.0
        elif 645 <= wavelength <= 780:
            attenuation = 0.3 + 0.7 * (780 - wavelength) / (780 - 645)
            R = (1.0 * attenuation) ** gamma
            G = 0.0
            B = 0.0
        else:
            R = 0.0
            G = 0.0
            B = 0.0

        # Scale to max intensity
        R *= intensity_max
        G *= intensity_max
        B *= intensity_max

        self.set_progress_color(('#%02x%02x%02x' % (int(R), int(G), int(B))))
    
    
    def set_progress_color(self, color):
        self.hour_label['bg'] = color
        self.minute_label['bg'] = color
        self.second_label['bg'] = color
    
        style.configure("Horizontal.TProgressbar", background=color, troughcolor=dark_bg, bordercolor=dark_bg)
        root.configure(bg=color)
    

class PrimeFun(tk.Frame):
    def __init__(self, parent, width, trigger, c2="black", c1="white"):
        super().__init__(parent, width=width, bg=c2, highlightthickness=1, highlightbackground=c1)

        self.c1=c1
        self.c2=c2

        self.enable_entry()

        self.prime_entry = tk.Entry(self, validate="key", validatecommand=(root.register(self.only_numbers), '%S'), relief="flat", font=("Courier", 40), highlightthickness=1)
        self.set_entry_color(outline=self.c1, background=self.c2, text=self.c1)
        self.primes_box = tk.Label(self, text="[]", font=("Courier", 40))# tk text box, storing primes. right aligned, find two sets named entered and not_entered, this one displaying entered primes
        self.set_primes_box_color(background=c2, text=self.c1, outline=c1)

        self.prime_entry.pack(side='left', padx=5, pady=5)
        self.primes_box.pack(side='left', expand=False, fill=None)

        self.change_trigger(trigger)

        self.prime_entry.bind("<Return>", self.return_key)


    def return_key(self, event):
        return self.entry_in_all_primes()


    def primes_clear(self): # clears the internal accepted primes list (and the display)

        self.all_primes=self.get_prime_dict(self.trigger)
        self.accepted_primes=[]
        self.set_primes_box_color(outline="red", background="red", text=self.c2)

        print("before scheduling clearing " + str(datetime.now()))
        self.after(500, self.primes_box_clear)
        print("clearing primes box scheduled at " + str(datetime.now()))

    def primes_update(self, prime): # updates the internal tracking (subsequently the display) of primes, including accepted_primes
        self.all_primes[prime] = self.all_primes[prime] - 1
        if self.all_primes[prime] == 0:
            del self.all_primes[prime]

        self.accepted_primes.append(prime)

        self.after(500, self.primes_box_update)

    def prime_refuse(self):
        self.primes_clear()
        print("completion scheduled at " + str(datetime.now()))
        self.disable_entry()
        self.set_entry_color(outline="red", background="red", text=self.c2)
        #then
        self.after(500, self.entry_clear)

    def prime_accept(self, prime):
        self.primes_update(prime)
        self.disable_entry()
        self.set_entry_color(outline="green", background="green", text=self.c2)
        #after half a second,
        self.after(500, self.entry_clear)

    def change_trigger(self, new_trigger):
        self.trigger=new_trigger
        self.primes_clear()
        self.set_entry_color(outline="blue", background="blue", text=self.c2)
        #self.disable_entry()

        self.after(500, lambda: self.set_entry_color(outline=self.c1, background=self.c2, text=self.c1))


    def entry_in_all_primes(self):
        rn_entry = int(self.prime_entry.get() if self.prime_entry.get() != "" else 1)
        if rn_entry in self.all_primes:
            self.prime_accept(rn_entry)
            return True
        
        self.prime_refuse()
        return False
    


    # functions governing the entry box

    def only_numbers(self, char):
        print("this is called, " + str(char.isdigit()) + str(self.allow_input))
        return char.isdigit() and self.allow_input

    def entry_clear(self):
        self.enable_entry()
        self.prime_entry.delete(0, tk.END)
        self.set_entry_color(outline=self.c1, background=self.c2, text=self.c1)

    def disable_entry(self):
        print("disable_entry is being called")
        self.allow_input = False

    def enable_entry(self):
        self.allow_input = True

    def set_entry_color(self, outline, background, text): # change color of text and outline
        self.prime_entry.configure(highlightcolor=outline, highlightbackground=outline, insertbackground=outline, bg=background, fg=text)


    # functions governing the prime box

    def primes_box_clear(self):
        print("bruh")
        self.primes_box['text'] = "[]"
        #def# clear text
        self.set_primes_box_color(text=self.c1, outline=self.c1, background=self.c2)


    def primes_box_update(self):
        self.primes_box['text'] = str(self.accepted_primes)
        #def# update primes box display
        # anything else?

    def set_primes_box_color(self, outline, background, text):
        self.primes_box.configure(highlightcolor=outline, highlightbackground=outline, bg=background, fg=text)


    
    # GET functions

    def get_prime_dict(self, n):

        if n <= 0:
            return {}
        
        factors = {}
        # Check for divisibility by 2
        count = 0
        while n % 2 == 0:
            count += 1
            n //= 2
        if count > 0:
            factors[2] = count

        # Check for odd factors
        factor = 3
        while n > 1:
            count = 0
            while n % factor == 0:
                count += 1
                n //= factor
            if count > 0:
                factors[factor] = count
            factor += 2

        return factors


    def get_complete(self):
        return not self.all_primes






root = tk.Tk()
root.title("Ground Zero")

dark_bg = "#000000"
dark_fg = "#FFFFFF"

root.configure(bg=dark_bg)
root.attributes('-fullscreen', True)  # For fullscreen

style = ThemedStyle(root)
style.set_theme('black')
style.configure("Horizontal.TProgressbar", background=dark_fg, troughcolor=dark_bg, bordercolor=dark_bg)


# Create frames for each section
top_frame = tk.Frame(root, height=root.winfo_screenheight()//5)
middle_frame = tk.Frame(root, height=root.winfo_screenheight()//5)
bottom_frame = tk.Frame(root, height=3*root.winfo_screenheight()//5)

top_frame.configure(bg=dark_bg)
middle_frame.configure(bg=dark_bg)
bottom_frame.configure(bg=dark_bg)

top_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10)
middle_frame.pack(side=tk.TOP, fill=tk.BOTH)
bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Subdivide middle frame
rn = datetime.now()
left_middle_frame = ProgressClock(middle_frame, width=root.winfo_screenwidth()//2, c2=dark_bg, c1=dark_fg)
right_middle_frame = PrimeFun(middle_frame, width=root.winfo_screenwidth()//2, trigger=int(rn.hour * 100) + int(rn.minute), c2=dark_bg, c1=dark_fg)

right_middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10,5), expand=True)
left_middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5,10), expand=True)


# Top frame text
explanation_text = Marquee(top_frame, borderwidth=1, c2=dark_bg, c1=dark_fg)
explanation_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Bottom frame - large text input box
large_text_box = tk.Text(bottom_frame, relief="flat", font=("Courier", 20))
large_text_box.configure(bg=dark_bg, fg=dark_fg, insertbackground=dark_fg, highlightthickness=1, highlightbackground=dark_fg)
large_text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)


root.mainloop()
