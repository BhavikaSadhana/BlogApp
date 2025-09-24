from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version="1.0", title="Blog API",
          description="A simple Blog API with Swagger UI")

ns = api.namespace('posts', description='Blog operations')

# Define model for input validation and Swagger documentation
post_model = api.model('Post', {
    'title': fields.String(required=True, description='Title of the post'),
    'content': fields.String(required=True, description='Content of the post')
})

# In-memory storage for demo
posts = []

@ns.route('/add_post')
class AddPost(Resource):
    @ns.expect(post_model)  # For Swagger UI
    def post(self):
        data = request.json
        posts.append(data)
        return {"message": "Post added successfully!", "post": data}, 201

@ns.route('/all_posts')
class AllPosts(Resource):
    def get(self):
        return {"posts": posts}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
