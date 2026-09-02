import bleach
import markdown as md

ALLOWED_TAGS = [
    "p", "br", "hr", "h1", "h2", "h3", "h4", "strong", "em",
    "ul", "ol", "li", "blockquote", "code", "pre", "a", "img",
    "table", "thead", "tbody", "tr", "th", "td",
]

ALLOWED_ATTRS = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title", "loading"],
}


def render_markdown(body_markdown: str) -> str:
    """Render post markdown to sanitized HTML.
    Sanitization runs after markdown rendering, not instead of it,
    because an author-authored post can still contain raw HTML inside
    markdown (a deliberate markdown feature), and that HTML must be
treated as untrusted input exactly like any other user-submitted
HTML would be.
"""
    raw_html = md.markdown(body_markdown, extensions=["fenced_code","tables","toc"],
                           )
    return bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )