"""Method"""
import random
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSet, Card
from .forms import CardSetForm, CardForm



def home(request):
    """Method"""
    sets = CardSet.objects.all().order_by('-created_at')
    return render(request, 'vocab/home.html', {'sets': sets})

def create_set(request):
    """Method"""
    if request.method == 'POST':
        form = CardSetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CardSetForm()
    return render(request, 'vocab/create_set.html', {'form': form})

def edit_set(request, set_id):
    """Method"""
    card_set = get_object_or_404(CardSet, id=set_id)
    if request.method == 'POST':
        form = CardSetForm(request.POST, instance=card_set)
        if form.is_valid():
            form.save()
            return redirect('study_set', set_id=set_id)
    else:
        form = CardSetForm(instance=card_set)
    return render(request, 'vocab/edit_set.html', {'form': form, 'set': card_set})

def add_card(request, set_id):
    """Method"""
    card_set = get_object_or_404(CardSet, pk=set_id)
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.set = card_set
            card.save()
            return redirect('study_set', set_id=set_id)
    else:
        form = CardForm()
    return render(request, 'vocab/add_card.html', {'form': form, 'set': card_set})

def study_set(request, set_id):
    """Method"""
    card_set = get_object_or_404(CardSet, pk=set_id)
    cards = card_set.card_set.all()
    return render(request, 'vocab/study_set.html', {'set': card_set, 'cards': cards})

def quiz(request, set_id):
    """Method"""
    card_set = get_object_or_404(CardSet, pk=set_id)
    if 'quiz_data' not in request.session or request.session['quiz_data']['set_id'] != set_id:
        cards = list(card_set.card_set.all())
        if not cards:
            messages.warning(request, "Набор пуст! Добавьте карточки для тренировки.")
            return redirect('study_set', set_id=set_id)
        random.shuffle(cards)
        request.session['quiz_data'] = {
            'set_id': set_id,
            'card_ids': [card.id for card in cards],
            'current_index': 0,
            'correct': 0
        }
    quiz_data = request.session['quiz_data']
    if quiz_data['current_index'] >= len(quiz_data['card_ids']):
        result = {
            'total': len(quiz_data['card_ids']),
            'correct': quiz_data['correct']
        }
        del request.session['quiz_data']
        return render(request, 'vocab/quiz_complete.html', {'result': result, 'set_id': set_id})
    current_card_id = quiz_data['card_ids'][quiz_data['current_index']]
    current_card = Card.objects.get(id=current_card_id)
    if request.method == 'POST':
        if 'user_answer' in request.POST:
            user_answer = request.POST.get('user_answer', '').strip().lower()
            correct_answer = current_card.term.strip().lower()
            is_correct = user_answer == correct_answer
            if is_correct:
                quiz_data['correct'] += 1
            context = {
                'is_correct': is_correct,
                'correct_answer': current_card.term,
                'current_card': current_card,
                'progress': f"{quiz_data['current_index'] + 1}/{len(quiz_data['card_ids'])}",
                'set_id': set_id
            }
            request.session.modified = True
            return render(request, 'vocab/quiz_result.html', context)
        quiz_data['current_index'] += 1
        request.session.modified = True
        return redirect('quiz', set_id=set_id)
    context = {
        'current_card': current_card,
        'progress': f"{quiz_data['current_index'] + 1}/{len(quiz_data['card_ids'])}",
        'set_id': set_id
    }
    return render(request, 'vocab/quiz_start.html', context)

@require_POST
def delete_card(request, card_id):
    """Method"""
    card = get_object_or_404(Card, id=card_id)
    set_id = card.set.id
    card.delete()
    return redirect('study_set', set_id=set_id)

@require_POST
def delete_set(request, set_id):
    """Method"""
    card_set = get_object_or_404(CardSet, id=set_id)
    card_set.delete()
    return redirect('home')

def edit_card(request, card_id):
    """Method"""
    card = get_object_or_404(Card, id=card_id)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('study_set', set_id=card.set.id)
    else:
        form = CardForm(instance=card)
    return render(request, 'vocab/edit_card.html', {'form': form, 'card': card})
