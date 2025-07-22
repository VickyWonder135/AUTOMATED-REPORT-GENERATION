import pandas as pd
from fpdf import FPDF

df = pd.read_csv("data.csv")

avg_score = df['Score'].mean()
max_score = df['Score'].max()
min_score = df['Score'].min()
top_performer = df[df['Score'] == max_score]['Name'].values[0]
dept_avg = df.groupby('Department')['Score'].mean().round(2)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Student Performance Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section_title(self, title):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.ln(4)

    def add_text(self, text):
        self.set_font("Arial", '', 11)
        self.multi_cell(0, 10, text)
        self.ln()

pdf = PDF()
pdf.add_page()

pdf.add_section_title("1. Summary Statistics")
summary = (
    f"Average Score: {avg_score:.2f}\n"
    f"Maximum Score: {max_score}\n"
    f"Minimum Score: {min_score}\n"
    f"Top Performer: {top_performer}"
)
pdf.add_text(summary)

pdf.add_section_title("2. Department-wise Average Score")
for dept, score in dept_avg.items():
    pdf.add_text(f"{dept}: {score}")

pdf.add_section_title("3. Full Data Table")
for index, row in df.iterrows():
    line = f"{row['Name']} - {row['Department']} - Score: {row['Score']}"
    pdf.add_text(line)

pdf.output("student_report.pdf")
print("PDF report created as 'student_report.pdf'")
