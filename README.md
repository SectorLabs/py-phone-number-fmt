# py-phone-number-fmt

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
