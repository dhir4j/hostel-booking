import hashlib, hmac, json, pytest

def make_sig(secret, body):
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

def test_full_booking_flow(client, admin_token, user_token, app):
    """Register -> admin creates hostel+room -> user books -> admin approves -> user pays -> confirmed."""
    # 1. Admin creates hostel
    r = client.post('/api/v1/admin/hostels', json={
        'name': 'Flow Hostel', 'city': 'Goa', 'address': 'Beach Rd'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 201
    hostel_id = r.get_json()['data']['hostel']['id']

    # 2. Admin creates room
    r = client.post('/api/v1/admin/rooms', json={
        'hostel_id': hostel_id, 'room_number': 'F01',
        'capacity': 2, 'price_per_night': '1000.00'
    }, headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 201
    room_id = r.get_json()['data']['room']['id']

    # 3. User views hostel (public)
    r = client.get(f'/api/v1/hostels/{hostel_id}')
    assert r.status_code == 200

    # 4. User creates booking (future dates)
    r = client.post('/api/v1/bookings', json={
        'hostel_id': hostel_id, 'room_id': room_id,
        'check_in': '2027-06-01', 'check_out': '2027-06-03',
        'guests_count': 2
    }, headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code == 201
    booking = r.get_json()['data']['booking']
    booking_id = booking['id']
    assert booking['status'] == 'pending_admin_approval'

    # 5. Admin approves
    r = client.post(f'/api/v1/admin/bookings/{booking_id}/approve',
                    json={}, headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 200
    assert r.get_json()['data']['booking']['status'] == 'awaiting_payment'

    # 6. User creates payment intent
    r = client.post('/api/v1/payments/create-intent',
                    json={'booking_id': booking_id},
                    headers={'Authorization': f'Bearer {user_token}'})
    assert r.status_code == 201
    payment_data = r.get_json()['data']['payment']
    provider_ref = payment_data['provider_ref']

    # 7. Simulate webhook success
    secret = app.config['WEBHOOK_SECRET']
    payload = {'provider_ref': provider_ref, 'status': 'success', 'amount': '2000.00'}
    body = json.dumps(payload).encode()
    sig = make_sig(secret, body)
    r = client.post('/api/v1/payments/webhook/mock',
                    data=body, content_type='application/json',
                    headers={'X-Mock-Signature': sig})
    assert r.status_code == 200

    # 8. Verify booking confirmed
    r = client.get(f'/api/v1/bookings/{booking_id}',
                   headers={'Authorization': f'Bearer {user_token}'})
    assert r.get_json()['data']['booking']['status'] == 'confirmed'

    # 9. Admin check-in
    r = client.post(f'/api/v1/admin/bookings/{booking_id}/checkin',
                    headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 200
    assert r.get_json()['data']['booking']['status'] == 'checked_in'

    # 10. Admin check-out
    r = client.post(f'/api/v1/admin/bookings/{booking_id}/checkout',
                    headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 200

    # 11. Admin complete
    r = client.post(f'/api/v1/admin/bookings/{booking_id}/complete',
                    headers={'Authorization': f'Bearer {admin_token}'})
    assert r.status_code == 200
    assert r.get_json()['data']['booking']['status'] == 'completed'
