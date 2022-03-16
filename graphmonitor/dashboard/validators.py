from re import fullmatch
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address

def validate_domain_or_ipv4(value):
    if fullmatch(r"^([a-zA-Z1-9]+\.)+[a-zA-Z1-9]+$", value) is None:
        try:
            validate_ipv4_address(value)
        except ValidationError:
            raise ValidationError("Enter a valid IPv4 address or domain.")

def validate_query(value):
    if "[PORT]" not in value:
        raise ValidationError('Enter a query command that includes the placeholder "[PORT]" in it.')