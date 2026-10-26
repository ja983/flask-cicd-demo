import os

from flask import Flask, jsonify, request

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")
GIT_SHA = os.getenv("GIT_SHA", "dev")


@app.get("/")
def home():
    return jsonify(
        message="Hello from the CI/CD pipeline! v2",
        version=VERSION,
        commit=GIT_SHA[:7],
    )


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/api/add")
def add():
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
    except (KeyError, ValueError):
        return jsonify(error="Provide numeric query params a and b"), 400
    return jsonify(result=a + b)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
