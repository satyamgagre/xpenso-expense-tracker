from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.expense_list, name='index'),
    path('add/', views.add_expense, name='add_expense'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('report/', views.monthly_report, name='monthly_report'),
    path('edit', views.edit, name='edit'),
]
