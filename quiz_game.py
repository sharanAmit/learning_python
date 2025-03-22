import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

# Data
questions = {
    "easy": [
        {"type": "multiple", "question": "Capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
        {"type": "truefalse", "question": "The sky is blue.", "answer": "True"},
    ],
    "medium": [
        {"type": "open", "question": "Element with symbol 'O'?", "answer": "Oxygen"},
        {"type": "truefalse", "question": "Python is statically typed.", "answer": "False"},
    ],
    "hard": [
        {"type": "multiple", "question": "Which has O(n log n) average time?", "options": ["Bubble", "Insertion", "Merge", "Selection"], "answer": "Merge"},
        {"type": "open", "question": "DNS stands for?", "answer": "Domain Name System"},
    ]
}

difficulty_points = {"easy": 10, "medium": 20, "hard": 30}
LEADERBOARD_FILE = "leaderboard.txt"
TIME_LIMIT = 15

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Quiz Game")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.player_name = ""
        self.difficulty = "easy"
        self.score = 0
        self.correct = 0
        self.q_index = 0
        self.questions = []
        self.timer = TIME_LIMIT
        self.timer_id = None

        self.setup_start_screen()

    def name_exists(self, name):
        try:
            with open(LEADERBOARD_FILE, "r") as file:
                for line in file:
                    if line.split(",")[0].strip().lower() == name.lower():
                        return True
        except FileNotFoundError:
            pass
        return False

    def setup_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.unbind("<Return>")

        tk.Label(self.root, text="Welcome to the Quiz Game!", font=("Arial", 18)).pack(pady=20)

        tk.Label(self.root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Select difficulty:").pack(pady=10)
        self.diff_var = tk.StringVar(value="easy")
        for level in ["easy", "medium", "hard"]:
            tk.Radiobutton(self.root, text=level.title(), variable=self.diff_var, value=level).pack()

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=20)

    def start_quiz(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        if self.name_exists(name):
            messagebox.showerror("Name Taken", f"The name '{name}' already exists.\nPlease choose a different name.")
            return
        self.player_name = name
        self.difficulty = self.diff_var.get()
        self.score = 0
        self.correct = 0
        self.q_index = 0
        self.questions = random.sample(questions[self.difficulty], len(questions[self.difficulty]))
        self.next_question()

    def next_question(self):
        if self.q_index >= len(self.questions):
            self.show_summary()
            return

        self.timer = TIME_LIMIT
        self.render_question(self.questions[self.q_index])
        self.start_timer()

    def render_question(self, q):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.bind("<Return>", lambda e: self.submit_answer())

        tk.Label(self.root, text=f"Time left: {self.timer} sec", font=("Arial", 12), fg="red", name="timer").pack(anchor="ne", padx=10, pady=5)
        tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 12)).pack(anchor="nw", padx=10)

        tk.Label(self.root, text=f"\nQ{self.q_index + 1}: {q['question']}", font=("Arial", 14)).pack(pady=10)

        self.answer_var = tk.StringVar()

        if q["type"] == "multiple":
            options = q["options"][:]
            random.shuffle(options)
            for opt in options:
                tk.Radiobutton(self.root, text=opt, variable=self.answer_var, value=opt).pack(anchor="w", padx=30)
        elif q["type"] == "truefalse":
            for opt in ["True", "False"]:
                tk.Radiobutton(self.root, text=opt, variable=self.answer_var, value=opt).pack(anchor="w", padx=30)
        elif q["type"] == "open":
            tk.Entry(self.root, textvariable=self.answer_var).pack(pady=10)

        tk.Button(self.root, text="Submit", command=self.submit_answer).pack(pady=20)

    def update_timer(self):
        self.timer -= 1
        if self.timer >= 0:
            try:
                timer_label = self.root.nametowidget("timer")
                timer_label.config(text=f"Time left: {self.timer} sec")
            except:
                return
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            messagebox.showinfo("Time's up!", "You ran out of time!")
            self.q_index += 1
            self.next_question()

    def start_timer(self):
        self.update_timer()

    def submit_answer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        user_ans = self.answer_var.get().strip()
        if not user_ans:
            messagebox.showerror("Error", "Please enter an answer before submitting.")
            self.start_timer()
            return

        correct_ans = self.questions[self.q_index]['answer'].strip().lower()
        if user_ans.lower() == correct_ans:
            self.correct += 1
            self.score += difficulty_points[self.difficulty]
            messagebox.showinfo("Correct", "✅ Good job!")
        else:
            messagebox.showinfo("Incorrect", f"❌ Correct Answer: {self.questions[self.q_index]['answer']}")

        self.q_index += 1
        self.next_question()

    def show_summary(self):
        self.root.unbind("<Return>")
        self.save_to_leaderboard()
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🎉 Quiz Completed!", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text=f"{self.player_name}, your score: {self.score}").pack()
        tk.Label(self.root, text=f"Correct: {self.correct} / {len(self.questions)}").pack()
        tk.Label(self.root, text=f"Accuracy: {(self.correct / len(self.questions)) * 100:.2f}%").pack(pady=10)

        tk.Button(self.root, text="Play Again", command=self.setup_start_screen).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

        self.display_leaderboard()

    def save_to_leaderboard(self):
        with open(LEADERBOARD_FILE, "a") as file:
            file.write(f"{self.player_name},{self.score},{self.difficulty}\n")

    def display_leaderboard(self):
        try:
            with open(LEADERBOARD_FILE, "r") as file:
                entries = [line.strip().split(",") for line in file.readlines()]
                entries.sort(key=lambda x: int(x[1]), reverse=True)
                top = entries[:5]

            tk.Label(self.root, text="\n🏆 Leaderboard:", font=("Arial", 14)).pack()
            for i, (name, score, diff) in enumerate(top, 1):
                color = "gold" if i == 1 else "black"
                tk.Label(self.root, text=f"{i}. {name} - {score} pts ({diff})", fg=color).pack()
        except FileNotFoundError:
            tk.Label(self.root, text="No leaderboard data yet.").pack()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
