# my-blog

## My app is live at [https://ljenchik-myblog.onrender.com](https://ljenchik-myblog.onrender.com)


### Welcome to my blog web app!
### I've developed this web application for sharing blog posts and ideas among colleagues and friends

This app:

- Allows register and login 
- Displays list of posts
- Each post comes with details like when it was added, the number of comments, and how many times it's been viewed
- The view count doesn't go up when the author checks out their own post
- A user can sort posts by Newest, Oldest, and Most Popular, and there's pagination for easy browsing
- Clicking on user's own post lets them read, edit, delete, and check comments
- If it's someone else's post, no editing, but an opportunity to drop a comment
- Profile link leads to a user's profile page, where they can create posts using markdown as well as update profile information
- For admin, there's a secret admin view link leading to the admin dashboard, where admins can efficiently manage users, posts, and comments


### Setup

Install Python requirements 

```
pip install -r requirements.txt
```

Run flask migrations to create empty SQLite database

```
flask db migrate
flask db upgrade
```

Start Flask application

```
flask run
```

or

```
gunicorn wsgi:application 
```

Connect to [http://localhost:5000](http://localhost:5000) and enjoy!
