from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

USER_MIN_AGE = 9
RESTRICTED_EMAIL_DOMAIN = "rambler.ru"


def check_birth_date(value: date) -> None:
    difference = relativedelta(date.today(), value).years

    if difference < USER_MIN_AGE:
        raise ValidationError("Вам должно быть 9 лет или больше для регистрации.")


def check_email_domain(value: str) -> None:

    if value.endswith(RESTRICTED_EMAIL_DOMAIN):
        raise ValidationError(
            f"Register with email domain {RESTRICTED_EMAIL_DOMAIN} was denied. Try to use email with another domain."
        )
