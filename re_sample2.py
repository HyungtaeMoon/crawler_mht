import re

file_name = 're_weekday_thumb.html'
# file_name에 해당하는 파일을 불러와서 html변수에 할당
with open(file_name, 'rt') as f:
    html = f.read()

p = re.compile(r'<div.*?class="thumb".*?>.*?<img.*?src="(.*?)".*?</div>', re.DOTALL)
result = re.findall(p, html)
print(result)