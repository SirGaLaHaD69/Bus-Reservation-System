from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Route(models.Model):
    route_no = models.AutoField(primary_key=True)
    route_dest = models.CharField(max_length = 100)
    route_src = models.CharField(max_length = 100)
    class Meta:
        unique_together = (('route_dest', 'route_src'),)

class Plane(models.Model):
    flight_code = models.CharField(max_length = 100, primary_key=True)
    def __str__(self):
        return self.flight_code

class FlightDetail(models.Model):
    flight_code = models.ForeignKey(Plane, on_delete=models.CASCADE)
    route_no = models.ForeignKey(Route, on_delete=models.CASCADE)
    arrival = models.TimeField()
    departure = models.TimeField(null=True)
    price = models.FloatField()
    bus_route=models.CharField(max_length=1000)
    seats_available=models.PositiveIntegerField();
    def get_route_path(self,args):
        gap='-->'
        self.bus_route=gap.join(list(args.split()))
    @property
    def refund(self):
        return self.price * 0.8;
    
    def get_absolute_url(self):
        return reverse("plane_detail_book",kwargs={'pk': self.pk})
    class Meta:
        unique_together = (('flight_code', 'route_no'),)

class Ticket(models.Model):
    JDate = models.DateField()
    PNR = models.PositiveIntegerField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Date_of_booking = models.DateField()
    fk_flights = models.ForeignKey(FlightDetail, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse("my_tickets",kwargs={'pk': self.PNR})
    def __str__(self):
        return str(self.PNR)

class Passenger(models.Model):
    GENDER_CHOICES = (
        ('male', 'MALE'),
        ('female', 'FEMALE'),
        ('other', 'OTHER'),
    )
    SSN = models.CharField(max_length=12, primary_key=True)
    passenger_firstname = models.CharField(max_length = 100)
    passenger_lastname = models.CharField(max_length = 100)
    passenger_dob = models.DateField()
    passenger_gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female')
    def get_absolute_url(self):
        return reverse("passenger_info", kwargs={'pk': self.pk})

class PassengerTicketRel(models.Model):
    PNR = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    SSN = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('PNR', 'SSN'),)

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return self.user.username

class NoFlightDay(models.Model):
    DAYS = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    Days = models.CharField(null=True, max_length=10, choices=DAYS)
    fk_flights = models.ForeignKey(FlightDetail, on_delete=models.CASCADE)
