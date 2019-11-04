from typing import Optional, Union

from phonenumbers import PhoneNumberFormat

from .format_phone_number_list import format_phone_number_list


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
    valid_phone_numbers = format_phone_number_list(
        phone_number, implied_phone_region, fmt
    )
    return valid_phone_numbers[0] if len(valid_phone_numbers) > 0 else None


__all__ = ["format_phone_number"]
