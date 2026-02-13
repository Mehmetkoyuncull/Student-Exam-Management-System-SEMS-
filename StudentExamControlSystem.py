import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date


DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Mehmet423431",
    "database": "StudentExamDB"
}


class StudentExamApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Student Exam System")
        self.root.geometry("1100x700")

        # DB bağlantısı
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

        # Notebook (sekme yapısı)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Sekmeler
        self.tab_students = ttk.Frame(self.notebook)
        self.tab_instructors = ttk.Frame(self.notebook)
        self.tab_courses = ttk.Frame(self.notebook)
        self.tab_reg = ttk.Frame(self.notebook)
        self.tab_exams = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_students, text="Students")
        self.notebook.add(self.tab_instructors, text="Instructors")
        self.notebook.add(self.tab_courses, text="Courses & Offerings")
        self.notebook.add(self.tab_reg, text="Registration")
        self.notebook.add(self.tab_exams, text="Exams & Grades")

        # UI’leri kur
        self.build_students_tab()
        self.build_instructors_tab()
        self.build_courses_tab()
        self.build_registration_tab()
        self.build_exams_tab()

        # Başlangıç yüklemeleri
        self.load_students()
        self.load_instructors()
        self.load_courses()
        self.load_offerings()
        self.load_registration()
        self.refresh_exam_dropdowns()

    # ====================================================
    #                        STUDENTS
    # ====================================================
    def build_students_tab(self):
        frame = ttk.LabelFrame(self.tab_students, text="Add / Edit Student")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Full Name:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        ttk.Label(frame, text="Department:").grid(row=2, column=0, sticky="w", padx=5, pady=3)

        self.st_name = ttk.Entry(frame, width=40)
        self.st_email = ttk.Entry(frame, width=40)
        self.st_dep = ttk.Entry(frame, width=40)

        self.st_name.grid(row=0, column=1, padx=5, pady=3)
        self.st_email.grid(row=1, column=1, padx=5, pady=3)
        self.st_dep.grid(row=2, column=1, padx=5, pady=3)

        ttk.Button(frame, text="Save Student",
                   command=self.save_student).grid(row=3, column=1, pady=8, sticky="e")

        table_frame = ttk.Frame(self.tab_students)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.st_table = ttk.Treeview(
            table_frame,
            columns=("id", "full_name", "email", "department", "reg_date"),
            show="headings"
        )

        self.st_table.heading("id", text="ID")
        self.st_table.heading("full_name", text="Full Name")
        self.st_table.heading("email", text="Email")
        self.st_table.heading("department", text="Department")
        self.st_table.heading("reg_date", text="Reg. Date")

        self.st_table.column("id", width=60)
        self.st_table.column("full_name", width=230)
        self.st_table.column("email", width=260)
        self.st_table.column("department", width=180)
        self.st_table.column("reg_date", width=100)

        self.st_table.pack(fill="both", expand=True)

        ttk.Button(self.tab_students, text="Delete Selected",
                   command=self.delete_student).pack(pady=5)

    def load_students(self):
        self.st_table.delete(*self.st_table.get_children())
        self.cursor.execute("""
            SELECT student_id, first_last_name, email, department, registration_date
            FROM Student ORDER BY first_last_name
        """)
        for row in self.cursor.fetchall():
            self.st_table.insert(
                "", "end",
                values=(row["student_id"], row["first_last_name"],
                        row["email"], row["department"], row["registration_date"])
            )

    def save_student(self):
        name = self.st_name.get().strip()
        email = self.st_email.get().strip()
        dep = self.st_dep.get().strip()

        if not name or not email or not dep:
            messagebox.showwarning("Warning", "All fields are required.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO Student(first_last_name, email, department, registration_date)
                VALUES (%s, %s, %s, %s)
            """, (name, email, dep, date.today()))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.st_name.delete(0, tk.END)
        self.st_email.delete(0, tk.END)
        self.st_dep.delete(0, tk.END)
        self.load_students()

    def delete_student(self):
        sel = self.st_table.selection()
        if not sel:
            messagebox.showwarning("Delete", "Please select a student.")
            return

        student_id = self.st_table.item(sel[0], "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete student ID {student_id}?"):
            return

        try:
            self.cursor.execute("DELETE FROM Student WHERE student_id = %s", (student_id,))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.load_students()

    # ====================================================
    #                        INSTRUCTORS
    # ====================================================
    def build_instructors_tab(self):
        frame = ttk.LabelFrame(self.tab_instructors, text="Add / Edit Instructor")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Full Name:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        ttk.Label(frame, text="Title:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        ttk.Label(frame, text="Department:").grid(row=3, column=0, sticky="w", padx=5, pady=3)

        self.ins_name = ttk.Entry(frame, width=40)
        self.ins_title = ttk.Entry(frame, width=40)
        self.ins_email = ttk.Entry(frame, width=40)
        self.ins_dep = ttk.Entry(frame, width=40)

        self.ins_name.grid(row=0, column=1, padx=5, pady=3)
        self.ins_title.grid(row=1, column=1, padx=5, pady=3)
        self.ins_email.grid(row=2, column=1, padx=5, pady=3)
        self.ins_dep.grid(row=3, column=1, padx=5, pady=3)

        ttk.Button(frame, text="Save Instructor",
                   command=self.save_instructor).grid(row=4, column=1, pady=8, sticky="e")

        table_frame = ttk.Frame(self.tab_instructors)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.ins_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "title", "email", "dep"),
            show="headings"
        )

        self.ins_table.heading("id", text="ID")
        self.ins_table.heading("name", text="Full Name")
        self.ins_table.heading("title", text="Title")
        self.ins_table.heading("email", text="Email")
        self.ins_table.heading("dep", text="Department")

        self.ins_table.column("id", width=60)
        self.ins_table.column("name", width=230)
        self.ins_table.column("title", width=120)
        self.ins_table.column("email", width=260)
        self.ins_table.column("dep", width=180)

        self.ins_table.pack(fill="both", expand=True)

        ttk.Button(self.tab_instructors, text="Delete Selected",
                   command=self.delete_instructor).pack(pady=5)

    def load_instructors(self):
        self.ins_table.delete(*self.ins_table.get_children())
        self.cursor.execute("""
            SELECT instructor_id, first_last_name, title, email, department
            FROM Instructor ORDER BY first_last_name
        """)
        for r in self.cursor.fetchall():
            self.ins_table.insert(
                "", "end",
                values=(r["instructor_id"], r["first_last_name"],
                        r["title"], r["email"], r["department"])
            )

    def save_instructor(self):
        name = self.ins_name.get().strip()
        title = self.ins_title.get().strip()
        email = self.ins_email.get().strip()
        dep = self.ins_dep.get().strip()

        if not name or not email:
            messagebox.showwarning("Warning", "Name and Email are required.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO Instructor(first_last_name, title, email, department)
                VALUES (%s, %s, %s, %s)
            """, (name, title, email, dep))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.ins_name.delete(0, tk.END)
        self.ins_title.delete(0, tk.END)
        self.ins_email.delete(0, tk.END)
        self.ins_dep.delete(0, tk.END)
        self.load_instructors()
        self.refresh_exam_dropdowns()
        self.load_offerings()

    def delete_instructor(self):
        sel = self.ins_table.selection()
        if not sel:
            messagebox.showwarning("Delete", "Please select an instructor.")
            return

        instructor_id = self.ins_table.item(sel[0], "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete instructor ID {instructor_id}?"):
            return

        try:
            self.cursor.execute("DELETE FROM Instructor WHERE instructor_id = %s", (instructor_id,))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.load_instructors()
        self.load_offerings()

    # =================================================
    #                   COURSES & OFFERINGS
    # ====================================================
    def build_courses_tab(self):
        # ---- Course form ----
        course_frame = ttk.LabelFrame(self.tab_courses, text="Create / Update Course")
        course_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(course_frame, text="Code:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(course_frame, text="Name:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(course_frame, text="Credit:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(course_frame, text="Department:").grid(row=3, column=0, padx=5, pady=3, sticky="w")

        self.crs_code = ttk.Entry(course_frame, width=25)
        self.crs_name = ttk.Entry(course_frame, width=40)
        self.crs_credit = ttk.Entry(course_frame, width=10)
        self.crs_dep = ttk.Entry(course_frame, width=30)

        self.crs_code.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.crs_name.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.crs_credit.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.crs_dep.grid(row=3, column=1, padx=5, pady=3, sticky="w")

        ttk.Button(course_frame, text="Save Course",
                   command=self.save_course).grid(row=4, column=1, pady=5, sticky="e")

        # ---- Course list ----
        course_table_frame = ttk.LabelFrame(self.tab_courses, text="Course Catalog")
        course_table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.course_table = ttk.Treeview(
            course_table_frame,
            columns=("id", "code", "name", "credit", "dep"),
            show="headings"
        )

        self.course_table.heading("id", text="ID")
        self.course_table.heading("code", text="Code")
        self.course_table.heading("name", text="Name")
        self.course_table.heading("credit", text="Credit")
        self.course_table.heading("dep", text="Department")

        self.course_table.column("id", width=60)
        self.course_table.column("code", width=80)
        self.course_table.column("name", width=250)
        self.course_table.column("credit", width=80)
        self.course_table.column("dep", width=200)

        self.course_table.pack(fill="both", expand=True)

        # ---- Offering form ----
        offer_frame = ttk.LabelFrame(self.tab_courses, text="Create Course Offering")
        offer_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(offer_frame, text="Course:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(offer_frame, text="Term:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(offer_frame, text="Instructor:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(offer_frame, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(offer_frame, text="End Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=3, sticky="w")

        self.offer_course_cb = ttk.Combobox(offer_frame, width=40, state="readonly")
        self.offer_term_cb = ttk.Combobox(offer_frame, width=30, state="readonly")
        self.offer_instructor_cb = ttk.Combobox(offer_frame, width=35, state="readonly")
        self.offer_start = ttk.Entry(offer_frame, width=20)
        self.offer_end = ttk.Entry(offer_frame, width=20)

        self.offer_course_cb.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.offer_term_cb.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.offer_instructor_cb.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.offer_start.grid(row=3, column=1, padx=5, pady=3, sticky="w")
        self.offer_end.grid(row=4, column=1, padx=5, pady=3, sticky="w")

        ttk.Button(offer_frame, text="Save Offering",
                   command=self.save_offering).grid(row=5, column=1, pady=5, sticky="e")

        # ---- Offering list ----
        offer_table_frame = ttk.LabelFrame(self.tab_courses, text="Course Offerings")
        offer_table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.offer_table = ttk.Treeview(
            offer_table_frame,
            columns=("id", "course", "term", "instructor", "start", "end"),
            show="headings"
        )

        self.offer_table.heading("id", text="Offer ID")
        self.offer_table.heading("course", text="Course")
        self.offer_table.heading("term", text="Term")
        self.offer_table.heading("instructor", text="Instructor")
        self.offer_table.heading("start", text="Start")
        self.offer_table.heading("end", text="End")

        self.offer_table.column("id", width=70)
        self.offer_table.column("course", width=200)
        self.offer_table.column("term", width=120)
        self.offer_table.column("instructor", width=180)
        self.offer_table.column("start", width=90)
        self.offer_table.column("end", width=90)

        self.offer_table.pack(fill="both", expand=True)

    def load_courses(self):
        # Course list
        self.course_table.delete(*self.course_table.get_children())
        self.cursor.execute("""
            SELECT course_id, code, name, credit, department
            FROM Course ORDER BY code
        """)
        courses = self.cursor.fetchall()
        for r in courses:
            self.course_table.insert(
                "", "end",
                values=(r["course_id"], r["code"], r["name"],
                        r["credit"], r["department"])
            )

        # Offering combobox – course
        self.course_choices = {}
        for r in courses:
            label = f'{r["code"]} - {r["name"]}'
            self.course_choices[label] = r["course_id"]
        self.offer_course_cb["values"] = list(self.course_choices.keys())

        # Term combobox
        self.cursor.execute("SELECT term_id, name FROM Term ORDER BY term_id")
        terms = self.cursor.fetchall()
        self.term_choices = {t["name"]: t["term_id"] for t in terms}
        self.offer_term_cb["values"] = list(self.term_choices.keys())

        # Instructor combobox
        self.cursor.execute("SELECT instructor_id, first_last_name FROM Instructor ORDER BY first_last_name")
        ins = self.cursor.fetchall()
        self.instructor_choices = {
            i["first_last_name"]: i["instructor_id"] for i in ins
        }
        self.offer_instructor_cb["values"] = list(self.instructor_choices.keys())

    def save_course(self):
        code = self.crs_code.get().strip()
        name = self.crs_name.get().strip()
        credit = self.crs_credit.get().strip()
        dep = self.crs_dep.get().strip()

        if not code or not name or not credit:
            messagebox.showwarning("Warning", "Code, Name, and Credit are required.")
            return

        try:
            credit_int = int(credit)
        except ValueError:
            messagebox.showwarning("Warning", "Credit must be integer.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO Course(code, name, credit, department)
                VALUES (%s, %s, %s, %s)
            """, (code, name, credit_int, dep))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.crs_code.delete(0, tk.END)
        self.crs_name.delete(0, tk.END)
        self.crs_credit.delete(0, tk.END)
        self.crs_dep.delete(0, tk.END)
        self.load_courses()

    def save_offering(self):
        course_label = self.offer_course_cb.get()
        term_label = self.offer_term_cb.get()
        ins_label = self.offer_instructor_cb.get()
        start_date = self.offer_start.get().strip()
        end_date = self.offer_end.get().strip()

        if not course_label or not term_label or not ins_label or not start_date or not end_date:
            messagebox.showwarning("Warning", "All offering fields are required.")
            return

        course_id = self.course_choices.get(course_label)
        term_id = self.term_choices.get(term_label)
        instructor_id = self.instructor_choices.get(ins_label)

        try:
            self.cursor.execute("""
                INSERT INTO CourseOffering(course_id, term_id, instructor_id, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (course_id, term_id, instructor_id, start_date, end_date))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.offer_start.delete(0, tk.END)
        self.offer_end.delete(0, tk.END)
        self.load_offerings()
        self.load_registration()
        self.refresh_exam_dropdowns()

    def load_offerings(self):
        self.offer_table.delete(*self.offer_table.get_children())

        self.cursor.execute("""
            SELECT o.offer_id, c.code, c.name AS course_name,
                   t.name AS term_name,
                   i.first_last_name AS instructor_name,
                   o.start_date, o.end_date
            FROM CourseOffering o
            JOIN Course c ON o.course_id = c.course_id
            JOIN Term t ON o.term_id = t.term_id
            JOIN Instructor i ON o.instructor_id = i.instructor_id
            ORDER BY o.offer_id
        """)
        offers = self.cursor.fetchall()
        for r in offers:
            label = f'{r["code"]} - {r["course_name"]} ({r["term_name"]})'
            self.offer_table.insert(
                "", "end",
                values=(
                    r["offer_id"], label,
                    r["term_name"], r["instructor_name"],
                    r["start_date"], r["end_date"]
                )
            )

        # Registration ve exam sekmeleri için offering seçimi
        self.offer_choices = {}
        for r in offers:
            label = f'{r["offer_id"]} - {r["code"]} - {r["course_name"]} ({r["term_name"]})'
            self.offer_choices[label] = r["offer_id"]
        self.reg_offer_cb["values"] = list(self.offer_choices.keys())
        self.exam_offer_cb["values"] = list(self.offer_choices.keys())
        self.report_offer_cb["values"] = list(self.offer_choices.keys())

    # ==========  ========================================
    #                     REGISTRATION
    # =============================================
    def build_registration_tab(self):
        form = ttk.LabelFrame(self.tab_reg, text="Register Student to Offering")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Student:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(form, text="Offering:").grid(row=1, column=0, padx=5, pady=3, sticky="w")

        self.reg_student_cb = ttk.Combobox(form, width=45, state="readonly")
        self.reg_offer_cb = ttk.Combobox(form, width=60, state="readonly")

        self.reg_student_cb.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.reg_offer_cb.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        ttk.Button(form, text="Enroll", command=self.save_registration).grid(
            row=2, column=1, pady=5, sticky="e"
        )

        # Registration list
        table_frame = ttk.LabelFrame(self.tab_reg, text="Registrations")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.reg_table = ttk.Treeview(
            table_frame,
            columns=("id", "student", "offering", "date", "status"),
            show="headings"
        )

        self.reg_table.heading("id", text="Reg ID")
        self.reg_table.heading("student", text="Student")
        self.reg_table.heading("offering", text="Offering")
        self.reg_table.heading("date", text="Reg Date")
        self.reg_table.heading("status", text="Status")

        self.reg_table.column("id", width=70)
        self.reg_table.column("student", width=200)
        self.reg_table.column("offering", width=400)
        self.reg_table.column("date", width=90)
        self.reg_table.column("status", width=100)

        self.reg_table.pack(fill="both", expand=True)

    def load_registration(self):
        # Student combobox
        self.cursor.execute("SELECT student_id, first_last_name FROM Student ORDER BY first_last_name")
        students = self.cursor.fetchall()
        self.student_choices = {
            f'{s["student_id"]} - {s["first_last_name"]}': s["student_id"]
            for s in students
        }
        self.reg_student_cb["values"] = list(self.student_choices.keys())

        # Registration list
        self.reg_table.delete(*self.reg_table.get_children())
        self.cursor.execute("""
            SELECT r.registration_id, s.first_last_name AS student_name,
                   c.code, c.name AS course_name, t.name AS term_name,
                   r.registration_date, r.status, r.offer_id
            FROM Registration r
            JOIN Student s ON r.student_id = s.student_id
            JOIN CourseOffering o ON r.offer_id = o.offer_id
            JOIN Course c ON o.course_id = c.course_id
            JOIN Term t ON o.term_id = t.term_id
            ORDER BY r.registration_id
        """)
        for r in self.cursor.fetchall():
            label = f'{r["offer_id"]} - {r["code"]} - {r["course_name"]} ({r["term_name"]})'
            self.reg_table.insert(
                "", "end",
                values=(r["registration_id"], r["student_name"],
                        label, r["registration_date"], r["status"])
            )

    def save_registration(self):
        s_label = self.reg_student_cb.get()
        o_label = self.reg_offer_cb.get()

        if not s_label or not o_label:
            messagebox.showwarning("Warning", "Student and Offering are required.")
            return

        student_id = self.student_choices.get(s_label)
        offer_id = self.offer_choices.get(o_label)

        try:
            self.cursor.execute("""
                INSERT INTO Registration(student_id, offer_id, registration_date, status)
                VALUES (%s, %s, %s, %s)
            """, (student_id, offer_id, date.today(), "registered"))
            self.conn.commit()
        except mysql.connector.Error as err:
            # UNIQUE (student_id, offer_id) ihlali vs.
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.load_registration()

    # ====================================================
    #                     EXAMS & GRADES
    # ====================================================
    def build_exams_tab(self):
        # ---------- Exam definition ----------
        exam_frame = ttk.LabelFrame(self.tab_exams, text="Define Exam")
        exam_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(exam_frame, text="Offering:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(exam_frame, text="Exam Type (midterm/final/quiz):").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(exam_frame, text="Exam Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(exam_frame, text="Weight (0-100):").grid(row=3, column=0, padx=5, pady=3, sticky="w")

        self.exam_offer_cb = ttk.Combobox(exam_frame, width=60, state="readonly")
        self.exam_type_entry = ttk.Entry(exam_frame, width=20)
        self.exam_date_entry = ttk.Entry(exam_frame, width=20)
        self.exam_weight_entry = ttk.Entry(exam_frame, width=10)

        self.exam_offer_cb.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.exam_type_entry.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.exam_date_entry.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.exam_weight_entry.grid(row=3, column=1, padx=5, pady=3, sticky="w")

        ttk.Button(exam_frame, text="Save Exam",
                   command=self.save_exam).grid(row=4, column=1, pady=5, sticky="e")

        # ---------- Grade entry ----------
        grade_frame = ttk.LabelFrame(self.tab_exams, text="Enter Grade")
        grade_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(grade_frame, text="Exam:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(grade_frame, text="Student:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        ttk.Label(grade_frame, text="Score (0-100):").grid(row=2, column=0, padx=5, pady=3, sticky="w")

        self.grade_exam_cb = ttk.Combobox(grade_frame, width=60, state="readonly")
        self.grade_student_cb = ttk.Combobox(grade_frame, width=40, state="readonly")
        self.grade_score_entry = ttk.Entry(grade_frame, width=10)

        self.grade_exam_cb.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.grade_student_cb.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.grade_score_entry.grid(row=2, column=1, padx=5, pady=3, sticky="w")

        ttk.Button(grade_frame, text="Save Grade",
                   command=self.save_grade).grid(row=3, column=1, pady=5, sticky="e")

        # ---------- Report ----------
        report_frame = ttk.LabelFrame(self.tab_exams, text="Course Performance Report (Weighted Average)")
        report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(report_frame, text="Offering:").grid(row=0, column=0, padx=5, pady=3, sticky="w")

        self.report_offer_cb = ttk.Combobox(report_frame, width=60, state="readonly")
        self.report_offer_cb.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        ttk.Button(report_frame, text="Load Report", command=self.load_report).grid(
            row=0, column=2, padx=5, pady=3
        )

        self.report_table = ttk.Treeview(
            report_frame,
            columns=("student", "weighted_avg", "status"),
            show="headings"
        )

        self.report_table.heading("student", text="Student")
        self.report_table.heading("weighted_avg", text="Weighted Avg")
        self.report_table.heading("status", text="Pass/Fail")

        self.report_table.column("student", width=250)
        self.report_table.column("weighted_avg", width=120)
        self.report_table.column("status", width=100)

        self.report_table.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        report_frame.rowconfigure(1, weight=1)
        report_frame.columnconfigure(1, weight=1)

    def refresh_exam_dropdowns(self):
        # Exams için öğrenci listesi grade sırasında load edilecek
        # Exam listesi:
        self.cursor.execute("""
            SELECT e.exam_id, e.exam_type, e.exam_date,
                   c.code, c.name AS course_name, t.name AS term_name, e.offer_id
            FROM Exam e
            JOIN CourseOffering o ON e.offer_id = o.offer_id
            JOIN Course c ON o.course_id = c.course_id
            JOIN Term t ON o.term_id = t.term_id
            ORDER BY e.exam_id
        """)
        exams = self.cursor.fetchall()
        self.exam_choices = {}
        for e in exams:
            label = f'{e["exam_id"]} - {e["exam_type"]} {e["exam_date"]} ({e["code"]} {e["course_name"]} - {e["term_name"]})'
            self.exam_choices[label] = e
        self.grade_exam_cb["values"] = list(self.exam_choices.keys())

    def save_exam(self):
        offer_label = self.exam_offer_cb.get()
        exam_type = self.exam_type_entry.get().strip()
        exam_date_str = self.exam_date_entry.get().strip()
        weight_str = self.exam_weight_entry.get().strip()

        if not offer_label or not exam_type or not exam_date_str or not weight_str:
            messagebox.showwarning("Warning", "All exam fields are required.")
            return

        try:
            weight = int(weight_str)
        except ValueError:
            messagebox.showwarning("Warning", "Weight must be integer.")
            return

        if not (0 <= weight <= 100):
            messagebox.showwarning("Warning", "Weight must be between 0 and 100.")
            return

        offer_id = self.offer_choices.get(offer_label)

        # Toplam weight kontrolü (offer bazında 100'ü aşmasın)
        self.cursor.execute("SELECT COALESCE(SUM(weight),0) AS total_w FROM Exam WHERE offer_id = %s", (offer_id,))
        total_w = self.cursor.fetchone()["total_w"]
        if total_w + weight > 100:
            messagebox.showwarning("Constraint", f"Total weight would be {total_w + weight} (>100).")
            return

        # Exam tarihinin offering aralığında olup olmadığını DB tarafındaki constraint'e bırakıyoruz;
        # yine de minimum kontrol:
        self.cursor.execute("SELECT start_date, end_date FROM CourseOffering WHERE offer_id = %s", (offer_id,))
        off = self.cursor.fetchone()
        if off:
            if not (str(off["start_date"]) <= exam_date_str <= str(off["end_date"])):
                if not messagebox.askyesno(
                    "Date Warning",
                    "Exam date is outside offering range. Continue anyway?"
                ):
                    return

        try:
            self.cursor.execute("""
                INSERT INTO Exam(offer_id, exam_type, exam_date, weight)
                VALUES (%s, %s, %s, %s)
            """, (offer_id, exam_type, exam_date_str, weight))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.exam_type_entry.delete(0, tk.END)
        self.exam_date_entry.delete(0, tk.END)
        self.exam_weight_entry.delete(0, tk.END)
        self.refresh_exam_dropdowns()

    def save_grade(self):
        exam_label = self.grade_exam_cb.get()
        student_label = self.grade_student_cb.get()
        score_str = self.grade_score_entry.get().strip()

        if not exam_label or not student_label or not score_str:
            messagebox.showwarning("Warning", "Exam, Student, and Score are required.")
            return

        try:
            score = int(score_str)
        except ValueError:
            messagebox.showwarning("Warning", "Score must be integer.")
            return

        if not (0 <= score <= 100):
            messagebox.showwarning("Warning", "Score must be between 0 and 100.")
            return

        exam = self.exam_choices.get(exam_label)
        exam_id = exam["exam_id"]
        student_id = self.report_student_choices.get(student_label)

        # Basit pass_flag: score >= 60
        pass_flag = 1 if score >= 60 else 0

        try:
            self.cursor.execute("""
                INSERT INTO ExamResult(exam_id, student_id, score, pass_flag)
                VALUES (%s, %s, %s, %s)
            """, (exam_id, student_id, score, pass_flag))
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error: {err}")
            return

        self.grade_score_entry.delete(0, tk.END)

    def load_report(self):
        offer_label = self.report_offer_cb.get()
        if not offer_label:
            messagebox.showwarning("Warning", "Select an offering.")
            return

        offer_id = self.offer_choices.get(offer_label)

        self.report_table.delete(*self.report_table.get_children())

        # Weighted average: SUM(score * weight)/100
        self.cursor.execute("""
            SELECT s.first_last_name AS student_name,
                   ROUND(SUM(er.score * e.weight) / 100, 2) AS weighted_avg
            FROM Registration r
            JOIN Student s ON r.student_id = s.student_id
            JOIN Exam e ON e.offer_id = r.offer_id
            LEFT JOIN ExamResult er
                ON er.exam_id = e.exam_id AND er.student_id = r.student_id
            WHERE r.offer_id = %s
            GROUP BY s.student_id, s.first_last_name
        """, (offer_id,))
        rows = self.cursor.fetchall()

        for r in rows:
            avg = r["weighted_avg"] if r["weighted_avg"] is not None else 0
            status = "Pass" if avg >= 60 else "Fail"
            self.report_table.insert(
                "", "end",
                values=(r["student_name"], avg, status)
            )

        # Aynı anda grade girişi için öğrenci listesini de güncelle
        self.cursor.execute("""
            SELECT DISTINCT s.student_id, s.first_last_name
            FROM Registration r
            JOIN Student s ON r.student_id = s.student_id
            WHERE r.offer_id = %s
        """, (offer_id,))
        students = self.cursor.fetchall()
        self.report_student_choices = {
            f'{s["student_id"]} - {s["first_last_name"]}': s["student_id"]
            for s in students
        }
        self.grade_student_cb["values"] = list(self.report_student_choices.keys())


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentExamApp(root)
    root.mainloop()
