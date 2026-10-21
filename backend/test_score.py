from score import calculate_score


def test_equivalent_skill_names_match():
    result = calculate_score(
        ["ReactJS", "RESTAPIs", "Python"],
        ["React", "REST API", "Docker"],
    )

    assert result["matched"] == ["react", "rest"]
    assert result["missing"] == ["docker"]
    assert result["score"] == 67


def test_structured_query_language_matches_sql():
    result = calculate_score(
        ["SQL"],
        ["Structured Query Language"],
    )

    assert result["matched"] == ["sql"]
    assert result["missing"] == []
    assert result["score"] == 100


def test_empty_required_skills():
    result = calculate_score(["Python"], [])

    assert result == {
        "score": 0,
        "matched": [],
        "missing": [],
    }

if __name__ == "__main__":
    result = calculate_score(
        ["ReactJS", "RESTAPIs", "Python"],
        ["React", "REST API", "Docker"],
    )
    print(result)