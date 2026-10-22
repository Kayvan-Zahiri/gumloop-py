from __future__ import annotations

import asyncio

import pytest

from gumloop import AsyncGumloop
from gumloop import Gumloop


@pytest.mark.parametrize(
    "base_url, expected",
    [
        ("https://api.gumloop.com/api/v1", "https://ws.gumloop.com/api/v1"),
        ("http://localhost:8080/api/v1", "http://localhost:9093/api/v1"),
        ("https://api.gumloop.com.example.test/api/v1", "https://api.gumloop.com.example.test/api/v1"),
        ("https://example.test/api.gumloop.com/v1", "https://example.test/api.gumloop.com/v1"),
        ("https://example.test/v1?target=api.gumloop.com", "https://example.test/v1?target=api.gumloop.com"),
        ("https://my-api.gumloop.com/v1", "https://my-api.gumloop.com/v1"),
        ("http://localhost:8080/path/localhost:8080", "http://localhost:9093/path/localhost:8080"),
        ("https://example.test/localhost:8080/v1", "https://example.test/localhost:8080/v1"),
        ("https://API.GUMLOOP.COM/api/v1", "https://ws.gumloop.com/api/v1"),
        ("http://LOCALHOST:8080/api/v1", "http://localhost:9093/api/v1"),
        ("https://example.test/api/v1", "https://example.test/api/v1"),
    ],
)
@pytest.mark.parametrize("asynchronous", [False, True])
def test_stream_url_derivation_uses_hostname_and_exact_port(
    monkeypatch: pytest.MonkeyPatch, base_url: str, expected: str, asynchronous: bool
) -> None:
    monkeypatch.delenv("GUMLOOP_STREAM_BASE_URL", raising=False)
    if asynchronous:

        async def run() -> None:
            async with AsyncGumloop(api_key="test", base_url=base_url) as client:
                assert client.stream_base_url == expected

        asyncio.run(run())
    else:
        with Gumloop(api_key="test", base_url=base_url) as client:
            assert client.stream_base_url == expected


@pytest.mark.parametrize("asynchronous", [False, True])
def test_explicit_stream_url_is_preserved(asynchronous: bool) -> None:
    url = "https://custom-stream.example.test/api.gumloop.com"
    if asynchronous:

        async def run() -> None:
            async with AsyncGumloop(api_key="test", stream_base_url=url) as client:
                assert client.stream_base_url == url

        asyncio.run(run())
    else:
        with Gumloop(api_key="test", stream_base_url=url) as client:
            assert client.stream_base_url == url
