"""
Integration tests for FastAPI routes with sherlock_ai middleware and decorators.
Uses FastAPI's built-in TestClient (no live server required).
"""

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from sherlock_ai import get_logger, set_request_id, log_performance, monitor_memory, monitor_resources
from sherlock_ai.config.logging import LoggingConfig
from sherlock_ai import SherlockAI


# ── App factory fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def app(tmp_path_factory):
    """
    Create a minimal FastAPI app wired with sherlock_ai middleware and
    representative decorated routes — mirrors real-world usage without
    coupling to any specific file in the project.
    """
    # Set up logging to a temp dir so tests don't pollute logs/
    logs_dir = str(tmp_path_factory.mktemp("logs"))
    config = LoggingConfig(logs_dir=logs_dir, auto_instrument=False)
    instance = SherlockAI(config=config)
    instance.setup()

    logger = get_logger("TestApiLogger")
    _app = FastAPI()

    @_app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        req_id = set_request_id()
        request.state.request_id = req_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response

    @_app.get("/health")
    async def health():
        logger.info("Health check called")
        return {"status": "ok"}

    @_app.get("/echo")
    async def echo(message: str):
        return {"echo": message}

    @_app.get("/error")
    async def trigger_error():
        raise ValueError("intentional test error")

    @_app.get("/performance")
    @log_performance
    async def performance_route():
        return {"result": "measured"}

    @_app.get("/memory")
    @monitor_memory
    async def memory_route():
        data = list(range(1000))
        return {"count": len(data)}

    @_app.get("/resources")
    @monitor_resources
    async def resources_route():
        return {"resources": "tracked"}

    yield _app
    instance.cleanup()


@pytest.fixture(scope="module")
def client(app):
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


# ── /health ────────────────────────────────────────────────────────────────────

class TestHealthRoute:
    def test_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_returns_ok_status(self, client):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}

    def test_response_has_request_id_header(self, client):
        response = client.get("/health")
        assert "x-request-id" in response.headers

    def test_request_id_header_is_not_empty(self, client):
        response = client.get("/health")
        assert response.headers["x-request-id"] != ""

    def test_each_request_gets_unique_request_id(self, client):
        r1 = client.get("/health")
        r2 = client.get("/health")
        assert r1.headers["x-request-id"] != r2.headers["x-request-id"]


# ── /echo ──────────────────────────────────────────────────────────────────────

class TestEchoRoute:
    def test_returns_200(self, client):
        response = client.get("/echo", params={"message": "hello"})
        assert response.status_code == 200

    def test_echoes_provided_message(self, client):
        response = client.get("/echo", params={"message": "sherlock"})
        assert response.json() == {"echo": "sherlock"}

    def test_echoes_special_characters(self, client):
        response = client.get("/echo", params={"message": "hello world 123"})
        assert response.json()["echo"] == "hello world 123"

    def test_missing_message_param_returns_422(self, client):
        response = client.get("/echo")
        assert response.status_code == 422


# ── /error ─────────────────────────────────────────────────────────────────────

class TestErrorRoute:
    def test_returns_500(self, client):
        response = client.get("/error")
        assert response.status_code == 500

    def test_response_still_has_request_id_header(self, client):
        response = client.get("/error")
        # Middleware runs before the error — header should still be set
        assert "x-request-id" in response.headers


# ── /performance (log_performance decorator) ───────────────────────────────────

class TestPerformanceRoute:
    def test_returns_200(self, client):
        response = client.get("/performance")
        assert response.status_code == 200

    def test_returns_expected_body(self, client):
        response = client.get("/performance")
        assert response.json() == {"result": "measured"}

    def test_response_has_request_id_header(self, client):
        response = client.get("/performance")
        assert "x-request-id" in response.headers


# ── /memory (monitor_memory decorator) ────────────────────────────────────────

class TestMemoryRoute:
    def test_returns_200(self, client):
        response = client.get("/memory")
        assert response.status_code == 200

    def test_returns_correct_count(self, client):
        response = client.get("/memory")
        assert response.json() == {"count": 1000}


# ── /resources (monitor_resources decorator) ──────────────────────────────────

class TestResourcesRoute:
    def test_returns_200(self, client):
        response = client.get("/resources")
        assert response.status_code == 200

    def test_returns_expected_body(self, client):
        response = client.get("/resources")
        assert response.json() == {"resources": "tracked"}


# ── Middleware behaviour ───────────────────────────────────────────────────────

class TestMiddleware:
    def test_all_routes_inject_request_id_header(self, client):
        routes = ["/health", "/echo?message=x", "/performance", "/memory", "/resources"]
        for route in routes:
            response = client.get(route)
            assert "x-request-id" in response.headers, f"Missing header on {route}"

    def test_request_ids_are_8_characters(self, client):
        response = client.get("/health")
        req_id = response.headers["x-request-id"]
        assert len(req_id) == 8, f"Expected 8-char ID, got: {req_id!r}"

    def test_concurrent_requests_produce_different_ids(self, client):
        ids = {client.get("/health").headers["x-request-id"] for _ in range(5)}
        assert len(ids) == 5, "Expected all request IDs to be unique"