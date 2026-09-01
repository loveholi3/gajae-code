#!/usr/bin/env python3
"""U10 regression tests - phase0 reddit fetcher error handling

Tests the error handling and happy paths for the Reddit router in phase0.py,
specifically focusing on the RSS and JSON routes and ensuring exceptions are
caught and properly logged in the attempts array.

Run:  python3 engine/tests/test_u10.py
"""
from __future__ import annotations

import os
import sys
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)

from engine import phase0

# ---------------------------------------------------------------------------
# Mock classes for _cffi_get responses
# ---------------------------------------------------------------------------

class MockResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


def t_reddit_rss_success() -> None:
    # Test that a successful RSS fetch returns immediately.
    rss_resp = MockResponse(200, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<feed>\n</feed>")

    with mock.patch.object(phase0, "_cffi_get", return_value=rss_resp) as mock_get:
        res = phase0._reddit("https://www.reddit.com/r/python", timeout=5)

    assert res["ok"] is True
    assert res["route"] == "rss"
    assert len(res["attempts"]) == 1
    assert res["attempts"][0]["route"] == "rss"
    assert res["attempts"][0]["ok"] is True
    print("  ✓ reddit RSS happy path works correctly")


def t_reddit_rss_exception_json_success() -> None:
    # Test when RSS throws an exception, it should fall back to JSON.
    json_resp = MockResponse(200, '{"data": "success"}')

    def mock_cffi_get_side_effect(url, timeout):
        if url.endswith(".rss"):
            raise ConnectionError("Connection reset by peer")
        elif url.endswith(".json"):
            return json_resp
        return MockResponse(404, "")

    with mock.patch.object(phase0, "_cffi_get", side_effect=mock_cffi_get_side_effect) as mock_get:
        res = phase0._reddit("https://www.reddit.com/r/python", timeout=5)

    assert res["ok"] is True
    assert res["route"] == "json"
    assert len(res["attempts"]) == 2

    # First attempt: RSS exception
    assert res["attempts"][0]["route"] == "rss"
    assert res["attempts"][0]["ok"] is False
    assert res["attempts"][0]["note"] == "ConnectionError"

    # Second attempt: JSON success
    assert res["attempts"][1]["route"] == "json"
    assert res["attempts"][1]["ok"] is True
    assert res["attempts"][1]["note"] == "json"
    print("  ✓ reddit RSS exception falls back to JSON successfully")


def t_reddit_rss_fails_json_exception() -> None:
    # Test when RSS fails (e.g. 403) and JSON throws an exception.
    # This specifically targets the issue "Missing error handling tests for reddit json fetch".
    rss_resp = MockResponse(403, "Forbidden")

    def mock_cffi_get_side_effect(url, timeout):
        if url.endswith(".rss"):
            return rss_resp
        elif url.endswith(".json"):
            raise TimeoutError("Read timed out")
        return MockResponse(404, "")

    with mock.patch.object(phase0, "_cffi_get", side_effect=mock_cffi_get_side_effect) as mock_get:
        res = phase0._reddit("https://www.reddit.com/r/python", timeout=5)

    assert res["ok"] is False
    assert res["route"] is None
    assert len(res["attempts"]) == 2

    # First attempt: RSS failure (not an exception, just 403)
    assert res["attempts"][0]["route"] == "rss"
    assert res["attempts"][0]["ok"] is False
    assert res["attempts"][0]["note"] == "no-feed-markers"

    # Second attempt: JSON exception
    assert res["attempts"][1]["route"] == "json"
    assert res["attempts"][1]["ok"] is False
    assert res["attempts"][1]["note"] == "TimeoutError"
    print("  ✓ reddit JSON exception is caught and recorded properly")


ALL = [
    ("reddit_rss_success", t_reddit_rss_success),
    ("reddit_rss_exception_json_success", t_reddit_rss_exception_json_success),
    ("reddit_rss_fails_json_exception", t_reddit_rss_fails_json_exception),
]


def main() -> int:
    p = f = 0
    for name, fn in ALL:
        try:
            print(f"[{name}]")
            fn()
            p += 1
        except AssertionError as e:
            f += 1
            print(f"  ✗ FAIL: {e}")
        except Exception as e:
            f += 1
            print(f"  ✗ ERROR: {type(e).__name__}: {e}")
    print(f"\n{p} passed, {f} failed")
    return 0 if f == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
