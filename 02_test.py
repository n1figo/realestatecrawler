import requests
import pandas as pd
import streamlit as st

def get_mwul_numbers(api_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # HTTPError 발생 시 예외 처리
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return []

    if response.status_code == 200:
        try:
            data = response.json()
            articles = data.get('body', [])
            return articles
        except ValueError as e:
            st.error(f"Failed to parse JSON: {e}")
            st.error(f"Response content: {response.content}")
            return []
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        st.error(f"Response content: {response.content}")
        return []

def save_to_csv_and_visualize(articles):
    if articles:
        df = pd.DataFrame(articles)
        
        # 모든 매물 정보 DataFrame 표시
        st.write("### 매물 정보")
        st.dataframe(df.style.set_properties(**{'text-align': 'left'}).set_table_styles({
            'all': [
                {
                    'selector': 'th',
                    'props': 'text-align: left;'
                }
            ]
        }))

        # CSV 다운로드 링크 생성
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="Download articles.csv",
            data=csv,
            file_name='articles.csv',
            mime='text/csv'
        )
    else:
        st.warning("No articles to save.")

def main():
    st.title("네이버 부동산 매물 정보 추출기")

    # URL 입력란
    api_url = st.text_input("API URL을 입력하세요:", "")
    
    if st.button("데이터 가져오기"):
        if api_url:
            articles = get_mwul_numbers(api_url)
            if articles:
                st.success("매물번호 추출 성공!")
                save_to_csv_and_visualize(articles)
            else:
                st.error("매물번호 추출 실패.")
        else:
            st.warning("URL을 입력하세요.")

if __name__ == "__main__":
    main()
