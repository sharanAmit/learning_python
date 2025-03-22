import random

# Define questions
questions = [
    {
        "type": "multiple",
        "difficulty": "easy",
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    {
        "type": "truefalse",
        "difficulty": "easy",
        "question": "The Earth is flat.",
        "answer": "False"
    },
    {
        "type": "open",
        "difficulty": "medium",
        "question": "Name the chemical element with the symbol 'O'.",
        "answer": "Oxygen"
    },
    {
        "type": "multiple",
        "difficulty": "hard",
        "question": "Which algorithm has O(n log n) average time complexity?",
        "options": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"],
        "answer": "Merge Sort"
    },
    {
        "type": "truefalse",
        "difficulty": "medium",
        "question": "Python is a statically typed language.",
        "answer": "False"
    }
]

# Points based on difficulty
difficulty_points = {
    "easy": 10,
    "medium": 20,
    "hard": 30
}


def ask_question(q):
    print(f"\nDifficulty: {q['difficulty'].capitalize()}")
    print(f"Q: {q['question']}")

    if q["type"] == "multiple":
        for i, option in enumerate(q["options"], start=1):
            print(f"{i}. {option}")
        while True:
            try:
                choice = int(input("Your choice (1-4): "))
                if 1 <= choice <= 4:
                    return q["options"][choice - 1] == q["answer"]
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    elif q["type"] == "truefalse":
        answer = input("True or False? ").strip().capitalize()
        return answer == q["answer"]

    elif q["type"] == "open":
        answer = input("Your answer: ").strip().lower()
        return answer == q["answer"].lower()


def play_game():
    print("\n🎮 Welcome to the Ultimate Quiz Challenge!")
    player_name = input("Enter your name: ").strip().title()
    print(f"\nHi {player_name}! Let's get started!")

    round_questions = random.sample(questions, len(questions))
    score = 0
    correct_answers = 0

    for q in round_questions:
        if ask_question(q):
            print("✅ Correct!")
            score += difficulty_points[q["difficulty"]]
            correct_answers += 1
        else:
            print(f"❌ Wrong! The correct answer was: {q['answer']}")

    print("\n🎉 Quiz Completed!")
    print(f"{player_name}, your score: {score}")
    print(f"Correct answers: {correct_answers} / {len(round_questions)}")
    print(f"Accuracy: {correct_answers / len(round_questions) * 100:.2f}%")


def main():
    while True:
        play_game()
        again = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if again != "yes":
            print("👋 Thanks for playing! See you next time!")
            break


if __name__ == "__main__":
    main()
