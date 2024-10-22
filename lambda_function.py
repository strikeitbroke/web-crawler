import json
import requests
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs


@dataclass
class LinkInfo:
    save_url: str
    run_id: str
    date: str
    referring_url: str
    root_url: str



def get_links():
    ROOT_URL = "https://crawler-test.com/"
    r = requests.get(ROOT_URL)

    soup = bs(r.content, 'html5lib')

    links = []
    for link in soup.find_all('a', href=True):
        curr_time = datetime.now()
        full_url = urljoin(ROOT_URL, link['href'])
        save_url = full_url
        run_id = "hello"
        date = curr_time.strftime("%Y-%m-%d %H:%M:%S")
        referring_url = ROOT_URL
        root_url = ROOT_URL

        links.append(LinkInfo(save_url, run_id, date, referring_url, root_url))
        break

    return links


def lambda_handler(event, context):
    # TODO implement
    links = get_links()
    data =[]
    for link in links:
        data.append([link.save_url, link.run_id, link.date, link.referring_url, link.root_url])

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }

print(lambda_handler("", ""))

