from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Region, RegionBlog

app = Flask(__name__)

engine = create_engine('sqlite:///regionblogs.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all regions
@app.route('/')
@app.route('/region/')
def showRegions():
    regions = session.query(Region).all()
    return render_template('regions.html', regions=regions)


# Create a new region
@app.route('/region/new/', methods=['GET', 'POST'])
def newRegion():
    if request.method == 'POST':
        newRegion = Region(name=request.form['name'])
        session.add(newRegion)
        session.commit()
        return redirect(url_for('showRegions'))
    else:
        return render_template('newRegion.html')


# Edit a region
@app.route('/region/<int:region_id>/edit/', methods=['GET', 'POST'])
def editRegion(region_id):
    editedRegion = session.query(
        Region).filter_by(id=region_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRegion.name = request.form['name']
            return redirect(url_for('showRegions'))
    else:
        return render_template(
            'editRegion.html', region=editedRegion)


# Delete a region
@app.route('/region/<int:region_id>/delete/', methods=['GET', 'POST'])
def deleteRegion(region_id):
    regionToDelete = session.query(
        Region).filter_by(id=region_id).one()
    if request.method == 'POST':
        session.delete(regionToDelete)
        session.commit()
        return redirect(
            url_for('showRegions', region_id=region_id))
    else:
        return render_template(
            'deleteRegion.html', region=regionToDelete)


# Show a region blog
@app.route('/region/<int:region_id>/')
@app.route('/region/<int:region_id>/blogs/')
def showBlogs(region_id):
    region = session.query(Region).filter_by(id=region_id).one()
    items = session.query(RegionBlog).filter_by(
        region_id=region_id).all()
    return render_template('blogs.html', items=items, region=region)


# Create a new blog item
@app.route(
    '/region/<int:region_id>/blogs/new/', methods=['GET', 'POST'])
def newRegionBlog(region_id):
    if request.method == 'POST':
        newItem = RegionBlog(
            name=request.form['name'], description=request.form['description'],
            url=request.form['url'], region_id=region_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showBlogs', region_id=region_id))
    else:
        return render_template('newRegionBlog.html', region_id=region_id)
    return render_template('newRegionBlog.html', region=region)


# Edit a blog item
@app.route('/region/<int:region_id>/blogs/<int:blog_id>/edit',
           methods=['GET', 'POST'])
def editRegionBlog(region_id, blog_id):
    editedItem = session.query(RegionBlog).filter_by(id=blog_id).one()
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


# Delete a blog item
@app.route('/region/<int:region_id>/blogs/<int:blog_id>/delete',
           methods=['GET', 'POST'])
def deleteRegionBlog(region_id, blog_id):
    itemToDelete = session.query(RegionBlog).filter_by(id=blog_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showBlogs', region_id=region_id))
    else:
        return render_template('deleteRegionBlog.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
