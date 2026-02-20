from common.game_rules import GameRule
import random as r
import streamlit as st

class Game:

    def __init__(self):
        #랜덤으로 컴퓨터 가위바위보 3개요소중 2개가 골라짐
        self.com_choice = [r.choice(list(GameRule)),r.choice(list(GameRule))]
        self.com_last_choice = r.choice(self.com_choice)
        #본인이 선택한 가위바위보 >> Streamlit에서 받아와야함
        self.self_choice = [1,2]
        #게임 총 수
        self.game_count = 0


    #컴퓨터와 나의 선택을 

    #게임의 결과를 알려주는 마지막
    def do_game(self):
        
        
        game = GameRule
        result = game.game_ruel(3, self.com_last_choice.value)
        print(result)

    # DB game_history/game_history의 총 갯수승률을 계산하는
    def cal_winper(self):
        return 
    
    #DB에 본인의 게임 전적을 저장+게임토탈 카운트 저장