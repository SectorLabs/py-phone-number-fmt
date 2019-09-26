import re

from typing import Optional, Union
from urllib.parse import unquote

import phonenumbers

from phonenumbers import PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException

from .country import dialing_prefix_for_region


def _is_valid(phone_number: str) -> bool:
    """Gets whether the specified phone number is a valid one."""
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_possible_number(parsed_number) is True:
            return True

        if phonenumbers.is_valid_number(parsed_number) is True:
            return True
    except NumberParseException:
        pass

    return False


def format_phone_number(
    phone_number: Union[str, int],
    implied_phone_region: str,
    fmt: PhoneNumberFormat = PhoneNumberFormat.E164,
) -> Optional[str]:
    """Formats/validates the specified phone number.

    This method will parse almost anything. You can throw crazy
    digits in-between, pass comma-separate values etc. It'll attempt
    everything it can to build a valid phone number from the input.

    In short, the strategy is like this:

        - Split string by comma and slash, and try every
          item until a valid one is found.
          (Helpful in case the user tried to enter multiple
          in a single field, we'll take the first valid one)
        - Remove everything except numbers and +
        - Attempt validation as is
        - Attempt validation with configured dialing code in front
          (This helps in case its a local number)
        - Attempt adding a leading +
          (This helps in case the user forgot a +)
        - Attempt validation by removing first digit, and then
          adding the dialing code.
          (This helps if we have a leading zero which implies
           the current country's dialing prefix)
        - Attempt validation by removing first two digits and then
          adding the dialing code.
          (This helps if we have two leading zeroes which
          implies the current country's dialing prefix)

    Under the hood, this uses Google's libphonenumber. If this
    method doesn't find a phone number valid, then it must really
    not be a valid number.
    """
    phone_number = str(phone_number)

    if not phone_number or len(phone_number) < 3:
        return None

    dialing_prefix = dialing_prefix_for_region(implied_phone_region) or ""

    variants = []
    for number in [phone_number, *re.split("/|,", phone_number)]:
        try:
            unquoted_number = unquote(number)
        except Exception:
            unquoted_number = number

        variants.append(unquoted_number.split("#", maxsplit=1)[0])
        variants.append(unquoted_number.split(":", maxsplit=1)[0])

        cleaned_number = "".join(re.findall("[0-9+]+", unquoted_number))
        variants.append(cleaned_number)
        variants.append("+%s" % cleaned_number)
        if cleaned_number.startswith("00"):
            variants.append("+%s" % cleaned_number.replace("00", "", 1))
        variants.append("%s%s" % (dialing_prefix, cleaned_number))
        variants.append("%s%s" % (dialing_prefix, cleaned_number[1:]))
        variants.append("%s%s" % (dialing_prefix, cleaned_number[2:]))

    for variant in variants:
        if not _is_valid(variant):
            continue

        phone_number = str(
            phonenumbers.format_number(phonenumbers.parse(variant), fmt)
        )

        if len(phone_number) <= 16:
            return phone_number

    return None


__all__ = ["format_phone_number"]
