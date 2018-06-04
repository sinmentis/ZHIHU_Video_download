# -*- coding: utf-8 -*-
import re
import uuid
import subprocess
import requests


# fill in  your cookie
HEADERS = {'cookie': ''}
QUALITY = 'ld'    # 'ld'/'sd'/'hd' =低清/中清/高清


def get_video_ids_from_url(url):
    """
    回答或者文章的 url
    """
    html = requests.get(url, headers=HEADERS).text
    video_ids = re.findall(r'data-lens-id="(\d+)"', html)
    if video_ids:
        return set([int(video_id) for video_id in video_ids])
    return []


def yield_video_m3u8_url_from_video_ids(video_ids):
    for video_id in video_ids:
        api_video_url = 'https://lens.zhihu.com/api/videos/{}'.format(int(video_id))
        r = requests.get(api_video_url, headers=HEADERS)
        playlist = r.json()['playlist']
        m3u8_url = playlist[QUALITY]['play_url']
        yield m3u8_url


def download(url):
    video_ids = get_video_ids_from_url(url)
    print("Got video ids successly!")
    print(video_ids)
    m3u8_list = list(yield_video_m3u8_url_from_video_ids(video_ids))
    print("Got m3u8 successly!")
    print(m3u8_list)
    filename = '{}.mp4'.format(uuid.uuid4())
    for idx, m3u8_url in enumerate(m3u8_list):
        print('download {}'.format(m3u8_url))
        subprocess.call(['ffmpeg', '-i', m3u8_url, filename.format(str(idx))])


if __name__ == '__main__':
    # copy the address below
    url = ''
    download(url)