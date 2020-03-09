"""Forms."""

from django import forms


class CouponApplyForm(forms.Form):
    """Coupon form."""

    code = forms.CharField()
