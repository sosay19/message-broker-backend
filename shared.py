from flask_socketio import SocketIO

socketio = SocketIO()

# Hardcoded data for demonstration
subscriptions = set()
recent_messages = []