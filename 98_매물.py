import pandas as pd
import pickle
import os

def excel_to_pickle(excel_path, pickle_path):
    excel_file = pd.ExcelFile(excel_path)
    df = excel_file.parse(excel_file.sheet_names[1])
    with open(pickle_path, 'wb') as f:
        pickle.dump(df, f)
    print(f"데이터가 {pickle_path}에 저장되었습니다.")
    return df

def load_pickle(pickle_path):
    with open(pickle_path, 'rb') as f:
        df = pickle.load(f)
    print(f"{pickle_path}에서 데이터를 로드했습니다.")
    return df

def print_column_list(df):
    print("\n컬럼 리스트:")
    for column in df.columns:
        print(column)

def analyze_data(df, column_name):
    print(f"\n'{column_name}' 컬럼 분석:")
    print(df[column_name].describe())
    print(f"\n'{column_name}' 컬럼의 처음 10개 값:")
    print(df[column_name].head(10))
    print(f"\n'{column_name}' 컬럼의 유니크한 값 (처음 10개):")
    print(df[column_name].unique()[:10])

def filter_data(df, column_name, max_value):
    # '(N/A)' 값을 NaN으로 변경
    df[column_name] = df[column_name].replace('(N/A)', pd.NA)
    
    # 콤마 제거 및 숫자로 변환
    df[column_name] = pd.to_numeric(df[column_name].str.replace(',', ''), errors='coerce')
    
    print(f"\n숫자 변환 후 '{column_name}' 컬럼 분석:")
    print(df[column_name].describe())
    print(f"\nNaN 값의 개수: {df[column_name].isna().sum()}")
    
    # NaN 값 제거
    df = df.dropna(subset=[column_name])
    
    # 필터링 (음수 값 포함)
    filtered_df = df[df[column_name] <= max_value]
    return filtered_df

def save_to_csv(df, csv_path):
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"필터링된 데이터가 {csv_path}에 저장되었습니다.")

if __name__ == "__main__":
    excel_path = '/workspaces/realestatecrawler/서울시 아파트_2024-09-18.xlsx'
    pickle_path = 'second_sheet_data.pkl'
    csv_path = 'filtered_real_estate_data.csv'
    column_name = 'min(매매) - MAX(전세)'
    max_value = 600000000
    
    try:
        df = load_pickle(pickle_path)
    except FileNotFoundError:
        df = excel_to_pickle(excel_path, pickle_path)
    
    print_column_list(df)
    print(f"\n원본 데이터 shape: {df.shape}")
    
    analyze_data(df, column_name)
    
    filtered_df = filter_data(df, column_name, max_value)
    
    print(f"\n필터링된 데이터 shape: {filtered_df.shape}")
    print(f"'{column_name}' 값이 {max_value:,} 이하인 데이터 수: {len(filtered_df)}")
    
    if not filtered_df.empty:
        print("\n필터링된 데이터의 처음 5행:")
        print(filtered_df.head())
        save_to_csv(filtered_df, csv_path)
        csv_size = os.path.getsize(csv_path) / (1024 * 1024)  # MB 단위로 변환
        print(f"\nCSV 파일 크기: {csv_size:.2f} MB")
    else:
        print("\n필터링된 데이터가 없습니다.")