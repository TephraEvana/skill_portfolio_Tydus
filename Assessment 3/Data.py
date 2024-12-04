import tkinter as tk
from tkinter import ttk, messagebox

# Data storage
students = []

def load_data():
    """Load student data from the file."""
    try:
        global students
        with open("Assessment 3\\studentMarks.txt", "r") as file:
            lines = file.readlines()
            num_students = int(lines[0].strip())

            for line in lines[1:]:
                parts = line.strip().split(",")
                student_code = int(parts[0])
                student_name = parts[1]
                coursework_marks = list(map(int, parts[2:5]))
                exam_mark = int(parts[5])
                students.append({
                    "code": student_code,
                    "name": student_name,
                    "coursework": coursework_marks,
                    "exam": exam_mark,
                    "total": sum(coursework_marks) + exam_mark
                })
    except Exception as e:
        messagebox.showerror("Error", f"Error loading file: {e}")

def clear_text_area():
    """Clear the text area."""
    text_area.delete(1.0, tk.END)

def view_all_records():
    """View all student records."""
    clear_text_area()
    total_percentage = 0
    output = ""

    for student in students:
        percentage = round((student["total"] / 160) * 100, 2)
        grade = get_grade(percentage)
        total_percentage += percentage
        output += (f"Name: {student['name']}\n"
                   f"Code: {student['code']}\n"
                   f"Total Coursework Mark: {sum(student['coursework'])}\n"
                   f"Exam Mark: {student['exam']}\n"
                   f"Overall Percentage: {percentage}%\n"
                   f"Grade: {grade}\n\n")

    avg_percentage = total_percentage / len(students)
    output += f"Total Students: {len(students)}\nAverage Percentage: {avg_percentage:.2f}%\n"
    text_area.insert(tk.END, output)

def view_individual_record():
    """View individual student record."""
    selected = record_combobox.get()
    if not selected:
        clear_text_area()
        text_area.insert(tk.END, "Please select a student from the dropdown menu to view their record.\n")
        return

    student_index = int(selected.split(".")[0]) - 1
    student = students[student_index]

    percentage = round((student["total"] / 160) * 100, 2)
    grade = get_grade(percentage)

    clear_text_area()
    text_area.insert(tk.END, (f"Name: {student['name']}\n"
                               f"Code: {student['code']}\n"
                               f"Total Coursework Mark: {sum(student['coursework'])}\n"
                               f"Exam Mark: {student['exam']}\n"
                               f"Overall Percentage: {percentage}%\n"
                               f"Grade: {grade}\n"))

def highest_score():
    """Show student with the highest score."""
    clear_text_area()
    highest = max(students, key=lambda x: x["total"])
    percentage = round((highest["total"] / 160) * 100, 2)
    grade = get_grade(percentage)

    text_area.insert(tk.END, (f"Name: {highest['name']}\n"
                               f"Code: {highest['code']}\n"
                               f"Total Coursework Mark: {sum(highest['coursework'])}\n"
                               f"Exam Mark: {highest['exam']}\n"
                               f"Overall Percentage: {percentage}%\n"
                               f"Grade: {grade}\n"))

def lowest_score():
    """Show student with the lowest score."""
    clear_text_area()
    lowest = min(students, key=lambda x: x["total"])
    percentage = round((lowest["total"] / 160) * 100, 2)
    grade = get_grade(percentage)

    text_area.insert(tk.END, (f"Name: {lowest['name']}\n"
                               f"Code: {lowest['code']}\n"
                               f"Total Coursework Mark: {sum(lowest['coursework'])}\n"
                               f"Exam Mark: {lowest['exam']}\n"
                               f"Overall Percentage: {percentage}%\n"
                               f"Grade: {grade}\n"))

def get_grade(percentage):
    """Determine the grade based on percentage."""
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

# Initialize GUI
root = tk.Tk()
root.title("Student Manager")
root.geometry("900x500")  # Set the initial size
root.configure(bg="black")

# Prevent window resizing
root.resizable(False, False)  # Disable resizing in both directions

# Load data
load_data()

# Header
header_label = tk.Label(root, text="Student Manager", font=("Arial", 25, "bold"), bg="black", fg="lightgreen")
header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Buttons and Dropdown Section
menu_frame = tk.Frame(root, bg="black")
menu_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

button_style = {"font": ("Arial", 12), "bg": "gray", "fg": "lightgreen", "activebackground": "darkgray", "width": 25}

view_all_button = tk.Button(menu_frame, text="View All Student Records", **button_style, command=view_all_records)
view_all_button.pack(pady=7)

highest_score_button = tk.Button(menu_frame, text="Show Highest Score", **button_style, command=highest_score)
highest_score_button.pack(pady=7)

lowest_score_button = tk.Button(menu_frame, text="Show Lowest Score", **button_style, command=lowest_score)
lowest_score_button.pack(pady=7)

individual_label = tk.Label(menu_frame, text="View Individual Student Record:", bg="black", fg="lightgreen")
individual_label.pack(pady=7)

student_names = [f"{i + 1}. {student['name']}" for i, student in enumerate(students)]
record_combobox = ttk.Combobox(menu_frame, values=student_names, width=30, state="readonly")
record_combobox.pack(pady=7)

view_record_button = tk.Button(menu_frame, text="View Record", **button_style, command=view_individual_record)
view_record_button.pack(pady=7)

# Text Area for Displaying Results
text_area = tk.Text(root, height=20, width=70, bg="black", fg="lightgreen", insertbackground="lightgreen")
text_area.grid(row=1, column=1, padx=10, pady=10, sticky="n")

root.mainloop()
