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

    # Group by category
    category_summary = expenses.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    return render(request, 'expenses/monthly_report.html', {
        'expenses': expenses,
        'total': total,
        'category_summary': category_summary,
        'month': month,
        'year': year
    })

def edit(request, id):
    expense_form = ExpenseForm
    return render(request, 'Finzoo/edit.html', {'expense_form':expense_form})


    