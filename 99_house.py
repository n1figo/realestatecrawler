import pandas as pd
import os

path_filename = '/workspaces/realestatecrawler/서울시 아파트_2024-09-18.xlsx'

# 서울시 아파트_2024-09-18.xlsx 파일을 읽어옵니다.
excel_file = pd.ExcelFile(path_filename)

# 첫 번째 시트를 데이터프레임으로 변환합니다.
df1 = excel_file.parse(excel_file.sheet_names[0])

# 두 번째 시트를 데이터프레임으로 변환합니다.
df2 = excel_file.parse(excel_file.sheet_names[1])

# '매매가/보증금(원)' 열을 float 형태로 변환합니다.
df1['매매가/보증금(원)'] = df1['매매가/보증금(원)'].astype(float)

# 첫 번째 시트에서 매매금액이 15억 이하인 아파트 매물리스트를 출력합니다.
result = df1[df1['매매가/보증금(원)'] <= 1500000000].head()
print(result)