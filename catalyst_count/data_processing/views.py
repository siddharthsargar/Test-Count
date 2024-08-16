from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import Company
import pandas as pd
import io
from .tasks import import_csv
from .forms import QueryForm 
from rest_framework import viewsets
from .models import Company
from .serializers import CompanyDataSerializer
from .tasks import import_csv  # Import the Celery task

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')



# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             df = pd.read_csv(file)
#             for index, row in df.iterrows():
#                 Company.objects.create(
#                     name=row['name'],
#                     domain=row['domain'],
#                     year_founded=row['year_founded'],
#                     industry=row['industry'],
#                     size_range=row['size_range'],
#                     locality=row['locality'],
#                     country=row['country'],
#                     linkedin_url=row['linkedin_url'],
#                     current_employee_estimate=row['current_employee_estimate'],
#                     total_employee_estimate=row['total_employee_estimate']
#                 )
#             return HttpResponse('File uploaded successfully')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Define the file path
            file_path = f'/tmp/{file.name}'
            # Save the uploaded file to the server
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Trigger the Celery task to process the file
            import_csv.delay(file_path)
            #return HttpResponse('File uploaded and is being processed')
            messages.success(request, 'File uploaded and is being processed.')
            return render(request, 'home.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             file_path = f'/tmp/{file.name}'
#             with open(file_path, 'wb+') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)
#             import_csv.delay(file_path)
#             return HttpResponse('File uploaded and is being processed')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})

# def query_data(request):
#     form = QueryForm(request.GET or None)
#     if form.is_valid():
#         name = form.cleaned_data.get('name')
#         industry = form.cleaned_data.get('industry')
#         year_founded = form.cleaned_data.get('year_founded')
#         city = form.cleaned_data.get('city')
#         state = form.cleaned_data.get('state')
#         country = form.cleaned_data.get('country')
#         employees_from = form.cleaned_data.get('employees_from')
#         employees_to = form.cleaned_data.get('employees_to')

#         filters = {}
#         if industry:
#             filters['industry'] = industry
#         if min_revenue is not None:
#             filters['revenue__gte'] = min_revenue
#         if max_revenue is not None:
#             filters['revenue__lte'] = max_revenue

#         count = Company.objects.filter(**filters).count()

#         return render(request, 'query.html', {'form': form, 'count': count})

#     return render(request, 'query.html', {'form': form})

def query_data(request):
    form = QueryForm(request.GET or None)
    if form.is_valid():
        # Get cleaned data from the form
        name = form.cleaned_data.get('name')
        industry = form.cleaned_data.get('industry')
        year_founded = form.cleaned_data.get('year_founded')
        city = form.cleaned_data.get('city')
        state = form.cleaned_data.get('state')
        country = form.cleaned_data.get('country')
        employees_from = form.cleaned_data.get('employees_from')
        employees_to = form.cleaned_data.get('employees_to')

        # Initialize filters dictionary
        filters = {}

        # Add filters based on form data
        if name:
            filters['name__icontains'] = name
        if industry:
            filters['industry__icontains'] = industry
        if year_founded:
            filters['year_founded'] = year_founded
        if city:
            filters['locality__icontains'] = city
        if state:
            filters['state__icontains'] = state
        if country:
            filters['country__icontains'] = country
        if employees_from is not None:
            filters['current_employee_estimate__gte'] = employees_from
        if employees_to is not None:
            filters['current_employee_estimate__lte'] = employees_to

        # Query the database with the filters
        count = Company.objects.filter(**filters).count()

        # Render the template with the form and count
        return render(request, 'query.html', {'form': form, 'count': count})

    # Render the template with the form (if not valid)
    return render(request, 'query.html', {'form': form})

class CompanyDataViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyDataSerializer


