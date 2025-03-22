# Folder structure:
# quiz_app/
# ├── quiz_gui.py
# ├── assets/
# │   ├── images/
# │   │   └── mars.png (etc.)
# │   └── sounds/
# │       ├── correct.mp3
# │       ├── wrong.mp3
# │       └── timer_end.mp3
# └── leaderboard.txt

import tkinter as tk
from tkinter import messagebox
import PIL
import playsound3
from PIL import Image, ImageTk
from playsound3 import playsound
import random
import os

TIME_LIMIT = 15
LEADERBOARD_FILE = "leaderboard.txt"

# Example categorized question set with difficulty
questions = {
    "science": {
        "easy": [
            {"type": "multiple", "question": "What planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "answer": "Mars", "image": "mars.png"},
            {"type": "truefalse", "question": "Water freezes at 0°C.", "answer": "True"},
        ],
        "medium": [
            {"type": "open", "question": "Symbol for Gold?", "answer": "Au"},
        ],
        "hard": [
            {"type": "open", "question": "What does DNA stand for?", "answer": "Deoxyribonucleic acid"},
        ]
    },
    "history": {
        "easy": [
            {"type": "truefalse", "question": "The Great Wall is in China.", "answer": "True"},
        ],
        "medium": [
            {"type": "multiple", "question": "Who discovered America?", "options": ["Columbus", "Vespucci", "Cook", "Magellan"], "answer": "Columbus"},
        ],
        "hard": [
            {"type": "open", "question": "Year WW2 ended?", "answer": "1945"},
        ]
    }
}

points = {"easy": 10, "medium": 20, "hard": 30}
themes = {
    "light": {"bg": "#ffffff", "fg": "#000000"},
    "dark": {"bg": "#222222", "fg": "#f5f5f5"}
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x500")
        self.score = 0
        self.correct = 0
        self.q_index = 0
        self.timer = TIME_LIMIT
        self.timer_id = None
        self.theme_choice = "light"

        self.setup_start_screen()

    def setup_start_screen(self):
        self.clear_screen()

        self.player_name = tk.StringVar()
        self.difficulty = tk.StringVar(value="easy")
        self.category = tk.StringVar(value="science")
        self.theme = tk.StringVar(value="light")

        tk.Label(self.root, text="Name:").pack()
        tk.Entry(self.root, textvariable=self.player_name).pack(pady=5)

        tk.Label(self.root, text="Select Category:").pack()
        for cat in questions.keys():
            tk.Radiobutton(self.root, text=cat.title(), variable=self.category, value=cat).pack()

        tk.Label(self.root, text="Select Difficulty:").pack()
        for level in ["easy", "medium", "hard"]:
            tk.Radiobutton(self.root, text=level.title(), variable=self.difficulty, value=level).pack()

        tk.Label(self.root, text="Theme:").pack()
        for t in ["light", "dark"]:
            tk.Radiobutton(self.root, text=t.title(), variable=self.theme, value=t).pack()

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=10)

    def apply_theme(self):
        theme = themes[self.theme_choice]
        self.root.configure(bg=theme["bg"])
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            except:
                pass

    def play_sound(self, name):
        try:
            playsound(os.path.join("assets/sounds", f"{name}.mp3"), block=False)
        except:
            pass

    def start_quiz(self):
        name = self.player_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter your name.")
            return

        self.name = name
        self.theme_choice = self.theme.get()
        self.apply_theme()

        self.q_list = questions[self.category.get()][self.difficulty.get()]
        random.shuffle(self.q_list)
        self.score = 0
        self.correct = 0
        self.q_index = 0
        self.next_question()

    def next_question(self):
        if self.q_index >= len(self.q_list):
            return self.show_summary()
        self.timer = TIME_LIMIT
        self.render_question(self.q_list[self.q_index])
        self.update_timer()

    def render_question(self, q):
        self.clear_screen()
        tk.Label(self.root, text=f"Time: {self.timer}s", name="timer", font=("Arial", 12), fg="red").pack(anchor="ne", padx=10, pady=5)
        tk.Label(self.root, text=f"Score: {self.score}").pack(anchor="nw", padx=10)

        if "image" in q:
            img_path = os.path.join("assets/images", q["image"])
            img = Image.open(img_path)
            img = img.resize((200, 150))
            img = ImageTk.PhotoImage(img)
            lbl = tk.Label(self.root, image=img)
            lbl.image = img
            lbl.pack(pady=5)

        tk.Label(self.root, text=f"Q{self.q_index+1}: {q['question']}", font=("Arial", 14)).pack(pady=10)

        self.answer = tk.StringVar()
        if q["type"] == "multiple" or q["type"] == "truefalse":
            opts = q.get("options", ["True", "False"])
            for opt in opts:
                tk.Radiobutton(self.root, text=opt, variable=self.answer, value=opt).pack(anchor="w", padx=30)
        elif q["type"] == "open":
            tk.Entry(self.root, textvariable=self.answer).pack(pady=5)

        tk.Button(self.root, text="Submit", command=self.submit_answer).pack(pady=10)

    def update_timer(self):
        self.timer -= 1
        if self.timer >= 0:
            try:
                timer_label = self.root.nametowidget("timer")
                timer_label.config(text=f"Time: {self.timer}s")
            except:
                pass
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.play_sound("timer_end")
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self.q_index += 1
            self.next_question()

    def submit_answer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        user = self.answer.get().strip().lower()
        correct = self.q_list[self.q_index]['answer'].lower()

        if user == correct:
            self.score += points[self.difficulty.get()]
            self.correct += 1
            self.play_sound("correct")
            messagebox.showinfo("Correct", "Good job!")
        else:
            self.play_sound("wrong")
            messagebox.showinfo("Incorrect", f"Answer: {self.q_list[self.q_index]['answer']}")

        self.q_index += 1
        self.next_question()

    def show_summary(self):
        self.save_score()
        self.clear_screen()
