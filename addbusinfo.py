import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airline3.settings')

import django
django.setup()

import datetime
import random

from airline3app.models import FlightDetail, Route, Plane, NoFlightDay

while True:
    f_code = input("Flight No.: ")
    src = input("Source: ")
    dest = input("Destination: ")
    dptre = input("Departure (<HH:MM> 24hf): ")
    dptre_o = datetime.datetime.strptime(dptre, '%H:%M')
    arr = input("Arrival (<HH:MM> 24hf): ")
    arr_o = datetime.datetime.strptime(arr, '%H:%M')
    day = input("Days not available (separate them with spaces): ")
    rt = Route.objects.filter(route_src=src, route_dest=dest)
    r_path=input("de: ")
    seats=int(input("No of available seats: "))
    if not rt:
        rt = Route(route_src=src, route_dest=dest)
        rt.save()
    else:
        rt = rt[0]
    pl = Plane(flight_code=f_code)
    pl.save()
    fl = FlightDetail(
        flight_code=pl,
        route_no=rt,
        arrival=arr,
        departure=dptre,
        price=random.randint(300, 700),
        bus_route='',
        seats_available=seats
    )
    fl.save()
    fl.get_route_path(r_path)
    fl.save()
    print(fl.bus_route)
    if day != '':
        dayL = day.split(' ')
        print('yay')
        for d in dayL:
            nfj = NoFlightDay(fk_flights=fl, Days=d)
            nfj.save()
