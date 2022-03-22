from re import fullmatch
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address

def validate_domain_or_ipv4(value):
    # Match domains with at least two levels containing alphabetical charectors, numbers, and hyphens
    if fullmatch(r"^([a-zA-Z1-9-]+\.)+[a-zA-Z1-9-]+$", value) is None:
        try:
            validate_ipv4_address(value)
        except ValidationError:
            raise ValidationError("Enter a valid IPv4 address or domain.")


def validate_query(value):
    if "[PORT]" not in value:
        raise ValidationError('Enter a query command that includes the placeholder "[PORT]" in it.')


def validate_regex_capture_groups(value):
    ommitted_charectors = ['^', '$']

    signs = []
    escaped = False
    for char in value:
        if escaped is True:
            escaped = False
            continue

        if char == '\\':
            escaped = True
        elif char == '(':
            signs.append(char)
        elif char == ')':
            if len(signs) > 0:
                del signs[-1]
            else:
                raise ValidationError("Capture groups must match in your regex.")

        elif char in ommitted_charectors:
            raise ValidationError(f"Your regex may not contain these charectors: {ommitted_charectors.join(', ')}")

    if len(signs) != 0:
        raise ValidationError("Capture groups must match in your regex.")


def validate_regex_capture_detail(value):
    if value.count("(") - value.count("\(") != 4:
        raise ValidationError('Exactly four capture groups must be defined in your regex.')

    if "?P<input_data>" not in value or "?P<output_data>" not in value:
        raise ValidationError("Your query regex must include '?P<input_data>' and '?P<output_data>' in the start of your data capture groups.")

    if "?P<input_unit>" not in value or "?P<output_unit>" not in value:
        raise ValidationError("Your query regex must include '?P<input_unit>' and '?P<output_unit>' in the start of your unit capture groups.")
