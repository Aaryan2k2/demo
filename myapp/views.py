from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models import Question
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm
# Create your views here.

class IndexView(generic.ListView):
    template_name='index.html'
    context_object_name='latest_question_list'
    
    def get_queryset(self):
         return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model=Question
    template_name='detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model=Question
    template_name='results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))

def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.pub_date = timezone.now()  
            question.save()
            return redirect('myapp:detail', pk=question.id)
    else:
        question_form = QuestionForm()

    return render(request, 'create_question.html', {'question_form': question_form})

def add_choices(request, question_id):
    question = Question.objects.get(id=question_id)
    
    if request.method == 'POST':
        choice_form = ChoiceForm(request.POST)
        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.question = question  # Associate the choice with the question
            choice.save()
            return redirect('myapp:add_choices', question_id=question.id)
    else:
        choice_form = ChoiceForm()

    return render(request, 'add_choices.html', {'question': question, 'choice_form': choice_form})
