from flask import Flask
from flask import request, jsonify
from .service.messageService import MessageService
from kafka import KafkaProducer
import json
import os

app = Flask(__name__)
app.config.from_pyfile("config.py")

messageService = MessageService()


kafka_host = os.getenv("KAFKA_HOST", "localhost")
kafka_port = os.getenv("KAFKA_PORT", "9092")

producer = KafkaProducer(
    bootstrap_servers=f"{kafka_host}:{kafka_port}",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


@app.route("/v1/ds/message/", methods=["POST"])
def handle_message():
    message = request.json.get("message")
    result = messageService.process_message(message)
    serialized_result = result.serialize()

    producer.send("expense_service", serialized_result)
    return jsonify(result)


@app.route("/", methods=["GET"])
def handle_get():
    return "Hello world"


if __name__ == "__main__":
    app.run(host="localhost", port=8010, debug=True)
