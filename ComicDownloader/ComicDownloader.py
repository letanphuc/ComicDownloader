from JobPool import *
import os
import requests
from bs4 import BeautifulSoup
import urllib.request

_logger = get_logger(__name__)


def comic_parser(url):
    ret = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    items = soup.find_all('div', class_="col-xs-5 chapter")
    for i in items:
        chapter = i.find('a')
        ret.append(JobItem(chapter_parser, chapter.attrs['href']))

    return ret


def chapter_parser(url: str):
    ret = []
    items = url.split('/')
    name = items[len(items) - 3]
    chapter = items[len(items) - 2]
    dir_name = os.path.join('data', name, chapter)
    ret.append(JobItem(create_dir, dir_name))

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    items = soup.find_all('div', class_="page-chapter")
    for i in items:
        for img in i.find_all('img'):
            link = img.attrs['src']
            ret.append(JobItem(img_download, (link, dir_name)))

    return ret


def img_download(args):
    url, path = args
    name = url.split('/')[-1]
    path = os.path.join(path, name)
    urllib.request.urlretrieve(url, path)
    _logger.debug(f'Complete downloading {path}')


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
