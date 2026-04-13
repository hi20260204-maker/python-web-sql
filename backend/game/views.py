from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GameHistory
from user.models import Profile
import random

def home(request):
    """메인 랜딩 페이지"""
    return render(request, 'index.html')

def index(request):
    if request.method == 'POST':
        # 1. 사용자의 선택 가져오기
        player_choice = request.POST.get('choice') # 'R', 'P', 'S'
        
        if player_choice not in ['R', 'P', 'S']:
            return redirect('game-index')

        # 2. 컴퓨터의 무작위 선택
        cpu_choice = random.choice(['R', 'P', 'S'])
        
        # 3. 승패 판정 로직
        # W: Win, L: Loss, D: Draw
        if player_choice == cpu_choice:
            result = 'D'
        elif (player_choice == 'R' and cpu_choice == 'S') or \
             (player_choice == 'S' and cpu_choice == 'P') or \
             (player_choice == 'P' and cpu_choice == 'R'):
            result = 'W'
        else:
            result = 'L'

        # 4. 게임 결과 저장 (GameHistory)
        history = GameHistory.objects.create(
            player=request.user if request.user.is_authenticated else None,
            player_choice=player_choice,
            cpu_choice=cpu_choice,
            result=result
        )

        # 5. 유저 프로필 통계 업데이트 (로그인 시)
        if request.user.is_authenticated:
            # 프로필이 없을 경우 자동으로 생성
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            profile.total_games += 1
            if result == 'W':
                profile.total_wins += 1
                profile.streak += 1
            elif result == 'L':
                profile.streak = 0 # 연승 초기화
            # Draw(무승부)일 때는 streak 유지 또는 정책에 따라 변경 가능
            profile.save()

        context = {
            'player_choice': player_choice,
            'cpu_choice': cpu_choice,
            'result': result,
            'history': history,
            'name': 'django'
        }
        return render(request, 'game.html', context)

    # GET 요청 시 초기 화면
    return render(request, 'game.html', {'name': 'django'})
