import pytest

from phonenumberfmt import format_phone_number
from phonenumberfmt.country import dialing_prefix_for_region


@pytest.mark.parametrize("phone_region", ["AE", "PK", "SA", "JO"])
@pytest.mark.parametrize(
    "input,output",
    [
        # empty phone numbers
        (None, None),
        ("-", None),
        ("--", None),
        ("No", None),
        ("", None),
        # phone number without a country prefix
        ("55-4396334", "PREFIX554396334"),
        ("+55-6934369", "PREFIX556934369"),
        ("5(5-4(//39(63)3--4", "PREFIX554396334"),
        # some crazy combos
        ("+40773818041", "+40773818041"),
        ("+31318655336", "+31318655336"),
        ("+97172273000", "+97172273000"),
        ("+92238923892", "+92238923892"),
        ("+40773818041/+97172273000", "+40773818041"),
        ("+40773818041 / +97172273000", "+40773818041"),
        ("+971-50-1896203", "+971501896203"),
        ("+971(0)508882395", "+971508882395"),
        ("+971-50-1003023 / +971-558683397", "+971501003023"),
        ("971-50-1896203", "+971501896203"),
        ("+92 321 9224895", "+923219224895"),
        ("+971-50-2516838, +971- 55-4396334/ 6934365", "+971502516838"),
        ("////////+40773818041", "+40773818041"),
        ("1234/    +40773818041", "+40773818041"),
        ("+.4.0.7.7.3.8.1.8.0.4.1++++++++++", "+40773818041"),
        ("40773818041", "+40773818041"),
        ("971501230869", "+971501230869"),
        ("00962799506073", "+962799506073"),
        ("00971529010000", "+971529010000"),
        ("%2b97144298820", "+97144298820"),
        ("+97144220125#40,+971503292710#40", "+97144220125"),
        ("+97144220125:40,+971503292710:40", "+97144220125"),
        ("+92-3002125421 +92-312-8222973", "+923002125421"),
    ],
)
def test_format_phone_number(phone_region, input, output):
    data = format_phone_number(input, implied_phone_region=phone_region)

    localized_output = (output or "").replace(
        "PREFIX", dialing_prefix_for_region(phone_region)
    )
    assert data == (localized_output or None)
