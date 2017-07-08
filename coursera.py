import xml.etree.ElementTree as ElementTree

import requests

def fetch_course_urls():
    xml_sitemap_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    xml_list = requests.get(xml_sitemap_url).text
    urlset = ElementTree.fromstring(xml_list)
    course_urls = [url[0].text for url in urlset]
    return course_urls

def fetch_course_info(course_slug):
    pass


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    course_urls = fetch_course_urls()
