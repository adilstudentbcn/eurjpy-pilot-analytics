from pilot_analytics.brief import generate_niche_brief
from pilot_analytics.funnel import calculate_funnel_dropoff


class FakeFrame:
    def __init__(self, rows):
        self.rows = rows

    def iterrows(self):
        return enumerate(self.rows)


def test_calculate_funnel_dropoff():
    frame = FakeFrame(
        [
            {"stage": "Visited", "users": 1000},
            {"stage": "Signed Up", "users": 500},
            {"stage": "Traded", "users": 100},
        ]
    )

    result = calculate_funnel_dropoff(frame)

    assert result["Signed Up"]["conversion_rate"] == 0.50
    assert result["Traded"]["conversion_rate"] == 0.20


def test_generate_niche_brief():
    brief = generate_niche_brief({"name": "EUR/JPY Day Trader", "pain_point": "High spread costs"})

    assert "EUR/JPY Day Trader" in brief
    assert "Pain Point: High spread costs" in brief
    assert "Target Audience" in brief
