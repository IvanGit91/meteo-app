import os
import marshmallow

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import BadRequest

from app.server.exceptions.MeteoException import MeteoException
from app.server.exceptions.NotFoundException import NotFoundException

db = SQLAlchemy()
migrate = Migrate()

def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.server.routes.station_routes import station_bp
    from app.server.routes.sensor_routes import sensor_bp
    from app.server.routes.forecast_routes import forecast_bp
    from app.server.routes.measurement_routes import measurement_bp

    app.register_blueprint(station_bp)
    app.register_blueprint(sensor_bp)
    app.register_blueprint(forecast_bp)
    app.register_blueprint(measurement_bp)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    @app.errorhandler(MeteoException)
    def handle_meteo_exception(e):
        return make_response(e.to_json(), e.code)

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return {'error': 'Bad Request', 'message': e.data['message']}, 400

    @app.errorhandler(marshmallow.exceptions.ValidationError)
    def handle_marshmallow_exception(err):
        return jsonify(err.messages), 400

    # Flask routes
    @app.route("/")
    def home():
        return jsonify({"message": "Pong"})

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    ######################### NEW
    # Kafka configuration
    # KAFKA_BROKER = 'kafka:9092'  # Docker service name for Kafka
    # KAFKA_TOPIC = 'iot-data'
    #
    # # MQTT configuration
    # MQTT_BROKER = 'test.mosquitto.org'  # Replace with your MQTT broker
    # MQTT_PORT = 1883
    # MQTT_TOPIC = 'iot/sensors/#'
    #
    # # Initialize Kafka producer
    # producer = KafkaProducer(
    #     bootstrap_servers=KAFKA_BROKER,
    #     value_serializer=lambda v: json.dumps(v).encode('utf-8')
    # )
    #
    # def on_connect(client, userdata, flags, rc):
    #     print(f"Connected to MQTT Broker with result code {rc}")
    #     client.subscribe(MQTT_TOPIC)
    #
    # def on_message(client, userdata, msg):
    #     print(f"Received MQTT message: {msg.topic} {msg.payload}")
    #     try:
    #         data = {
    #             'topic': msg.topic,
    #             'payload': msg.payload.decode('utf-8')
    #         }
    #         producer.send(KAFKA_TOPIC, value=data)
    #         print("Data forwarded to Kafka.")
    #     except Exception as e:
    #         print(f"Error forwarding to Kafka: {e}")
    #
    # # Function to start MQTT client
    # def start_mqtt_client():
    #     mqtt_client = mqtt.Client()
    #     mqtt_client.on_connect = on_connect
    #     mqtt_client.on_message = on_message
    #     mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    #     mqtt_client.loop_forever()
    #
    # # Start MQTT client in a separate thread
    # mqtt_thread = threading.Thread(target=start_mqtt_client)
    # mqtt_thread.daemon = True
    # mqtt_thread.start()

    return app
