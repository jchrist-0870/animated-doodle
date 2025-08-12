from claims_finder.scoring import compute_score

def test_compute_score_basics():
    row = {
        'annual_maintenance_years': 5,
        'km_to_producer': 1.0,
        'km_to_occurrence': 2.0,
        'commodity': 'Gold',
        'asking_price': 1000.0
    }
    s = compute_score(row, focus_commodities=['Gold'])
    assert 0.0 <= s <= 1.0
