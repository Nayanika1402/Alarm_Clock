import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import time
import threading
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("⏰ Stylish Python Alarm Clock")
        self.root.geometry("480x620")
        self.root.configure(bg="#f4f7fc")

        self.alarm_time = None
        self.alarm_thread = None
        self.alarm_active = False
        self.snooze_minutes = 5
        self.alarm_tone = None

        # Title Label
        tk.Label(root, text="Alarm Clock", font=("Poppins", 22, "bold"), fg="#333", bg="#f4f7fc").pack(pady=15)

        # Clock Display with Circular Frame
        self.clock_canvas = tk.Canvas(root, width=250, height=250, bg="#f4f7fc", highlightthickness=0)
        self.clock_canvas.pack()
        self.clock_canvas.create_oval(25, 25, 225, 225, outline="#6c63ff", width=5, fill="#dcdcff")
        self.time_text = self.clock_canvas.create_text(125, 125, text="", font=("Helvetica", 28, "bold"), fill="#333")
        self.update_clock_time()

        # Alarm Time Inputs
        time_frame = tk.Frame(root, bg="#f4f7fc")
        time_frame.pack(pady=15)

        self.hour_var = tk.StringVar(value="00")
        self.min_var = tk.StringVar(value="00")

        tk.Label(time_frame, text="Hour", font=("Helvetica", 12), bg="#f4f7fc").grid(row=0, column=0, padx=8)
        tk.Entry(time_frame, textvariable=self.hour_var, width=5, font=("Helvetica", 12)).grid(row=0, column=1, padx=5)

        tk.Label(time_frame, text="Minute", font=("Helvetica", 12), bg="#f4f7fc").grid(row=0, column=2, padx=8)
        tk.Entry(time_frame, textvariable=self.min_var, width=5, font=("Helvetica", 12)).grid(row=0, column=3, padx=5)

        # Alarm Tone Dropdown
        tk.Label(root, text="🎵 Select Alarm Tone", font=("Helvetica", 12, "bold"), bg="#f4f7fc").pack(pady=(10, 5))
        self.tones = ["tone1.mp3", "tone2.mp3", "tone3.mp3", "tone4.mp3", "tone5.mp3"]
        self.tone_var = tk.StringVar()
        self.tone_dropdown = ttk.Combobox(root, values=self.tones, textvariable=self.tone_var, state="readonly", font=("Helvetica", 11))
        self.tone_dropdown.set("tone1.mp3")
        self.tone_dropdown.pack()

        # Snooze Spinner
        tk.Label(root, text="😴 Snooze Duration (minutes)", font=("Helvetica", 12, "bold"), bg="#f4f7fc").pack(pady=(15, 5))
        self.snooze_spin = ttk.Spinbox(root, from_=1, to=30, width=5, font=("Helvetica", 11))
        self.snooze_spin.set(self.snooze_minutes)
        self.snooze_spin.pack()

        # Buttons
        btn_frame = tk.Frame(root, bg="#f4f7fc")
        btn_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11, "bold"), padding=6)
        style.map("TButton", foreground=[('active', '#fff')], background=[('active', '#6c63ff')])

        ttk.Button(btn_frame, text="✅ Set Alarm", command=self.set_alarm).grid(row=0, column=0, padx=15)
        ttk.Button(btn_frame, text="⛔ Stop Alarm", command=self.stop_alarm).grid(row=0, column=1, padx=15)

    def update_clock_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_canvas.itemconfig(self.time_text, text=now)
        self.root.after(1000, self.update_clock_time)

    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.min_var.get())
            now = datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if alarm_time < now:
                alarm_time += timedelta(days=1)

            self.alarm_time = alarm_time
            self.snooze_minutes = int(self.snooze_spin.get())

            selected_tone = self.tone_var.get()
            tone_path = os.path.join("alarm_tones", selected_tone)

            if not os.path.exists(tone_path):
                messagebox.showerror("Tone Missing", f"{selected_tone} not found in alarm_tones folder.")
                return

            self.alarm_tone = tone_path
            self.alarm_active = True

            self.alarm_thread = threading.Thread(target=self.check_alarm)
            self.alarm_thread.daemon = True
            self.alarm_thread.start()

            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time.strftime('%H:%M')}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for hour and minute.")

    def check_alarm(self):
        while self.alarm_active:
            if datetime.now() >= self.alarm_time:
                self.play_alarm()
                self.show_snooze_popup()
                break
            time.sleep(1)

    def play_alarm(self):
        pygame.mixer.music.load(self.alarm_tone)
        pygame.mixer.music.play(-1)

    def stop_alarm(self):
        self.alarm_active = False
        pygame.mixer.music.stop()

    def snooze(self):
        pygame.mixer.music.stop()
        self.alarm_time = datetime.now() + timedelta(minutes=self.snooze_minutes)
        self.alarm_thread = threading.Thread(target=self.check_alarm)
        self.alarm_thread.daemon = True
        self.alarm_thread.start()

    def show_snooze_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("⏰ Alarm")
        popup.geometry("260x130")
        popup.config(bg="#fff3cd")

        tk.Label(popup, text="🔔 Wake Up!", font=("Helvetica", 16, "bold"), bg="#fff3cd").pack(pady=10)
        ttk.Button(popup, text="Snooze", command=lambda: [popup.destroy(), self.snooze()]).pack(side="left", padx=20, pady=10)
        ttk.Button(popup, text="Stop", command=lambda: [popup.destroy(), self.stop_alarm()]).pack(side="right", padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import time
import threading
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("⏰ Stylish Python Alarm Clock")
        self.root.geometry("480x620")
        self.root.configure(bg="#f4f7fc")

        self.alarm_time = None
        self.alarm_thread = None
        self.alarm_active = False
        self.snooze_minutes = 5
        self.alarm_tone = None

        # Title Label
        tk.Label(root, text="Alarm Clock", font=("Poppins", 22, "bold"), fg="#333", bg="#f4f7fc").pack(pady=15)

        # Clock Display with Circular Frame
        self.clock_canvas = tk.Canvas(root, width=250, height=250, bg="#f4f7fc", highlightthickness=0)
        self.clock_canvas.pack()
        self.clock_canvas.create_oval(25, 25, 225, 225, outline="#6c63ff", width=5, fill="#dcdcff")
        self.time_text = self.clock_canvas.create_text(125, 125, text="", font=("Helvetica", 28, "bold"), fill="#333")
        self.update_clock_time()

        # Alarm Time Inputs
        time_frame = tk.Frame(root, bg="#f4f7fc")
        time_frame.pack(pady=15)

        self.hour_var = tk.StringVar(value="00")
        self.min_var = tk.StringVar(value="00")

        tk.Label(time_frame, text="Hour", font=("Helvetica", 12), bg="#f4f7fc").grid(row=0, column=0, padx=8)
        tk.Entry(time_frame, textvariable=self.hour_var, width=5, font=("Helvetica", 12)).grid(row=0, column=1, padx=5)

        tk.Label(time_frame, text="Minute", font=("Helvetica", 12), bg="#f4f7fc").grid(row=0, column=2, padx=8)
        tk.Entry(time_frame, textvariable=self.min_var, width=5, font=("Helvetica", 12)).grid(row=0, column=3, padx=5)

        # Alarm Tone Dropdown
        tk.Label(root, text="🎵 Select Alarm Tone", font=("Helvetica", 12, "bold"), bg="#f4f7fc").pack(pady=(10, 5))
        self.tones = ["tone1.mp3", "tone2.mp3", "tone3.mp3", "tone4.mp3", "tone5.mp3"]
        self.tone_var = tk.StringVar()
        self.tone_dropdown = ttk.Combobox(root, values=self.tones, textvariable=self.tone_var, state="readonly", font=("Helvetica", 11))
        self.tone_dropdown.set("tone1.mp3")
        self.tone_dropdown.pack()

        # Snooze Spinner
        tk.Label(root, text="😴 Snooze Duration (minutes)", font=("Helvetica", 12, "bold"), bg="#f4f7fc").pack(pady=(15, 5))
        self.snooze_spin = ttk.Spinbox(root, from_=1, to=30, width=5, font=("Helvetica", 11))
        self.snooze_spin.set(self.snooze_minutes)
        self.snooze_spin.pack()

        # Buttons
        btn_frame = tk.Frame(root, bg="#f4f7fc")
        btn_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 11, "bold"), padding=6)
        style.map("TButton", foreground=[('active', '#fff')], background=[('active', '#6c63ff')])

        ttk.Button(btn_frame, text="✅ Set Alarm", command=self.set_alarm).grid(row=0, column=0, padx=15)
        ttk.Button(btn_frame, text="⛔ Stop Alarm", command=self.stop_alarm).grid(row=0, column=1, padx=15)

    def update_clock_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_canvas.itemconfig(self.time_text, text=now)
        self.root.after(1000, self.update_clock_time)

    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.min_var.get())
            now = datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if alarm_time < now:
                alarm_time += timedelta(days=1)

            self.alarm_time = alarm_time
            self.snooze_minutes = int(self.snooze_spin.get())

            selected_tone = self.tone_var.get()
            tone_path = os.path.join("alarm_tones", selected_tone)

            if not os.path.exists(tone_path):
                messagebox.showerror("Tone Missing", f"{selected_tone} not found in alarm_tones folder.")
                return

            self.alarm_tone = tone_path
            self.alarm_active = True

            self.alarm_thread = threading.Thread(target=self.check_alarm)
            self.alarm_thread.daemon = True
            self.alarm_thread.start()

            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time.strftime('%H:%M')}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for hour and minute.")

    def check_alarm(self):
        while self.alarm_active:
            if datetime.now() >= self.alarm_time:
                self.play_alarm()
                self.show_snooze_popup()
                break
            time.sleep(1)

    def play_alarm(self):
        pygame.mixer.music.load(self.alarm_tone)
        pygame.mixer.music.play(-1)

    def stop_alarm(self):
        self.alarm_active = False
        pygame.mixer.music.stop()

    def snooze(self):
        pygame.mixer.music.stop()
        self.alarm_time = datetime.now() + timedelta(minutes=self.snooze_minutes)
        self.alarm_thread = threading.Thread(target=self.check_alarm)
        self.alarm_thread.daemon = True
        self.alarm_thread.start()

    def show_snooze_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("⏰ Alarm")
        popup.geometry("260x130")
        popup.config(bg="#fff3cd")

        tk.Label(popup, text="🔔 Wake Up!", font=("Helvetica", 16, "bold"), bg="#fff3cd").pack(pady=10)
        ttk.Button(popup, text="Snooze", command=lambda: [popup.destroy(), self.snooze()]).pack(side="left", padx=20, pady=10)
        ttk.Button(popup, text="Stop", command=lambda: [popup.destroy(), self.stop_alarm()]).pack(side="right", padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
