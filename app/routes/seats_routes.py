from flask import Blueprint, request, jsonify

from app.repository.seats_repository import reserve_seat, is_seat_exists, seat_ttl, reserved_seat_create_key, \
    RESERVED_TIME
import toolz as t

seat_bluprint = Blueprint("seat", __name__)


@seat_bluprint.route("/reserve_seat", methods=['POST'])
def reserve_seat_key():
    data = request.json

    seat_number = data.get('seat_number')
    movie_id = data.get('movie_id')
    key = reserved_seat_create_key(movie_id, seat_number)

    if not seat_number or not movie_id:
        return jsonify({'error': 'Missing seat number or movie ID'}), 400

    # Check if seat is already reserved
    if is_seat_exists(key):
        return jsonify({'error': 'Seat already reserved'}), 409

    # Reserve the seat with 15-minute timeout
    reserve_seat(key)

    return jsonify({
        'message': 'Seat reserved successfully',
        'seat_number': seat_number,
        'movie_id': movie_id,
        'timeout_minutes': RESERVED_TIME
    })


@seat_bluprint.route('/check_seat/<movie_id>/<seat_number>', methods=['GET'])
def check_seat(movie_id, seat_number):
    return jsonify(
        t.pipe(
            reserved_seat_create_key(movie_id, seat_number),
            lambda key: {
                'seat_number': seat_number,
                'movie_id': movie_id,
                'is_reserved': is_seat_exists(key),
                'minutes_remaining': seat_ttl(key)
            }
        )
    )
