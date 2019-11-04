import collections
import re

from typing import List, Union
from urllib.parse import unquote

import phonenumbers

from phonenumbers import PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException

from .country import dialing_prefix_for_region


def _is_valid(phone_number: str, dialing_prefix: str) -> bool:
    """Gets whether the specified phone number is a valid one."""
    try:
        parsed_number = phonenumbers.parse(phone_number, region=dialing_prefix)
        if phonenumbers.is_possible_number(parsed_number) is True:
            return True

        if phonenumbers.is_valid_number(parsed_number) is True:
            return True
    except NumberParseException:
        pass

    return False


def format_phone_number_list(
    phone_number: Union[str, int],
    implied_phone_region: str,
    fmt: PhoneNumberFormat = PhoneNumberFormat.E164,
) -> List[str]:
    """Formats/validates the specified phone number.

    This method will parse almost anything. You can throw crazy
    digits in-between, pass comma-separate values etc. It'll attempt
    everything it can to build a valid phone number from the input.

    In short, the strategy is like this:

        - Split string by comma, slash or space, and try every
          item.
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
        return []

    dialing_prefix = dialing_prefix_for_region(implied_phone_region) or ""

    valid_phone_numbers = collections.OrderedDict()
    for number in [
        phone_number,
        *re.split(r"/|,", phone_number),
        *phone_number.split(" "),
    ]:
        try:
            unquoted_number = unquote(number)
        except Exception:
            unquoted_number = number
        valid_numbers = []
        _append_valid_number(
            valid_numbers,
            unquoted_number.split("#", maxsplit=1)[0],
            dialing_prefix,
            fmt,
        )
        _append_valid_number(
            valid_numbers,
            unquoted_number.split(":", maxsplit=1)[0],
            dialing_prefix,
            fmt,
        )

        cleaned_number = "".join(re.findall("[0-9+]+", unquoted_number))
        _append_valid_number(valid_numbers, cleaned_number, dialing_prefix, fmt)
        _append_valid_number(
            valid_numbers, "+%s" % cleaned_number, dialing_prefix, fmt
        )
        if cleaned_number.startswith("00"):
            _append_valid_number(
                valid_numbers,
                "+%s" % cleaned_number.replace("00", "", 1),
                dialing_prefix,
                fmt,
            )
        if len(valid_numbers) == 0 and not _is_already_contained(
            valid_phone_numbers, cleaned_number
        ):
            _append_valid_number(
                valid_numbers,
                "%s%s" % (dialing_prefix, cleaned_number),
                dialing_prefix,
                fmt,
            )
            if len(valid_numbers) == 0:
                _append_valid_number(
                    valid_numbers,
                    "%s%s" % (dialing_prefix, cleaned_number[1:]),
                    dialing_prefix,
                    fmt,
                )
            if len(valid_numbers) == 0:
                _append_valid_number(
                    valid_numbers,
                    "%s%s" % (dialing_prefix, cleaned_number[2:]),
                    dialing_prefix,
                    fmt,
                )

        for valid_number in valid_numbers:
            valid_phone_numbers[valid_number] = valid_number

    return list(valid_phone_numbers.keys())


def _append_valid_number(
    valid_numbers: list,
    variant: str,
    dialing_prefix: str,
    fmt: PhoneNumberFormat = PhoneNumberFormat.E164,
) -> None:
    if not _is_valid(variant, dialing_prefix):
        return None
    phone_number = str(
        phonenumbers.format_number(phonenumbers.parse(variant), fmt)
    )
    if len(phone_number) <= 16:
        valid_numbers.append(phone_number)


def _is_already_contained(
    valid_phone_numbers: collections.OrderedDict, cleaned_number: str
) -> bool:
    for key in valid_phone_numbers.keys():
        if cleaned_number in key:
            return True
    return False


__all__ = ["format_phone_number_list"]
