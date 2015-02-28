from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine= create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind= engine

DBSession= sessionmaker(bind= engine)
session= DBSession()

#how to use a session:
#newEntry= ClassName(property= "vale",...)
#session.add(newEntry)
#session.commit()

#example of using a session by adding a Restaurant:
myFirstRestaurant= Restaurant(name= "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

#returns all listed Restaurants in a non-friendly way:
session.query(Restaurant).all()

#example of using a session by adding a MenuItem
cheesepizza= MenuItem(
	name= "Cheese Pizza", 
	description= "Made with all natural ingredients and fresh mozzarella", 
	course= "Entree", 
	price= "$8.99", 
	restaurant= myFirstRestaurant)
session.add(cheesepizza)
session.commit()

#returns all listed MenuItems:
session.query(MenuItem).all()