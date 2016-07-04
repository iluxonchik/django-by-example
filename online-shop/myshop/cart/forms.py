from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)  # coerce=int ---> convert input to an int
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)