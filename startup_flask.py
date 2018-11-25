from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Startup, Base, Founder

app = Flask(__name__)

engine = create_engine('sqlite:///startup.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def allStartups():
	startups = session.query(Startup).all()
	return render_template('startups.html', startups=startups)


@app.route('/startup/<int:startup_id>/founder')
def startupDetails(startup_id):
	startup = session.query(Startup).filter_by(id=startup_id).one()
	founders = session.query(Founder).filter_by(startup_id=startup_id).all()
	return render_template('startup_details.html',startup=startup, founders=founders)

@app.route('/startup/<int:startup_id>/edit', methods=['GET', 'POST'])
def editStartup(startup_id):
	startup = session.query(Startup).filter_by(id=startup_id).one()
	if request.method == 'POST':
		if request.form['name']:
			startup.name = request.form['name']
		return redirect(url_for('allStartups'))
	else:
		return render_template('startup_edit.html', startup=startup)


@app.route('/startup/<int:startup_id>/delete', methods=['GET', 'POST'])
def deleteStartup(startup_id):
	startupToDelete = session.query(Startup).filter_by(id=startup_id).one()
	if request.method == 'POST':
		session.delete(startupToDelete)
		session.commit()
		return redirect(url_for('allStartups'))
	else:
		return render_template('startup_delete.html', startup=startupToDelete)


@app.route('/startup/<int:startup_id>/founder/new', methods=['GET', 'POST'])
def newFounder(startup_id):
	startup = session.query(Startup).filter_by(id=startup_id).one()
	if request.method == 'POST':
		newFounder = Founder(name=request.form['name'], bio=request.form['bio'], startup_id=startup_id)
		session.add(newFounder)
		session.commit()
		flash("Founder Successfully added")
		return redirect(url_for('startupDetails', startup_id=startup_id, startup=startup))
	else:

		return render_template('newFounder.html', startup_id=startup_id, startup=startup)

@app.route('/startup/<int:startup_id>/founder/<int:founder_id>/edit', methods=['GET', 'POST'])

def editFounder(startup_id, founder_id):
	startup = session.query(Startup).filter_by(id=startup_id).one()
	founderToEdit = session.query(Founder).filter_by(id=founder_id).one()
	if request.method == 'POST':
		if request.form['name']:
			founder.name = request.form['name']
		if request.form['bio']:
			founder.bio = request.form['bio']
		session.add(founderToEdit)
		session.commit()
		return redirect(url_for('startupDetails', startup_id=startup_id))
	else:
		return render_template('editFounderpage.html', startup=startup, founder=founderToEdit, founder_id=founder_id)


@app.route('/startup/<int:startup_id>/founder/<int:founder_id>/delete', methods=['GET', 'POST'])
def deleteFounder(startup_id, founder_id):
	startup = session.query(Startup).filter_by(id=startup_id).one()
	founderToDelete = session.query(Founder).filter_by(id=founder_id).one()
	if request.method == 'POST':
		session.delete(founderToDelete)
		session.commit()
		return redirect(url_for('startupDetails', startup_id=startup_id))
	else:
		return render_template('deleteFounderpage.html', startup=startup, founder=founderToDelete, founder_id=founder_id)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)