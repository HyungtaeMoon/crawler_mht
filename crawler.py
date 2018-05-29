# 1. HTML받아와서 html변수에 문자열을할당
#  1-1. 만약 'data/episode_list.html'이 없다면
#   -> 내장모듈 os의 'exists'함수를 사용해본다
#   -> 파이썬 공식문서 확인
# http://comic.naver.com/webtoon/list.nhn?titleId=703845&weekday=wed
# 죽음에 관하여 (재) 페이지를
# requests를 사용해서 data/episode_list.html에 저장
#  list.nhn뒤 ?부터는 url에 넣지 말고 GET parameters로
#   -> requests문서의 'Passing Parameters In URLs'
# 저장 후에는
#  requests로 받은 데이터를 html변수에 할당
#
#  1-2. 이미 'data/episode_list.html'이 있다면
#   html변수에 파일을 불러와 할당

# 1.
#  os.path.exists(경로)의 결과는 파일이 존재하는지, 존재하지 않는지 여부를 True/False로 반환해준다
#  os.path.exists()의 결과를 분기로
#   파일이 존재하면 -> open()을 사용해 가져온 파일 객체를 read()한 결과 문자를 html변수에 할당
#   존재하지 않으면 -> 1. requests.get()의 결과인 response의 text속성값을 html변수에 할당
#               -> 2. response의 text속성값을 'data/episode_list.html'파일에 저장

# requests문서 아래 3개는 보고나서 진행
# Make a Request
# Passing Parameters In URLs
# Response Content
import os

import requests
from bs4 import BeautifulSoup

# HTML파일을 저장하거나 불러올 경로
file_path = 'data/episode_list.html'
# HTTP요청을 보낼 주소
url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
# HTTP요청시 전달할 GET Parameters
params = {
    'titleId': 703845,
}
# -> 'http://com....nhn?titleId=703845

# HTML파일이 로컬에 저장되어 있는지 검사
if os.path.exists(file_path):
    # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
    html = open(file_path, 'rt').read()
else:
    # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
    response = requests.get(url_episode_list, params)
    # 요청 응답객체의 text속성값을 html변수에 할당
    html = response.text
    # 받은 텍스트 데이터를 HTML파일로 저장
    open(file_path, 'wt').write(html)

# BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
soup = BeautifulSoup(html, 'lxml')

# div.detail > h2 (제목, 작가)의
#  0번째 자식: 제목 텍스트
#  1번째 자식: 작가정보 span Tag
#   Tag로부터 문자열을 가져올때는 get_text()
h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
# div.detail > p (설명)
description = soup.select_one('div.detail > p').get_text(strip=True)

print(title)
print(author)
print(description)


# 3. 에피소드 정보 목록을 가져오기
#  url_thumbnail:   썸네일 URL
#  title:           제목
#  rating:          별점
#  created_date:    등록일
#  no:              에피소드 상세페이지의 고유 번호
#   각 에피소드들은 하나의 dict데이터
#   모든 에피소드들을 list에 넣는다

# 에피소드 목록을 담고 있는 table
table = soup.select_one('table.viewList')

# table내의 모든 tr요소 목록
tr_list = table.select('tr')

# 첫 번째 tr은 thead의 tr이므로 제외, tr_list의 [1:]부터 순회
for index, tr in enumerate(tr_list[1:]):
    # 에피소드에 해당하는 tr은 클래스가 없으므로,
    # 현재 순회중인 tr요소가 클래스 속성값을 가진다면 continue
    if tr.get('class'):
        continue

    # 현재 tr의 첫 번째 td요소의 하위 img태그의 'src'속성값
    url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
    # 현재 tr의 첫 번째 td요소의 자식   a태그의 'href'속성값
    from urllib import parse
    url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
    query_string = parse.urlsplit(url_detail).query
    query_dict = parse.parse_qs(query_string)
    # print(query_dict)
    no = query_dict['no'][0]

    # 현재 tr의 두 번째 td요소의 자식 a요소의 내용
    title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
    # 현재 tr의 세 번째 td요소의 하위 strong태그의 내용
    rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
    # 현재 tr의 네 번째 td요소의 내용
    created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

    print(url_thumbnail)
    print(title)
    print(rating)
    print(created_date)
    print(no)

episode_list = [
    {
        'url_thumbnail': ...,
    },
    {

    }
]

# 4. 에피소드를 클래스로 구현
#   class Episode
#       attrs:
#           webtoon_id:     웹툰의 고유번호
#           no:             에피소드의 고유번호
#           url_thumbnail
#           title
#           rating
#           created_date

#       property:
#           url (실제 에피소드 페이지의 URL을 리턴)
#               파이썬 내장 urllib에 탑재되어있는 함수를 사용해서 생성
#               ex) http://comic.naver.com/webtoon/detail.nhn?titleId=703845&no=18

# 4-1. 위에서 dict형태로 만들던 로직을 클래스 인스턴스 생성방식으로 변경
#  episode_list리스트는 Episode인스턴스들을 자신의 요소로 가짐


# 숙제 1. 웹툰, 에피소드 이미지 클래스 작성, 에피소드 클래스 인스턴스를 내부에 가짐
# class Webtoon
#       attrs:
#           webtoon_id
#           title
#           author
#           description
#           episode_list
#       methods:
#           update: 웹에서 가져온 데이터를 사용해 Episode인스턴스들을 생성, 자신의 episode_list에 추가
#
#
# >>> yumi = Webtoon(651673)
# >>> yumi.title
# 유미와 세포들

# >>> yumi.author
# 이동건

# >>> yumi.update() <- update() 호출 안하고 yumi.episode_list에도 접근할 수 있도록 한다면?
# >>> for episode in yumi.episode_list:
# >>>    print(episode.title)
# 306화 ...
# 305화 ...

# 숙제 1. extra1) 에피소드 이미지 클래스 추가
# class EpisodeImage (각 에피소드가 가진 이미지들 중 하나를 나타냄)
#       attrs:
#           episode
#           url
#
# Episode클래스에 image_list 속성 추가
#  상세페이지 크롤링 시 image_list를 EpisodeImage의 인스턴스로 채움

# 숙제 1. extra2) 웹툰 검색하기
# >>> webtoon = Webtoon.search_webtoon('대학')
# 1. 대학일기
# 2. 안녕, 대학생
#  선택: 1
# webtoon에 해당 웹툰의 id를 기반으로 생성자 실행 결과 (인스턴스) 할당

# 숙제 1. extra3) 에피소드의 이미지 다운로드 및 HTML생성 (매우오래걸림)
# >>> episode = Webtoon.episode_list[0]
# >>> episode.download()
# 특정 폴더에 해당 웹툰의 이미지들 다운로드하고 해당 이미지에 src속성을 가진 img태그들 목록을 갖는 HTML을 생성


# 숙제 2. DjangoGirls Tutorial 읽고 오기
#  https://tutorial.djangogirls.org/ko/

# extra1) 해보기
#  설치하기
#  Python설치하기
#  코드에디터
#  pythonanywhere배포
#   부분은 제외
#  django설치시 버전 특정화 해서 설치 (최신버전 안됨)
