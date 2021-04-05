from django.shortcuts import render
from .main import main

from .models import UserDetails
# Create your views here.





def home(request):

    users = UserDetails.objects.all()

    return render(request,'index.html',{'users':users,})