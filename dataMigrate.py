import json
from models import Project, HomePost, User
from PortfolioSiteDataMigration import app
from flask import jsonify
from datetime import datetime

with app.app_context():
    data = {}
    data['PROJECT'] = []
    data['HOMEPOST'] = []
    data['USER'] = []

    projects = Project.query.all()
    for project in projects:
        data['PROJECT'].append({
            'id':project.id,
            'title': project.title,
            'type': project.type,
            'content': project.content,
            'files': project.files,
            'date_posted': project.date_posted.strftime('%Y-%m-%d %H:%M'),
            'user_id': project.user_id,
            'home_post': project.home_post.id
            # we only need the id, we can query the home_posts once they're all in and assign accordingly

        })


    #migrate all homeposts first, that way we can backref all the homeposts objects by just checking
    #they're proj id

    data['HOMEPOST'] = []
    homeposts = HomePost.query.all()
    for post in homeposts:
        data['HOMEPOST'].append({
            'id':post.id,
            'project_id':post.project_id,
            'type_image':post.type_image,
            'content': post.content
        })

    user = User.query.first()
    data['USER'] = {
        'id': user.id,
        'username': user.username,
        'password': user.password

        #We can leave this out because we'll backref it later to save time
        #'posts': user.posts

    }

    with open ('data.json', 'w') as outfile:
        json.dump(data, outfile)
