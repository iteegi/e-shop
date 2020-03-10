"""Forms."""

from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    """Coupon form."""

    code = forms.CharField(label=_('Coupon'))
