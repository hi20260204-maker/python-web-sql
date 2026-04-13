from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 프로필은 시그널에서 자동 생성되지만, 명시적으로 로그인 처리
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
