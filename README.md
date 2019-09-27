# py-phone-number-fmt

[![License](https://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
[![PyPi](https://badge.fury.io/py/py-phone-number-fmt.svg)](https://pypi.python.org/pypi/py-phone-number-fmt)
[![CircleCI](https://circleci.com/gh/SectorLabs/py-phone-number-fmt/tree/master.svg?style=svg&circle-token=134c614a21ff3a5ca674d34d67d3b65b429b86d8)](https://circleci.com/gh/SectorLabs/py-phone-number-fmt/tree/master)

Sanitize, validate and format phone numbers into E.164 valid phone numbers.

Google's libphonenumber on steroids. Tries all sorts of crazy combinations in an attempt to create a valid phone number. Useful for those of us who have to deal with poorly sanitized data.

[See the list of test cases](./tests/test_format_phone_number.py)

## Installation

    $ pip install py-phone-number-fmt

## Usage

    from phonenumberfmt import format_phone_number

    # implied phone region is the country of which to
    # use the dialing prefix in case the number appears
    # to be local
    result = format_phone_number('778\173 0.92', implied_phone_region='RO')
    assert result == '+40778173092'

The resulting phone number will be formatted according to the E.164 standard. Want to change the output format? Pass the third, optional parameter `fmt` with a valid member of `phonenumbers.NumberFormat`:

    from phonenumbers import NumberFormat
    result = format_phone_number(
        '778\173 0.92',
        implied_phone_region='RO',
        fmt=NumberFormat.INTERNATIONAL, # default is NumberFormat.E164
    )
