import xml.etree.ElementTree as ElementTree

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def fetch_course_urls():
    xml_sitemap_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    xml_list = requests.get(xml_sitemap_url).text
    urlset = ElementTree.fromstring(xml_list)
    course_urls = [url[0].text for url in urlset]
    return course_urls


def fetch_course_info(course_url):
    html_doc = requests.get(course_url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    tags = {
        'name': soup.find('h1', class_='title'),
        'languages': soup.find('div', class_='rc-Language'),
        'start_date': soup.find('div', class_='rc-StartDateString'),
        'rating': soup.find('div', class_='ratings-text'),
    }
    course = {}
    for tag_name, tag_content in tags.items():
        course[tag_name] = tag_content.get_text() if tag_content else 'N/A'
    weeks_tag = soup.find('div', class_='rc-WeekView')
    course['number_of_weeks'] = len(weeks_tag.contents) if weeks_tag else 'N/A'
    return course


def output_courses_info_to_xlsx(courses, filepath):
    if not courses:
        raise ValueError('There must be at least one course to save')
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(list(courses[0].keys()))
    for course in courses:
        worksheet.append(list(course.values()))
    workbook.save(filepath)


if __name__ == '__main__':
    course = fetch_course_info('https://www.coursera.org/learn/algorithms-part1')
    courses = [{'name': 'Gamification', 'languages': 'English, Subtitles: Ukrainian, Chinese (Simplified), Portuguese (Brazilian), Vietnamese, Russian, Turkish, Spanish, Kazakh', 'start_date': 'Starts Jul 17', 'rating': 'N/A', 'number_of_weeks': 6}, {'name': 'Algorithms, Part I', 'languages': 'English', 'start_date': 'Starts Jul 10', 'rating': '4.9 stars', 'number_of_weeks': 6}]
    output_courses_info_to_xlsx(courses, 'text.xlsx')
