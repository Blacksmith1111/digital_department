from django import forms
from .models import CardSet, Card
from django import forms
from django.core.validators import MinLengthValidator
from .models import CardSet, Card

class CardSetForm(forms.ModelForm):
    class Meta:
        model = CardSet
        fields = ['title', 'description']
        labels = {
            'title': 'Название набора',
            'description': 'Описание'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите описание набора'}), 'title': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите название набора'})
        }

class CardForm(forms.ModelForm):
    term = forms.CharField(
        label="Слово/Термин",
        validators=[MinLengthValidator(2, "Слово должно содержать минимум 2 символа")],
        widget=forms.TextInput(attrs={'placeholder': 'Введите слово'})
    )
    definition = forms.CharField(
        label="Перевод/Определение",
        validators=[MinLengthValidator(2, "Перевод должен содержать минимум 2 символа")],
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Введите перевод или определение'
        })
    )

    class Meta:
        model = Card
        fields = ['term', 'definition']
