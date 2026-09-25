from backend.core.rate_limit import RateLimit, RateLimiter


def test_limit_and_window() -> None:
    limiter = RateLimiter(RateLimit(2, 10))
    assert limiter.allow("task", now=100.0)
    assert limiter.allow("task", now=101.0)
    assert not limiter.allow("task", now=102.0)
    assert limiter.allow("task", now=110.0)


def test_keys_are_isolated_and_resettable() -> None:
    limiter = RateLimiter(RateLimit(1, 10))
    assert limiter.allow("a", now=1.0)
    assert limiter.allow("b", now=1.0)
    assert not limiter.allow("a", now=2.0)
    limiter.reset("a")
    assert limiter.allow("a", now=2.0)


def test_invalid_key_fails_closed() -> None:
    limiter = RateLimiter(RateLimit(1, 10))
    assert not limiter.allow("")
    assert not limiter.allow("x" * 257)
