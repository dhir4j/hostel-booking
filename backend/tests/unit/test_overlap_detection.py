from datetime import date
from app.utils.dates import ranges_overlap

def d(s): return date.fromisoformat(s)

def test_overlap_middle():
    assert ranges_overlap(d('2024-01-01'), d('2024-01-10'), d('2024-01-05'), d('2024-01-15'))

def test_overlap_contained():
    assert ranges_overlap(d('2024-01-01'), d('2024-01-20'), d('2024-01-05'), d('2024-01-10'))

def test_no_overlap_before():
    assert not ranges_overlap(d('2024-01-01'), d('2024-01-05'), d('2024-01-05'), d('2024-01-10'))

def test_no_overlap_after():
    assert not ranges_overlap(d('2024-01-10'), d('2024-01-20'), d('2024-01-01'), d('2024-01-10'))

def test_no_overlap_gap():
    assert not ranges_overlap(d('2024-01-01'), d('2024-01-05'), d('2024-01-06'), d('2024-01-10'))

def test_same_day_exclusive():
    # half-open [start, end): a_end==b_start means no overlap
    assert not ranges_overlap(d('2024-01-01'), d('2024-01-05'), d('2024-01-05'), d('2024-01-08'))
