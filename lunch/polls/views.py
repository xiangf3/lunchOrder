from django.shortcuts import render
from polls.models import Preference, User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

import os, hashlib, binascii

# Create your views here.

def index(request):
    return HttpResponseRedirect(reverse('polls:home'))

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
    username = request.session.get('username')
    if username == None:
        raise PermissionDenied
    brought = request.POST.get('brought')
    if brought is not None:
        if brought=='YES':
            Preference(username=username, pub_date=timezone.now(), choice="None", remark="Have brought").save()
            return HttpResponseRedirect(reverse('polls:done'))
        elif brought=='NO':
            request.session['brought_answered'] = True
            return HttpResponseRedirect(reverse('polls:home'))
        else:
            raise PermissionDenied
    else:
        choice = request.POST.get('choice')
        remark = request.POST.get('remark')
        budget = request.POST.get('budget')
        try:
            budget = int(budget)
        except ValueError:
            budget = 20
        if budget < 0:
            budget = 0
        if choice is None or budget is None:
            raise PermissionDenied
        Preference(username=username, pub_date=timezone.now(), choice=choice, remark=remark, budget=budget).save()
        return HttpResponseRedirect(reverse('polls:done'))

def register(request):
    return render(request, 'polls/register.html', {})

def login(request):
    username = request.POST.get('username')
    psw = request.POST.get('psw')
    if username is None or psw is None or len(username)>32 or len(psw)>32:
        return HttpResponseRedirect(reverse('polls:home'))
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('polls:failure', args=(0,)))
    salt = binascii.unhexlify(u.psw.encode('utf-8')[:64])
    stored_key = binascii.unhexlify(u.psw.encode('utf-8')[64:])
    key = hashlib.pbkdf2_hmac('sha256', psw.encode('utf-8'), salt, 100000)
    if key == stored_key:
        request.session['username'] = username
        return HttpResponseRedirect(reverse('polls:home'))
    else:
        return HttpResponseRedirect(reverse('polls:failure', args=(0,)))

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('polls:home'))

def signup(request):
    username = request.POST.get('username')
    psw = request.POST.get('psw')
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')

    if any(elem is None or len(elem)>32 for elem in [username, psw, first_name, last_name]):
        return HttpResponseRedirect(reverse('polls:register'))

    if len(User.objects.filter(username=username))>0:
        return HttpResponseRedirect(reverse('polls:failure', args=(2,)))

    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', psw.encode('utf-8'), salt, 100000)
    hashed = binascii.hexlify(salt) + binascii.hexlify(key)
    User(username=username, psw=hashed.decode('utf-8'), first_name=first_name, last_name=last_name).save()
    request.session['username'] = username
    return HttpResponseRedirect(reverse('polls:home'))

def done(request):
    username = request.session.get('username')
    if username is None:
        raise PermissionDenied

    if request.session.get('brought_answered') is not None:
        del request.session['brought_answered']
        
    if len(Preference.objects.filter(username=username, pub_date__year=timezone.now().year, \
             pub_date__month=timezone.now().month, pub_date__day=timezone.now().day)) < 1:
             return HttpResponseRedirect(reverse('polls:home'))

    context = {}
    context['username'] = username
    context['total_today'] = Preference.objects.raw('SELECT id, choice, count(*) AS cnt FROM polls_preference WHERE choice!="None" GROUP BY choice')
    return render(request, 'polls/done.html', context)

def records(request):
    username = request.session.get('username')
    if username is None:
        raise PermissionDenied
    context = {}
    context['username'] = username
    context['records'] = Preference.objects.all()
    return render(request, 'polls/records.html', context)

def failure(request, code):
    context = {'errcode': code}
    return render(request, 'polls/failure.html', context)

def edit(request):
    username = request.session.get('username')
    if username == None:
        raise PermissionDenied
    for p in Preference.objects.filter(username=username, pub_date__year=timezone.now().year, \
            pub_date__month=timezone.now().month, pub_date__day=timezone.now().day):
        p.delete()
    return HttpResponseRedirect(reverse('polls:home'))