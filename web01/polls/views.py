from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from .models import Choice, Question

from django.template import loader


def detail(request,question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question': question})
    # return HttpResponse("You're looking at question {}".format(question_id))


def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})
    # return HttpResponse("You're looking at the results of question {}".format(question_id))

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(request.POST['choice'])
        print(selected_choice)
    except(KeyError,Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # 使用reverse()函数,需要给出我们想要跳转的视图名字和该视图对应的ＵＲＬ模式中需要给该视图提供的参数．
    # return HttpResponse("You're voting on question %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request,'polls/index.html',context)