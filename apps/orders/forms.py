from django import forms

class CartAddForm(forms.Form):

    quantity = forms.IntegerField(min_value=1)

class CouponForm(forms.Form):
    code = forms.CharField(max_length=30, required=False)