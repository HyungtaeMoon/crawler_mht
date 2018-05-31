import os
from io import BytesIO
from urllib import parse

import requests
from bs4 import BeautifulSoup

class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail,
                 title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date
# 에피소드 클래스는 웹툰 클래스에서 끌어온 데이터를 바탕으로 작업을 진행한다.
# 웹툰 클래스에서는 webtoon_id 만 제외하고 나머지 속성은 외부에서 받고 있지만 에피소드 클래스는
# 각자 자기 자신이 인스턴스 주체로 할당되기 때문에 빈 값은 가질 필요 없다....


    @property
    def url(self):
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }
        episode_url = url + parse.urlencode(params)
        return episode_url
        # url 전체를 변수로 선언 안하고 dic 형식으로 하는 것은 requests 로
        # 한 개의 값이 아니라 여러 에피소드를 받아오기 위함이다.

    def get_image_url_list(self):
        print('get_image_url_list start')


        file_path = 'data/episode_detail-{webtoon_id}-{episode_no}.html'.format(
            webtoon_id=self.webtoon_id,
            episode_no=self.no,
        )
        print('file_path:', file_path)


        if os.path.exists(file_path):
            print('os.path.exists: True')
        # os 모듈을 사용하여 조건문을 만들어줌, os 모듈은 폴더, 파일을 생성하는 모듈로
        # requests, beautifulSoup 모듈과 함께 크롤링에서 꼭 필요한 모듈로 생각한다.
        # 만약 os.path.exists(내가 지정한 경로)에 파일이 있다면 html 변수에
        # file_path 경로를 열고 읽어라..?

            html = open(file_path, 'rt').read()
        else:

            # 없다면 self.url에 requests를 사용해서 요청
            #  요청의 결과를 html변수에 할당
            #  요청의 결과를 file_path에 해당하는 파일에 기록
            print('os.path.exists: False')
            print(' http get request, url:', self.url)
            response = requests.get(self.url)
            # 만약에 그렇지 않다면 self.url에 requests 모듈을 사용하여
            # response 변수에 할당해라.
            html = response.text
            # html 변수에 이 reponse 변수를 넣고,
            # (response.text 파일이 된 것은 t 가 텍스트 타입으로 텍스트 타입의 문서를 생성?)
            open(file_path, 'wt').write(html)
            # 그래서 오픈하고 파일이 존재할 경우에 덮어쓴다.


        soup = BeautifulSoup(html, 'lxml')
        #beautifulsoup모듈로 파서(크롤링과 비슷한 개념)한다.
        #가져오는 주체는 위에 response 변수, 즉 requests.get(self.url)이다.

        # img목록을 찾는다. 위치는 "div.wt_viewer > img"
        img_list = soup.select('div.wt_viewer > img')
        # 이미지의 목록을 찾는데 beautifulsoup의 select기능을 사용하여
        # 변수에 저장한다. beautifulsoup는 대소문자 확실히 구분해서 import 해야
        # 기능이 정상저그로 작동한다.

        # 이미지 URL(src의 값)을 저장할 리스트
        # url_list = []
        # for img in img_list:
        #     url_list.append(img.get('src'))

        return [img.get('src') for img in img_list]
            #이미지를 src에서 가져와 url_list에 src속성을 추가한다.
            # 바로 위에 for 문이 return과 동일한 내용 같은데 이 컴프리헨션에서는
            # append가 없이 추가를 한다..?

    def download_all_images(self):
        for url in self.get_image_url_list():
            self.download(url)
        # self.get_img_url_list()를 호출하여 url에 넣은 후
        # ......self.download(url)??
        # for x in range(5):
        #   print() 이런 형식이 for 문이 아니라
        # self.download(url) 인스턴스가 아래에 오면 무슨 일이..?

    def download(self, url_img):
        """
        :param url_img: 실제 이미지의 URL
        :return:
        """
        # 네이버에서는 바로 전의 경로로 진입하지 않을 경우에는 막는다.
        # 예를 들면 url 703 -> 704 로 넘어가야 하는데 701 -> 704 넘어가면 막는다는 뜻
        url_referer = f'http://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}'
        headers = {
            'Referer': url_referer,
        }
        response = requests.get(url_img, headers=headers)
        #requests 모듈의 get 함수를 호출하여 response에 할당


        file_name = url_img.rsplit('/', 1)[-1]
        # http://www.naver.com/asfd/afwd/ 이런 형식을 rsplit 과 인덱싱으로 원하는 값만 가져옴
        # rsplit 은 오른쪽부터 ( )를 제외하고 출력,(보통 split, 왼쪽은 lsplit


        dir_path = f'data/{self.webtoon_id}/{self.no}'
        os.makedirs(dir_path, exist_ok=True)
        # print(dir_path) 했는데 아무런 반응이 없다.
        # os 모듈을 사용하는걸 보니 dir_path 경로로 폴더를 만드는 것으로 보인다.

        file_path = f'{dir_path}/{file_name}'
        open(file_path, 'wb').write(response.content)
        # os모듈이 사용되지 않으니 위와는 다르다. wb 모드(쓰기, 이진데이터 타입)이다.


