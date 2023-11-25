import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from datetime import datetime

import csv
import random
import math
import re


from threading import Thread
import os


class Marquee(tk.Canvas):
    def __init__(self, parent, margin=2, borderwidth=1, c1="white", c2="black"):
        super().__init__(parent, borderwidth=borderwidth, bg=c2, highlightthickness=1, highlightbackground=c1)

        self.fps = 45
        self.margin = margin
        self.borderwidth = borderwidth
        self.c1 = c1
        self.c2 = c2
        
        self.displayed_min = -1  # Invalid initial value to ensure update
        self.current_text = ""
        #self.load_text_data()
        self.init_text_widget()
        self.animate()

    def init_text_widget(self):
        self.text_widget = self.create_text(0, -1000, anchor="w", tags=("text",), font=("Courier", 20), fill=self.c1)
        #self.update_text_content()

    def tick(self, rn):
        if rn.minute != self.displayed_min:
            new_text = self.get_random_entry(int(rn.hour), int(rn.minute))[2]
            if new_text != self.current_text:
                self.current_text = new_text
                self.itemconfig(self.text_widget, text=new_text)
                self.displayed_min = int(rn.minute)
                self.update_widget_size()

    def update_widget_size(self):
        (x0, y0, x1, y1) = self.bbox("text")
        self.width = (x1 - x0) + (2 * self.margin) + (2 * self.borderwidth)
        self.height = (y1 - y0) + (2 * self.margin) + (2 * self.borderwidth)
        self.configure(width=self.width, height=self.height)

    def animate(self):
        #self.update_text_content()
        self.move_text()
        self.blackbody_to_rgb(abs((datetime.now().second * 1000 + datetime.now().microsecond//1000)-30000)*2/3+500)
        self.after(int(1000 / self.fps), self.animate)

    def move_text(self):
        (x0, y0, x1, y1) = self.bbox("text")
        if x1 < 0:
            x0 = self.winfo_width()
        else:
            x0 -= 4  # Speed of text movement
        y0 = int(self.winfo_height() / 2)
        self.coords("text", x0, y0)

    def get_random_entry(self, h, m):

        time_csv=(str(h) if h >= 10 else "0" + str(h)) + (str(m) if m >= 10 else "0" + str(m))
        lit_clock_selected = [time_csv, self.print_words(h, m), self.print_words(h, m)]

        try:
            with open(os.path.join(os.getcwd(), "times", time_csv + ".csv"),newline='', encoding="utf8") as lit_clock_time:
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
    
    def get_displayed_min(self):
        return self.displayed_min


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
        
    def blackbody_to_rgb(self, temperature):
        # Constants for the calculation
        intensity_max = 255

        # Convert temperature to Kelvin
        temperature = temperature / 100

        # Calculate Red
        if temperature <= 66:
            R = intensity_max
        else:
            R = temperature - 60
            R = 329.698727446 * (R ** -0.1332047592)
            R = max(0, min(intensity_max, R))

        # Calculate Green
        if temperature <= 66:
            G = temperature
            G = 99.4708025861 * math.log(G) - 161.1195681661
        else:
            G = temperature - 60
            G = 288.1221695283 * (G ** -0.0755148492)
        G = max(0, min(intensity_max, G))

        # Calculate Blue
        if temperature >= 66:
            B = intensity_max
        elif temperature <= 19:
            B = 0
        else:
            B = temperature - 10
            B = 138.5177312231 * math.log(B) - 305.0447927307
            B = max(0, min(intensity_max, B))

        self.itemconfig("text", fill=('#%02x%02x%02x' % (int(R), int(G), int(B))))
        #self.set_progress_color(('#%02x%02x%02x' % (int(R), int(G), int(B))))



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
        #self.animate()

    def tock(self, rn):
        self.hour_label['text'] = f"TFHOUR: {rn.hour}"
        self.hour_progress['value'] = rn.hour
        self.minute_label['text'] = f"MINUTE: {rn.minute}"
        self.minute_progress['value'] = rn.minute
        self.second_label['text'] = f"SECOND: {rn.second}"
        self.second_progress['value'] = rn.second

        # Calculate remaining milliseconds until the next second
        millisec_until_next_sec = (1000 - rn.microsecond // 1000) if (1000 - rn.microsecond // 1000) < 1000 else 1000 

        #self.after(millisec_until_next_sec, self.animate)
    

class PrimeFun(tk.Frame):
    def __init__(self, parent, width, trigger, c2="black", c1="white"):
        super().__init__(parent, width=width, bg=c2, highlightthickness=1, highlightbackground=c1)

        self.c1=c1
        self.c2=c2

        self.enable_entry()

        self.prime_entry = tk.Entry(self, validate="key", validatecommand=(self.register(self.only_numbers_valid_times), '%S'), relief="flat", font=("Courier", 40), highlightthickness=1)
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

    def only_numbers_valid_times(self, char):
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
    



class TextEditor(tk.Frame):
    def __init__(self, parent, bg_color, fg_color, font=("Courier", 20), *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(bg=bg_color)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create the text box
        self.text_box = tk.Text(self, relief="flat", font=font, bg=bg_color, fg=fg_color, insertbackground=fg_color, highlightthickness=1, highlightbackground=fg_color)
        self.text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def save(self, filename):
        # Save the content in another thread
        thread = Thread(target=self._save_content, args=(filename,))
        thread.start()

    def _save_content(self, filename):
        # Get the content of the text box
        content = self.text_box.get("1.0", tk.END)

        # Create the directory if it doesn't exist
        directory = '.traces'

        full = os.path.join(os.getcwd(), "traces", filename)

        # Write the content to the file
        with open(full, 'w', encoding='utf-8') as file:
            file.write(content)
        print("Content saved to:", full)





class GroundZero(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ground Zero")
        self.dark_bg = "#000000"
        self.dark_fg = "#FFFFFF"

        self.configure(bg=self.dark_bg)
        self.attributes('-fullscreen', True)  # For fullscreen
        self.configure_styles()
        self.create_widgets()

        self.last_checked_second=-1

    def configure_styles(self):
        self.style = ThemedStyle(self)
        self.style.set_theme('black')
        self.style.configure("Horizontal.TProgressbar", background=self.dark_fg, troughcolor=self.dark_bg, bordercolor=self.dark_bg)

    def create_widgets(self):
        self.create_top_frame()
        self.create_middle_frame()
        self.create_bottom_frame()

    def create_top_frame(self):
        self.top_frame = tk.Frame(self, height=self.winfo_screenheight() // 5, bg=self.dark_bg)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10)
        self.marquee = Marquee(self.top_frame, borderwidth=1, c2=self.dark_bg, c1=self.dark_fg)
        self.marquee.pack(pady=10, fill=tk.BOTH, expand=True)

    def create_middle_frame(self):
        self.middle_frame = tk.Frame(self, height=self.winfo_screenheight() // 5, bg=self.dark_bg)
        self.middle_frame.pack(side=tk.TOP, fill=tk.BOTH)
        rn = datetime.now()
        self.right_clock = ProgressClock(self.middle_frame, width=self.winfo_screenwidth() // 2, c2=self.dark_bg, c1=self.dark_fg)
        self.left_primes = PrimeFun(self.middle_frame, width=self.winfo_screenwidth() // 2, trigger=int(rn.hour * 100) + int(rn.minute), c2=self.dark_bg, c1=self.dark_fg)
        self.left_primes.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 5), expand=True)
        self.right_clock.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 10), expand=True)

    def create_bottom_frame(self):
        self.bottom_frame = TextEditor(self, height=3 * self.winfo_screenheight() // 5, bg_color=self.dark_bg, fg_color=self.dark_fg)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def goes_the_clock(self):
        rn=datetime.now()
        
        if self.left_primes.get_complete(): # exit if we're all finished
            self.destroy()
            return

        #self.after_idle I accidentally typed this... or autocomplete or something. that's interesting that I decided to type that. i'll keep it!
        self.right_clock.tock(rn)
        
        if self.marquee and self.marquee.get_displayed_min() != rn.minute:
            self.left_primes.change_trigger(int(rn.hour * 100) + int(rn.minute))
            self.marquee.tick(rn)
            self.bottom_frame.save(f'{datetime.now().strftime("%Y%m%dT%H%M%S")}.txt')
        self.after((1000 - rn.microsecond // 1000), self.goes_the_clock)

    def run(self):
        self.after((1000 - datetime.now().microsecond // 1000), self.goes_the_clock)
        self.mainloop()

if __name__ == "__main__":
    app = GroundZero()
    app.run()