from django.shortcuts import render,redirect
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import ExpenseForm
from datetime import datetime

# Create your views here.

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'Finzoo/index.html', {
    'expenses': expenses,
    'total': total
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    return render(request, 'Finzoo/add_expense.html', {'form': form})



    