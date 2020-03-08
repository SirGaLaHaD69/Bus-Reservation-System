from django.contrib import admin
from airline3app.models import Route, FlightDetail, PassengerTicketRel, Plane, UserProfileInfo, Ticket, Passenger, NoFlightDay

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Route)
admin.site.register(FlightDetail)
admin.site.register(PassengerTicketRel)
admin.site.register(Ticket)
admin.site.register(Plane)
admin.site.register(Passenger)
admin.site.register(NoFlightDay)