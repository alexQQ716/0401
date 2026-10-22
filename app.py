import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="WMS Склад Аналитика", page_icon="📦", layout="wide")
st.title(" Панель управления начальника склада")

# БОКОВАЯ ПАНЕЛЬ ФИЛЬТРОВ И УПРАВЛЕНИЯ КЭШЕМ

with st.sidebar:
    st.header("Временной фильтр")
    days = st.selectbox ("Аналитический период", index=1, format_func=lambda x: f"{x} дней")
    if st.button("🔄 Сбросить кэш данных"):
        st.cache_data.clear()
        st.sidebar.success("Кэш API очищен!")

# ФУНКЦИИ СИНХРОНИЗАЦИИ И СБОРА СТАТИСТИКИ

@st.cache_data(ttl=30)
def fetch_kpi(days):
    return requests.get(f"{API_URL}/api/analytics/kpi/", params={"days": days}).json()

@st.cache_data(ttl=30)
def fetch_turnover(days):
    data = requests.get(f"{API_URL}/api/analytics/turnover/", params={"days": days}).json()
    return pd.DataFrame(data)

@st.cache_data(ttl=30)
def fetch_high_demand():
    return pd.DataFrame(requests.get(f"{API_URL}/api/analytics/high-demand/").json())

@st.cache_data(ttl=30)
def fetch_staff_load(days):
    return pd.DataFrame(requests.get(f"{API_URL}/api/analytics/staff-load/", params={"days": days}).json())

@st.cache_data(ttl=30)
def fetch_stock_balance():
    return pd.DataFrame(requests.get(f"{API_URL}/api/analytics/stock/").json())

# ОТРИСОВКА KPI ТАБЛО
kpi_data = fetch_kpi(days)
m1, m2, m3, m4 = st.columns(4)
m1.metric(" Оборот ТМЦ (Закупки)", f"{kpi_data['turnover_amount']:,.2f} ₽")
m2.metric(" Проведено накладных", kpi_data["operations_count"])
m3.metric(" Средний чек поставки", f"{kpi_data['avg_consignment_cost']:,.2f} ₽")
m4.metric(" Активных позиций ТМЦ", kpi_data["items_in_stock"])

# ДИНАМИКА ДВИЖЕНИЯ СРЕДСТВ
st.header("📊 Хронология финансового оборота склада")
df_turnover = fetch_turnover(days)
if not df_turnover.empty:
    fig_line = px.line(df_turnover, x="date", y="total", markers=True, labels={"total": "Сумма в рублях", "date": "Дата"})
    st.plotly_chart(fig_line, use_container_width=True)

# ГРУППОВЫЕ МЕТРИКИ
c_left, c_right = st.columns(2)

with c_left:
    st.header(" Востребованные позиции (По отгрузкам)")
    df_top = fetch_high_demand()
    if not df_top.empty:
        fig_bar = px.bar(df_top, x="count", y="product", color="category", orientation="h", labels={"count": "Количество единиц", "product": "Товар"})
        st.plotly_chart(fig_bar, use_container_width=True)

with c_right:
    st.header(" Выработка сотрудников (Накладные)")
    df_workers = fetch_staff_load(days)
    if not df_workers.empty:
        fig_pie_staff = px.pie(df_workers, values="documents", names="worker", hole=0.3)
        st.plotly_chart(fig_pie_staff, use_container_width=True)

# СОСТОЯНИЕ АДРЕСНОГО ХРАНЕНИЯ НА СКЛАДЕ
st.header(" Текущий статус заполненности ячеек склада")
df_stock = fetch_stock_balance()
if not df_stock.empty:
    fig_pie_stock = px.pie(
        df_stock, values="count", names="status",
        color_discrete_map={"available": "#2ca02c", "reserved": "#ff7f0e", "out_of_stock": "#d62728"}
    )
    st.plotly_chart(fig_pie_stock, use_container_width=True)
