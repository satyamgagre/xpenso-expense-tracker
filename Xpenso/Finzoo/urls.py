from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.expense_list, name='index'),  
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:id>/', views.edit_expense, name='edit'),  
    path('report/', views.monthly_report, name='monthly_report'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('export/csv/<int:month>/<int:year>/', views.export_csv, name='export_csv'),
    path('export/pdf/<int:month>/<int:year>/', views.export_pdf, name='export_pdf'),

    path('search/', views.search_expenses, name='search_expenses'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    
    path('register/', views.register_view, name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Finzoo/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Finzoo/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Finzoo/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Finzoo/password_reset_complete.html'), name='password_reset_complete'),




]
