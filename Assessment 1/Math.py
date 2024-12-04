import tkinter as tk
from PIL import Image, ImageTk  # For handling the PNG background image
import random

# Global variables
root = tk.Tk()
canvas = None
background_image = None
score = 0
attempt = 0
current_question = 1
difficulty = None
num1 = 0
num2 = 0
operation = ""
answer = 0
feedback_label = None
user_input = None

def initialize_app():
    """Initialize the application window and variables."""
    global canvas, background_image
    root.title("Math Quiz!")
    root.geometry("400x300")  # Set window size
    root.resizable(False, False)  # Disable resizing

    # Load the background image
    background_image = ImageTk.PhotoImage(Image.open("Assessment 1\Math_bg.png"))
    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    create_menu()

def create_menu():
    """Display the difficulty menu.""" 
    clear_window()

    label = tk.Label(root, text="Math Quiz!", font=("Arial", 16), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 50, window=label)

    label = tk.Label(root, text="Please select a difficulty!", font=("Arial", 14), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 100, window=label)

    # Easy button
    easy_button = tk.Button(root, text="Easy", bg="green", fg="white", font=("Arial", 18), width=12, command=lambda: start_quiz(1))
    canvas.create_window(200, 140, window=easy_button)

    # Normal button
    normal_button = tk.Button(root, text="Normal", bg="orange", fg="black", font=("Arial", 18), width=12, command=lambda: start_quiz(2))
    canvas.create_window(200, 180, window=normal_button)

    # Advanced button
    advanced_button = tk.Button(root, text="Advanced", bg="red", fg="black", font=("Arial", 18), width=12, command=lambda: start_quiz(4))
    canvas.create_window(200, 220, window=advanced_button)


def start_quiz(selected_difficulty):
    """Initialize quiz based on difficulty."""
    global score, current_question, difficulty
    score = 0
    current_question = 0
    difficulty = selected_difficulty
    next_question()

def random_int():
    """Generate random integers based on difficulty."""
    if difficulty == 1:
        return random.randint(1, 9)
    elif difficulty == 2:
        return random.randint(10, 99)
    elif difficulty == 4:
        return random.randint(1000, 9999)

def decide_operation():
    """Randomly decide addition or subtraction."""
    return random.choice(["+", "-"])

def display_problem():
    """Display the problem and collect user input."""
    global num1, num2, operation, answer, feedback_label, user_input
    clear_window()

    # Question label
    question_label = tk.Label(root, text=f"Question {current_question}/10", font=("Arial", 14), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 50, window=question_label)

    num1 = random_int()
    num2 = random_int()
    operation = decide_operation()

    if operation == "+":
        answer = num1 + num2
    else:
        answer = num1 - num2

    problem_label = tk.Label(root, text=f"{num1} {operation} {num2} =", font=("Arial", 14), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 100, window=problem_label)

    # Input field
    user_input = tk.Entry(root, font=("Arial", 14))
    canvas.create_window(200, 140, window=user_input)

    # Feedback label
    feedback_label = tk.Label(root, text="", font=("Arial", 12), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 180, window=feedback_label)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=check_answer)
    canvas.create_window(200, 220, window=submit_button)

def check_answer():
    """Check the user's answer and award points."""
    global score, attempt, current_question, feedback_label
    try:
        user_answer = int(user_input.get())
    except ValueError:
        feedback_label.config(text="Please enter a valid number!")
        return

    if user_answer == answer:
        if attempt == 0:
            score += 10
        elif attempt == 1:
            score += 5
        attempt = 0
        feedback_label.config(text="Correct!", fg="green")
        if current_question >= 10:
            root.after(1000, display_results)
        else:
            root.after(1000, next_question)
    else:
        if attempt == 0:
            attempt += 1
            feedback_label.config(text="Wrong answer! Try again.", fg="red")
        else:
            attempt = 0
            feedback_label.config(text=f"Wrong again! The correct answer was {answer}.", fg="red")
            if current_question >= 10:
                root.after(1000, display_results)
            else:
                root.after(1000, next_question)

def next_question():
    """Proceed to the next question."""
    global current_question
    current_question += 1
    display_problem()

def display_results():
    """Display the final results."""
    clear_window()

    grade = ""
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "F"

    result_label = tk.Label(root, text=f"Quiz Completed!", font=("Arial", 16), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 50, window=result_label)

    score_label = tk.Label(root, text=f"Your Score: {score}/100", font=("Arial", 14), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 100, window=score_label)

    grade_label = tk.Label(root, text=f"Grade: {grade}", font=("Arial", 14), bg="#000000", fg="#FFFFFF")
    canvas.create_window(200, 150, window=grade_label)

    play_again_button = tk.Button(root, text="Play Again", command=create_menu)
    canvas.create_window(200, 200, window=play_again_button)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    canvas.create_window(200, 250, window=exit_button)

def clear_window():
    """Clear all widgets from the canvas."""
    canvas.delete("all")
    canvas.create_image(0, 0, image=background_image, anchor="nw")

# Main application loop
initialize_app()
root.mainloop()