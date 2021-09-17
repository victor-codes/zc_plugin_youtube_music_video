from music.utils.request_client import RequestClient
from django.conf import settings
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

plugin_id = settings.PLUGIN_ID
org_id = settings.ORGANIZATON_ID
centrifugo = settings.CENTRIFUGO_TOKEN

headers = {"Authorization": "headers"}


def user_login():
    payload = {"email": "hng.user01@gmail.com", "password": "password"}

    request_client = RequestClient()

    response = request_client.request(
        method="POST",
        url="https://api.zuri.chat/auth/login",
        headers={"Content-Type": "application/json"},
        post_data=payload,
    )
    return response


def verify_token():
    headers = {
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJhdXRob3JpemVkIjp0cnVlLCJVc2VyIjp7ImlkIjoiN"
        "jEzNTkwZmQwMzY2YjY4MTZhMGI3NWVlIiwiZW1haWwiOiJ"
        "obmcudXNlcjAxQGdtYWlsLmNvbSJ9LCJleHAiOjE2MzEyND"
        "E1OTIsImlzcyI6ImFwaS56dXJpLmNoYXQifQ.XZPFXTTdIBL"
        "GlMSRi_3nziOXYFOidCWFiPsMIxdy2Y0"
    }

    request_client = RequestClient()

    response = request_client.request(
        method="GET",
        url="https://api.zuri.chat/auth/verify-token",
        headers={"Authorization": headers},
    )
    return response


def read_data(collection=None, filter_data=None):
    if filter_data is None:
        filter_data = {}

    request_client = RequestClient()

    response = request_client.request(
        method="GET",
        url=f"https://api.zuri.chat/data/read/{plugin_id}/{collection}/{org_id}",
        headers={"Authorization": headers},
        post_data=filter_data
    )
    return response


def write_data(collection, object_id, filter_data, payload, bulk_write=False, ):
    if filter_data is None:
        filter_data = {}

    if payload is None:
        payload = {}

    if object_id is None:
        object_id = {}

    post_data = {
        "plugin_id": plugin_id,
        "organization_id": org_id,
        "collection_name": collection,
        "bulk_write": bulk_write,
        "object_id": object_id,
        "filter": filter_data,
        "payload": payload
    }
    request_client = RequestClient()

    response = request_client.request(
        method="GET",
        url=f"https://api.zuri.chat/data/write/",
        headers=headers,
        post_data=post_data
    )
    return response


def centrifugo_post(room, data):
    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + centrifugo}
    post_data = {
        "method": "publish",
        "params": {
            "channel": room,
            "data": data
        }
    }
    request_client = RequestClient()

    response = request_client.request(
        method="POST",
        url="https://realtime.zuri.chat/api",
        headers=headers,
        post_data=post_data
    )
    return response


# init session
session = HTMLSession()

def get_video_info(url):
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(timeout=0)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    # open("index.html", "w").write(response.html.html)
    # initialize the result
    result = {}

    # video title
    result["title"] = soup.find("meta", itemprop="name")['content']
    
    # get the duration of the video
    result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text

    # thumbnail url
    result["thumbnail_url"] = soup.find("meta", property="og:image") ['content']

    # video url
    result["track_url"] = soup.find("meta", property="og:url")['content']

    return result
    

