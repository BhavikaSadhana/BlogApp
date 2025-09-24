from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
user_requests = Counter('user_requests_total', 'Total number of user requests')

# In-memory storage for blog posts
blog_posts = []

@app.route('/')
def home():
    return "Welcome to EED BlogApp!"

# Endpoint to add blog post (takes user input)
@app.route('/add_post', methods=['POST'])
def add_post():
    user_requests.inc()
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    post = {'title': title, 'content': content}
    blog_posts.append(post)
    return jsonify({'message': 'Post added successfully!', 'post': post}), 201

# Endpoint to list all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    user_requests.inc()
    return jsonify(blog_posts)

# Endpoint for Prometheus to scrape metrics
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
