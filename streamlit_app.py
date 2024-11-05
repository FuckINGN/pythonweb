import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time
# 设置 Flask API 的 URL
API_URL = 'http://localhost:5000/api'

# 页面设置
st.title("全球天气数据仪表板")
st.sidebar.title("导航")
page = st.sidebar.selectbox("选择页面", ["数据仪表板", "实时数据更新"])

# 页面 1: 数据仪表板
if page == "数据仪表板":
    st.header("清洁的全球天气数据")
    country = st.sidebar.text_input("按国家过滤")  # 输入国家名称
    location_name = st.sidebar.text_input("按地点过滤")  # 输入地点名称

    # 请求清洁数据
    params = {"country": country, "location_name": location_name}
    response = requests.get(f"{API_URL}/weather_data", params=params)
    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        if not data.empty:
            st.write(data)

            # 绘制图表
            fig = px.scatter(data, x='temperature_celsius', y='humidity', color='country', title="温度 vs 湿度")
            st.plotly_chart(fig)
        else:
            st.write("未找到匹配的数据，请检查国家或地点名称。")
    else:
        st.write("请求数据失败，请检查 API 是否运行。")

# 页面 2: 实时数据更新
elif page == "实时数据更新":
    st.header("实时天气更新")
    placeholder = st.empty()

    # 实时数据流
    while True:
        response = requests.get(f"{API_URL}/live_weather")
        if response.status_code == 200:
            live_data = pd.DataFrame(response.json())
            placeholder.write(live_data)

            # 实时折线图
            if not live_data.empty:
                fig = px.line(live_data, x=live_data.index, y="temperature_celsius", title="实时温度变化")
                st.plotly_chart(fig)

        time.sleep(5)  # 每5秒更新一次
