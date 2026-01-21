from django import template
import math

register = template.Library()

@register.filter
def stars_from_10(value):
    """
    παίρνει rating 0-10 και επιστρέφει dict:
    full, half, empty για 5 αστέρια
    """
    if value is None:
        return {"full": 0, "half": 0, "empty": 5}

    try:
        v = float(value)
    except (TypeError, ValueError):
        return {"full": 0, "half": 0, "empty": 5}

    # μετατροπή 10-άρι -> 5-άρι
    x = max(0, min(5, v / 2.0))

    full = int(math.floor(x))
    half = 1 if (x - full) >= 0.5 else 0
    empty = 5 - full - half

    return {"full": full, "half": half, "empty": empty}