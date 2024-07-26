from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Parent
from rest_framework import generics
from .serializers import StudentSerializer, ParentSerializer

def universal_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        
        user = authenticate(request, username=phone_number, password=phone_number)
        
        if user is not None:
            auth_login(request, user)
            try:
                student = Student.objects.get(user=user)
                return redirect('student_dashboard')
            except Student.DoesNotExist:
                try:
                    parent = Parent.objects.get(user=user)
                    return redirect('parent_dashboard')
                except Parent.DoesNotExist:
                    messages.error(request, 'No associated student or parent account found.')
        else:
            messages.error(request, 'Invalid phone number.')
    return render(request, 'students/login.html')

@login_required
def student_dashboard(request):
   
    student = Student.objects.get(user=request.user)
    
    
    return render(request, 'students/student_dashboard.html', {'student': student})

@login_required
def parent_dashboard(request):
    
    parent = Parent.objects.get(user=request.user)
    students = Student.objects.filter(parent=parent)
    
    
    return render(request, 'students/parent_dashboard.html', {'parent': parent, 'students': students})

def logout_view(request):
    auth_logout(request)
    return redirect('universal_login')  

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ParentList(generics.ListAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer



class ParentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
