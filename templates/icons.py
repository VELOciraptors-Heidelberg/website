"""
Icon lookup for social media links in the header.

To support a new platform: add a new "platform-name": "<svg>...</svg>"
entry below. If a site.yml entry uses a platform name that isn't listed
here, it automatically falls back to the generic ICONS["website"] icon
instead of breaking the build.
"""

ICONS = {
    "instagram": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
        '<circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/>'
        '<circle cx="17.2" cy="6.8" r="1.1" fill="currentColor"/>'
        "</svg>"
    ),
    "facebook": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<circle cx="12" cy="12" r="10" fill="currentColor"/>'
        '<path d="M13.5 21v-7h2.3l.35-2.7h-2.65V9.6c0-.78.22-1.3 1.33-1.3h1.42V5.9c-.25-.03-1.1-.1-2.1-.1-2.08 0-3.5 1.27-3.5 3.6v2h-2.35v2.7h2.35v7h2.85z" fill="#fff"/>'
        "</svg>"
    ),
    "whatsapp": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M12 2a10 10 0 0 0-8.66 15L2 22l5.2-1.36A10 10 0 1 0 12 2Z" fill="currentColor"/>'
        '<path d="M8.5 7.5c.3-.6.6-.6.9-.6h.6c.2 0 .5 0 .7.5.3.6.9 2 1 2.1.1.2.1.4 0 .6-.1.2-.2.3-.4.5-.2.2-.4.4-.2.7.2.3.9 1.5 2 2.4 1.4 1.2 2.1 1.4 2.4 1.5.3.1.5.1.7-.1.2-.2.8-.9 1-1.2.2-.3.4-.2.7-.1.3.1 1.9.9 2.2 1.1.3.1.5.2.6.4.1.2.1 1-.3 1.9-.4.9-2.1 1.7-2.9 1.8-.7.1-1.6.2-5-1.2-4.1-1.7-6.6-6-6.8-6.3-.2-.3-1.6-2.1-1.6-4 0-1.9 1-2.8 1.3-3.2Z" fill="#fff"/>'
        "</svg>"
    ),
    "strava": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M10.5 2 4 14h4.2l2.3-4.3L12.8 14H17L10.5 2Z" fill="currentColor"/>'
        '<path d="M13.2 14.4 11 18.6l-2.2-4.2H5l6 9.6 6-9.6h-3.8Z" fill="currentColor" opacity="0.55"/>'
        "</svg>"
    ),
    "komoot": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M12 2c-4.1 0-7.5 3.4-7.5 7.5C4.5 15.5 12 22 12 22s7.5-6.5 7.5-12.5C19.5 5.4 16.1 2 12 2Z" fill="currentColor"/>'
        '<circle cx="12" cy="9.3" r="2.6" fill="#fff"/>'
        "</svg>"
    ),
    "youtube": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<rect x="2" y="5" width="20" height="14" rx="4" fill="currentColor"/>'
        '<path d="M10 8.5v7l6-3.5-6-3.5Z" fill="#fff"/>'
        "</svg>"
    ),
    "tiktok": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M14 3v10.2a3.3 3.3 0 1 1-2-3V3h2Z" fill="currentColor"/>'
        '<path d="M14 3c.3 2 1.8 3.5 3.8 3.7V9c-1.5-.1-2.8-.6-3.8-1.4V3Z" fill="currentColor"/>'
        "</svg>"
    ),
    "website": (
        '<svg viewBox="0 0 24 24" aria-hidden="true">'
        '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/>'
        '<path d="M3 12h18M12 3c2.5 2.5 2.5 15.5 0 18M12 3c-2.5 2.5-2.5 15.5 0 18" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        "</svg>"
    ),
}


def get_icon(platform):
    return ICONS.get((platform or "").strip().lower(), ICONS["website"])
