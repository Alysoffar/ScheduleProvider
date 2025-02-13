Timetable Generator

This project is a Python-based timetable generator that extracts course information from a PDF timetable, processes it, and generates valid schedules based on user preferences. The tool is designed to help students or faculty members create conflict-free schedules while considering constraints such as preferred lecturers, preferred time slots, and days to avoid.

Features
1.	PDF Extraction:

2.	Extracts timetable data from a PDF file using pdfplumber.

3.	Timetable Parsing:

4.	Parses the extracted data into a structured format (list of dictionaries) with details such as course code, course name, section type, room, lecturer, time, and day.

Schedule Generation:

1.	Generates valid schedules by avoiding:

2.	Time clashes within the same day.

3.	Time clashes for the same lecturer.

4.	Days to avoid.

5.	Prioritizes courses taught by preferred lecturers.

User Preferences:

Allows users to specify:

1.	Preferred lecturers.

2.	Preferred time slots.

3.	Days to avoid.

4.	Output:

5.	Displays valid schedules in a readable format, sorted by day and time.

Code Overview
1. PDF Extraction (extract_table_from_pdf)
Extracts table data from a specified range of pages in a PDF file.

Uses the pdfplumber library to read the PDF and extract tables.

2. Timetable Parsing (parse_timetable)
Processes the extracted table data into a list of course dictionaries.




Handles:

1.	Identifying days (e.g., "Su", "Mon").

2.	Parsing course details (e.g., course code, lecturer, room).

3.	Avoiding duplicates using a set for current_day.

4.	Time Slot Parsing (parse_time_slot and parse_time_range)
•	Converts time slot numbers (e.g., 1, 2) into human-readable time ranges (e.g., "8:30 - 9:20").

5.	Parses time strings (e.g., "8:30 - 9:20") into datetime.time objects for comparison.

5.	Schedule Validation (is_valid_schedule)
•	Ensures that the generated schedule is valid by:

6.	Avoiding time clashes within the same day.

7.	Avoiding time clashes for the same lecturer.

8.	Respecting user preferences (e.g., preferred lecturers, preferred times, days to avoid).

6.	Schedule Generation (generate_possible_schedules)
•	Generates possible schedules by permuting the list of filtered courses.

9.	Limits the number of permutations to 10 for performance reasons.

10.	Filters schedules based on user constraints.

6. Output (print_schedule)
1.	Displays the generated schedules in a readable format.

2.	Sorts courses by day and time for better readability.

How It Works
Input:

1.	The user provides a PDF file containing the timetable.

2.	The user specifies preferences:

3.	Preferred lecturers.

4.	Preferred time slots.

5.	Days to avoid.

Processing:

1.	The PDF is parsed to extract timetable data.

2.	The data is processed into a list of course dictionaries.

3.	Valid schedules are generated based on user preferences.

Output:

The valid schedules are displayed, sorted by day and time.

Install the required Python libraries:

Usage
1.	Provide the PDF File:

2.	Place the PDF file (e.g., v30_publish.pdf) in the project directory.

Running the Script:

Enter Preferences:

When prompted, enter your preferences:

Preferred lecturers (comma-separated).

Preferred time slots (e.g., "8:30 - 9:20,10:30 - 11:20").

Days to avoid (e.g., "Sa,Su").

View the Output:

The script will display valid schedules that meet your preferences.

Example
Input PDF
A PDF file containing a timetable with courses, days, times, lecturers, and rooms.

User Preferences
Preferred lecturers: Dr. Smith, Dr. Johnson

Preferred time slots: 8:30 - 9:20,10:30 - 11:20

Days to avoid: Sa,Su

Output
Copy
========================================
Schedule 1:
========================================

Mon:
  8:30 - 9:20: CS101 Intro to CS
    Section: (L)
    Room: 101
    Lecturer: Dr. Smith

Tue:
  10:30 - 11:20: MATH101 Calculus
    Section: (L)
    Room: 102
    Lecturer: Dr. Johnson
========================================


Code Structure
main.py:

The main script that ties everything together.

Calls the functions to extract, parse, and generate schedules.

extract_table_from_pdf:

Extracts table data from the PDF.

parse_timetable:

Parses the extracted data into a list of course dictionaries.

parse_time_slot and parse_time_range:

Converts time slot numbers and time strings into usable formats.

is_valid_schedule:

Validates schedules based on user constraints.

generate_possible_schedules:

Generates valid schedules by permuting the list of courses.

print_schedule:

Displays the generated schedules in a readable format.

Dependencies
pdfplumber:

A Python library for extracting text and tables from PDF files.

datetime:

A Python module for handling date and time objects.

itertools:

A Python module for efficient looping and permutations.

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

Acknowledgments
Thanks to the pdfplumber library for making PDF extraction easy.

Inspired by the need for a simple and efficient timetable generator.
