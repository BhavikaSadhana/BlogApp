from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

# File paths
USER_FILE = "\\path of the file"
POST_FILE = "\\path of the file"

# Ensure files exist
for file in [USER_FILE, POST_FILE]:
    if not os.path.exists(file):
        open(file, "w").close()

# Models
class User(BaseModel):
    username: str
    email: str

class BlogPost(BaseModel):
    title: str
    content: str
    author: str

# Helper functions
def read_users():
    """Read users from the file and return a dictionary {username: email}"""
    users = {}
    with open(USER_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(", ")
            if len(parts) == 2:
                username = parts[0].split(": ")[1]
                email = parts[1].split(": ")[1]
                users[username] = email
    return users

def write_users(users):
    """Write users dictionary back to the file."""
    with open(USER_FILE, "w") as file:
        for username, email in users.items():
            file.write(f"Username: {username}, Email: {email}\n")

def read_posts():
    """Read posts from the file and return a list of dictionaries"""
    posts = []
    with open(POST_FILE, "r") as file:
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 3:
                posts.append({"title": parts[0], "content": parts[1], "author": parts[2]})
    return posts

def write_posts(posts):
    """Write posts list back to the file."""
    with open(POST_FILE, "w") as file:
        for post in posts:
            file.write(f"{post['title']}|{post['content']}|{post['author']}\n")

# API Routes
@app.post("/register")
def register(user: User):
    """Register a new user and store in a text file."""
    users = read_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[user.username] = user.email
    write_users(users)
    return {"message": f"User {user.username} registered successfully"}

@app.post("/login")
def login(user: User):
    """Login a user by checking if they exist in the text file."""
    users = read_users()
    if user.username not in users:
        raise HTTPException(status_code=401, detail="Invalid username or not registered")

    return {"message": f"User {user.username} logged in successfully"}

@app.post("/create_post")
def create_post(post: BlogPost):
    """Create a new blog post and store in a text file."""
    users = read_users()
    if post.author not in users:
        raise HTTPException(status_code=403, detail="Only registered users can create posts")

    posts = read_posts()
    posts.append({"title": post.title, "content": post.content, "author": post.author})
    write_posts(posts)

    return {"message": f"Post '{post.title}' created successfully"}

@app.get("/posts")
def get_posts():
    """Retrieve all blog posts."""
    return {"posts": read_posts()}

@app.get("/posts/user/{username}")
def get_posts_by_user(username: str):
    """Retrieve all blog posts created by a specific user."""
    posts = read_posts()
    user_posts = [post for post in posts if post["author"] == username]
    if not user_posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")

    return {"posts": user_posts}

@app.get("/posts/title/{title}")
def get_post_by_title(title: str):
    """Retrieve a blog post by its title."""
    posts = read_posts()
    for post in posts:
        if post["title"].lower() == title.lower():
            return post

    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/update_post")
def update_post(title: str, updated_post: BlogPost):
    """Update a blog post by title."""
    posts = read_posts()
    updated = False

    for i, post in enumerate(posts):
        if post["title"].lower() == title.lower():
            posts[i] = {"title": updated_post.title, "content": updated_post.content, "author": updated_post.author}
            updated = True
            break

    if not updated:
        raise HTTPException(status_code=404, detail="Post not found")

    write_posts(posts)
    return {"message": f"Post '{title}' updated successfully"}

@app.delete("/delete_post")
def delete_post(title: str):
    """Delete a blog post by title."""
    posts = read_posts()
    new_posts = [post for post in posts if post["title"].lower() != title.lower()]

    if len(new_posts) == len(posts):
        raise HTTPException(status_code=404, detail="Post not found")

    write_posts(new_posts)
    return {"message": f"Post '{title}' deleted successfully"}

@app.get("/dashboard")
def dashboard(username: str):
    """Show dashboard only if the user is registered."""
    users = read_users()
    if username not in users:
        raise HTTPException(status_code=403, detail="Access denied. Please register first.")

    return {"message": f"Welcome {username} to the dashboard"}

@app.get("/users")
def get_users():
    """Retrieve all registered users."""
    return {"users": read_users()}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
