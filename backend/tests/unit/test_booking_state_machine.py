import pytest
from app import create_app

def test_legal_transitions(app):
    with app.app_context():
        from app.services.booking_service import _assert_transition
        from app.utils.errors import InvalidStateTransitionError
        legal = [
            ('draft', 'pending_admin_approval'),
            ('pending_admin_approval', 'awaiting_payment'),
            ('pending_admin_approval', 'rejected'),
            ('awaiting_payment', 'payment_pending'),
            ('awaiting_payment', 'cancelled'),
            ('payment_pending', 'confirmed'),
            ('payment_pending', 'awaiting_payment'),
            ('confirmed', 'checked_in'),
            ('confirmed', 'cancelled'),
            ('checked_in', 'checked_out'),
            ('checked_out', 'completed'),
        ]
        for frm, to in legal:
            _assert_transition(frm, to)  # must not raise

def test_illegal_transitions(app):
    with app.app_context():
        from app.services.booking_service import _assert_transition
        from app.utils.errors import InvalidStateTransitionError
        illegal = [
            ('confirmed', 'draft'),
            ('completed', 'confirmed'),
            ('rejected', 'confirmed'),
            ('cancelled', 'confirmed'),
            ('checked_in', 'pending_admin_approval'),
        ]
        for frm, to in illegal:
            with pytest.raises(InvalidStateTransitionError):
                _assert_transition(frm, to)