class Webtoon:
    def __init__(self, webtoon_id):
        """
        형태: 초기화메서드를 선언할 때 self, webtoon_id만 속성에 선언한 것은
        네이버 웹툰에서 set_info()메서드가 BeautifulSoup 모듈을 이용하여
        인스턴스로 선언하기 때문에 빈 값으로 설정했다.
        """
        self.webtoon_id = webtoon_id
        self._title = None
        self._author = None
        self._description = None
        self._episode_list = list()
        self._html = ''

    def _get_info(self, attr_name):
        """
        형태: 메서드명을 더이상은 바꿀 일이 없을 때 의미상으로 언더스코어(_) 하나를 사용(protected)
        언더스코어(__) 2개를 사용하면 정말 확실한 때에만 사용한다. 보통 정해진 함수(init, repr 등에서만 사용하는듯)
        """
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)
        print(_get_info)

    """
    형태: property 를 쓰는 이유는 반복되는 동일한 메서드의 호출을 한꺼번에 묶어서 사용을 하는 방식이다.
    """
    @property
    def title(self):
        return self._get_info('_title')

    @property
    def author(self):
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')

    @property
    def html(self):
        if not self._html:

            file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
            # 파일의 경로를 지정해준다.
            url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
            #
            params = {
                'titleId': self.webtoon_id,
            }

            if os.path.exists(file_path):
                html = open(file_path, 'rt').read()
            else:
                response = requests.get(url_episode_list, params)
                print(response.url)
                html = response.text
                open(file_path, 'wt').write(html)
            self._html = html
        return self._html

    def set_info(self):
        soup = BeautifulSoup(self.html, 'lxml')
        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)
        # beautifulsoup을 이용하여 self.html에 url을 뽑아오겠다고 선언(?)
        #beautifulsoup 모듈을 사용하여 각 카테고리별로 값을 뽑아왔다.

        self._title = title
        self._author = author
        self._description = description
        #....self 인스턴스들이 왜 이곳에 있는지 모르겠다.
        # 웹툰클래스에서 이 self로 선언을 했으면 set_info 는 상위로 올라가서
        # 호출을 하면 되지 않는가..?

    def crawl_episode_list(self):
        soup = BeautifulSoup(self.html, 'lxml')

        table = soup.select_one('table.viewList')
        tr_list = table.select('tr')
        episode_list = list()
        for index, tr in enumerate(tr_list[1:]):
            if tr.get('class'):
                continue

            url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
            from urllib import parse
            url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
            query_string = parse.urlsplit(url_detail).query
            query_dict = parse.parse_qs(query_string)
            no = query_dict['no'][0]

            title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
            rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
            created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

            new_episode = Episode(
                webtoon_id=self.webtoon_id,
                no=no,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
            )
            episode_list.append(new_episode)
        self._episode_list = episode_list

    @property
    def episode_list(self):
        if not self._episode_list:
            self.crawl_episode_list()
        return self._episode_list


if __name__ == '__main__':
    webtoon1 = Webtoon(651673)
    # print(webtoon1.title)
    # print(webtoon1.author)
    # print(webtoon1.description)
    # e1 = webtoon1.episode_list[0]
    # e1.download_all_images()
    #
    print(episode_url)