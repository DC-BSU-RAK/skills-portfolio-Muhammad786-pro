import tkinter as tk
from PIL import Image, ImageTk
import random

# -------------------------------------------------------
# DYNAMIC IMAGE LOADER (Resizes perfectly to window size)
# -------------------------------------------------------
def load_bg(path):
    img = Image.open(path)
    img = img.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def update_background(label, path):
    """Reloads & resizes background image when window size changes"""
    new_img = load_bg(path)
    label.config(image=new_img)
    label.image = new_img

# -------------------------------------------------------
# MAIN FUNCTIONS
# -------------------------------------------------------
def show_homepage():
    clear_window()
    global homepage_label
    homepage_img = load_bg(r"Assessment 1 - Skills Portfolio\Ex-1\1.png")
    homepage_label = tk.Label(root, image=homepage_img)
    homepage_label.image = homepage_img
    homepage_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Homepage buttons
    tk.Button(root, text="START GAME", command=displayMenu, **start_style).place(relx=0.5, rely=0.70, anchor="center")
    tk.Button(root, text="INSTRUCTIONS", command=show_instructions, **start_style).place(relx=0.5, rely=0.80, anchor="center")
    tk.Button(root, text="QUIT", command=root.destroy, **start_style).place(relx=0.5, rely=0.90, anchor="center")

def show_instructions():
    clear_window()
    global instr_label
    instr_img = load_bg(r"Assessment 1 - Skills Portfolio\Ex-1\3.png")
    instr_label = tk.Label(root, image=instr_img)
    instr_label.image = instr_img
    instr_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    tk.Button(root, text="BACK", command=show_homepage, **back_style).place(relx=0.5, rely=0.90, anchor="center")

def displayMenu():
    clear_window() 
    global menu_label
    bg = load_bg(r"Assessment 1 - Skills Portfolio\Ex-1\4.png")
    menu_label = tk.Label(root, image=bg)
    menu_label.image = bg
    menu_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Bigger difficulty Buttons
    tk.Button(root, text="Easy", command=lambda: start_quiz(1), **difficulty_style).place(relx=0.5, rely=0.40, anchor="center")
    tk.Button(root, text="Moderate", command=lambda: start_quiz(2), **difficulty_style).place(relx=0.5, rely=0.52, anchor="center")
    tk.Button(root, text="Advanced", command=lambda: start_quiz(4), **difficulty_style).place(relx=0.5, rely=0.64, anchor="center")
    
    # Smaller Back button
    tk.Button(root, text="BACK", command=show_homepage, **back_style).place(relx=0.5, rely=0.80, anchor="center")

def randomInt(diff):
    if diff == 1:
        return random.randint(1, 9)
    if diff == 2:
        return random.randint(10, 99)
    return random.randint(1000, 9999)

def decideOperation():
    return random.choice(["+", "-"])

def start_quiz(level):
    global difficulty, score, question_number, feedback_label, attempt
    difficulty = level
    score = 0
    question_number = 1
    attempt = 1
    feedback_label = None
    next_question()

def displayProblem(n1, n2, op):
    clear_window()
    global problem_label
    bg = load_bg(r"Assessment 1 - Skills Portfolio\Ex-1\2.png")  # Use difficulty page bg for consistency
    problem_label = tk.Label(root, image=bg)
    problem_label.image = bg
    problem_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Score & Question on top
    tk.Label(root, text=f"Score: {score}", font=("Arial Black", 20), fg="#484a8b", bg="#eb6d57").place(relx=0.1, rely=0.05, anchor="w")
    tk.Label(root, text=f"Question: {question_number}/10", font=("Arial Black", 20), fg="#484a8b", bg="#eb6d57").place(relx=0.9, rely=0.05, anchor="e")

    # Question displayed like difficulty buttons
    tk.Label(root, text=f"{n1} {op} {n2} =", font=("Arial Black", 36, "bold"),
             fg="#000000", bg="#eb6d57", width=15, height=2, bd=4, relief="ridge").place(relx=0.5, rely=0.45, anchor="center")

    # Answer entry
    answer = tk.Entry(root, font=("Arial Black", 28), width=6,
                      justify="center", bg="#eb6d57", fg="#000000", insertbackground="black")
    answer.place(relx=0.5, rely=0.58, anchor="center")

    global feedback_label
    feedback_label = tk.Label(root, text="", font=("Arial Black", 20, "bold"), fg="#FFD700", bg="#484a8b")
    feedback_label.place(relx=0.5, rely=0.65, anchor="center")

    tk.Button(root, text="Submit", font=("Arial Black", 18, "bold"),
              bg="#eb6d57", fg="#000000", width=15,
              command=lambda: check_answer(n1, n2, op, answer.get())).place(relx=0.5, rely=0.75, anchor="center")

