import pdfplumber
import re
from itertools import permutations
from datetime import datetime, time
from itertools import islice

def extract_table_from_pdf(pdf_path, start_page=30, end_page=39):
    timetables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
            page = pdf.pages[page_num]
            tables = page.extract_table()
            if tables:
                timetables.extend(tables)
    return timetables

def parse_time_slot(slot_number):
    time_slots = {
        1: "8:30 - 9:20",
        2: "9:20 - 10:10",
        3: "10:30 - 11:20",
        4: "11:20 - 12:10",
        5: "12:30 - 13:20",
        6: "13:20 - 14:10",
        7: "14:30 - 15:20",
        8: "15:20 - 16:10",
        9: "16:30 - 17:20",
        10: "17:20 - 18:10"
    }
    return time_slots.get(slot_number, "")
def parse_timetable(table_data):
    """Parses the extracted table data into a list of course dictionaries."""
    all_courses = []
    current_day = None


    def is_day(text):
        if isinstance(text, list):  # Check if text is a list
            text = ' '.join(str(cell) for cell in text if cell)  # Join list elements into a single string
        # Check for common day abbreviations (e.g., "Su", "Mon", "Tue", etc.)
        return bool(re.match(r'^(Sat|Sun|Mon|Tue|Wed|Thu|Fri|Sa|Su|Mo|Tu|We|Th)$', text.strip(), re.IGNORECASE))

    def is_header_or_time(text):
        return (
            'aastmt' in text.lower() or
            'timetable generated' in text.lower() or
            bool(re.search(r'\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}', text)) or
            text.strip().isdigit()
        )

    def parse_course_entry(text, column_index):
        if not text.strip():
            return None

        course_info = {
            'course_code': '',
            'course_name': '',
            'section_type': '',
            'room': '',
            'lecturer': '',
            'time': parse_time_slot(column_index),
        }

        text = text.strip()  # Remove leading/trailing whitespace

        # Extract room number
        room_match = re.search(r'(?:L\.|)\d{3}(?:[A-Z])?', text)
        if room_match:
            course_info['room'] = room_match.group(0)
            text = text.replace(room_match.group(0), '').strip()

        # Extract course code
        code_match = re.search(r'([A-Z][-A-Z0-9]*)\s*', text, re.IGNORECASE)
        if code_match:
            course_info['course_code'] = code_match.group(1).strip()
            text = text.replace(code_match.group(0), '').strip()

        # Extract course name
        name_match = re.search(r'\s*([A-Za-z\s]+)(?:\s*?\([LS]\))?', text)
        if name_match:
            course_info['course_name'] = name_match.group(1).strip()  # Store only the course name

        # Extract section type
        section_match = re.search(r'\(([LS])\)', text)
        if section_match:
            course_info['section_type'] = section_match.group(1)

        # Extract lecturer
        lecturer_match = re.search(r'(?:Dr\.|Eng\.|Prof\.)\s+([A-Za-z]+\s*[A-Za-z]+)', text)
        if lecturer_match:
            course_info['lecturer'] = lecturer_match.group(0).strip()

        return course_info

    for row_index, row in enumerate(table_data):
        if not row or all(cell is None or cell.strip() == '' for cell in row):
            continue

        # Debug: Print the row to inspect its structure
        print(f"Row {row_index}: {row}")
          # Initialize current_day as an empty list

        # Check if the first cell in the row is a day
        if is_day(row[0]):
            # Append the day to the current_day list
            if isinstance(row[0], str):  # If row[0] is a string
                current_day=row[0].strip()
                for i, cell in enumerate(row[1:], 1):  # Start from the second column
                    if cell and str(cell).strip():
                        course_info = parse_course_entry(str(cell), i)
                        if course_info:
                            course_info['day'] = current_day  # Assign the current day to the course
                            all_courses.append(course_info)

            print(f"Updated current_day to: {current_day}")  # Debug: Print the updated day
            continue  # Skip to the next row after updating the day

        # Skip headers or time rows
        if is_header_or_time(' '.join(str(cell) for cell in row if cell)):
            continue


    for course in all_courses:  # Check if lecturer information is present
        print(f" 👨‍🏫 {course['lecturer']}")

        print(f" 👨‍🏫 {course['course_code']}")

        print(f" 👨‍🏫 {course['course_name']}")

        print(f" 👨‍🏫 {course['room']}")

        print(f" 👨‍🏫 {course['section_type']}")

        print(f" 👨‍🏫 {course['time']}")
        print(f" 👨‍🏫 {course['day']}")

        print("\n")
    return all_courses




def parse_time_range(time_str):
    start, end = map(str.strip, time_str.split('-'))
    start_time = datetime.strptime(start, '%H:%M').time()
    end_time = datetime.strptime(end, '%H:%M').time()
    return start_time, end_time
