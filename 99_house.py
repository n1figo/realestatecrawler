import pandas as pd
import os
import pickle

def process_data(path_filename):
    # 서울시 아파트_2024-09-18.xlsx 파일을 읽어옵니다.
    excel_file = pd.ExcelFile(path_filename)

    # 첫 번째 시트를 데이터프레임으로 변환합니다.
    df = excel_file.parse(excel_file.sheet_names[0])

    # '거래종류' 열을 모두 '매매'로 변경합니다.
    df['거래종류'] = '매매'

    # '매매가/보증금(원)' 컬럼의 인덱스를 찾습니다.
    price_column_index = df.columns.get_loc('매매가/보증금(원)')

    # '매매가/보증금(원)' 컬럼 이후의 모든 컬럼에 대해 숫자 데이터를 float으로 변환합니다.
    for column in df.columns[price_column_index:]:
        df[column] = pd.to_numeric(df[column].replace('(매물없음)', pd.NA), errors='coerce')

    # 거래종류가 '매매'이고 전용면적이 84㎡ 이상이며, 단지명에 '주상복합'이 포함되지 않은 데이터만 필터링합니다.
    df_filtered = df[(df['거래종류'] == '매매') & 
                     (df['전용면적'] >= 84) & 
                     (~df['단지명'].str.contains('주상복합', case=False, na=False))]

    # 필터링된 데이터를 전용면적 기준으로 내림차순 정렬합니다.
    df_sorted = df_filtered.sort_values('전용면적', ascending=False)

    return df_sorted

def save_to_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print(f"데이터가 {filename}에 저장되었습니다.")

def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print(f"{filename}에서 데이터를 로드했습니다.")
    return data

def save_to_csv(data, filename):
    data.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"데이터가 {filename}에 저장되었습니다.")

# 메인 실행 부분
if __name__ == "__main__":
    path_filename = '/workspaces/realestatecrawler/서울시 아파트_2024-09-18.xlsx'
    pickle_filename = 'processed_real_estate_data.pkl'
    csv_filename = 'real_estate_under_15billion_no_residential_complex.csv'

    # 사용자 입력을 받아 피클 파일 사용 여부 결정
    use_pickle = input("피클 파일을 사용하시겠습니까? (y/n): ").lower() == 'y'

    if use_pickle and os.path.exists(pickle_filename):
        df_sorted = load_from_pickle(pickle_filename)
    else:
        df_sorted = process_data(path_filename)
        save_to_pickle(df_sorted, pickle_filename)

    # 결과 출력
    print("\n정렬된 데이터의 처음 5개 행:")
    print(df_sorted.head())

    print(f"\n총 데이터 수: {len(df_sorted)}")
    
    # 15억 이하 매물 필터링
    df_under_15billion = df_sorted[df_sorted['매매가/보증금(원)'] <= 1500000000]
    print(f"15억 이하 매물 수: {len(df_under_15billion)}")

    # 15억 이하 매물 데이터를 CSV 파일로 저장
    save_to_csv(df_under_15billion, csv_filename)

    # 데이터 타입 확인
    print("\n데이터 타입:")
    print(df_sorted.dtypes)

    # 단지명 유니크 값 확인 (처음 20개만)
    print("\n단지명 유니크 값 (처음 20개):")
    print(df_sorted['단지명'].unique()[:20])