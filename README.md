# 📊 Student Performance Dashboard

A Python script that reads a student dataset, performs subject-wise and
composite performance analysis, generates 6 charts, and opens a fully
styled dark-mode HTML dashboard automatically in your browser.

---

## 🖥️ Output Preview



file:///C:/Users/Dell/Desktop/StudentPerformanceDashboard.html
<img width="1248" height="560" alt="image" src="https://github.com/user-attachments/assets/dd936814-e0e2-448e-a7d7-57a07c0171c0" />
<img width="1251" height="634" alt="image" src="https://github.com/user-attachments/assets/47bc31a4-c3eb-47a4-b0c5-d0997d3751bf" />
<img width="1268" height="567" alt="image" src="https://github.com/user-attachments/assets/b4eff46c-fc7e-4d87-ba11-f5ffdab79b33" />
<img width="1211" height="619" alt="image" src="https://github.com/user-attachments/assets/14ec11c2-59ea-4d85-9775-e3a0fe3d3358" />
<img width="1324" height="450" alt="image" src="https://github.com/user-attachments/assets/9f7c5820-a029-479e-8503-acf1766d826a" />
<img width="1153" height="597" alt="image" src="https://github.com/user-attachments/assets/66535d6f-cc26-4ebc-b536-23d566fb3830" />








---

## 📌 What It Does

### Analysis 1 — Average Marks per Subject
- Computes **Mean, Median, Std Dev, Min, Max** for Math, Physics, Chemistry, English
- Identifies the strongest and weakest subject in the class

### Analysis 2 — Top-Performing Students
- Ranks students using a **composite score formula**:
  - 60% Academic Score + 20% Attendance + 20% Study Hours (normalised)
- Displays Top 5 students with medals 🥇🥈🥉

---

## 📈 Charts Generated

| Chart | Type | Description |
|-------|------|-------------|
| A | Grouped Bar | Mean · Median · Min · Max per subject |
| B | Error Bar | Mean ± Standard Deviation |
| C | Radar | Top-3 students' subject profiles |
| D | Horizontal Bar | Composite score ranking |
| E | Box Plot | Score spread per subject |
| F | Strip / Scatter | Individual student scores |

All charts are embedded as **base64 PNGs** inside a single self-contained HTML file.

---

## 🛠️ Built With

- Python 3
- pandas
- numpy
- matplotlib
- base64, io, tempfile (standard library)

---

## 📂 Project Structure

```
Student-Analysis-report/
├── student_marks_analysis_web.py   ← main script
├── student_dataset.csv             ← input data (not included)
└── README.md
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install pandas numpy matplotlib
```

### 2. Update the CSV path
Open `student_marks_analysis_web.py` and change line 11:
```python
CSV_PATH = r"C:/Users/YourName/Downloads/student_dataset.csv"
```

### 3. Run the script
```bash
python student_marks_analysis_web.py
```

The dashboard will **automatically open in your browser**. ✅

---

## 📋 Dataset Requirements

Your CSV file must contain these columns:

| Column | Description |
|--------|-------------|
| `Name` | Student name |
| `Math` | Marks in Math |
| `Physics` | Marks in Physics |
| `Chemistry` | Marks in Chemistry |
| `English` | Marks in English |
| `Percentage` | Overall percentage |
| `Attendance` | Attendance percentage |
| `Study_Hours` | Daily study hours |
| `Grade` | Letter grade (A, B, C…) |

---

## 👩‍💻 Author

**Kritika** — College Assignment Project
