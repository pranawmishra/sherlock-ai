import pytest
from unittest.mock import patch, PropertyMock
from sherlock_ai.analysis.code_analyzer import CodeAnalyzer


# ── CodeAnalyzer.detect_hardcoded_values ──────────────────────────────────────

class TestDetectHardcodedValues:
    """Tests for the static detect_hardcoded_values method.
    This is a pure function that takes source code as a string and returns findings.
    """

    def test_detects_string_constant(self):
        source = "def fn():\n    msg = 'Hello World'\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        values = [v for v, _, _ in results]
        assert "Hello World" in values

    def test_detects_integer_constant(self):
        source = "def fn():\n    timeout = 30\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        values = [v for v, _, _ in results]
        assert "30" in values

    def test_detects_float_constant(self):
        source = "def fn():\n    rate = 3.14\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        values = [v for v, _, _ in results]
        assert "3.14" in values

    def test_detects_url_constant(self):
        source = "def fn():\n    url = 'https://example.com'\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        url_results = [(v, t) for v, t, _ in results if t == "url"]
        assert any("https://example.com" in v for v, _ in url_results)

    def test_classifies_url_type_correctly(self):
        source = "url = 'https://api.example.com/endpoint'\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        assert any(t == "url" for _, t, _ in results)

    def test_classifies_plain_string_type_correctly(self):
        source = "msg = 'hello'\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        assert any(t == "string" for _, t, _ in results)

    def test_classifies_number_type_correctly(self):
        source = "n = 42\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        assert any(t == "number" for _, t, _ in results)

    def test_skips_zero(self):
        source = "def fn():\n    x = 0\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        values = [v for v, _, _ in results]
        assert "0" not in values

    def test_skips_empty_string(self):
        source = "x = ''\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        values = [v for v, _, _ in results]
        assert "" not in values

    def test_skips_dict_keys(self):
        source = "d = {'key': 'value'}\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        # 'key' is a dict key and should be skipped; 'value' is a regular string
        values = [v for v, _, _ in results]
        assert "key" not in values
        assert "value" in values

    def test_deduplicates_repeated_values(self):
        source = "a = 'hello'\nb = 'hello'\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        values = [v for v, _, _ in results]
        assert values.count("hello") == 1

    def test_returns_empty_list_for_no_constants(self):
        source = "def fn():\n    pass\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        assert results == []

    def test_returns_empty_list_for_syntax_error(self):
        source = "def fn(:\n    pass\n"  # invalid syntax
        results = CodeAnalyzer.detect_hardcoded_values(source)
        assert results == []

    def test_returns_empty_list_for_empty_source(self):
        results = CodeAnalyzer.detect_hardcoded_values("")
        assert results == []

    def test_multiple_constants_detected(self):
        source = "def fn():\n    a = 'foo'\n    b = 42\n    c = 'https://x.com'\n"
        results = CodeAnalyzer.detect_hardcoded_values(source)
        assert len(results) == 3


# ── CodeAnalyzer.suggest_constant_name (heuristic path) ───────────────────────

class TestSuggestConstantName:
    """Tests for the heuristic fallback in suggest_constant_name.
    Groq LLM is disabled via mock to test heuristic logic deterministically.
    """

    @pytest.fixture
    def analyzer(self):
        with patch(
            "sherlock_ai.providers.groq_provider.GroqProvider.enabled",
            new_callable=PropertyMock,
            return_value=False,
        ):
            instance = CodeAnalyzer()
            yield instance

    def test_string_value_produces_uppercase_name(self, analyzer):
        name = analyzer.suggest_constant_name("Hello World", "string")
        assert name == name.upper()
        assert "HELLO" in name

    def test_url_value_gets_url_prefix(self, analyzer):
        name = analyzer.suggest_constant_name("https://example.com", "url")
        assert name.startswith("URL_")

    def test_number_value_gets_num_prefix(self, analyzer):
        name = analyzer.suggest_constant_name("30", "number")
        assert name.startswith("NUM_")

    def test_result_is_at_most_30_chars(self, analyzer):
        long_value = "This is a very long string that exceeds thirty characters easily"
        name = analyzer.suggest_constant_name(long_value, "string")
        assert len(name) <= 30

    def test_result_contains_no_special_chars(self, analyzer):
        name = analyzer.suggest_constant_name("hello-world.api/v1", "string")
        import re
        assert re.match(r'^[A-Z0-9_]+$', name), f"Invalid chars in: {name}"

    def test_digit_leading_value_gets_const_prefix(self, analyzer):
        name = analyzer.suggest_constant_name("42abc", "number")
        # After uppercasing, leading digit should be handled
        assert not name[0].isdigit(), f"Name should not start with digit: {name}"

    def test_empty_value_falls_back_to_const_value(self, analyzer):
        name = analyzer.suggest_constant_name("", "string")
        assert name  # must return something non-empty