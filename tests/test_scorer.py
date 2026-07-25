from analyzer.scorer import calculate_score


def test_score_returns_dictionary():

    result = calculate_score(
        {},
        {},
        {},
        {}
    )

    assert isinstance(result, dict)


def test_score_has_total():

    result = calculate_score(
        {},
        {},
        {},
        {}
    )

    assert "total" in result


def test_score_has_rating():

    result = calculate_score(
        {},
        {},
        {},
        {}
    )

    assert "rating" in result


def test_score_has_breakdown():

    result = calculate_score(
        {},
        {},
        {},
        {}
    )

    assert "breakdown" in result