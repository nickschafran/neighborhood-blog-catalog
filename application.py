#!/usr/bin/env python
#
# application.py -- A Flask application which serves a user-contributable
# directory of neighborhood blogs
#
# Author: Nick Schafran, Sept. 2015

import random
import string
import httplib2
import json
import requests

from database_setup import Base, Region, RegionBlog, User
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import session as login_session
from flask import make_response
from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Neighborhood Blogs App"

engine = create_engine('postgresql://catalog:password@localhost/catalog')Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """Returns login.html template"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Validate state token"""
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
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    """Add user to db"""
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Returns User Info"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Returns User ID"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """Revoke a current user's token and reset their login_session"""
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
def regionBlogsJSON(region_id):
    """JSON Endpoint for Region Blogs"""
    items = session.query(RegionBlog).filter_by(
        region_id=region_id).all()
    return jsonify(RegionBlogs=[i.serialize for i in items])


@app.route('/region/<int:region_id>/blogs/<int:blog_id>/JSON')
def blogJSON(region_id, blog_id):
    """JSON Endpoint for specific blog"""
    Blog = session.query(RegionBlog).filter_by(id=blog_id).one()
    return jsonify(Blog=Blog.serialize)


@app.route('/region/JSON')
def regionsJSON():
    """JSON Endpoint for Regions"""
    regions = session.query(Region).all()
    return jsonify(regions=[r.serialize for r in regions])


@app.route('/')
@app.route('/region/')
def showRegions():
    """Show all Regions"""
    regions = session.query(Region).all()
    if 'username' not in login_session:
        return render_template('publicregions.html', regions=regions)
    else:
        return render_template('regions.html', regions=regions)


@app.route('/about')
def about():
    """About page"""
    if 'username' not in login_session:
        return render_template('publicabout.html')
    else:
        return render_template('about.html')


@app.route('/contact')
def contact():
    """Contact page"""
    if 'username' not in login_session:
        return render_template('publiccontact.html')
    else:
        return render_template('contact.html')


@app.route('/region/new/', methods=['GET', 'POST'])
def newRegion():
    """Create a new page"""
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # Region w/ description
        newRegion = Region(
            name=request.form['name'], description=request.form['description'],
            user_id=login_session['user_id'])

        session.add(newRegion)
        session.commit()
        return redirect(url_for('showRegions'))
    else:
        return render_template('newRegion.html')


@app.route('/region/<int:region_id>/edit/', methods=['GET', 'POST'])
def editRegion(region_id):
    """Edit a region"""
    if 'username' not in login_session:
        return redirect('/login')
    editedRegion = session.query(
        Region).filter_by(id=region_id).one()
    if editedRegion.user_id != login_session['user_id']:
        flash("You may only edit neighborhoods you have created!")
        return redirect(url_for('showRegions'))
    if request.method == 'POST':
        if request.form['name']:
            editedRegion.name = request.form['name']
            return redirect(url_for('showRegions'))
    else:
        return render_template(
            'editRegion.html', region=editedRegion)


@app.route('/region/<int:region_id>/delete/', methods=['GET', 'POST'])
def deleteRegion(region_id):
    """Delete a region"""
    if 'username' not in login_session:
        return redirect('/login')
    regionToDelete = session.query(
        Region).filter_by(id=region_id).one()
    if regionToDelete.user_id != login_session['user_id']:
        flash("You may only delete neighborhoods you have created!")
        return redirect(url_for('showRegions'))
    if request.method == 'POST':
        session.delete(regionToDelete)
        session.commit()
        return redirect(
            url_for('showRegions', region_id=region_id))
    else:
        return render_template(
            'deleteRegion.html', region=regionToDelete)


@app.route('/region/<int:region_id>/')
@app.route('/region/<int:region_id>/blogs/')
def showBlogs(region_id):
    """Show region blogs"""
    region = session.query(Region).filter_by(id=region_id).one()
    creator = getUserInfo(region.user_id)
    items = session.query(RegionBlog).filter_by(
        region_id=region_id).all()
    if 'username' not in login_session:
        return render_template(
            'publicblogs.html', items=items, region=region, creator=creator)
    else:
        return render_template(
            'blogs.html', items=items, region=region, creator=creator)


@app.route(
    '/region/<int:region_id>/blogs/new/', methods=['GET', 'POST'])
def newRegionBlog(region_id):
    """Create a new region blog"""
    if 'username' not in login_session:
        return redirect('/login')
    region = session.query(Region).filter_by(id=region_id).one()
    if request.method == 'POST':
        newItem = RegionBlog(
            name=request.form['name'],
            description=request.form['description'],
            url=request.form['url'],
            region_id=region_id,
            user_id=region.user_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showBlogs', region_id=region_id))
    else:
        return render_template('newRegionBlog.html', region_id=region_id)
    return render_template('newRegionBlog.html', region=region)


@app.route('/region/<int:region_id>/blogs/<int:blog_id>/edit',
           methods=['GET', 'POST'])
def editRegionBlog(region_id, blog_id):
    """Edit a blog item"""
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(RegionBlog).filter_by(id=blog_id).one()
    if editedItem.user_id != login_session['user_id']:
        flash("You may only edit blogs you have created!")
        return redirect(url_for('showBlogs', region_id=region_id))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['url']:
            editedItem.url = request.form['url']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showBlogs', region_id=region_id))
    else:

        return render_template(
            'editRegionBlog.html', region_id=region_id, blog_id=blog_id,
            item=editedItem)


@app.route('/region/<int:region_id>/blogs/<int:blog_id>/delete',
           methods=['GET', 'POST'])
def deleteRegionBlog(region_id, blog_id):
    """Delete a region blog"""
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(RegionBlog).filter_by(id=blog_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash("You may only delete blogs you have created!")
        return redirect(url_for('showBlogs', region_id=region_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showBlogs', region_id=region_id))
    else:
        return render_template('deleteRegionBlog.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
