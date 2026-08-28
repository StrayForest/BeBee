#!/usr/bin/env python3
"""Serve locally built BeBee HTML5 bundles with browser-correct MIME types."""

from __future__ import annotations

import argparse
import functools
import http.server
import mimetypes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        type=Path,
        default=ROOT / "build" / "html5",
        help="Directory containing development/ and release/ HTML5 bundle roots.",
    )
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    directory = args.directory.expanduser().resolve()
    if not directory.is_dir():
        raise SystemExit(f"HTML5 serve directory does not exist: {directory}")

    mimetypes.add_type("application/wasm", ".wasm")
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(directory),
    )
    server = http.server.ThreadingHTTPServer((args.bind, args.port), handler)
    print(
        f"Serving BeBee HTML5 from {directory} at http://{args.bind}:{args.port}/",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
