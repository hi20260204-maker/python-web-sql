#써드파티 라이브러리
import streamlit as st 

#개인 라이브러리
from common.go_to_pages import go_to_start


if __name__=="__main__":

    st.title("하나빼기 게임")
    
    go_to_start()