from sherlock_ai.utils.request_context import (
    set_request_id,
    get_request_id,
    clear_request_id,
)


class TestRequestContext:
    def setup_method(self):
        """Reset context before every test to prevent cross-test leakage."""
        clear_request_id()

    def test_get_returns_empty_string_before_any_set(self):
        clear_request_id()
        assert get_request_id() == ""

    def test_set_without_argument_generates_id(self):
        req_id = set_request_id()
        assert req_id != ""

    def test_set_without_argument_generates_8_char_id(self):
        req_id = set_request_id()
        assert len(req_id) == 8

    def test_get_returns_id_after_set(self):
        set_request_id()
        assert get_request_id() != ""

    def test_set_with_custom_id_returns_that_id(self):
        req_id = set_request_id("custom-id-123")
        assert req_id == "custom-id-123"

    def test_get_returns_custom_id_after_set(self):
        set_request_id("my-request-id")
        assert get_request_id() == "my-request-id"

    def test_subsequent_set_overwrites_previous_id(self):
        set_request_id("first-id")
        set_request_id("second-id")
        assert get_request_id() == "second-id"

    def test_clear_resets_to_empty_string(self):
        set_request_id("some-id")
        clear_request_id()
        assert get_request_id() == ""

    def test_set_returns_the_value_that_get_retrieves(self):
        returned = set_request_id()
        retrieved = get_request_id()
        assert returned == retrieved

    def test_auto_generated_ids_are_unique(self):
        id1 = set_request_id()
        clear_request_id()
        id2 = set_request_id()
        # UUIDs are random; collision is astronomically unlikely
        assert id1 != id2

    def test_clear_is_idempotent(self):
        clear_request_id()
        clear_request_id()
        assert get_request_id() == ""