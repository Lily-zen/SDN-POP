import streamlit as st
import pandas as pd

st.set_page_config(page_title="SDN POP 查询工具", page_icon="🌐")

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
        # 自动尝试多种方式读取，防止文件名和格式对不上
        try:
            return pd.read_excel('机房清单.xlsx')
        except:
            return pd.read_csv('机房清单.xlsx')

    df = load_data()
    # 自动识别列名，防止大小写或空格问题
    df.columns = [str(c).strip() for c in df.columns]
    
    query = st.text_input("🔍 输入城市、机房名或地址关键词：")
    if query:
        # 这里会搜索所有列，只要包含关键词就显示
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("目前所有可用 POP 点：")
        st.dataframe(df, use_container_width=True)