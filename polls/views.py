from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.views import generic

# from django.template import loader

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name='polls/details.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template=loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    # output=', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)  # Usage of render method which return HttpResponse

def details(request, question_id):
    # try:
    #     question=Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist.")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    #return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    return HttpResponse("You are voting on question %s " % question_id)
