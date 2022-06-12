from hashlib import md5
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_avatar_url(context, user=None, email=None, size=None, default="mp"):
    """Get a gravatar image url.
    If no image is found, gravatar will return an image based on the 'default'
    keyword. See http://en.gravatar.com/site/implement/images/ for more info.

    This function will get the profile email in this order:
        The 'email' argument,
        The 'user' argument if it has an 'email' attribute,

    NOTE: Method does not work if context is not taken in despite it not using it.
    """
    if not size:
        size = 25

    email = email or ""

    if not email and user and hasattr(user, "email"):
        email = user.email or ""
    return "https://www.gravatar.com/avatar/{hash}?s={size}&d={default}".format(
        hash=md5(email.encode("utf-8")).hexdigest(),
        size=size or "",
        default=default,
    )
