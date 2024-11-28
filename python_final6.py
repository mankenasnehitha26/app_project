import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import random
import time

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quiz Application")
        self.root.geometry("600x500")
        
        # Initializing variables
        self.time_limit = 5 * 60  # Default 5 minutes (in seconds)
        self.total_questions = 0
        self.positive_marks = 1
        self.negative_marks = -0.5
        self.questions = []
        self.question_index = 0
        self.user_answers = []
        self.selected_answers = {}  # To track selected answer for each question
        self.time_left = self.time_limit  # Initialize time left
        
        # Background color settings
        self.bg_color = "#f0f4f7"
        self.button_color = "#FFFFFF"
        self.highlight_color = "#ffdd99"  # Highlight color for selected option
        self.root.configure(bg=self.bg_color)

        # Admin Panel - First screen
        self.admin_button = tk.Button(self.root, text="Admin Panel", font=("Arial", 16), command=self.create_admin_tab, bg=self.button_color, fg="green", width=20)
        self.admin_button.pack(pady=20)

    def create_admin_tab(self):
        # Hide the admin button and show admin setup UI
        self.admin_button.pack_forget()

        self.upload_button = tk.Button(self.root, text="Upload Questions", font=("Arial", 16), command=self.load_questions_from_csv, bg=self.button_color, fg="green", width=20)
        self.upload_button.pack(pady=40)

    def load_questions_from_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        questions = []

        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        try:
            with open(file_path, newline='', encoding="ISO-8859-1") as file:
                reader = csv.DictReader(file)
                required_headers = {"question", "option1", "option2", "option3", "option4", "answer"}
                headers = set(reader.fieldnames)

                # Check for missing headers
                if not required_headers.issubset(headers):
                    missing = required_headers - headers
                    raise KeyError(f"CSV file is missing required columns: {', '.join(missing)}")

                for row in reader:
                    questions.append({
                        "question": row["question"],
                        "options": [row["option1"], row["option2"], row["option3"], row["option4"]],
                        "answer": row["answer"]
                    })

            if not questions:
                raise ValueError("No questions found in the file.")

            # Shuffle questions and store them
            self.questions = random.sample(questions, len(questions))  # Load all questions
            print(f"Questions loaded: {len(self.questions)} questions.")  # Debugging line to confirm the questions are loaded
            messagebox.showinfo("Success", f"Questions loaded successfully! Please fill in the quiz details.")
            self.show_quiz_details()

        except KeyError as e:
            messagebox.showerror("Error", str(e))
        except csv.Error as e:
            messagebox.showerror("Error", f"CSV file could not be read properly: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

    def show_quiz_details(self):
        # Prompt for quiz details like time limit, marks
        self.upload_button.pack_forget()

        self.questions_count_label = tk.Label(self.root, text="Enter number of questions for quiz:", font=("Arial", 14), bg=self.bg_color, fg="#1e3d59")
        self.questions_count_label.pack(pady=10)

        self.questions_count_entry = tk.Entry(self.root, font=("Arial", 14))
        self.questions_count_entry.pack(pady=10)

        self.time_limit_label = tk.Label(self.root, text="Enter time limit in minutes:", font=("Arial", 14), bg=self.bg_color, fg="#1e3d59")
        self.time_limit_label.pack(pady=10)

        self.time_limit_entry = tk.Entry(self.root, font=("Arial", 14))
        self.time_limit_entry.pack(pady=10)

        self.positive_marks_label = tk.Label(self.root, text="Enter marks for correct answer:", font=("Arial", 14), bg=self.bg_color, fg="#1e3d59")
        self.positive_marks_label.pack(pady=10)

        self.positive_marks_entry = tk.Entry(self.root, font=("Arial", 14))
        self.positive_marks_entry.pack(pady=10)

        self.negative_marks_label = tk.Label(self.root, text="Enter negative marks for wrong answer:", font=("Arial", 14), bg=self.bg_color, fg="#1e3d59")
        self.negative_marks_label.pack(pady=10)

        self.negative_marks_entry = tk.Entry(self.root, font=("Arial", 14))
        self.negative_marks_entry.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Quiz Details", font=("Arial", 16), command=self.save_admin_data, bg=self.button_color, fg="green", width=20)
        self.save_button.pack(pady=20)

    def save_admin_data(self):
        try:
            # Get admin data from entries
            self.total_questions = int(self.questions_count_entry.get())
            self.time_limit = int(self.time_limit_entry.get()) * 60  # Convert to seconds
            self.time_left = self.time_limit  # Set time_left to admin-defined limit
            self.positive_marks = float(self.positive_marks_entry.get())
            self.negative_marks = float(self.negative_marks_entry.get())

            if self.total_questions <= 0 or self.time_limit <= 0:
                raise ValueError("Invalid input! Ensure all values are positive.")

            # Limit the questions to the number specified by the admin
            self.questions = self.questions[:self.total_questions]

            # Clear quiz detail UI and proceed to user detail collection
            self.clear_ui()
            self.create_user_tab()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def create_user_tab(self):
        # Ask user for login details before the quiz
        self.name_label = tk.Label(self.root, text="Enter your Name:", font=("Arial", 14), bg=self.bg_color)
        self.name_label.pack(pady=10)

        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.name_entry.pack(pady=10)

        self.email_label = tk.Label(self.root, text="Enter your Email:", font=("Arial", 14), bg=self.bg_color)
        self.email_label.pack(pady=10)

        self.email_entry = tk.Entry(self.root, font=("Arial", 14))
        self.email_entry.pack(pady=10)

        self.start_quiz_button = tk.Button(self.root, text="Start Quiz", font=("Arial", 16), command=self.start_quiz, bg=self.button_color, fg="green", width=20)
        self.start_quiz_button.pack(pady=20)

    def start_quiz(self):
        # Hide login details screen and start quiz
        self.clear_ui()

        self.timer_label = tk.Label(self.root, text="Time Left: 05:00", font=("Arial", 14), bg=self.bg_color, fg="#1e3d59")
        self.timer_label.pack(pady=10)

        self.question_label = tk.Label(self.root, text="", font=("Arial", 16, "italic"), wraplength=500, bg=self.bg_color, fg="#1e3d59")
        self.question_label.pack(pady=20)

        # Answer options and selected answer
        self.selected_answer = tk.StringVar()
        self.option_buttons = []
        self.option_frame = tk.Frame(self.root, bg=self.bg_color)
        self.option_frame.pack(pady=10)

        # Navigation buttons
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.prev_button = tk.Button(self.button_frame, text="Previous", command=self.previous_question, bg=self.button_color, fg="green", font=("Arial", 12))
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_question, bg=self.button_color, fg="green", font=("Arial", 12))
        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit_answer, state="disabled", bg=self.button_color, fg="green", font=("Arial", 12))

        self.prev_button.pack(side="left", padx=5)
        self.next_button.pack(side="left", padx=5)
        self.submit_button.pack(side="left", padx=5)
        self.button_frame.pack(pady=20)  # Ensure the button frame is packed

        self.update_timer()
        self.display_question()

    def display_question(self):
        if self.question_index >= len(self.questions):
            self.submit_answer()
            return

        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data["question"])

        # Clear previous options
        for button in self.option_buttons:
            button.destroy()
        self.option_buttons = []

        # Display answer options
        for option in question_data["options"]:
            option_button = tk.Button(self.option_frame, text=option, font=("Arial", 14), bg=self.button_color, width=30,
                                      command=lambda option=option: self.select_answer(option))
            option_button.pack(pady=5)
            self.option_buttons.append(option_button)

        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        self.prev_button.config(state="normal" if self.question_index > 0 else "disabled")
        self.next_button.config(state="normal" if self.question_index < len(self.questions) - 1 else "disabled")
        self.submit_button.config(state="normal" if self.question_index == len(self.questions) - 1 else "disabled")

    def select_answer(self, selected_option):
        self.selected_answers[self.question_index] = selected_option
        for button in self.option_buttons:
            button.config(bg=self.highlight_color if button["text"] == selected_option else self.button_color)

    def previous_question(self):
        if self.question_index > 0:
            self.question_index -= 1
            self.display_question()

    def next_question(self):
        if self.question_index < len(self.questions) - 1:
            self.question_index += 1
            self.display_question()

    def submit_answer(self):
        score = sum(
            self.positive_marks if self.selected_answers.get(i) == q["answer"] else self.negative_marks
            for i, q in enumerate(self.questions)
        )
        self.clear_ui()
        score_label = tk.Label(self.root, text=f"Your Score: {score}", font=("Arial", 24), bg=self.bg_color, fg="green")
        score_label.pack(pady=20)

    def update_timer(self):
        minutes, seconds = divmod(self.time_left, 60)
        self.timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.submit_answer()

    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

# Run the quiz application
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
