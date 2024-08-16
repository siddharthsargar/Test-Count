from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyDataViewSet
from .views import upload_file, query_data
from .views import register, user_login, user_logout, home

# router = DefaultRouter()
# router.register(r'companydata', CompanyDataViewSet)

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('query/', query_data, name='query_data'),
   # path('', include(router.urls)),
    path('', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('/home', home, name='home'),
]
