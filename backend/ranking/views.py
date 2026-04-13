from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from game.models import GameHistory
from django.contrib.auth.models import User

def index(request):
    # 1. 7일 전 날짜 계산
    seven_days_ago = timezone.now() - timedelta(days=7)

    # 2. 최근 7일간 승리('W') 횟수를 기준으로 유저 집계
    # 비로그인 유저(player__isnull=True)는 제외
    rankings = User.objects.filter(
        games__result='W',
        games__created_at__gte=seven_days_ago
    ).annotate(
        win_count=Count('games', filter=Q(games__result='W'))
    ).order_by('-win_count', 'id')[:100] # 상위 100명

    context = {
        'rankings': rankings,
        'days': 7
    }
    return render(request, 'ranking.html', context)