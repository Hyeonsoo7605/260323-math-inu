import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('데이터 시각화 데모')
st.write('이 페이지에서는 사용자가 데이터를 입력하고 다양한 시각화 예시를 확인할 수 있습니다.')

# 데이터 입력 옵션
st.sidebar.header('데이터 입력')
input_mode = st.sidebar.selectbox('데이터 입력 방식 선택', ['샘플 데이터', 'CSV 업로드', '텍스트(CSV 형식) 입력'])

data = None

if input_mode == '샘플 데이터':
    sample = st.sidebar.selectbox('샘플 데이터셋 선택', ['타이타닉', 'iris', '랜덤'])
    if sample == '타이타닉':
        data = px.data.titanic()
    elif sample == 'iris':
        data = px.data.iris()
    else:
        np.random.seed(42)
        data = pd.DataFrame({
            'x': np.arange(1, 51),
            'y': np.random.randn(50).cumsum(),
            'category': np.random.choice(['A', 'B', 'C'], 50),
            'value': np.random.randint(1, 100, 50)
        })

elif input_mode == 'CSV 업로드':
    uploaded_file = st.sidebar.file_uploader('CSV 파일 업로드', type=['csv'])
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            st.sidebar.error(f'CSV 로드 오류: {e}')

else:
    raw_csv = st.sidebar.text_area('CSV 텍스트 입력', 'x,y,category,value\n1,10,A,23\n2,15,A,26\n3,5,B,35\n4,20,C,17')
    if st.sidebar.button('데이터 파싱'):
        try:
            from io import StringIO
            data = pd.read_csv(StringIO(raw_csv))
            st.sidebar.success('데이터 로드 성공')
        except Exception as e:
            st.sidebar.error(f'CSV 파싱 오류: {e}')

if data is None:
    st.info('왼쪽 사이드바에서 입력 방식을 선택하고 데이터를 불러오세요.')
    st.stop()

st.subheader('데이터 미리보기')
st.dataframe(data.head())

st.subheader('기본 통계 및 정보')
with st.expander('데이터 정보'):
    st.write(data.describe(include='all'))
    st.write('행/열:', data.shape)

numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
all_columns = data.columns.tolist()

if not numeric_columns:
    st.warning('숫자형 열이 없습니다. 시각화는 숫자형 열이 있는 경우에만 다양하게 지원됩니다.')

chart_type = st.sidebar.selectbox('차트 유형 선택', ['선형(Line)', '막대(Bar)', '산점도(Scatter)', '히스토그램', '원형(Pie)', '박스(Box)'])

if chart_type == '선형(Line)':
    if len(numeric_columns) < 2:
        st.warning('2개 이상의 숫자형 컬럼이 필요합니다.')
    else:
        x_col = st.sidebar.selectbox('X축', numeric_columns, index=0)
        y_col = st.sidebar.selectbox('Y축', numeric_columns, index=1)
        fig = px.line(data, x=x_col, y=y_col, title=f'{y_col} vs {x_col}', markers=True)
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == '막대(Bar)':
    x_col = st.sidebar.selectbox('X축 (범주형/숫자형)', all_columns)
    y_col = st.sidebar.selectbox('Y축 (숫자형)', numeric_columns)
    fig = px.bar(data, x=x_col, y=y_col, title=f'{y_col} by {x_col}')
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == '산점도(Scatter)':
    if len(numeric_columns) < 2:
        st.warning('2개 이상의 숫자형 컬럼이 필요합니다.')
    else:
        x_col = st.sidebar.selectbox('X축', numeric_columns, index=0)
        y_col = st.sidebar.selectbox('Y축', numeric_columns, index=1)
        color_col = st.sidebar.selectbox('색상 그룹(옵션)', [None] + all_columns)
        fig = px.scatter(data, x=x_col, y=y_col, color=color_col if color_col and color_col in data.columns else None,
                         title=f'{y_col} vs {x_col}')
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == '히스토그램':
    if not numeric_columns:
        st.warning('숫자형 열이 필요합니다.')
    else:
        col = st.sidebar.selectbox('변수 선택', numeric_columns)
        bins = st.sidebar.slider('빈 수', 5, 100, 20)
        fig = px.histogram(data, x=col, nbins=bins, title=f'{col} 히스토그램')
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == '원형(Pie)':
    cat_col = st.sidebar.selectbox('범주형 변수', all_columns)
    if cat_col:
        summary = data[cat_col].value_counts().reset_index()
        summary.columns = [cat_col, 'count']
        fig = px.pie(summary, names=cat_col, values='count', title=f'{cat_col} 분포')
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == '박스(Box)':
    if not numeric_columns:
        st.warning('숫자형 열이 필요합니다.')
    else:
        col = st.sidebar.selectbox('숫자형 변수', numeric_columns)
        fig = px.box(data, y=col, title=f'{col} 분포(Box Plot)')
        st.plotly_chart(fig, use_container_width=True)

st.markdown('---')
st.write('원하는 데이터를 넣고 시각화 유형을 바꿔가며 실험해 보세요!')
