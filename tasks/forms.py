from django import forms
from .models import Task

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description'}),
            'is_priority': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

