import requests
from bs4 import BeautifulSoup
import pandas as pd

# 웹페이지 URL (실제 URL로 변경해야 합니다)
url = "https://new.land.naver.com/houses?ms=37.5342137,127.0625872,16&a=VL:DDDGG:JWJT:SGJT:HOJT&b=A1&e=RETAIL"

# 웹페이지 내용 가져오기
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 매물 정보를 저장할 리스트
properties = []

# 각 매물 정보 추출
for item in soup.find_all('div', class_='item'):
    property_info = {}
    
    property_info['매물 유형'] = item.find('div', class_='item_title').text.strip()
    property_info['거래 방식'] = item.find('span', class_='type').text
    property_info['가격'] = item.find('span', class_='price').text
    
    info_area = item.find('div', class_='info_area')
    specs = info_area.find_all('span', class_='spec')
    property_info['면적'] = specs[0].text if len(specs) > 0 else ''
    property_info['층수'] = specs[1].text if len(specs) > 1 else ''
    property_info['방향'] = specs[2].text if len(specs) > 2 else ''
    
    property_info['특징'] = info_area.find('span', class_='spec').text if info_area.find('span', class_='spec') else ''
    
    tags = item.find('div', class_='tag_area')
    property_info['태그'] = ', '.join([tag.text for tag in tags.find_all('span', class_='tag')]) if tags else ''
    
    property_info['확인 날짜'] = item.find('span', class_='label--confirm').text.replace('확인', '').strip() if item.find('span', class_='label--confirm') else ''
    
    cp_area = item.find('div', class_='cp_area_inner')
    property_info['중개사'] = cp_area.find_all('span', class_='agent_name')[1].text if len(cp_area.find_all('span', class_='agent_name')) > 1 else ''
    
    properties.append(property_info)

# DataFrame 생성 및 Excel 파일로 저장
df = pd.DataFrame(properties)
df.to_excel('naver_real_estate.xlsx', index=False)

print("데이터가 성공적으로 추출되어 'naver_real_estate.xlsx' 파일로 저장되었습니다.")
