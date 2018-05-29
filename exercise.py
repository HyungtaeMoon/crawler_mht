
import os #내장모듈
from bs4 import BeautifulSoup

import requests #서브파티모듈
file_path = 'data/episode_list.html'
url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'


params = {
    'titleId' : 703845,
}

if os.path.exists(file_path):
    html = open(file_path, 'rt').read()

else:
    response = requests.get('url_episode_list', params)
    html = response.text
    open(file_path, 'wt').write(html)

soup = BeautifulSoup(html, 'lxml')

h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
description = soup.select_one('div.detail > p').get_text(strip=True)

print(title)
print(author)
print(description)



# 3 에피소드 정보 목록을 가져오기
# url_thumbnail: 썸네일 URL
# title: 제목
# rating: 별점
# created_date: 등록일
# no : 에피소드 상세페이지의 고유번호
# 각 에피소드들은 하나의 dict데이터
# 모든 에피소드들을 list에 넣는다