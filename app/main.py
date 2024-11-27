from flask import Flask

from app.routes.seats_routes import seat_bluprint

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(seat_bluprint, url_prefix="/api/seats")
    app.run()