import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title('이차함수 시각화 & 설명')
st.write('이 페이지에서는 이차함수 y = ax² + bx + c를 이해하고 시각화할 수 있습니다.')

st.sidebar.header('이차함수 계수 입력')
a = st.sidebar.number_input('a', value=1.0, format='%.3f')
b = st.sidebar.number_input('b', value=0.0, format='%.3f')
c = st.sidebar.number_input('c', value=0.0, format='%.3f')

st.write(f'함수: $y = {a}x^2 + {b}x + {c}$')

# 그래프 범위 설정
x_min, x_max = st.sidebar.slider('x 범위', -20.0, 20.0, (-10.0, 10.0), step=1.0)
num_points = st.sidebar.slider('포인트 수', 50, 500, 200)

x = np.linspace(x_min, x_max, num_points)
y = a * x ** 2 + b * x + c

# 꼭짓점
x_v = -b / (2 * a) if a != 0 else None
y_v = a * x_v ** 2 + b * x_v + c if a != 0 else None

# 판별식 및 성격
discriminant = b ** 2 - 4 * a * c
if a > 0:
    orientation = '위로 열린 포물선 (계수 a > 0)'
elif a < 0:
    orientation = '아래로 열린 포물선 (계수 a < 0)'
else:
    orientation = '직선 (a = 0)'

roots = []
if a != 0:
    if discriminant > 0:
        roots = [(-b + np.sqrt(discriminant)) / (2 * a), (-b - np.sqrt(discriminant)) / (2 * a)]
    elif discriminant == 0:
        roots = [(-b) / (2 * a)]
    else:
        roots = []

st.subheader('함수 성질')
st.write(f'- 판별식: $D = {discriminant:.3f}$')
st.write(f'- {orientation}')
if x_v is not None:
    st.write(f'- 꼭짓점: ({x_v:.3f}, {y_v:.3f})')
if roots:
    st.write(f'- 근: {", ".join([f"{root:.3f}" for root in roots])}')
else:
    st.write('- 실근 없음')

# 그래프
fig = px.line(pd.DataFrame({'x': x, 'y': y}), x='x', y='y', title='이차함수 그래프', labels={'x': 'x', 'y': 'y'})
if x_v is not None:
    fig.add_scatter(x=[x_v], y=[y_v], mode='markers', name='꼭짓점', marker=dict(size=10, color='red'))
if roots:
    fig.add_scatter(x=roots, y=[0] * len(roots), mode='markers', name='근', marker=dict(size=8, color='green'))

st.plotly_chart(fig, use_container_width=True)

st.subheader('설명')
st.markdown('''
- 이차함수는 포물선을 그립니다.
- 계수 a는 포물선의 열림 방향과 폭을 결정합니다.
- b와 c는 위치를 이동시킵니다.
- 판별식 D = b² - 4ac로 실근 존재 여부를 판단합니다.
''')
