from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import login, logout



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def hello(request):                       
    return HttpResponse("Nah u Good") 
 
def createAccount(request):
    if 'q' in request.GET:
        message = 'Account Created'
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)
