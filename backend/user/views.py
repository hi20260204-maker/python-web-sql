from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from game.models import GameHistory

@login_required
def index(request):
    # 프로필이 없을 경우 자동으로 생성 (안전장치)
    from .models import Profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # 최근 10개의 게임 기록 가져오기
    recent_games = GameHistory.objects.filter(player=request.user)[:10]
    
    context = {
        'profile': profile,
        'recent_games': recent_games
    }
    return render(request, 'user.html', context)
