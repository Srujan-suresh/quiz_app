from django.contrib import admin
from .models import Quiz, Question, Leaderboard

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'duration', 'max_attempts', 'created_at']
    inlines = [QuestionInline]

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'user', 'score', 'attempts', 'completed_at']
    list_filter = ['quiz']


