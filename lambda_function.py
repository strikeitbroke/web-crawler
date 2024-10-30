import boto3
import uuid
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


def push_to_queue(msg):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName="web-crawler-queue")
    res = queue.send_message(MessageBody=json.dumps(msg))
    return res



def push_to_db():
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ROOT_URL = "https://crawler-test.com/"
    run_id = curr_time + "#" + str(uuid.uuid4())

    dynamodb = boto3.resource("dynamodb")
    table_name = "web-crawler"
    table = dynamodb.Table(table_name)
    item = {
            "visited_url": ROOT_URL,
            "run_id": run_id,
            "date": curr_time,
            "referring_url": None,
            "root_url": ROOT_URL
        }
    table.put_item(
        Item=item
    )

    push_to_queue(item)

    
    # r = requests.get(ROOT_URL)
    #
    # soup = bs(r.content, 'html5lib')
    #
    # links = []
    # for link in soup.find_all('a', href=True):
    #     curr_time = datetime.now()
    #     full_url = urljoin(ROOT_URL, link['href'])
    #     save_url = full_url
    #     run_id = "hello"
    #     date = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    #     referring_url = ROOT_URL
    #     root_url = ROOT_URL
    #
    #     links.append(LinkInfo(save_url, run_id, date, referring_url, root_url))
    #     break
    #
    # return links


def lambda_handler(event, context):
    push_to_db()

    return {
        'statusCode': 200,
        'body': json.dumps("success")
    }



if __name__ == "__main__":
    lambda_handler("", "")

