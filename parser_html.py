# Libraries
import requests
from bs4 import BeautifulSoup
import time
import os
from concurrent.futures import ThreadPoolExecutor

def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    course_name = (
        soup.find("h1", class_="course-header__course-title").text.strip()
        if soup.find("h1", class_="course-header__course-title")
        else ""
    )
    university_name = (
        soup.find("a", class_="course-header__institution").text.strip()
        if soup.find("a", class_="course-header__institution")
        else ""
    )
    faculty_name = (
        soup.find("a", class_="course-header__department").text.strip()
        if soup.find("a", class_="course-header__department")
        else ""
    )
    is_full_time = (
        soup.find("a", title="View all Full time Masters courses").text.strip()
        if soup.find("a", title="View all Full time Masters courses")
        else ""
    )
    description = (
        soup.find("div", id="Snippet").text.strip()
        if soup.find("div", id="Snippet")
        else ""
    )
    start_date = (
        soup.find("span", class_="key-info__start-date").text.strip()
        if soup.find("span", class_="key-info__start-date")
        else ""
    )
    fees = (
        soup.find("div", class_="course-sections__fees")
        .find("p")
        .get_text(separator=" ")
        .strip()
        if soup.find("div", class_="course-sections__fees")
        else ""
    )
    modality = (
        soup.find("span", class_="key-info__qualification").text.strip()
        if soup.find("span", class_="key-info__qualification")
        else ""
    )
    duration = (
        soup.find("span", class_="key-info__duration").text.strip()
        if soup.find("span", class_="key-info__duration")
        else ""
    )
    city = (
        soup.find("a", class_="course-data__city").text.strip()
        if soup.find("a", class_="course-data__city")
        else ""
    )
    country = (
        soup.find("a", class_="course-data__country").text.strip()
        if soup.find("a", class_="course-data__country")
        else ""
    )
    administration = (
        soup.find("a", class_="course-data__on-campus").text.strip()
        if soup.find("a", class_="course-data__on-campus")
        else ""
    )
    url = (
        soup.select_one('link[rel="canonical"]')["href"]
        if soup.select_one('link[rel="canonical"]')
        else ""
    )

    course_info = {
        "courseName": course_name,
        "universityName": university_name,
        "facultyName": faculty_name,
        "isItFullTime": is_full_time,
        "description": description,
        "startDate": start_date,
        "fees": fees,
        "modality": modality,
        "duration": duration,
        "city": city,
        "country": country,
        "administration": administration,
        "url": url,
    }

    return course_info

def write_to_tsv(course_info, filename):
    with open("TSV/" + filename, "w", encoding="utf-8") as f:
        # First row we write the column names
        column_names = "\t".join(course_info.keys())
        f.write(column_names + "\n")    
        # Second row we write the values of columns
        column_values = "\t".join(str(value) for value in course_info.values())
        f.write(column_values + "\n")



def main():
    root_path = "HTML/"

    course_counter = 1
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    # Reading HTML
                    html_content = f.read()

                    # Parsing HTML
                    course_info = parse_html(html_content)

                    # " was giving us troubles so we removed it
                    for key, value in course_info.items():
                        course_info[key] = value.replace('"', "")

                    # Writing to the .tsv file
                    tsv_filename = f"course_{course_counter}.tsv"
                    write_to_tsv(course_info, tsv_filename)

                    course_counter += 1

if __name__ == '__main__':
    main()