from flask import Flask, render_template, request, redirect, url_for
app= Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import re

engine= create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind= engine

DBSession= sessionmaker(bind= engine)
session= DBSession()

#@app.route('/')
@app.route('/restaurants/<int:id_of_restaurant>/')
def restaurantMenu(id_of_restaurant):
	oneRestaurant= session.query(Restaurant).filter_by(id=id_of_restaurant).one()
	items_in_restaurant= session.query(MenuItem).filter_by(restaurant_id=id_of_restaurant).all()
	# output=""
	# for item in items_in_restaurant:
	# 	output+= item.name
	# 	output+= "<br>"
	# 	output+= item.price
	# 	output+= "<br>"
	# 	output+= item.description
	# 	output+= "<br>"
	# 	output+= "<br>"
	return render_template('menu.html',restaurant=oneRestaurant,items=items_in_restaurant)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method== 'POST':
		newItem= MenuItem(name= request.form['name'], restaurant_id= restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu',id_of_restaurant=restaurant_id))
	else: 
		return render_template('NewMenuItem.html',restaurant_id=restaurant_id)
	return "page to create a new menu item. Task 1 complete!"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "page to edit a menu item. Task 2 complete!"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
	app.debug= True
	app.run(port= 5000)
