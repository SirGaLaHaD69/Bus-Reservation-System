from django.shortcuts import render
from airline3app.models import Route, FlightDetail, Plane, UserProfileInfo, Ticket, Passenger, NoFlightDay, PassengerTicketRel
from airline3app.forms import SearchForm, UserForm, UserProfileInfoForm, PassengerForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import DetailView
from . import models
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.forms import formset_factory
import random
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
# Create your views here.

cities = [
    'BHUBANESWAR','CUTTACK',
    'BRAHMAPUR','SAMBALPUR',
    'KHORDHA','PURI','BARGARH',
    'ANGUL','TALCHER','JHARSUGUDA',
    'DHENKANAL','RAIPUR',
    'KOLKATA','KENDRAPADA',
    'KEONJHAR','BHADRAK',
    'BALESHWAR','ROURKELA'
]
class DeleteTicketView(DeleteView,LoginRequiredMixin):
    model=Ticket
    success_url = reverse_lazy('ticket_list')
@login_required
def index(request):
    global cities
    form = SearchForm()
    source = ''
    destination = ''
    q1 = FlightDetail.objects.none()
    if request.method == "POST":
        form = SearchForm(request.POST)
        print(request.POST)
        if form.is_valid():
            jdte = form.cleaned_data.get('Date')
            Day = jdte.strftime("%a").upper()
            source = form.cleaned_data.get('source')
            destination = form.cleaned_data.get('destination')
            request.session['jdte'] = jdte.strftime("%m/%d/%Y")
            q1 = FlightDetail.objects.filter(route_no__route_src__iexact=source, route_no__route_dest__iexact=destination).exclude(noflightday__Days=Day)
            if q1:
                request.session['R_No'] = q1[0].route_no_id
        else:
            print("ERROR")
    else:
        q1 = FlightDetail.objects.all()
    return render(request,'index.html',{'form':form, 'flights':q1, 'dest':destination, 'src':source, 'cities':cities})

@login_required
def plane_detail_book(request, pk):
    request.session['F_No'] = pk
    if request.method == "POST":
        request.session['N'] = int(request.POST.get("number_of_passengers"))
        return HttpResponseRedirect(reverse('airline3app:passenger_info'))
    else:
        print("ERROR")
    return render(request, 'flightdetail.html',{'flight':pk})

@login_required
def passenger_info(request):
    PassengerFormSet = formset_factory(PassengerForm, extra=request.session.get('N'))
    if request.method == "POST":
        passenger_details = PassengerFormSet(request.POST)
        if passenger_details.is_valid():
            p_ssn = list()
            p_fname = list()
            p_lname = list()
            p_sex = list()
            p_dob = list()
            for K in passenger_details.forms:
                psngr = K.save(commit=False)
                p_ssn.append(psngr.SSN)
                p_fname.append(psngr.passenger_firstname)
                p_lname.append(psngr.passenger_lastname)
                p_dob.append(psngr.passenger_dob.strftime("%m/%d/%Y"))
                p_sex.append(psngr.passenger_gender)
            request.session['p_ssn'] = p_ssn
            request.session['p_fname'] = p_fname
            request.session['p_lname'] = p_lname
            request.session['p_dob'] = p_dob
            request.session['p_sex'] = p_sex
        return HttpResponseRedirect(reverse('payments_page'))
    else:
        passenger_details = PassengerFormSet()
    return render(request,'passenger_info.html',{'passenger_details':passenger_details})

@login_required
def payments_page(request):
    F_No = request.session.get('F_No')
    R_No = request.session.get('R_No')
    N = request.session.get('N')

    t = Ticket.objects.all()
    final2 = FlightDetail.objects.get(flight_code=F_No, route_no=R_No)
    final2.reduce_ticket(N)
    price = final2.price
    t_price = price*N
    p_ssn = request.session.get('p_ssn')
    p_fname = request.session.get('p_fname')
    p_lname = request.session.get('p_lname')
    p_dob = request.session.get('p_dob')
    p_sex = request.session.get('p_sex')
    print(request.session.keys())
    if request.method == "POST":
        key = makePNR()
        while t.filter(PNR=key).exists():
            key = makePNR()
        jdte = datetime.datetime.strptime(request.session.get('jdte'), "%m/%d/%Y")
        T = Ticket(PNR=key, JDate=jdte, username=request.user, Date_of_booking=datetime.date.today(), fk_flights=final2)
        T.save()
        for k in range(0, len(p_ssn)):
            p = Passenger(
                SSN=p_ssn[k],
                passenger_firstname=p_fname[k],
                passenger_lastname=p_lname[k],
                passenger_gender=p_sex[k].lower(),
                passenger_dob=datetime.datetime.strptime(p_dob[k], "%m/%d/%Y")
            )
            p.save()
            p_rel = PassengerTicketRel(PNR=T, SSN=p)
            p_rel.save()
            R = request.session.keys()
        request.session['key'] = key
        return HttpResponseRedirect(reverse('congrats'))
    return render(request,'payments_page.html',{'price':t_price})

@login_required
def congrats(request):
    t = Ticket.objects.get(PNR=request.session['key'])
    return render(request,'congrats.html', {'ticket':t})

"""
@login_required
def plane_list(request):
    form = SearchForm(request.POST or None)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            global num
            num = form.cleaned_data.get('number_of_passengers')
            for i in range(int(num)+1):
                p = ForPass(passenger=i+1)
                p.save()
            p = Route.objects.filter(route_dest=form.cleaned_data.get('destination'), route_src = form.cleaned_data.get('source'))
            if not p:
                route_id = 1000
            else:
                route_id = p[0].route_no
            flights = FlightDetail.objects.filter(route=route_id)
            dest = form.cleaned_data.get('destination')
            src = form.cleaned_data.get('source')
            q = DateRoute(Route = route_id,Date=form.cleaned_data.get('Date'))
            q.save()
    return render(request, 'plane_list.html', {'form': form,'flights': flights,'dest':dest,'src':src})
"""

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(username=request.user).select_related('fk_flights')
    return render(request, 'ticket_list.html', {'ticket': tickets})

@login_required
def my_tickets(request, pk):
    tickets = Ticket.objects.filter(username=request.user).select_related('fk_flights')
    p = tickets.filter(PNR=pk).prefetch_related('PNR__passengerticketrel_set__SSN')
    t_price = p[0].passengerticketrel_set.count()*p[0].fk_flights.price
    psngr = p[0].passengerticketrel_set.all()
    return render(request, 'my_tickets.html', {'passenger':psngr, 'ticket':p[0], 't_price':t_price})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print("ERROR")
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'register.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('airline3app:user_login'))

def makePNR():
    PNR = ''
    while len(PNR) < 10:
        n = random.randint(0,9)
        PNR = PNR + str(n)
    k = int(PNR)
    return k

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("ACCOUNT NOT ACTIVE")
            else:
                messages.error(request,'Username or Password not correct! Try Again!')
                return render(request, 'login.html',{})
        else:
            return render(request, 'login.html',{})
    else:
        return HttpResponseRedirect(reverse('index'))
