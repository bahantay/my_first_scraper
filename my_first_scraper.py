import requests
from bs4 import BeautifulSoup
import csv

url = 'https://github.com/trending'

def request_github_trending(url) -> object:
    req_res = requests.get(url)  # get the page by url
    return req_res


def extract(page):
    soup = BeautifulSoup(page.content, 'html.parser')  # get content as HTML
    trending_rows = soup.find_all(class_='Box-row')  # get all trending row
    return trending_rows


def transform(html_repos):
    top_25 = []
    for row in html_repos:
        auth_repo = row.find(class_ = 'h3').find('a').get_text().strip().replace('\n', '').replace(' ', '').split('/')                      # So, here we just found 'h3' tags, then 'a' tags, then cleaned from new_line charachters and spaces. The result is array of arrays of developer name and repo_name.
        nmbr_stars = row.find(class_ = 'f6').find('a').get_text().strip().replace('\n', '').replace(' ', '').replace(',', '`').split('/')   # Getting number of stars
        top_25.append({'developer': auth_repo[0], 'repository_name': auth_repo[1], 'nbr_stars': nmbr_stars[0]})                            # Adding array data to our hash of data
    return top_25

def format(repositories_data):
    csv_file = ','.join(repositories_data[0].keys()) + '\n'         # adding header for csv
    for user in repositories_data:
        line = ','.join(user.values()) + '\n'                       # getting lines of repo_data
        csv_file += line                                            # adding those lines to csv

    return csv_file


get_page = request_github_trending(url)
extracted_rows = extract(get_page)
cleaned_rows = transform(extracted_rows)
csv_file = format(cleaned_rows)

print(csv_file)