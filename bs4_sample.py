# 1. HTML 받아와서 html 변수에 문자열을 할당
# 1-1. 만약 'data/episode_list.html'이 없다면
# https://comic.naver.com/webtoon/list.nhn?titleId=703845
# 죽음에 관하여 (재) 페이지를
# requests를 사용해서
# data/episode_list.html에 저장
# list.nhn뒤 ?부터는 url에 넣지 말고 GET parametrs 로
# 저장 후에는 파일을 불러와 html변수에 할당
#
# 1-2. 이미 'data/episode_list.html'이 있다면
# html변수에 파일을 불러와 할당

# 2. 제목, 저자, 웹툰정보 탐색하기
# html변수를 사용해 soup변수에 BeautifulSoup객체를 생성
# soup객체에서
# - 제목: 죽음에 관하여 (재)
# - 작가: 시니/혀노
# - 설명: 삶과 죽음의 경계선, 그 곳엔 누가 있을까.
# 의 내용을 가져와 title, author, description변수에 할당



import requests
import os

html = open('data/weekday.html', 'xt')

if os.path.exists:
