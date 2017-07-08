import sys
import logging
import xml.etree.ElementTree as ElementTree
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

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


def output_courses_into_xlsx(courses, filepath):
    if not courses:
        raise ValueError('There must be at least one course to save')
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(list(courses[0].keys()))
    for course in courses:
        worksheet.append(list(course.values()))
    workbook.save(filepath)


def parse_args(argv):
    parser = ArgumentParser()
    parser.add_argument('--number_of_courses', '-n', type=int, default=20)
    parser.add_argument('--filepath', '-f', type=str, default='output.xlsx')
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    logger.info('fetching course urls...')
    course_urls = fetch_course_urls()
    courses = []
    for course_url in course_urls[:args.number_of_courses]:
        logger.info('fetching {0}...'.format(course_url))
        courses.append(fetch_course_info(course_url))
    output_courses_into_xlsx(courses, args.filepath)
    logger.info('successfully saved to {0}'.format(args.filepath))