def is_valid_schedule(schedule, constraints):
    time_slots_used = {}  # Track time slots used by day
    lecturer_time_slots = {}  # Track time slots used by lecturers
    has_preferred_lecturer = False

    # Create a copy of the schedule to avoid modifying the original list while iterating
    schedule_copy = schedule.copy()

    for course in schedule_copy:
        day = course["day"]
        lecturer = course["lecturer"]

        # Check if the day is to be avoided
        if day.strip() in constraints["days_to_avoid"]:
            schedule.remove(course)  # Remove the course from the original schedule
            continue

        # Initialize time slots for the day and lecturer if not already done
        if day not in time_slots_used:
            time_slots_used[day] = set()
        if lecturer not in lecturer_time_slots:
            lecturer_time_slots[lecturer] = set()

        # Check if the lecturer is preferred
        if lecturer in constraints["preferred_lecturers"]:
            has_preferred_lecturer = True

        # Check if the course time is preferred
        if constraints["preferred_times"]:
            course_time = course["time"]
            if course_time not in constraints["preferred_times"]:
                schedule.remove(course)  # Remove the course from the original schedule
                continue

        # Parse the course time
        start_time, end_time = parse_time_range(course["time"])

        # Check for time clashes within the same day
        clash_found = False
        for used_start, used_end in time_slots_used[day]:
            if (start_time >= used_start and start_time < used_end) or \
               (end_time > used_start and end_time <= used_end):
                schedule.remove(course)  # Remove the course from the original schedule
                clash_found = True
                break  # Exit the inner loop after removing the conflicting course

        if clash_found:
            continue  # Skip to the next course

        # Check for time clashes for the lecturer
        for used_start, used_end in lecturer_time_slots[lecturer]:
            if (start_time >= used_start and start_time < used_end) or \
               (end_time > used_start and end_time <= used_end):
                schedule.remove(course)  # Remove the course from the original schedule
                clash_found = True
                break  # Exit the inner loop after removing the conflicting course

        if clash_found:
            continue  # Skip to the next course

        # If the course wasn't removed, add its time slots to the tracking sets
        time_slots_used[day].add((start_time, end_time))
        lecturer_time_slots[lecturer].add((start_time, end_time))

    return has_preferred_lecturer and schedule  # Return both has_preferred_lecturer and the modified schedule
def generate_possible_schedules(all_courses, constraints):
    """
    Generates possible schedules, prioritizing courses with preferred lecturers.

    Args:
      all_courses: A list of dictionaries, where each dictionary represents a course
                   with keys like 'course_code', 'course_name', 'time', 'day', 'lecturer', etc.
      constraints: A dictionary containing the user's preferences:
                   - "preferred_lecturers": A list of preferred lecturer names.
                   - "preferred_times": A list of preferred time slots.
                   - "days_to_avoid": A list of days to avoid.

    Returns:
      A list of valid schedules, where each schedule is a list of courses.
    """

    courses_with_preferred_lecturers = [
        course for course in all_courses
        if any(lecturer.strip() in course["lecturer"] for lecturer in constraints["preferred_lecturers"])
    ]

    if not courses_with_preferred_lecturers:
        print("No courses found with preferred lecturers.")
        return []

    filtered_courses = []
    for course in all_courses:
        if course["day"] not in constraints["days_to_avoid"]:
            if not constraints["preferred_times"] or course["time"] in constraints["preferred_times"]:
                filtered_courses.append(course)

    # Limit permutations to 10
    limited_permutations = islice(permutations(filtered_courses), 10)
    valid_schedules = []
    for perm in limited_permutations:
        schedule = list(perm)
        if is_valid_schedule(schedule, constraints):
            valid_schedules.append(schedule)


    return valid_schedules
def print_schedule(schedule, schedule_number):
    print(f"\n{'=' * 40}")
    print(f"Schedule {schedule_number}:")
    print(f"{'=' * 40}")

    # Define the order of days
    day_order = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

    # Sort the schedule by day and time
    sorted_schedule = sorted(
        schedule,
        key=lambda x: (
            day_order.index(x['day']),  # Sort by day order
            parse_time_range(x['time'])[0]  # Sort by start time
        )
    )

    # Print the sorted schedule
    for course in sorted_schedule:
        print(f"\n{course['day']}:")
        print(f"  {course['time']}: {course['course_code']} {course['course_name']}")
        print(f"    Section: ({course['section_type']})")
        print(f"    Room: {course['room']}")
        print(f"    Lecturer: {course['lecturer']}")
    print(f"{'=' * 40}\n")

# ... rest of the code (extract_table_from_pdf, parse_timetable, main, etc.)

def main():
    pdf_path = 'v30_publish.pdf'
    try:
        table_data = extract_table_from_pdf(pdf_path)
        if not table_data:
            print("No table data extracted. Please check the PDF file.")
            return

        timetable = parse_timetable(table_data)

        print("\nEnter your preferences:")
        constraints = {
            "preferred_lecturers": [name.strip() for name in
                                    input("Preferred lecturers (comma-separated): ").split(",")],
            "preferred_times": [time.strip() for time in
                                input("Preferred time slots (e.g., '8:30 - 9:20,10:30 - 11:20'): ").split(",")],
            "days_to_avoid": [day.strip() for day in input("Days to avoid (e.g., 'Sa,Su'): ").split(",")]
        }

        valid_schedules = generate_possible_schedules(timetable, constraints)

        if valid_schedules:
            print(f"\nFound {len(valid_schedules)} valid schedule(s).")
            for i, schedule in enumerate(valid_schedules, 1):
                print_schedule(schedule, i)
        else:
            print("\nNo valid schedules found with your constraints.")
            print("Try adjusting your preferences:")
            print("1. Choose different preferred lecturers")
            print("2. Be more flexible with time slots")
            print("3. Reduce the number of days to avoid")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()