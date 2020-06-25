from django.shortcuts import render
from polls.models import Preference, User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import os, hashlib

# Create your views here.

def home(request):
    context = {}
    username = None
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        username = request.session['username']
    if username:
        # check if already submitted, redirect to done
        if len(Preference.objects.filter(username=username, pub_date__year=timezone.now().year, \
             pub_date__month=timezone.now().month, pub_date__day=timezone.now().day)) >= 1:
             return HttpResponseRedirect(reverse('polls:done'))

        # not submitted:
        if request.session.get('brought_answered') is None:
            context['brought_answered'] = False
        else:
            context['brought_answered'] = True
    return render(request, 'polls/home.html', context)

def submit(request):
    username = request.session['username']
    brought = request.POST['brought']
    if brought is not None:
        request.session['brought_answered'] = True
        if brought:
            Preference(username=username, pub_date=timezone.now(), choice=0, remark="Have brought").save()
            return HttpResponseRedirect(reverse('polls:done'))
        else:
            return HttpResponseRedirect(reverse('polls:home'))
    else:
        choice = request.POST['choice']
        remark = request.POST['remark']
        Preference(username=username, pub_date=timezone.now(), choice=choice, remark=remark).save()
        return HttpResponseRedirect(reverse('polls:done'))

def register(request):
    return render(request, 'polls/register.html', {})

def login(request):
    username = request.POST['username']
    psw = request.POST['psw']
    u = User.objects.get(username=username)
    salt = u.psw[:64]
    key = hashlib.pbkdf2_hmac('sha256', psw.encode('utf-8'), salt, 100000)
    if key == u.psw[64:]:
        request.session['username'] = username
        return HttpResponseRedirect(reverse('polls:home'))
    else:
        return HttpResponseRedirect(reverse('polls:failure', args=(0,)))

def signup(request):
    username = request.POST['username']
    psw = request.POST['psw']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    salt = os.urandom(64)
    key = hashlib.pbkdf2_hmac('sha256', psw.encode('utf-8'), salt, 100000)
    User(username=username, psw=salt+key, first_name=first_name, last_name=last_name).save()
    request.session['username'] = username
    return HttpResponseRedirect(reverse('polls:home'))

def done(request):
    context = {}
    return render(request, 'polls/done.html', context)

def failure(request, code):
    context = {"errcode": code}
    return render(request, 'polls/failure.html', context)