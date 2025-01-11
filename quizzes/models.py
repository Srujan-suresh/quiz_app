from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField(null=True, blank=True)  # Add start time
    duration = models.IntegerField(default=300)  # Duration in seconds (e.g., 5 minutes = 300)
    max_attempts = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_text = models.TextField()  # Ensure this is a valid field for storing the question text
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    score = models.IntegerField(default=1)  # This field determines how many points the question is worth
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        default='A'  # This is the correct answer choice (A, B, C, D)
    )

    def __str__(self):
        return self.question_text


class Leaderboard(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="leaderboard", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)  # Ensure score defaults to 0 if not provided
    attempts = models.PositiveIntegerField(default=0)  # Keeps track of how many times the user attempted the quiz
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('quiz', 'user')  # Ensures each user can have only one leaderboard entry per quiz
        ordering = ['-score', 'completed_at']  # Orders by score in descending order, then by completion date

    def __str__(self):
        return f'{self.user.username} - {self.quiz.name} - Score: {self.score}'