def isCorrect(user, correct):
    try:
        return int(user) == correct
    except:
        return False

def check_answer(n1, n2, op, user_ans):
    global score, question_number, attempt
    correct = n1 + n2 if op == "+" else n1 - n2
    if isCorrect(user_ans, correct):
        score += 10 if attempt == 1 else 5
        feedback_label.config(text="✅ Well done!", fg="#00FF7F")
        question_number += 1
        attempt = 1
        root.after(700, lambda: displayResults() if question_number > 10 else next_question())
    else:
        if attempt == 1:
            attempt = 2
            feedback_label.config(text="⚠️ Try again!", fg="#FFD700")
        else:
            feedback_label.config(text=f"❌ Wrong! Answer = {correct}", fg="#FF4500")
            question_number += 1
            attempt = 1
            root.after(1000, lambda: displayResults() if question_number > 10 else next_question())

def next_question():
    displayProblem(randomInt(difficulty), randomInt(difficulty), decideOperation())

def grade(score):
    return ("A+" if score >= 90 else
            "A" if score >= 80 else
            "B" if score >= 70 else
            "C" if score >= 60 else
            "D" if score >= 50 else "F")

def displayResults():
    clear_window()
    global result_label
    bg = load_bg(r"Assessment 1 - Skills Portfolio\Ex-1\2.png")  # Use difficulty page bg
    result_label = tk.Label(root, image=bg)
    result_label.image = bg
    result_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(root, text="🏆 Quiz Completed! 🏆", font=("Orbitron", 36, "bold"),
             fg="#f9e6c5", bg="#484a8b").pack(pady=50)

    tk.Label(root, text=f"Score: {score}/100\nGrade: {grade(score)}",
             font=("Arial Black", 28), fg="#f9e6c5", bg="#484a8b").pack(pady=30)

    tk.Button(root, text="Play Again", font=("Arial Black", 20, "bold"),
              bg="#eb6d57", fg="#f9e6c5", width=20,
              command=show_homepage).pack(pady=15)

    tk.Button(root, text="Quit", font=("Arial Black", 20, "bold"),
              bg="#eb6d57", fg="#f9e6c5", width=20,
              command=root.destroy).pack(pady=15)

def clear_window():
    for w in root.winfo_children():
        w.destroy()

# -------------------------------------------------------
# WINDOW SETUP
# -------------------------------------------------------
root = tk.Tk()
root.title("Maths Quest – Arcade Game")
root.state("zoomed")
root.update()

# -------------------------------------------------------
# STYLES
# -------------------------------------------------------
button_style = {
    "font": ("Arial Black", 18, "bold"),
    "bg": "#eb6d57",
    "fg": "#f9e6c5",
    "width": 22
}

start_style = {
    "font": ("Arial Black", 26, "bold"),
    "bg": "#eb6d57",
    "fg": "#f9e6c5",
    "width": 20
}

difficulty_style = {
    "font": ("Arial Black", 24, "bold"),
   "bg": "#eb6d57",
    "fg": "#f9e6c5",
    "width": 20,
    "height": 1
}

back_style = {
    "font": ("Arial Black", 18, "bold"),
    "bg": "#eb6d57",
    "fg": "#f9e6c5",
    "width": 15,
    "height": 1
}

difficulty = score = question_number = attempt = 0

# -------------------------------------------------------
# START APP
# -------------------------------------------------------
show_homepage()
root.mainloop()
