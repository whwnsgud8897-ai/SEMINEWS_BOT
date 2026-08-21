import requests
from bs4 import BeautifulSoup
import urllib.parse

# 텔레그램 봇 및 사용자 정보
TOKEN = '8945059238:AAGafm3xLL529wadKtgTEn4TX4BbwwCBBq0'
CHAT_ID = '6660298619'

# 4가지 주제와 각각의 검색어 (노조, 주식 제외 / 신기술, 장비 포함 / 최근 1일)
queries = {
    '삼성전자': '삼성전자 (신기술 OR 신장비 OR 양산 OR 개발) -노조 -주식 -주가 -증권 -파업 when:1d',
    'SK하이닉스': 'SK하이닉스 (신기술 OR 신장비 OR 양산 OR 개발) -노조 -주식 -주가 -증권 -파업 when:1d',
    'CMP장비': '반도체 CMP (신기술 OR 신장비 OR 양산 OR 개발) -노조 -주식 -주가 -증권 -파업 when:1d',
    '세정장비': '반도체 세정 장비 (신기술 OR 신장비 OR 양산 OR 개발) -노조 -주식 -주가 -증권 -파업 when:1d'
}

message = '오늘의 핵심 동향\n\n'
article_found = False

for topic, query in queries.items():
    # 복잡한 검색어를 구글 주소 규칙에 맞게 변환
    encoded_query = urllib.parse.quote(query)
    url = f'https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    items = soup.find_all('item')
    
    if items:
        # 해당 주제의 가장 최신 기사 1개만 추출
        title = items[0].find('title').text
        link = items[0].find('link').text
        message += f'[{topic}]\n제목: {title}\n링크: {link}\n\n'
        article_found = True

if not article_found:
    message += '조건에 맞는 어제자 기사가 없습니다.'

# 텔레그램 서버로 전송
tg_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
requests.post(tg_url, data={'chat_id': CHAT_ID, 'text': message})
print('전송 성공 완료')
