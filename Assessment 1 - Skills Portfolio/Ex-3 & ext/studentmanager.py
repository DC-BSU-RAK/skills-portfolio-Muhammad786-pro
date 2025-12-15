import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

FILE_NAME = r"Assessment 1 - Skills Portfolio\Ex-3 & ext\studentMarks.txt"

# ------------------- DATA HANDLING ------------------- #

def calculate_grade(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"


def load_students():
    students = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            total = int(f.readline().strip())
            for line in f:
                sid, name, c1, c2, c3, exam = line.strip().split(",")
                c1, c2, c3, exam = map(int, (c1, c2, c3, exam))
                coursework = c1 + c2 + c3
                overall = coursework + exam
                percent = (overall / 160) * 100
                grade = calculate_grade(percent)

                students.append({
                    "id": sid,
                    "name": name,
                    "c1": c1, "c2": c2, "c3": c3,
                    "exam": exam,
                    "coursework": coursework,
                    "overall": overall,
                    "percent": percent,
                    "grade": grade
                })
        return students
    except:
        messagebox.showerror("Error", "studentMarks.txt missing or invalid")
        return []


def save_students():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            f.write(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")


# ------------------- DISPLAY ------------------- #

def display_all(data):
    output.delete("1.0", tk.END)
    for s in data:
        output.insert(tk.END,
            f"Name: {s['name']}\n"
            f"ID: {s['id']}\n"
            f"Coursework: {s['coursework']} / 60\n"
            f"Exam: {s['exam']} / 100\n"
            f"Percentage: {s['percent']:.2f}%\n"
            f"Grade: {s['grade']}\n"
            f"{'-'*40}\n"
        )


# ------------------- MENU FUNCTIONS ------------------- #

def view_all():
    display_all(students)


def show_highest():
    display_all([max(students, key=lambda x: x["overall"])])


def show_lowest():
    display_all([min(students, key=lambda x: x["overall"])])


def sort_students():
    choice = simpledialog.askstring("Sort", "Enter A for Ascending or D for Descending")
    if not choice: return
    reverse = True if choice.lower() == "d" else False
    sorted_list = sorted(students, key=lambda x: x["percent"], reverse=reverse)
    display_all(sorted_list)


def add_student():
    sid = simpledialog.askstring("Add", "Student ID:")
    name = simpledialog.askstring("Add", "Name:")
    c1 = simpledialog.askinteger("Add", "Coursework 1:")
    c2 = simpledialog.askinteger("Add", "Coursework 2:")
    c3 = simpledialog.askinteger("Add", "Coursework 3:")
    exam = simpledialog.askinteger("Add", "Exam:")

    coursework = c1 + c2 + c3
    overall = coursework + exam
    percent = (overall / 160) * 100

    students.append({
        "id": sid, "name": name,
        "c1": c1, "c2": c2, "c3": c3,
        "exam": exam,
        "coursework": coursework,
        "overall": overall,
        "percent": percent,
        "grade": calculate_grade(percent)
    })

    save_students()
    view_all()


def delete_student():
    key = simpledialog.askstring("Delete", "Enter ID or Name:")
    for s in students:
        if s["id"] == key or s["name"].lower() == key.lower():
            students.remove(s)
            save_students()
            view_all()
            return
    messagebox.showinfo("Not Found", "Student not found")


def update_student():
    key = simpledialog.askstring("Update", "Enter ID or Name:")
    for s in students:
        if s["id"] == key or s["name"].lower() == key.lower():
            s["c1"] = simpledialog.askinteger("Update", "New Coursework 1:", initialvalue=s["c1"])
            s["c2"] = simpledialog.askinteger("Update", "New Coursework 2:", initialvalue=s["c2"])
            s["c3"] = simpledialog.askinteger("Update", "New Coursework 3:", initialvalue=s["c3"])
            s["exam"] = simpledialog.askinteger("Update", "New Exam:", initialvalue=s["exam"])

            s["coursework"] = s["c1"] + s["c2"] + s["c3"]
            s["overall"] = s["coursework"] + s["exam"]
            s["percent"] = (s["overall"] / 160) * 100
            s["grade"] = calculate_grade(s["percent"])

            save_students()
            view_all()
            return
    messagebox.showinfo("Not Found", "Student not found")


# ------------------- GUI ------------------- #

students = load_students()

root = tk.Tk()
root.title("Student Record Manager")
root.state("zoomed")

# Left Menu
menu = tk.Frame(root, bg="#2c2f33", width=300)
menu.pack(side="left", fill="y")

btn_style = {
    "font": ("Arial Black", 12),
    "bg": "#eb6d57",
    "fg": "#ffffff",
    "width": 28,
    "bd": 0,
    "pady": 8
}

tk.Label(menu, text="MENU", bg="#2c2f33", fg="white",
         font=("Arial Black", 18)).pack(pady=20)

tk.Button(menu, text="1. View All Students", command=view_all, **btn_style).pack(pady=4)
tk.Button(menu, text="2. Highest Score", command=show_highest, **btn_style).pack(pady=4)
tk.Button(menu, text="3. Lowest Score", command=show_lowest, **btn_style).pack(pady=4)
tk.Button(menu, text="4. Sort Records", command=sort_students, **btn_style).pack(pady=4)
tk.Button(menu, text="5. Add Student", command=add_student, **btn_style).pack(pady=4)
tk.Button(menu, text="6. Delete Student", command=delete_student, **btn_style).pack(pady=4)
tk.Button(menu, text="7. Update Student", command=update_student, **btn_style).pack(pady=4)
tk.Button(menu, text="Exit", command=root.destroy, **btn_style).pack(pady=20)

# Output Area
output = scrolledtext.ScrolledText(root, font=("Consolas", 12))
output.pack(side="right", expand=True, fill="both")

root.mainloop()
