import re

file_name = 'weekday.html'
# file_name에 해당하는 파일을 불러와서 html변수에 할당
with open(file_name, 'rt') as f:
    html = f.read()

# <a...class="title"...>[내용]</a>
# [내용] 에 해당하는 부분을 추출하는 정규표현식을 작성해서
# 실행한 결과 -> '유미의 세포들'이라고 나올 수 있도록
# 정규표현식 패턴 (a태그이며, class="title"이 여는 태그에 포함되어있을 경우, 해당 a태그의 내용부분을 그룹화)
p = re.compile(r'''<a                       # <a로 시작하며
                   .*?class="title".*?>     # 중간에 class="title"문자열이 존재하며
                                            #  >가 등장하기 전까지의 임의의 문자 최소 반복, >까지
                   (.*?)                    # 임의의 문자 반복을 그룹화 (findall또는 finditer의 match object에서 사용)
                   </a>                     #   </a>가 나오기 전까지''', re.VERBOSE)
result = re.findall(p, html)
print(result)