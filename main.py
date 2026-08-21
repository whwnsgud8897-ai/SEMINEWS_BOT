import requests
from bs4 import BeautifulSoup

# 텔레그램 봇 및 사용자 정보
TOKEN = '8945059238:AAGafm3xLL529wadKtgTEn4TX4BbwwCBBq0'
CHAT_ID = '6660298619'

# 구글 검색 연산자를 활용해 검색어 범위를 세정 장비까지 확장
keyword = '반도체 (CMP OR 세정) 장비'
url = f'https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'xml')

# 뉴스 아이템 추출하기
items = soup.find_all('item')

message = '오늘의 반도체(CMP 및 세정) 핵심 동향\n\n'

if not items:
    message += '조건에 맞는 최신 기사가 없습니다.'
else:
    for i, item in enumerate(items[:3]):
        title = item.find('title').text
        link = item.find('link').text
        message += f'{i+1}. {title}\n바로가기: {link}\n\n'

# 텔레그램 서버로 전송
tg_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
requests.post(tg_url, data={'chat_id': CHAT_ID, 'text': message})
print('전송 성공!')
