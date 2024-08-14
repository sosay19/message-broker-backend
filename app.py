import eventlet

from flask import Flask, request, jsonify
from flask_cors import CORS
from mqtt_client import connect_mqtt, publish_message, subscribe_topic, unsubscribe_topic
from shared import subscriptions, recent_messages, socketio

eventlet.monkey_patch()

app = Flask(__name__)
socketio.init_app(app, cors_allowed_origins="*")  # Initialize socketio with app
CORS(app)

# Connect to MQTT broker
connect_mqtt()



@app.route('/api/publish', methods=['POST'])
def publish_message_endpoint():
    data = request.json
    topic = data.get('topic')
    message = data.get('message')
    
    if topic and message:
        publish_message(topic, message)
        recent_messages.append({'topic': topic, 'message': message})
        if len(recent_messages) > 10:
            recent_messages.pop(0)
        # Emit the message to all connected clients
        # socketio.emit('new_message', {'topic': topic, 'message': message})
        return jsonify({
            "status": "success",
            "message": "Message published successfully."
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid request."
        }), 400

@app.route('/api/recent-messages', methods=['GET'])
def get_recent_messages():
    return jsonify({
        "messages": recent_messages
    }), 200

@app.route('/api/subscribe', methods=['POST'])
def subscribe_topic_endpoint():
    data = request.json
    topic = data.get('topic')
    
    if topic and topic not in subscriptions:
        subscribe_topic(topic)
        subscriptions.add(topic)
        return jsonify({
            "status": "success",
            "message": "Subscription added successfully."
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid or duplicate subscription."
        }), 400

@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe_topic_endpoint():
    data = request.json
    topic = data.get('topic')
    
    if topic in subscriptions:
        unsubscribe_topic(topic)
        subscriptions.remove(topic)
        return jsonify({
            "status": "success",
            "message": "Unsubscribed successfully."
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Subscription not found."
        }), 400

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    return jsonify({
        "subscriptions": list(subscriptions)
    }), 200

if __name__ == '__main__':
    socketio.run(app, debug=True)
