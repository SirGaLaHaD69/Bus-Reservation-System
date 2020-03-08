from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.models import User
from airline3app.models import UserProfileInfo, Ticket, Passenger

GENDER_CHOICES = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
    ('other', 'OTHER'),
)

class SearchForm(forms.Form):
    source = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    destination = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    Date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class PassengerForm(forms.ModelForm):
    passenger_firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col textbox-translucent', 'autocomplete': 'off', 'placeholder': 'First Name'}), label='')
    passenger_lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col textbox-translucent', 'autocomplete': 'off', 'placeholder': 'Last Name'}), label='')
    passenger_dob = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker textbox-translucent', 'autocomplete': 'off', 'placeholder': 'Date of Birth'}), label='')
    passenger_gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(), label='')
    SSN = forms.CharField(max_length=12, min_length=12, widget=forms.TextInput(attrs={'class': 'form-control textbox-translucent', 'autocomplete': 'off', 'placeholder': 'Aadhaar Number'}), label='')
    class Meta():
        model = Passenger
        fields = (
            'passenger_firstname',
            'passenger_lastname',
            'passenger_dob',
            'passenger_gender',
            'SSN',
        )
