

from enum import Enum

class GameRule(Enum):
    
    가위 = 1
    바위 = 2
    보 = 3

    def game_ruel(ch1, ch2):
        
        if ch1 == ch2:
            return 0 #무승부
        
        elif ch1 < ch2:
    
            if ch1==GameRule.가위.value and ch2==GameRule.보.value:
                return 2 #승리
            
            return 1 #패배

        else : 
            if ch1==GameRule.보.value and ch2==GameRule.가위.value:
                return 1 #패배
                
            return 2 #승리

