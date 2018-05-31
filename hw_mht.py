import os

import requests
from bs4 import BeautifulSoup
#os는 내장모듈, requests는 서드파티모듈
# 내장모듈과 서드파티모듈은 한칸 띄어서 구분을 해둠

file_path = 'data2/test_list.html'
# 저장할 경로 생성
url_episode_list = 'https://comic.naver.com/webtoon/list.nhn'
# requests 로 불러오는 (변수명 생성 = 가져오는 웹 주소)
params = {
    'titleId':703845,
}

# 실수1. params { } 라고 선언, params 변수에 titleId 를 심어주는 것이기 때문에 변수화 시켜야 함
# 파라미터는 dic 값을 가진다. key 만 따로 변수로 할당하려고 하는건가..? 정확한 의도는 모르겠다.
# 맨 처음에는 '유미의 세포들'을 requests.get 하고(파일까지 생성)
# 나중에 '죽음에 관하여'로 id값을 바꿨는데도 불구하고 '유미의 세포들'이 나왔음. 최초 생성 기준인듯
#특이한 점은 파라미터를 만들 때 titleId 에 따옴표를 달아주고 숫자는 그대로 출력(딕셔너리로 숫자만 key값으로 다른 회차들도 쭉 출력하려는 듯)
#title다음부터는 각 웹툰의 숫자 고유 주소를 가지게 됨

if os.path.exists(file_path):
    html = open(file_path, 'rt').read()
else:
    response = requests.get(url_episode_list, params)

    html = response.text
    open(file_path, 'wt').write(html)
        #여기까지가 읽고 없으면 URL 주소를 통해서 저장하고 가져온다(폴더 생성)


soup = BeautifulSoup(html, 'lxml')
#
#대소문자 한글자도 틀리면 안됨 #lxml은 해석기

h2_title = soup.select_one('div.detail > h2')
# 개발자 선택도구로 div.detail를 선택, (detail? -> class 명) 의 하위요소 h2 를 하나 선택해라
# 개발자 선택도구로 찾아보고 그 다음 해당 페이지의 html 문서로 확인하 것도 괜찮은듯(화면이 커서 보기 편함)
# 찾아보고 프린트해보고, 반복 작업을 해서 원하는 값을 찾아라.

title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
description = soup.select_one('div.detail > p').get_text(strip=True)


table = soup.select_one('table.viewList')
tr_list = table.select('tr')
for index, tr in enumerate(tr_list[1:]):
    if tr.get('class'):
        continue

    print('=========={}\n{}\n'.format(index, tr))

    from urllib import parse
    url_detail = tr.select_one('td:nth-of-type(1) img').get('src')
    query_string = parse.urlsplit(url_detail).query
    query_dict = parse.parse_qs(query_string)
    print(query_dict)

    url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
    title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
    rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
    created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)



print(url_thumbnail)
print(title)
print(rating)
print(created_date)
print(no)
#soup.prettify()로 출력하면 html코드가 들여쓰기되어 사람이 볼 때 더 편하게 볼 수 있다.(2개 비교 출력완료)
#prettify()라는 함수를 호출한다.


# 셀렉트까지만 하고 장고 문서 읽어보고 예습하기..예습 안하면 또 따라가기 힘들듯
