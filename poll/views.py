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



@login_required(login_url='login')
def vote_results_view(request):
    # Отримуємо всі квіти
    flowers = Flower.objects.all()

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

    return render(request, 'poll/vote_results.html', {'flower_scores': flower_scores})


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
            return redirect('heuristic-application-result')
        else:
            error_message = "Будь ласка, виберіть від 1 до 3 евристик."
            return render(request, 'poll/voting_heuristics.html', {'error_message': error_message})
    return render(request, 'poll/voting_heuristics.html')

heuristic_descriptions = {
    'E1': "Видалити квітку, що отримала тільки одне 3-тє місце.",
    'E2': "Видалити квітку, що отримала тільки одне 2-ге місце.",
    'E3': "Видалити квітку, що отримала тільки одне 1-ше місце.",
    'E4': "Видалити квітку, що отримала два 3-х місця і більше нічого.",
    'E5': "Видалити квітку, що має і 2-ге і 3-тє місця, але немає 1-го.",
    'E6': "Залишити тільки квіти з сумою балів ≥ 5.",
    'E7': "Залишити тільки квіти, що мають мінімум 3 голоси сумарно."
}

def apply_heuristics(flower_scores, selected_heuristics):
    steps = []


    filtered_flowers = flower_scores.copy()

    for heuristic in selected_heuristics:
        before_flowers = filtered_flowers.copy()

        if heuristic == 'E1':
            filtered_flowers = [f for f in filtered_flowers if not (
                        f['third_place_votes'] == 1 and f['first_place_votes'] == 0 and f['second_place_votes'] == 0)]
        elif heuristic == 'E2':
            filtered_flowers = [f for f in filtered_flowers if not (
                        f['second_place_votes'] == 1 and f['first_place_votes'] == 0 and f['third_place_votes'] == 0)]
        elif heuristic == 'E3':
            filtered_flowers = [f for f in filtered_flowers if not (
                        f['first_place_votes'] == 1 and f['second_place_votes'] == 0 and f['third_place_votes'] == 0)]
        elif heuristic == 'E4':
            filtered_flowers = [f for f in filtered_flowers if not (
                        f['third_place_votes'] == 2 and f['first_place_votes'] == 0 and f['second_place_votes'] == 0)]
        elif heuristic == 'E5':
            filtered_flowers = [f for f in filtered_flowers if
                                not (f['third_place_votes'] >= 1 and f['second_place_votes'] >= 1)]
        elif heuristic == 'E6':
            filtered_flowers = [f for f in filtered_flowers if f['total_points'] >= 5]
        elif heuristic == 'E7':
            filtered_flowers = [f for f in filtered_flowers if
                                (f['first_place_votes'] + f['second_place_votes'] + f['third_place_votes']) >= 3]

        # Кого видалили
        removed_flowers = [f['flower'].name for f in before_flowers if f not in filtered_flowers]
        remaining_flowers = [f['flower'].name for f in filtered_flowers]

        steps.append({
            'heuristic': heuristic,
            'description': heuristic_descriptions.get(heuristic, ""),
            'removed': removed_flowers,
            'remaining': remaining_flowers
        })

    return steps, filtered_flowers

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Flower, HeuristicVote

@login_required(login_url='login')
def heuristic_application_result(request):
    votes = HeuristicVote.objects.all()

    # Всі можливі евристики
    all_heuristics = list(heuristic_descriptions.keys())
    heuristic_counts = {h: 0 for h in all_heuristics}

    # Підрахунок голосів за кожну евристику
    for vote in votes:
        if isinstance(vote.selected_heuristics, list):
            for h in vote.selected_heuristics:
                if h in heuristic_counts:
                    heuristic_counts[h] += 1

    # Підготовка даних про квіти
    flowers = Flower.objects.all()
    flower_scores = []
    for flower in flowers:
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

    flower_scores.sort(key=lambda x: x['total_points'], reverse=True)

    # Отримання евристик, які обрав поточний користувач
    user_vote = HeuristicVote.objects.filter(user=request.user).last()

    if user_vote and isinstance(user_vote.selected_heuristics, list):
        selected_codes = user_vote.selected_heuristics
    else:
        selected_codes = []

    # Готуємо красивий список для відображення обраних евристик
    selected_heuristics_data = [
        {'code': code, 'description': heuristic_descriptions.get(code, '')}
        for code in selected_codes
    ]

    # Готуємо красиву таблицю всіх евристик із кількістю голосів
    sorted_stats = sorted(heuristic_counts.items(), key=lambda x: x[1], reverse=True)
    heuristic_stats = [
        {'code': code, 'description': heuristic_descriptions.get(code, ''), 'count': count}
        for code, count in sorted_stats
    ]

    # Застосовуємо евристики до квітів
    steps, filtered_flowers = apply_heuristics(flower_scores, selected_codes)

    final_flowers = filtered_flowers[:10]

    return render(request, 'poll/heuristic_result.html', {
        'steps': steps,
        'heuristic_stats': heuristic_stats,
        'selected_heuristics_data': selected_heuristics_data,
        'final_flowers': final_flowers,
        'flower_scores': flower_scores,
    })


@login_required(login_url='login')
def heuristic_check(request):
    votes = HeuristicVote.objects.all()

    # Всі можливі евристики
    all_heuristics = list(heuristic_descriptions.keys())
    heuristic_counts = {h: 0 for h in all_heuristics}

    # Підрахунок голосів за кожну евристику
    for vote in votes:
        if isinstance(vote.selected_heuristics, list):
            for h in vote.selected_heuristics:
                if h in heuristic_counts:
                    heuristic_counts[h] += 1

    # Підготовка даних про квіти
    flowers = Flower.objects.all()
    flower_scores = []
    for flower in flowers:
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

    flower_scores.sort(key=lambda x: x['total_points'], reverse=True)

    # Отримання евристик, які обрав поточний користувач
    user_vote = HeuristicVote.objects.filter(user=request.user).last()

    if user_vote and isinstance(user_vote.selected_heuristics, list):
        selected_codes = user_vote.selected_heuristics
    else:
        selected_codes = []

    # Готуємо красивий список для відображення обраних евристик
    selected_heuristics_data = [
        {'code': code, 'description': heuristic_descriptions.get(code, '')}
        for code in selected_codes
    ]

    # Готуємо красиву таблицю всіх евристик із кількістю голосів
    sorted_stats = sorted(heuristic_counts.items(), key=lambda x: x[1], reverse=True)
    heuristic_stats = [
        {'code': code, 'description': heuristic_descriptions.get(code, ''), 'count': count}
        for code, count in sorted_stats
    ]

    # Застосовуємо евристики до квітів
    steps, filtered_flowers = apply_heuristics(flower_scores, selected_codes)

    final_flowers = filtered_flowers[:10]

    return render(request, 'poll/heuristic_check.html', {
        'steps': steps,
        'heuristic_stats': heuristic_stats,
        'selected_heuristics_data': selected_heuristics_data,
        'final_flowers': final_flowers,
        'flower_scores': flower_scores,
    })
