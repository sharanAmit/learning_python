import random
import time
import threading

# File to store leaderboard
LEADERBOARD_FILE = "/Users/amitsharan/learning_pyhton/quiz_game/leaderboard.txt"

# Define questions by category
questions = {
    "easy": [
        {
            "type": "multiple",
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Madrid"],
            "answer": "Paris"
        },
        {
            "type": "truefalse",
            "question": "The sky is blue.",
            "answer": "True"
        }
    ],
    "medium": [
        {
            "type": "open",
            "question": "Name the chemical element with the symbol 'O'.",
            "answer": "Oxygen"
        },
        {
            "type": "truefalse",
            "question": "Python is a statically typed language.",
            "answer": "False"
        }
    ],
    "hard": [
        {
            "type": "multiple",
            "question": "Which algorithm has O(n log n) average time complexity?",
            "options": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"],
            "answer": "Merge Sort"
        },
        {
            "type": "open",
            "question": "What does DNS stand for in computer networking?",
            "answer": "Domain Name System"
        }
    ]
}

# Points per difficulty
difficulty_points = {
    "easy": 10,
    "medium": 20,
    "hard": 30
}

# Timeout for each question
TIME_LIMIT = 15

# Global variable to handle timing
timeout_flag = False

def timeout_input(prompt, timeout=TIME_LIMIT):
    global timeout_flag
    user_input = [None]

    def ask():
        user_input[0] = input(prompt)

    thread = threading.Thread(target=ask)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        timeout_flag = True
        print(f"\n⏰ Time's up! ({timeout} seconds)")
        return None
    return user_input[0]

def ask_question(q):
    global timeout_flag
    timeout_flag = False
    print(f"\nQ: {q['question']}")

    if q["type"] == "multiple":
        for i, option in enumerate(q["options"], start=1):
            print(f"{i}. {option}")
        answer = timeout_input("Your choice (1-4): ")
        if timeout_flag or not answer:
            return False
        try:
            return q["options"][int(answer) - 1] == q["answer"]
        except:
            return False

    elif q["type"] == "truefalse":
        answer = timeout_input("True or False? ")
        if timeout_flag or not answer:
            return False
        return answer.strip().capitalize() == q["answer"]

    elif q["type"] == "open":
        answer = timeout_input("Your answer: ")
        if timeout_flag or not answer:
            return False
        return answer.strip().lower() == q["answer"].lower()

def save_score(name, score, difficulty):
    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"{name},{score},{difficulty}\n")

def display_leaderboard():
    print("\n🏆 Leaderboard:")
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            lines = file.readlines()
            scores = [line.strip().split(',') for line in lines]
            scores.sort(key=lambda x: int(x[1]), reverse=True)
            for i, (name, score, difficulty) in enumerate(scores[:10], start=1):
                print(f"{i}. {name} - {score} pts ({difficulty})")
    except FileNotFoundError:
        print("No leaderboard data yet.")

def choose_difficulty():
    while True:
        print("\nChoose Difficulty Level:")
        print("1. Easy\n2. Medium\n3. Hard")
        choice = input("Enter choice (1-3): ")
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        else:
            print("Invalid choice. Try again.")

def play_game():
    print("\n🎮 Welcome to the Ultimate Quiz Challenge!")
    player_name = input("Enter your name: ").strip().title()
    difficulty = choose_difficulty()

    print(f"\nHi {player_name}! Let's begin the {difficulty.capitalize()} Quiz! ⌛ You have {TIME_LIMIT} seconds per question.")
    selected_questions = random.sample(questions[difficulty], len(questions[difficulty]))
    score = 0
    correct_answers = 0

    for q in selected_questions:
        result = ask_question(q)
        if result:
            print("✅ Correct!")
            score += difficulty_points[difficulty]
            correct_answers += 1
        else:
            print(f"❌ Wrong or Timed Out! The correct answer was: {q['answer']}")

    print("\n🎉 Quiz Completed!")
    print(f"{player_name}, your score: {score}")
    print(f"Correct answers: {correct_answers} / {len(selected_questions)}")
    print(f"Accuracy: {correct_answers / len(selected_questions) * 100:.2f}%")

    save_score(player_name, score, difficulty)
    display_leaderboard()

def main():
    while True:
        play_game()
        again = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if again != "yes":
            print("👋 Thanks for playing! See you next time!")
            break

if __name__ == "__main__":
    main()
