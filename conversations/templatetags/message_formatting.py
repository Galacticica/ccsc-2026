from django import template
from django.template.defaultfilters import linebreaksbr
from django.utils.safestring import mark_safe

register = template.Library()

try:
    import bleach
    import markdown
except ImportError:  # pragma: no cover
    bleach = None
    markdown = None


ALLOWED_TAGS = [
    "a",
    "blockquote",
    "br",
    "code",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "ul",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "rel", "target", "title"],
    "code": ["class"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


@register.filter(name="render_markdown")
def render_markdown(value):
    text = (value or "").strip()
    if not text:
        return ""

    if markdown is None or bleach is None:
        return linebreaksbr(text)

    html = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
    )
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    linked = bleach.linkify(cleaned)
    return mark_safe(linked)
