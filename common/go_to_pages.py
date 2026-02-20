import streamlit as st

def go_to_user():
    if st.button("사용자 페이지"):
        st.switch_page("pages/user_page.py")

def go_to_start():
    if st.button("시작 페이지"):
        st.page_link(page ="./pages/start_page.py")

def go_to_game():
    if st.button("게임 페이지"):
        st.switch_page("pages/game_page.py")

def go_to_ranking():
    if st.button("랭킹 페이지"):
        st.switch_page("pages/ranking_page.py")