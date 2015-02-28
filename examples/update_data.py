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

veggieBurgers= session.query(MenuItem).filter_by(name="Veggie Burger")

#we print all the records of MenuItems with "Veggie Burger" as a name:
for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.restaurant.name
	print veggieBurger.price
	print "\n"

#we make a query to get the specific price of one MenuItem:
veggieBurgers= session.query(MenuItem).filter_by(id=10).one()
#we change the price to that MenuItem, we add and commit:
veggieBurgers.price= "$2.99"
session.add(veggieBurgers)
session.commit()

#we update all the records of MenuItems with "Veggie Burger" as a name to "$2.99":
veggieBurgers= session.query(MenuItem).filter_by(name="Veggie Burger")
for veggieBurger in veggieBurgers:
	if veggieBurger.price!= "$2.99":
		veggieBurger.price= "$2.99"
		session.add(veggieBurger)
		session.commit()