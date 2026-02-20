import streamlit as st

def go_to_user():
    st.link_button(
        url = "pages/user_page.py",
        label = "사용자 페이지"
    )

def go_to_start():
    if st.button("시작 페이지"):
        st.switch_page("pages/start_page.py")
    '''st.page_link(
        page ="pages/start_page.py",
        label = "시작 페이지"
    )'''

def go_to_game():
    st.link_button(
        url ="pages/game_page.py",
        label = "게임 페이지"
    )

def go_to_ranking():
    st.link_button(
        url ="pages/ranking_page.py",
        label = "랭킹 페이지"
    )