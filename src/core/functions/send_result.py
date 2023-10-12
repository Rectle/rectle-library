import socketio
import os


def send_result(score):
    socket = socketio.Client()
    headers = {"X-Build": os.environ["BUILD_ID"], "X-Token": os.environ["SECRET"]}
    socket.connect(os.environ["SERVER_URL"], headers=headers, namespaces=["/private"])

    socket.emit("build:result", score, namespace="/private")

    return True
