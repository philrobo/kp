from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Message
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .nlp import chat
import subprocess
from subprocess import Popen, PIPE, STDOUT
from .mongo import parseMango

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)


def index(request):
    # q = chat()
    return HttpResponse("q")


def chatindex(request):
    # question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html')


def mongoIndex(request):
    response = parseMango().mongo_response()
    # response = pm.mongo_response()
    return HttpResponse(response)


global path
path = ""


globvar = ""


def set_globvar_to_one(path):
    global globvar
    globvar = path


def print_globvar():
    print(globvar)


# def chatbot(request):
#     return HttpResponse("q")


def chatbot(request):
    print_globvar()       # Prints 1
    # question = get_object_or_404(Question, pk=question_id)
    input_text = pk = request.POST.get("input", "")
    if(input_text != ""):
        chatObj = chat(input_text)
        isExcecutable = False
        chat_response = chatObj.chat_response()
        print(chat_response[1])

        if(chat_response[1] in {"location", "list", "home"}):
            isExcecutable = True

        if(chat_response[1] in ['home', "application"]):
            set_globvar_to_one(chat_response[0])
            command_response = 'path set to location: '+chat_response[0]
        elif(chat_response[1] in ['goto', 'greeting', 'goodbye', 'thanks']):
            command_response = chat_response[0]
        else:
            command_response = commands(chat_response[0], isExcecutable)
            # set_globvar_to_one(chat_response[0])
        return render(request, 'polls/detail.html', {'message': command_response})
    else:
        return HttpResponse("")


def commands(cmd, isExcecutable):
    print(isExcecutable)
    print(cmd)
    print(globvar)
    print("-----------------------------")
    if(globvar == "" and isExcecutable):
        result = subprocess.getoutput(cmd)
    elif not isExcecutable:
        result = subprocess.getoutput(cmd)
    else:
        print("command to be executed is : "+cmd)
        output = subprocess.Popen(
            cmd, cwd=globvar, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        result = output.stdout.read().decode("utf-8")
    print("path : " + globvar + " command :" + cmd + "; output : "+result)
    return result


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
