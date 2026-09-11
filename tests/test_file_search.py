import pytest
from agent.file_search import find_file, search_file


@pytest.fixture
def filepath(tmp_path):
    file = tmp_path / "langgraph.txt"
    file.write_text("hello \n Langgraph is great tool. \n checking tools")
    return file


def test_search_file(filepath):
    result = search_file(file_path=filepath, query="langgraph")
    assert len(result) > 0
    assert "langgraph" in result[0]["snippet"].lower()


def test_search_lineno(filepath):
    result = search_file(file_path=filepath, query="langgraph")
    assert result[0]["line"] == 2


def test_search_results_notfound(filepath):
    result = search_file(file_path=filepath, query="langchain")
    assert result == "query not found in given file"


def test_search_case_insensitive(filepath):
    result = search_file(filepath, "LANGGRAPH")

    assert len(result) > 0


def test_found_file():
    results = find_file("dummy_search")
    assert results["status"] == "found"
    assert len(results["matches"]) == 1
    assert "dummy_search" in results["matches"][0]


def test_found_multi_file():
    results = find_file("agent")
    assert results["status"] == "multiple_matches"
    assert len(results["matches"]) > 1
    assert all("agent" in path.lower() for path in results["matches"])


def test_notfound_file():
    results = find_file("missing_file")
    assert results["status"] == "not_found"
    assert results["matches"] == []
