from django.shortcuts import render
from django.http import HttpResponse
from .models import Student

# Create your views here.
def index(request):
    students = Student.objects.all()
    print("++++++++++++++++++++++++")
    print("++++++++++++++++++++++++")
    print("++++++++++++++++++++++++")
    print("++++++++++++++++++++++++")
    print(students)
    return render(request, 'home.html', {'students': students})
