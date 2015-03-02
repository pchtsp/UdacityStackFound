from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import re

engine= create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind= engine

DBSession= sessionmaker(bind= engine)
session= DBSession()

def getIDfrompath(path):
	p=re.compile('\d+')
	p_answer= p.search(path)
	if p_answer==None:
		return False
	else: 
		return int(p.search(path).group())

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('content-type','text/html')
				self.end_headers()

				output= ""
				output+= "<html><body>"
				output+= "Hello there!"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output+= "</body></html>"
				self.wfile.write(output)
				# print output
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('content-type','text/html')
				self.end_headers()

				output= ""
				output+= "<html><body>"
				allRestaurants= session.query(Restaurant).all()

				#we print all the records of restaurants names':
				for resto in allRestaurants:
					output+= "<p>"
					output+= "<h2>"+resto.name+ "</h2>"
					output+= "<a href='restaurants/"+str(resto.id)+"/edit'>Edit</a><br/>"
					output+= "<a href='restaurants/"+str(resto.id)+"/delete'>Delete</a>"
					output+= "<br>"
					output+= "</p>"

				output+= "<a href='/restaurants/new'>Create a new Restaurant</a><br/>"
				output+= "</body></html>"

				self.wfile.write(output)
				#print output
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('content-type','text/html')
				self.end_headers()

				output= ""
				output+= "<html><body>"
				output+= "new Resto insert page..."
				output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What's the name of your new restaurant?</h2><input name="newResto" type="text" ><input type="submit" value="Submit"> </form>'''
				output+= "</body></html>"
				self.wfile.write(output)
				# print output
				return
			
			#if we find a number in the path: maybe it is an id for a restaurant:
			if getIDfrompath(self.path):
				#we initialize output
				output=""
				#we need to know if the restaurant really exists:
				allRestaurants= session.query(Restaurant).all()
				id_list= [resto.id for resto in allRestaurants]
				possible_id= getIDfrompath(self.path)
				#print possible_id
				#print id_list
				if possible_id not in id_list: 
					self.send_error(404,"File not found %s" % self.path)
					return
				#since the id exists: we will take the resto that corresponds to that id:
				restoToEdit= session.query(Restaurant).filter_by(id=possible_id).one()
				print "creo objeto"
				#now: we need to know if we will edit it or delete it:
				if self.path.endswith("/edit"):
					print "llego al /edit"
					self.send_response(200)
					self.send_header('content-type','text/html')
					self.end_headers()
					output+= "<html><body>"
					output += "<form method='POST' enctype='multipart/form-data' action='"+self.path+"'><h2>"+restoToEdit.name+"</h2><h3>Please, insert the new name for the restaurant:</h3><input name='editResto' type='text' ><input type='submit' value='Submit'> </form>"
					output+= "</body></html>"
					self.wfile.write(output)
					return

				if self.path.endswith("/delete"):
					self.send_response(200)
					self.send_header('content-type','text/html')
					self.end_headers()
					output+= "<html><body>"
					output += "<form method='POST' enctype='multipart/form-data' action='"+self.path+"'><h2>Are you sure you want to delete restaurant named '"+restoToEdit.name +"'?</h2><input type='submit' value='Yes'> </form>"
					output+= "</body></html>"
					self.wfile.write(output)
					return


		except IOError:
			self.send_error(404,"File not found %s" % self.path)

	def do_POST(self):
		print "enter POST"
#		try:
		self.send_response(301)
		self.end_headers()

		messagecontent=[]
		print self.path
		output= ""

		#here we create a new restaurant.
		if self.path.endswith("/restaurants/new"):
			ctype, pdict= cgi.parse_header(self.headers.getheader('content-type'))
			if ctype== 'multipart/form-data':
				fields= cgi.parse_multipart(self.rfile, pdict)
				messagecontent= fields.get('newResto')
			if len(messagecontent)>0:
				new_restaurant= Restaurant(name= messagecontent[0])
				session.add(new_restaurant)
				session.commit()
				output= "<html><body><h1> Restaurante creado! </h1> <a href='/restaurants'>Volver a restaurantes</a> </body></html>"
			else:
				output= "<html><body><h1> Hubo algun problema... </h1> <a href='/restaurants'>Volver a restaurantes</a> </body></html>"
			self.wfile.write(output)
			print output
			return

		possible_id= getIDfrompath(self.path)
		if not possible_id: 
			self.send_error(404,"File not found %s" % self.path)
			return
		allRestaurants= session.query(Restaurant).all()
		id_list= [resto.id for resto in allRestaurants]
		if possible_id not in id_list: 
			self.send_error(404,"File not found %s" % self.path)
			return
		restoToEdit= session.query(Restaurant).filter_by(id=possible_id).one()
		#here we delete an existing restaurant
		if self.path.endswith("/delete"):
			#since the id exists: we will take the resto that corresponds to that id:
			session.delete(restoToEdit)
			session.commit()
			output= "<html><body><h1> Restaurante eliminado! </h1> <a href='/restaurants'>Volver a restaurantes</a> </body></html>"
			self.wfile.write(output)

		if self.path.endswith("/edit"):
			#since the id exists: we will take the resto that corresponds to that id:
			ctype, pdict= cgi.parse_header(self.headers.getheader('content-type'))
			if ctype== 'multipart/form-data':
				fields= cgi.parse_multipart(self.rfile, pdict)
				messagecontent= fields.get('editResto')
			if len(messagecontent)>0:
				restoToEdit.name=messagecontent[0]
				session.add(restoToEdit)
				session.commit()
				output= "<html><body><h1> Restaurante editado! </h1> <a href='/restaurants'>Volver a restaurantes</a> </body></html>"
			else:
				output= "<html><body><h1> Hubo algun problema... </h1> <a href='/restaurants'>Volver a restaurantes</a> </body></html>"
			self.wfile.write(output)

#		except:
#			pass

def main():
	try:
		port= 8080
		server= HTTPServer(('',port),webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()

 