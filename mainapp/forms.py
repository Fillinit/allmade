from django import forms
from .models import Guest_Review, Review

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class Guest_ReviewForm(forms.ModelForm):
    class Meta:
        model = Guest_Review
        fields = ['name', 'tel_number', 'email', 'product', 'text', 'is_public']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'text', 'stars', 'is_public']