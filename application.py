#!/usr/bin/env python
"""A Flask app which serves a user-contributable directory of blogs."""
import random
import string
import httplib2
import json
import requests
from database_setup import Base, Region, RegionBlog, User
from flask import (Flask, render_template, request, redirect, jsonify, url_for,
                   session as login_session, make_response, flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Neighborhood Blogs App"

engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def show_login():
    """Return login.html template."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Validate state token."""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ('<h1>Welcome, ' + login_session['username'] +
              '!</h1><img src="' + login_session['picture'] +
              ' " style = "width: 300px; height: 300px;border-radius:' +
              ' 150px;-webkit-border-radius:' +
              ' 150px;-moz-border-radius: 150px;"> ')

    print "done!"
    return output


# User Helper Functions
def create_user(login_session):
    """Add user to db."""
    new_user = User(name=login_session['username'], email=login_session[
                    'email'], picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    """Return User Info."""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    """Return User ID."""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """Revoke a current user's token and reset their login_session."""
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/region/<int:region_id>/blogs/JSON')
def region_blogs_json(region_id):
    """JSON Endpoint for Region Blogs."""
    items = session.query(RegionBlog).filter_by(
        region_id=region_id).all()
    return jsonify(RegionBlogs=[i.serialize for i in items])


@app.route('/region/<int:region_id>/blogs/<int:blog_id>/JSON')
def blog_json(region_id, blog_id):
    """JSON Endpoint for specific blog."""
    blog = session.query(RegionBlog).filter_by(id=blog_id).one()
    return jsonify(blog=blog.serialize)


@app.route('/region/JSON')
def regions_json():
    """JSON Endpoint for Regions."""
    regions = session.query(Region).all()
    return jsonify(regions=[r.serialize for r in regions])


@app.route('/')
@app.route('/region/')
def show_regions():
    """Show all Regions."""
    regions = session.query(Region).all()
    if 'username' not in login_session:
        return render_template('publicregions.html', regions=regions)
    else:
        return render_template('regions.html', regions=regions)


@app.route('/about')
def about():
    """About page."""
    if 'username' not in login_session:
        return render_template('publicabout.html')
    else:
        return render_template('about.html')


@app.route('/contact')
def contact():
    """Contact page."""
    if 'username' not in login_session:
        return render_template('publiccontact.html')
    else:
        return render_template('contact.html')


@app.route('/region/new/', methods=['GET', 'POST'])
def new_region():
    """Create a new page."""
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # Region w/ description
        new_region = Region(
            name=request.form['name'], description=request.form['description'],
            user_id=login_session['user_id'])

        session.add(new_region)
        session.commit()
        return redirect(url_for('show_regions'))
    else:
        return render_template('new_region.html')


@app.route('/region/<int:region_id>/edit/', methods=['GET', 'POST'])
def edit_region(region_id):
    """Edit a region."""
    if 'username' not in login_session:
        return redirect('/login')
    edited_region = session.query(
        Region).filter_by(id=region_id).one()
    if edited_region.user_id != login_session['user_id']:
        flash("You may only edit neighborhoods you have created!")
        return redirect(url_for('show_regions'))
    if request.method == 'POST':
        if request.form['name']:
            edited_region.name = request.form['name']
            return redirect(url_for('show_regions'))
    else:
        return render_template(
            'edit_region.html', region=edited_region)


@app.route('/region/<int:region_id>/delete/', methods=['GET', 'POST'])
def delete_region(region_id):
    """Delete a region."""
    if 'username' not in login_session:
        return redirect('/login')
    region_to_delete = session.query(
        Region).filter_by(id=region_id).one()
    if region_to_delete.user_id != login_session['user_id']:
        flash("You may only delete neighborhoods you have created!")
        return redirect(url_for('show_regions'))
    if request.method == 'POST':
        session.delete(region_to_delete)
        session.commit()
        return redirect(
            url_for('show_regions', region_id=region_id))
    else:
        return render_template(
            'delete_region.html', region=region_to_delete)


@app.route('/region/<int:region_id>/')
@app.route('/region/<int:region_id>/blogs/')
def show_blogs(region_id):
    """Show region blogs."""
    region = session.query(Region).filter_by(id=region_id).one()
    creator = get_user_info(region.user_id)
    items = session.query(RegionBlog).filter_by(
        region_id=region_id).all()
    if 'username' not in login_session:
        return render_template(
            'publicblogs.html', items=items, region=region, creator=creator)
    else:
        return render_template(
            'blogs.html', items=items, region=region, creator=creator)


@app.route('/region/<int:region_id>/blogs/new/', methods=['GET', 'POST'])
def new_region_blog(region_id):
    """Create a new region blog."""
    if 'username' not in login_session:
        return redirect('/login')
    region = session.query(Region).filter_by(id=region_id).one()
    if request.method == 'POST':
        new_item = RegionBlog(
            name=request.form['name'],
            description=request.form['description'],
            url=request.form['url'],
            region_id=region_id,
            user_id=region.user_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('show_blogs', region_id=region_id))
    else:
        return render_template('new_region_blog.html', region_id=region_id)
    return render_template('new_region_blog.html', region=region)


@app.route('/region/<int:region_id>/blogs/<int:blog_id>/edit',
           methods=['GET', 'POST'])
def edit_region_blog(region_id, blog_id):
    """Edit a blog item."""
    if 'username' not in login_session:
        return redirect('/login')
    edited_item = session.query(RegionBlog).filter_by(id=blog_id).one()
    if edited_item.user_id != login_session['user_id']:
        flash("You may only edit blogs you have created!")
        return redirect(url_for('show_blogs', region_id=region_id))
    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        if request.form['description']:
            edited_item.description = request.form['name']
        if request.form['url']:
            edited_item.url = request.form['url']
        session.add(edited_item)
        session.commit()
        return redirect(url_for('show_blogs', region_id=region_id))
    else:

        return render_template(
            'edit_region_blog.html', region_id=region_id, blog_id=blog_id,
            item=edited_item)


@app.route('/region/<int:region_id>/blogs/<int:blog_id>/delete',
           methods=['GET', 'POST'])
def delete_region_blog(region_id, blog_id):
    """Delete a region blog."""
    if 'username' not in login_session:
        return redirect('/login')
    item_to_delete = session.query(RegionBlog).filter_by(id=blog_id).one()
    if item_to_delete.user_id != login_session['user_id']:
        flash("You may only delete blogs you have created!")
        return redirect(url_for('show_blogs', region_id=region_id))
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        return redirect(url_for('show_blogs', region_id=region_id))
    else:
        return render_template('delete_region_blog.html', item=item_to_delete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
