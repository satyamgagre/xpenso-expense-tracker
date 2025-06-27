from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 
                'amount', 
                'category', 
                'payment_method', 
                'description', 
                'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # ✅ this triggers native calendar
        }
