import tkinter
import threading
import time
import os
import sys


class Window(tkinter.Tk):
    def __init__(self, height, width, start_pos_x, start_pos_y, bg):
        self.window = super().__init__()
        self.configuration = super().configure(bg=bg)
        self.geometry = super().geometry(f"{height}x{width}+{start_pos_x}+{start_pos_y}")
        self.text_bg = tkinter.Canvas(width=800, height=120, bg='#002e63')
        self.text_bg.pack()
        self.lbl = tkinter.Label(self, text="Type Here", fg='green', font=("Helvetica", 25), bg='#000a17')
        self.lbl.pack(pady='5')
        self.entry = tkinter.Entry(self, width=50, font=("Helvetica", 20))
        self.entry.pack(ipady='2')
        self.req_text = tkinter.Text(self.text_bg, width=44, height=3, bg='#002e63', fg='white', font=("Helvetica", 25))
        self.req_text.place(x=2, y=4)
        self.req_text.configure(state='disabled')
        self.time = [0, 0]
        self.timer = tkinter.Label(self, text=f"{':'.join([str(i_) for i_ in self.time])} Minutes Elapsed",
                                   fg='yellow', font=("Helvetica", 20), bg='#000a17')
        self.t1 = threading.Thread(target=self._increment_time, daemon=True)
        self.calculate_btn = tkinter.Button(self, bg='Purple', font=("Helvetica", 20), fg='White', text='Calculate',
                                            command=self.return_result, borderwidth='0')
        self.wpm_lbl = tkinter.Label(self, fg='green', font=("Helvetica", 20), bg='#000a17')
        self.accuracy_lbl = tkinter.Label(self, fg='green', font=("Helvetica", 20), bg='#000a17')
        self.time_lbl = tkinter.Label(self, fg='green', font=("Helvetica", 20), bg='#000a17')
        self.total_correct_characters_lbl = tkinter.Label(self, fg='green', font=("Helvetica", 20), bg='#000a17')
        self.total_correct_words_lbl = tkinter.Label(self, fg='green', font=("Helvetica", 20), bg='#000a17')

    def add_text(self, new_text):
        self.req_text.configure(state='normal')
        self.req_text.insert(tkinter.INSERT, new_text)
        self.req_text.configure(state='disabled')
        self.req_text.tag_add("Correct", "1.0", "1.0")
        self.req_text.tag_add("Wrong", "1.0", "1.0")
        self.req_text.tag_add("Current", "1.0", "1.0")
        self.req_text.tag_add("Normal", "1.0", "1.0")
        self.req_text.tag_config("Correct", foreground="light green")
        self.req_text.tag_config("Wrong", foreground="red")
        self.req_text.tag_config("Current", foreground="blue")
        self.req_text.tag_config("Normal", foreground="white")

    def mark(self, mark_type, start_idx, end_idx):
        self.req_text.tag_add(mark_type, str(start_idx), str(end_idx))

    def un_mark(self, start_idx, end_idx):
        self.req_text.tag_remove(self.req_text.tag_names(start_idx)[0], start_idx, end_idx)

    def get_user_input(self):
        return self.entry.get()

    def bind_user_input(self, func):
        self.entry.bind('<Key>', func)

    def see_text(self, idx):
        self.req_text.see(str(idx))

    def clear_input(self):
        self.entry.delete(0, 'end')

    def _increment_time(self):
        # time[0] = minutes, time[1] = secs
        while True:
            time.sleep(1)
            if self.time[0] == 10:
                self.return_result()
                return
            if self.time[1] == 59:
                self.time[1] = 0
                self.time[0] += 1
            else:
                self.time[1] += 1
            self.timer["text"] = f"{self.time[0]}:{self.time[1]} Minutes Elapsed"

    def run_timer(self):
        if not self.t1.is_alive():
            self.timer.pack()
            self.t1.start()
            return True
        else:
            return False

    def place_calculate_btn(self):
        if self.calculate_btn.winfo_viewable:
            self.calculate_btn.pack()
            return True
        else:
            return False

    def forget_calculate_btn(self):
        self.calculate_btn.pack_forget()

    def return_result(self):
        self.timer.pack_forget()
        correct_chars = []
        curr_char_idx = 0
        curr_line = 1
        curr_idx = 0
        total_chars = 0
        while True:
            tag = self.req_text.tag_names(f"{curr_line}.{curr_idx}")
            if tag:
                total_chars += 1
                if tag[0] == "Correct":
                    correct_chars.append(self.words_string_list[curr_char_idx])
            elif not tag:
                curr_line += 1
                curr_idx = -1
                if not self.req_text.tag_names(f"{curr_line}.{curr_idx+1}"):
                    break
            curr_idx += 1
            curr_char_idx += 1
        unwrapped_words = []
        for word in self.words_list:
            unwrapped_words.append(self.reg.sub('', word))
        user_words = ''.join(correct_chars).split(' ')
        total_correct_chars = len(correct_chars)
        total_correct_words = 0
        for x, y in zip(user_words, unwrapped_words):
            if not x:
                break
            if x.lower() == y.lower():
                total_correct_words += 1
        wpm = ((total_chars / 5) - (total_chars - total_correct_chars)) / (self.time[0] + (self.time[1] / 60))
        accuracy = (total_correct_chars / total_chars) * 100
        self.calculate_btn.pack_forget()
        self.wpm_lbl["text"] = f"WPM: {round(wpm, 2)}"
        self.accuracy_lbl["text"] = f"Accuracy: {round(accuracy, 2)}%"
        self.time_lbl["text"] = f"Time: {self.time[0]} Minutes {self.time[1]} Seconds"
        self.total_correct_words_lbl["text"] = f"Total Correct Words: {total_correct_words}"
        self.total_correct_characters_lbl["text"] = f"Total Correct Characters: {total_correct_chars}"
        self.entry.delete(0, 'end')
        self.entry.config(state='disabled')
        self.wpm_lbl.pack()
        self.accuracy_lbl.pack()
        self.time_lbl.pack()
        self.total_correct_words_lbl.pack()
        self.total_correct_characters_lbl.pack()
