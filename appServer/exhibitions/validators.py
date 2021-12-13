import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_cell_number(value):
    pattern = re.compile(r'^(0|\+98)9[0-9]{9}$')
    if not pattern.match(value):
        raise ValidationError(_("شماره همراه وارد شده معتبر نمی باشد"))


def validate_phone_number(value):
    pattern = re.compile(r'0[1-9]{2}[0-9]{8}')
    if not pattern.match(value):
        raise ValidationError(_("شماره تلفن وارد شده معتبر نمی باشد"))
