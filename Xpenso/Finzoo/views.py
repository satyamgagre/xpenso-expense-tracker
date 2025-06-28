from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from datetime import datetime

from .models import Expense
from .forms import ExpenseForm, CustomUserCreationForm, UserCreationForm

from django.contrib.auth import authenticate, login, logout

import csv
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas

from django.db.models import Q



@login_required
def expense_list(request):
    query = request.GET.get('q', '')
    expenses = Expense.objects.filter(user=request.user)

    if query:
        expenses = expenses.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(payment_method__icontains=query) |
            Q(description__icontains=query)
        )

    expenses = expenses.order_by('-date')
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'Finzoo/index.html', {
        'expenses': expenses,
        'total': total,
        'query': query
    })


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExpenseForm()

    return render(request, 'Finzoo/add_expense.html', {'form': form})


@login_required
def monthly_report(request):
    month = int(request.GET.get('month', datetime.now().month))
    year = int(request.GET.get('year', datetime.now().year))

    expenses = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    category_summary = expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    return render(request, 'Finzoo/monthly_report.html', {
        'expenses': expenses,
        'total': total,
        'category_summary': category_summary,
        'month': month,
        'year': year
    })


@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
            return redirect('expense_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'Finzoo/edit.html', {'expense_form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # redirect to dashboard or homepage
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Finzoo/login.html')


@login_required
def export_csv(request, month, year):
    expenses = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="expenses_{month}_{year}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Title', 'Category', 'Payment Method', 'Amount'])

    for expense in expenses:
        writer.writerow([expense.date, expense.title, expense.category, expense.payment_method, expense.amount])

    return response


@login_required
def export_pdf(request, month, year):
    expenses = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expenses_{month}_{year}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(100, y, f"Expenses Report ({month}/{year})")
    y -= 30

    for expense in expenses:
        line = f"{expense.date} - {expense.title} - {expense.category} - {expense.payment_method} - ₹{expense.amount}"
        p.drawString(50, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response



@login_required
def search_expenses(request):
    query = request.GET.get('q', '')
    expenses = Expense.objects.filter(
        Q(title__icontains=query) |
        Q(category__icontains=query) |
        Q(description__icontains=query),
        user=request.user
    ).order_by('-date')
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'Finzoo/index.html', {
        'expenses': expenses,
        'total': total,
        'search_query': query
    })


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        return redirect('index')  # Replace with your list view name

    return render(request, 'expenses/confirm_delete.html', {'expense': expense})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # or your dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'Finzoo/register.html', {'form': form})
