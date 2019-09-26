from typing import Optional

import phonenumbers


def dialing_code_for_region(phone_region: str) -> Optional[str]:
    """Gets the dialing code for the specified region.

    The dialing code is not the same as the dialing prefix.
    The dialing code is without the '+'. For example '971' for
    the UAE.

    Arguments:
        phone_region:
            Country code as defined by ISO 3166-1 alpha-2.

    Returns:
        The dialing code for the specified region.
    """
    return phonenumbers.country_code_for_region(phone_region) or None


def dialing_prefix_for_region(phone_region: str) -> Optional[str]:
    """Gets the dialing prefix for the specified region.

    The dialing prefix is the dialing code prefixed by '+'

    Arguments:
        phone_region:
            Country code as defined by ISO 3166-1 alpha-2.

    Returns:
        The dialing prefix for the specified region, example
        of a returned dialing code: '+971'.
    """
    dialing_code = dialing_code_for_region(phone_region)
    if not dialing_code:
        return None

    return "+%s" % dialing_code
