#!/usr/bin/env python3
"""Serve BeBee HTML5 bundles locally with an explicit WebAssembly MIME type."""

from __future__ import annotations

import argparse
import functools
import http.server
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BeBeeHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".wasm": "application/wasm",
    }

    def do_GET(self) -> None:
        # Chromium requests a root favicon even when the Defold template does not
        # declare one. Keep that browser chrome request out of QA console evidence
        # without masking any game/bundle resource path.
        if self.path.split("?", 1)[0] == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT / "build" / "html5",
        help="Directory to serve. Defaults to build/html5 so development and release are both reachable.",
    )
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"HTML5 serve root does not exist: {root}")
    if not 0 <= args.port <= 65535:
        raise SystemExit("--port must be between 0 and 65535")

    handler = functools.partial(BeBeeHandler, directory=str(root))
    with http.server.ThreadingHTTPServer((args.bind, args.port), handler) as server:
        host, port = server.server_address[:2]
        print(f"Serving {root} at http://{host}:{port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
