from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Example blog data
blogs = [
    {"id": 1, "title": "First Blog", "content": "Hello, this is my first blog!"},
    {"id": 2, "title": "Second Blog", "content": "Flask + Prometheus + Grafana demo"}
]

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total HTTP Requests", ["method", "endpoint"])


@app.before_request
def before_request():
    REQUEST_COUNT.labels(request.method, request.path).inc()


@app.route("/blogs", methods=["GET"])
def get_blogs():
    return jsonify(blogs)


@app.route("/blogs/<int:blog_id>", methods=["GET"])
def get_blog(blog_id):
    blog = next((b for b in blogs if b["id"] == blog_id), None)
    if blog:
        return jsonify(blog)
    return jsonify({"error": "Blog not found"}), 404


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
