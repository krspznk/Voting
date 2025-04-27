from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Реєстрація нового експерта
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('voting')
    else:
        form = CustomUserCreationForm()
    return render(request, 'poll/register.html', {'form': form})

# Вхід у систему
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('voting')
    else:
        form = AuthenticationForm()
    return render(request, 'poll/login.html', {'form': form})

# Вихід із системи
def logout_view(request):
    logout(request)
    return redirect('login')


from .models import Flower, Vote

@login_required(login_url='login')
def voting_view(request):
    flowers = Flower.objects.all()

    try:
        existing_vote = Vote.objects.get(user=request.user)
    except Vote.DoesNotExist:
        existing_vote = None

    if request.method == 'POST':
        first_id = request.POST.get('first')
        second_id = request.POST.get('second')
        third_id = request.POST.get('third')

        if len({first_id, second_id, third_id}) < 3:
            # Повертаємо помилку на ту ж сторінку
            flowers = Flower.objects.all()
            error_message = "Будь ласка, оберіть різні квіти для кожного місця."
            return render(request, 'poll/voting.html',
                          {'flowers': flowers, 'existing_vote': existing_vote, 'error_message': error_message})

        first = Flower.objects.get(id=first_id)
        second = Flower.objects.get(id=second_id)
        third = Flower.objects.get(id=third_id)

        if existing_vote:
            existing_vote.first_place = first
            existing_vote.second_place = second
            existing_vote.third_place = third
            existing_vote.save()
        else:
            Vote.objects.create(user=request.user, first_place=first, second_place=second, third_place=third)
        print("done")
        return redirect('vote_success')

    return render(request, 'poll/voting.html', {'flowers': flowers, 'existing_vote': existing_vote})


from django.db.models import Count

from django.db.models import Count, F, ExpressionWrapper, IntegerField

from django.db.models import Count

@login_required(login_url='login')
def vote_success_view(request):
    # Отримуємо всі квіти
    flowers = Flower.objects.all()

    # Статистика для кожного місця
    first_place_stats = Flower.objects.annotate(first_place_count=Count('first_place_votes')).order_by('-first_place_count')
    second_place_stats = Flower.objects.annotate(second_place_count=Count('second_place_votes')).order_by('-second_place_count')
    third_place_stats = Flower.objects.annotate(third_place_count=Count('third_place_votes')).order_by('-third_place_count')

    # Обчислюємо загальний бал для кожної квітки з урахуванням коефіцієнтів
    flower_scores = []
    for flower in flowers:
        # Підраховуємо кількість балів з урахуванням коефіцієнтів
        first_place_points = flower.first_place_votes.count() * 3
        second_place_points = flower.second_place_votes.count() * 2
        third_place_points = flower.third_place_votes.count() * 1
        total_points = first_place_points + second_place_points + third_place_points

        flower_scores.append({
            'flower': flower,
            'first_place_votes': flower.first_place_votes.count(),
            'second_place_votes': flower.second_place_votes.count(),
            'third_place_votes': flower.third_place_votes.count(),
            'total_points': total_points
        })

    # Сортуємо квітки за загальним балом
    flower_scores.sort(key=lambda x: x['total_points'], reverse=True)

    return render(request, 'poll/vote_success.html', {'flower_scores': flower_scores})


from django.shortcuts import render, redirect
from .models import HeuristicVote  # Модель для збереження голосів (створимо нижче)

def voting_heuristics(request):
    if request.method == 'POST':
        selected_heuristics = request.POST.getlist('heuristics')
        if 1 <= len(selected_heuristics) <= 3:
            HeuristicVote.objects.create(
                user=request.user,
                selected_heuristics=selected_heuristics
            )
            return redirect('vote_heuristics_success')
        else:
            error_message = "Будь ласка, виберіть від 1 до 3 евристик."
            return render(request, 'poll/voting_heuristics.html', {'error_message': error_message})
    return render(request, 'poll/voting_heuristics.html')


def vote_heuristics_success(request):
    votes = HeuristicVote.objects.all()
    heuristic_counts = {}

    for vote in votes:
        for heuristic in vote.selected_heuristics:
            if heuristic not in heuristic_counts:
                heuristic_counts[heuristic] = 1
            else:
                heuristic_counts[heuristic] += 1

    heuristic_counts = dict(sorted(heuristic_counts.items(), key=lambda item: item[1], reverse=True))

    return render(request, 'poll/vote_heuristics_success.html', {'heuristic_counts': heuristic_counts})
