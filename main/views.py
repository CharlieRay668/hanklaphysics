from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from users.models import User
from .forms import CreateNewQuestion, CreateNewClass, CreateNewAnswer, SearchForm
from .models import Question, PhysicsClass, Answer
import datetime as dt
from datetime import timezone
# Create your views here.


common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']

def strip_punctuation(word):
    puncts = ['!', '?', '$',',','@','%','^','&','*','(',')','"',"'"]
    for punct in puncts:
        word = word.replace(punct, '')
    return word

def handle_search(query, strings):
    query = query.lower().split(' ')
    scores_words = []
    for string in strings:
        score = 0
        for word in string.lower().split(' '):
            if word in query and word in common_words:
                score += 1
            elif word in query:
                score += 10
            elif strip_punctuation(word) in query:
                score += 5
        scores_words.append((score, string))
    return scores_words

def home(response):
    return render(response, "main/home.html")

def create(response):
    if response.method == "POST":
        form = CreateNewQuestion(response.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            q = Question(title = cleaned['title'], body= cleaned['body'], physics_class = cleaned['physics_class'], score = 0, creation_date = dt.datetime.now())
            q.save()
            PhysicsClass.objects.get(id=cleaned['physics_class']).classquestions.add(q)
            response.user.questions.add(q)
        return redirect("/viewclass/"+response.user.physics_class.lower().split(' ')[0])
    else:
        form = CreateNewQuestion()

    return render(response, "main/create.html", {"form":form})

def handlesearch(response):
    prev_url = response.META.get('HTTP_REFERER')
    classname = prev_url.split('/')[-2]
    if classname != 'ap' and classname != 'standard' and classname != 'honors':
        classname = prev_url.split('=')[-1]
    if response.method == "POST":
        class_lookup = {'ap':1, 'standard':2, 'honors':3}
        physics_class = PhysicsClass.objects.get(id=class_lookup[classname])
        score = response.POST.get('scorecheckbox')
        date = response.POST.get('datecheckbox')
        num_days = response.POST.get('numdays')
        search = response.POST.get('searchtext')
        if date is not None:
            questions = physics_class.classquestions.all()
            true_questions = []
            for question in questions:
                difference = dt.datetime.now(timezone.utc) - question.creation_date
                if difference.days <= float(num_days):
                    true_questions.append(question)
            if len(search) > 0:
                questions = true_questions
                words = []
                for question in questions:
                    words.append(question.title)
                scores_words = handle_search(search, words)
                scores_words.sort(reverse=True)
                true_cards = []
                for score, word in scores_words:
                    for q in Question.objects.filter(title=word):
                        if q not in true_cards:
                            true_cards.append(q)
            else:
                if score is not None:
                    def max_sort(arr):
                        new_arr = []
                        while len(arr) > 0:
                            new_arr.append(max(arr))
                            arr.remove(max(arr))
                        return new_arr
                    true_cards = max_sort(true_questions)
                else:
                    true_cards = [question for question in true_questions]
        else:
            questions = [question for question in physics_class.classquestions.all()]
            questions.reverse()
            if len(search) > 0:
                words = []
                for question in questions:
                    words.append(question.title)
                scores_words = handle_search(search, words)
                scores_words.sort(reverse=True)
                true_cards = []
                for score, word in scores_words:
                    for q in Question.objects.filter(title=word):
                        if q not in true_cards:
                            true_cards.append(q)
            else:
                if score is not None:
                    def max_sort(arr):
                        new_arr = []
                        while len(arr) > 0:
                            new_arr.append(max(arr))
                            arr.remove(max(arr))
                        return new_arr
                    true_cards = max_sort(questions)
                else:
                    true_cards = [question for question in physics_class.classquestions.all()]
        base_url = reverse('viewsearch')  # 1 /products/
        cards = true_cards
        card_id = [q.id for q in cards]
        query_string =  urlencode({'cards': card_id, 'classname':classname})  # 2 category=42
        url = '{}?{}'.format(base_url, query_string)  # 3 /products/?category=42
        return redirect(url)  # 4
    return render(response, "main/home.html")


def viewsearch(response):
    class_lookup = {'ap':1, 'standard':2, 'honors':3}
    questions = response.GET.get('cards')
    classname = response.GET.get('classname')
    questions = questions.replace('[','').replace(']','').split(', ')
    true_questions = []
    for q_id in questions:
        true_questions.append(Question.objects.get(id=q_id))
    print(true_questions)
    cards = []
    row = []
    questions.reverse()
    for index, item in enumerate(true_questions):
        if index%7 == 0:
            cards.append(row)
            row = []
        row.append(item)
    cards.append(row)
    return render(response, "main/classquestions.html", {"cards" : cards, 'currenturl': class_lookup[classname]})

def viewclass(response, classname):
    class_lookup = {'ap':1, 'standard':2, 'honors':3}
    physics_class = PhysicsClass.objects.get(id=class_lookup[classname])
    cards = []
    row = []
    questions = [question for question in physics_class.classquestions.all()]
    questions.reverse()
    for index, item in enumerate(questions):
        if index%7 == 0:
            cards.append(row)
            row = []
        row.append(item)
    cards.append(row)
    return render(response, "main/classquestions.html", {"cards" : cards, 'currenturl': class_lookup[classname]})

def viewsortedclass(response, cards):
    class_lookup = {'ap':1, 'Standard':2, 'honors':3}
    physics_class = PhysicsClass.objects.get(id=class_lookup[classname])
    cards = []
    row = []
    true_cards = []
    def max_sort(arr):
        new_arr = []
        while len(arr) > 0:
            new_arr.append(max(arr))
            arr.remove(max(arr))
        return new_arr
    if sort == 'score':
        sorted_cards = [question for question in physics_class.classquestions.all()]
        true_cards = max_sort(sorted_cards)
    if sort == 'date':
        date_cards = [(question.creation_date, question.id) for question in physics_class.classquestions.all()]
        for date, q_id in date_cards:
            difference = dt.datetime.now(timezone.utc) - date
            if difference.days <= num_days:
                true_cards.append(Question.objects.get(id=q_id))
    if sort == 'both':
        date_cards = [(question.creation_date, question.id) for question in physics_class.classquestions.all()]
        for date, q_id in date_cards:
            difference = dt.datetime.now(timezone.utc) - date
            if difference.days <= num_days:
                true_cards.append(Question.objects.get(id=q_id))
        true_cards = max_sort(true_cards)
    for index, item in enumerate(true_cards):
        if index%7 == 0:
            cards.append(row)
            row = []
        row.append(item)
    cards.append(row)
    return render(response, "main/classquestions.html", {"cards" : cards, 'currenturl': class_lookup[classname]})

def answerquestion(response, id):
    question = Question.objects.get(id=id)
    if response.method == "POST":
        form = CreateNewAnswer(response.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            ans = Answer(body = cleaned['body'], creation_date = dt.datetime.now(), score = 0)
            ans.save()
            response.user.responses.add(ans)
            question.answers.add(ans)
        return redirect("/viewclass/"+response.user.physics_class.lower().split(' ')[0])
    else:
        form = CreateNewAnswer()
    answers = question.answers.all()
    return render(response, "main/viewquestion.html", {'question': question, 'form':form, 'answers':answers})

def viewpersonalized(response):
    user = response.user
    cards = []
    row = []
    for index, item in enumerate(user.questions.all()):
        if index%7 == 0:
            cards.append(row)
            row = []
        row.append(item)
    cards.append(row)
    return render(response, "main/classquestions.html", {"cards" : cards})


def updatesame(response, id):
    user = response.user
    question = Question.objects.get(id=id)
    question.score += 1
    question.save()
    user.questions.add(question)
    return redirect("/viewclass/"+user.physics_class.lower().split(' ')[0])

def removesame(response, id):
    user = response.user
    question = Question.objects.get(id=id)
    question.score -= 1
    question.save()
    user.questions.remove(question)
    return redirect("/viewclass/"+user.physics_class.lower().split(' ')[0])

def classcreate(response):
    if response.method == "POST":
        form = CreateNewClass(response.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            c = PhysicsClass(name = cleaned['name'])
            c.save()
        return redirect("/viewclass/"+response.user.physics_class.lower().split(' ')[0])
    else:
        form = CreateNewClass()

    return render(response, "main/classcreate.html", {"form":form})
