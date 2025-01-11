from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Quiz, Question, Leaderboard
from .forms import UserSignupForm, QuizAnswerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

# Home page view
def home(request):
    return render(request, 'quizzes/home.html')

# User signup view
def signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserSignupForm()
    return render(request, 'quizzes/signup.html', {'form': form})

# View to show list of quizzes
@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

# View to show quiz details along with questions and options
@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Get all questions for this quiz
    quiz_duration = quiz.duration  # Duration of the quiz in seconds

    current_time = timezone.now()

    # If start_time is None, use the current time as the fallback
    start_time = quiz.start_time or current_time

    # Calculate the time left for the quiz (in seconds)
    time_left = start_time + timedelta(seconds=quiz_duration) - current_time
    time_left_seconds = max(time_left.total_seconds(), 0)  # Ensure non-negative value

    if request.method == "POST":
        total_score = 0
        for question in questions:
            # Get the user's selected answer for this question
            answer = request.POST.get(f"question_{question.id}")
            if answer and answer.upper() == question.correct_answer:  # Ensure case matches
                total_score += question.score  # Add score for correct answer

        # Ensure the score is calculated before saving to Leaderboard
        if total_score > 0:
            leaderboard_entry, created = Leaderboard.objects.get_or_create(quiz=quiz, user=request.user)
            leaderboard_entry.score = total_score  # Set the calculated score
            leaderboard_entry.save()
        else:
            leaderboard_entry, created = Leaderboard.objects.get_or_create(quiz=quiz, user=request.user)
            leaderboard_entry.score = 0  # In case no answer was correct
            leaderboard_entry.save()

        return redirect('leaderboard', quiz_id=quiz.id)  # Redirect to the leaderboard page

    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
        'quiz_duration': time_left_seconds  # Pass the remaining time in seconds
    })


# View to display leaderboard of a quiz
@login_required
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    leaderboard = quiz.leaderboard.all()
    return render(request, 'quizzes/leaderboard.html', {'quiz': quiz, 'leaderboard': leaderboard})

# Generic ListView for quizzes (optional)
class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quizzes/quiz_list.html'

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    score = 0
    total_score = 0  # To keep track of the total score for all questions

    # Loop through each question and calculate the score
    for question in questions:
        total_score += question.score  # Add the score for each question
        answer = request.POST.get(f'question_{question.id}')

        # Check if the answer matches the correct answer
        if answer == question.correct_answer:
            score += question.score

    print(f"Calculated Score: {score}")  # Debugging: print the calculated score

    # Save the leaderboard entry with the calculated score
    leaderboard_entry, created = Leaderboard.objects.get_or_create(quiz=quiz, user=request.user)
    leaderboard_entry.score = score
    leaderboard_entry.save()

    # Redirect to the results page after submitting the quiz
    return render(request, 'quizzes/results.html', {'quiz': quiz, 'score': score, 'total_score': total_score})

@login_required
def quiz_question(request, quiz_id, question_number):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = quiz.questions.all()[question_number-1]
    quiz_duration = 300  # Example quiz duration in seconds (5 minutes)
    
    return render(request, 'quizzes/quiz_question.html', {
        'quiz': quiz,
        'question': question,
        'question_number': question_number,
        'quiz_duration': quiz_duration
    })



@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Fetch user answers or calculate the score here
    score = 100  # Example: calculated score
    total_score = 100  # Example: total score of the quiz
    return render(request, 'quizzes/quiz_results.html', {'score': score, 'total_score': total_score})
