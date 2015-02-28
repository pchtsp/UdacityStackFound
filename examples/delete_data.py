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

spinach= session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()
#check if the restaurant is correct:
print spinach.restaurant.name
session.delete(spinach)
session.commit()