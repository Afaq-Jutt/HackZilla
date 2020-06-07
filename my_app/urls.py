from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),          #Here we have gave the path of views.py(home function)
    path('new_search',views.new_search,name='new_search'),
]