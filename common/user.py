import streamlit as st

class start:

    def __init__(self, p_name):
        self.name = p_name
        self.win_sc = 0
        self.loose_sc = 0
        self.drqw_sc = 0
    
    def set_player(self):
        # DB에 연결해서 사용자의 이름과 정보를 DB로 저장해서 보내기
        # ID는 중복인 경우 못 오게 만들어야 함

    def get_player(self):
        # DB에서 플레이어 가져오기
