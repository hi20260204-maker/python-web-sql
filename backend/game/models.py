from django.db import models
from django.contrib.auth.models import User

class GameHistory(models.Model):
    # 선택지 상수 정의
    CHOICES = [
        ('R', 'Rock'),
        ('P', 'Paper'),
        ('S', 'Scissors'),
    ]
    
    # 결과 상수 정의
    RESULTS = [
        ('W', 'Win'),
        ('L', 'Loss'),
        ('D', 'Draw'),
    ]

    player = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='games')
    player_choice = models.CharField(max_length=1, choices=CHOICES)
    cpu_choice = models.CharField(max_length=1, choices=CHOICES)
    result = models.CharField(max_length=1, choices=RESULTS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Game Histories"
        ordering = ['-created_at']

    def __str__(self):
        player_name = self.player.username if self.player else "Guest"
        return f"{player_name}: {self.player_choice} vs {self.cpu_choice} ({self.get_result_display()})"
