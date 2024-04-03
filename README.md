# py-phone-number-fmt

[![License](https://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
[![PyPi](https://badge.fury.io/py/py-phone-number-fmt.svg)](https://pypi.python.org/pypi/py-phone-number-fmt)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/SectorLabs/py-phone-number-fmt/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/SectorLabs/py-phone-number-fmt/tree/master)

Sanitize, validate and format phone numbers into E.164 valid phone numbers.

Google's libphonenumber on steroids. Tries all sorts of crazy combinations in an attempt to create a valid phone number. Useful for those of us who have to deal with poorly sanitized data.

[See the list of test cases](./tests/test_format_phone_number.py)

## Installation

    $ pip install py-phone-number-fmt

## Usage

### Retrieve first valid number
    from phonenumberfmt import format_phone_number

    # implied phone region is the country of which to
    # use the dialing prefix in case the number appears
    # to be local
    result = format_phone_number('778\173 0.92', implied_phone_region='RO')
    assert result == '+40778173092'

### Retrieve all valid numbers
    # implied phone region is the country of which to
    # use the dialing prefix in case the number appears
    # to be local
    result = format_phone_number_list('+40773818041 / +97172273000', implied_phone_region='RO')
    assert result == ['+40778173092', '+97172273000']

The resulting phone number will be formatted according to the E.164 standard. Want to change the output format? Pass the third, optional parameter `fmt` with a valid member of `phonenumbers.NumberFormat`:

    from phonenumbers import NumberFormat
    result = format_phone_number(
        '778\173 0.92',
        implied_phone_region='RO',
        fmt=NumberFormat.INTERNATIONAL, # default is NumberFormat.E164
    )
