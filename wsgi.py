from home_automation import init_app, socketio

app = init_app()

if __name__ == "__main__":
    socketio.run(app, port=5002)
