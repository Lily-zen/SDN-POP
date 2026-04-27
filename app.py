import streamlit as st
import pandas as pd

st.set_page_config(page_title="SDN POP 查询工具", page_icon="🌐")

# 访问密码
PASSWORD = "pop_query_2024" 

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True
    st.title("🔐 访问受限")
    pwd = st.text_input("请输入访问密码：", type="password")
    if st.button("登录"):
        if pwd == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("密码错误！")
    return False

if check_password():
    st.title("🌐 SDN POP 点服务查询系统")
    @st.cache_data
    def load_data():
        # 这里强制匹配文件名 data.xlsx
        try:
            return pd.read_excel('data.xlsx')
        except Exception as e:
            st.error(f"加载文件失败，请检查文件名是否为 data.xlsx。错误信息: {e}")
            return pd.DataFrame()

    df = load_data()
    if not df.empty:
        query = st.text_input("🔍 输入城市、机房名或地址关键词：")
        if query:
            mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
            st.dataframe(df[mask], use_container_width=True)
        else:
            st.write("目前所有可用 POP 点：")
            st.dataframe(df, use_container_width=True)