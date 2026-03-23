import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('그래프 생성 페이지')
st.write('사용자 데이터를 입력해 다양한 그래프를 즉시 확인하세요.')

# 데이터 입력
mode = st.radio('입력 방식', ['샘플 데이터 생성', 'CSV 업로드', '텍스트 입력'])

data = None
if mode == '샘플 데이터 생성':
    n = st.number_input('데이터 포인트 수', min_value=10, max_value=1000, value=50)
    np.random.seed(0)
    data = pd.DataFrame({
        'x': np.arange(1, n+1),
        'y': np.random.randn(n).cumsum(),
        'group': np.random.choice(['G1', 'G2', 'G3'], size=n)
    })

elif mode == 'CSV 업로드':
    f = st.file_uploader('CSV 파일 업로드', type=['csv'])
    if f is not None:
        data = pd.read_csv(f)

else:
    raw = st.text_area('CSV 텍스트 입력', 'x,y,group\n1,10,G1\n2,15,G2\n3,12,G1')
    if st.button('파싱 실행'):
        from io import StringIO
        try:
            data = pd.read_csv(StringIO(raw))
            st.success('CSV 파싱 성공')
        except Exception as e:
            st.error(f'파싱 오류: {e}')

if data is None:
    st.info('데이터를 입력하거나 샘플 데이터를 생성해주세요.')
    st.stop()

st.subheader('데이터 미리보기')
st.dataframe(data.head())

numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
all_cols = data.columns.tolist()

if not numeric_cols:
    st.error('숫자 컬럼이 필요합니다. 숫자형 데이터를 포함하도록 CSV를 준비해주세요.')
    st.stop()

chart = st.selectbox('그래프 유형', ['선 그래프', '막대 그래프', '산점도', '히스토그램'])

if chart == '선 그래프':
    x_col = st.selectbox('X 컬럼', all_cols, index=0)
    y_col = st.selectbox('Y 컬럼', numeric_cols, index=0)
    fig = px.line(data, x=x_col, y=y_col, title='선 그래프')
    st.plotly_chart(fig, use_container_width=True)

elif chart == '막대 그래프':
    x_col = st.selectbox('X 컬럼', all_cols, index=0)
    y_col = st.selectbox('Y 컬럼', numeric_cols, index=0)
    fig = px.bar(data, x=x_col, y=y_col, title='막대 그래프')
    st.plotly_chart(fig, use_container_width=True)

elif chart == '산점도':
    x_col = st.selectbox('X 컬럼', numeric_cols, index=0)
    y_col = st.selectbox('Y 컬럼', numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
    color_col = st.selectbox('색상 컬럼(선택)', [None] + all_cols)
    fig = px.scatter(data, x=x_col, y=y_col, color=color_col if color_col else None, title='산점도')
    st.plotly_chart(fig, use_container_width=True)

else:
    col = st.selectbox('히스토그램 컬럼', numeric_cols)
    bins = st.slider('빈 수', 5, 100, 20)
    fig = px.histogram(data, x=col, nbins=bins, title='히스토그램')
    st.plotly_chart(fig, use_container_width=True)

st.markdown('---')
st.write('데이터를 변경하고 즉시 시각화 결과를 확인할 수 있습니다.')
