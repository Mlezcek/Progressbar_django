from django import forms
from .models import Progress, Update


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['percentage']

    def clean_percentage(self):
        percentage = self.cleaned_data.get('percentage')
        if percentage is not None and (percentage < 0 or percentage > 100):
            raise forms.ValidationError("Wartość procentowa musi być w zakresie 0-100.")
        return percentage

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-700 text-white rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 bg-gray-700 text-white rounded', 'rows': 4}),
        }

class ProgressCreateForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-700 text-white rounded', 'placeholder': 'Nazwa progress bara'})
        }