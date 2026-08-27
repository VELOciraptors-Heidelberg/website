#!/usr/bin/env python3
"""
Builds the site for viewing on your own computer and serves it locally.

This always builds as if baseUrl were empty, regardless of what
data/site.yml currently has it set to for the real deployment — so this
command works the same way whether or not the site is set up for GitHub
Pages project-page hosting.

Run with:  python3 scripts/preview.py
Stop with: Ctrl+C
"""

import functools
import os
import socketserver
import sys
from http.server import SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

os.environ["SITE_BASE_URL"] = ""

import build  # noqa: E402

PORT = 8000


def main():
    build.main()

    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(ROOT / "public"))

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"\nPreview ready — open http://localhost:{PORT}/de/ (or /en/) in your browser.")
        print("Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
