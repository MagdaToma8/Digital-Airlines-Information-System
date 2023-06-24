import time, json, os, sys
from typing import Iterable
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response, session
import json
from bson.objectid import ObjectId 
from datetime import timedelta


sys.path.append('./data')

#Connect to local MongoDB 
mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/') 

#Database
db = client['airlines']

#Collections
users = db['users']
flights = db['flights']
bookings = db['bookings']

# Initiate Flask App
app = Flask(__name__)

app.secret_key = "sec_key"
app.permanent_session_lifetime = timedelta(minutes=10)


#Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=400,mimetype='application/json')
    if data == None:
        return Response("Bad request",status=400,mimetype='application/json')
    if not "name" in data  or not "surname" in data or not "email" in data or not "password" in data  or not "dateOfBirth" in data or not "country" in data or not "passportNumber" in data or not "username" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    if int(data['passportNumber'])> 100000 and int(data['passportNumber'])<999999:

        error=0
        if db.users.find_one({"email":data['email']}):
            error=1
            return Response({"Email address already in use"},status=400,mimetype="application/json")
        if db.users.find_one({"username":data['username']}):
            error=1
            return Response({"Username already in use"},status=400,mimetype="application/json")
        
        if error==0:
            user = {"name":data['name'],"surname":data['surname'], "email": data['email'], "password": data['password'], "dateOfBirth": data['dateOfBirth'], "country": data['country'], "passportNumber": data['passportNumber'], "username": data['username'],"type":'user'}
            
            users.insert_one(user)
            return Response("Successful signup.",status=200,mimetype="application/json")
    
    else: 
        return Response('The passport number should be 6 integers.',status=500,mimetype='application/json')


def loggedIn():
    return "username" in session

def isUser():
    user = users.find({"type": "user"})
    for x in user:
        if session["username"] == x["username"]:
            return True
    return False

def isAdmin():
    if session["username"] == "AgliKupe127" or session["username"]=="MagdaTomazani199":
        return True



#Login
@app.route('/login', methods=['POST'])
def login():
     data = None 
     try:
         data = json.loads(request.data)
     except Exception as e:
         return Response("Bad json content",status=400,mimetype='application/json')
     if data == None:
         return Response("Bad request",status=400,mimetype='application/json')
     if not "email" in data or not "password" in data:
         return Response("Information incomplete",status=500,mimetype="application/json")
    
     user = users.find_one({"email": data['email'], "password": data['password']})

     if user != None:
         if not loggedIn():
            session["username"] = user["username"]
            return Response("Successful login.",status=200,mimetype="application/json")
         return Response('You are already logged in.',status=500,mimetype='application/json') 
     return Response('no such user found. Please try again.',status=500,mimetype='application/json')


#Logout
@app.route('/logout', methods=['POST'])
def logout():

    if loggedIn():
           session.pop('username', None)
           return Response("Successful logout.",status=200,mimetype="application/json")
    return Response('This user is not logged in.',status=401,mimetype='application/json')

         
    


#Search flights 
@app.route('/searchFlights', methods=['GET'])
def searchFlights():    

    if loggedIn() and (isUser() or isAdmin()):

        # we can search a flight with the airport of origin and airport of destination or 
        # with the airport of origin and airport of destination and the date of departure or
        # with just the date of departure or
        # without arguments 
        # Now we are gonna see the arguments 
        arg1 = request.args.get('airportOfOrigin')
        arg2 = request.args.get('airportOfDestination')
        arg3 = request.args.get('dateOfDeparture')

        availableFlights = []

        if arg1 != None and arg2 != None and arg3 != None:
        
            iteriable = flights.find({})

            for flight in iteriable: 
                if flight['airportOfOrigin'] == arg1 and flight['airportOfDestination'] == arg2 and flight['dateOfDeparture'] == arg3:
                        if int(flight["availableTicketsEconomy"]) > 0 or int(flight["availableTicketsBusiness"]) > 0:
                            flight = {'_id': str(flight["_id"]),'dateOfDeparture':flight["dateOfDeparture"],'airportOfOrigin': flight["airportOfOrigin"],'airportOfDestination': flight["airportOfDestination"]} 
                            availableFlights.append(flight)

            if availableFlights != []:
                return jsonify(availableFlights)
            else:
                return Response("No flights found.\n")
        
        elif arg1 != None and arg2 != None:
        
            iteriable = flights.find({})
            for flight in iteriable: 
                if flight['airportOfOrigin'] == arg1 and flight['airportOfDestination'] == arg2:
                        if int(flight["availableTicketsEconomy"]) > 0 or int(flight["availableTicketsBusiness"]) > 0:
                            flight1 = {'_id': str(flight["_id"]),'dateOfDeparture':flight["dateOfDeparture"],'airportOfOrigin': flight["airportOfOrigin"],'airportOfDestination': flight["airportOfDestination"]} 
                            availableFlights.append(flight1)

            if availableFlights != []:
                return jsonify(availableFlights)
            else:
                return Response("No flights found.\n")
        
        elif arg3 != None:

            iteriable = flights.find({})

            for flight in iteriable: 
                if flight['dateOfDeparture'] == arg3:
                        if int(flight["availableTicketsEconomy"]) > 0 or int(flight["availableTicketsBusiness"]) > 0:
                            flight = {'_id': str(flight["_id"]),'dateOfDeparture':flight["dateOfDeparture"],'airportOfOrigin': flight["airportOfOrigin"],'airportOfDestination': flight["airportOfDestination"]} 
                            availableFlights.append(flight)

            if availableFlights != []:
                return jsonify(availableFlights)
            else:
                return Response("No flights found.\n")
        
        else:

            iteriable = flights.find({})

            for flight in iteriable: 
                if int(flight["availableTicketsEconomy"]) > 0 or int(flight["availableTicketsBusiness"]) > 0:
                    flight = {'_id': str(flight["_id"]),'dateOfDeparture':flight["dateOfDeparture"],'airportOfOrigin': flight["airportOfOrigin"],'airportOfDestination': flight["airportOfDestination"]} 
                    availableFlights.append(flight)

            if availableFlights != []:
                return jsonify(availableFlights)
            else:
                return Response("No flights found.\n")
    return Response('You are not logged in. Please login.',status=401,mimetype='application/json')

#Show flight details
@app.route('/getFlightDet/<id>', methods=['GET'])
def getFlightDet(id):
    if loggedIn():
        if id == None:
            return Response("Bad request", status=500, mimetype='application/json')
        
        flight = flights.find_one({"_id": ObjectId(id)})

        if flight != None:
            if isUser():

                flight["_id"] = str(flight["_id"])
                return jsonify(flight)
            elif isAdmin():

                iteriable = bookings.find({})
                x= 0
                z = 0

                for booking in iteriable:
                    if flight['airportOfOrigin'] == booking['airportOfOrigin'] and flight['airportOfDestination'] == booking['airportOfDestination'] and flight['dateOfDeparture'] == booking['dateOfDeparture']:
                        
                        if booking["typeOfTicket"] == "economy":
                            x = x +1
                        elif booking["typeOfTicket"] == "business":
                            z=z+1

                    
                totalEcon = int(flight['availableTicketsEconomy']) + x
                totalBus = int(flight['availableTicketsBusiness']) + z
                totalAll = totalEcon + totalBus
                totalAvailable = int(flight["availableTicketsEconomy"]) + int(flight["availableTicketsBusiness"])
                
                y ={"airportOfOrigin":flight['airportOfOrigin'],"airportOfDestination":flight['airportOfDestination'],"totalAmountOfTickets": str(totalAll),"totalAmountEconomy":str(totalEcon),"totalAmountBusiness":str(totalBus),
                    "totalAmountAvailTickets": str(totalAvailable),"availableTicketsEconomy":flight['availableTicketsEconomy'],"availableTicketsBusiness":flight['availableTicketsBusiness'],"valueTicketEconomy": flight['valueTicketEconomy'],"valueTicketBusiness": flight['valueTicketBusiness'],
                    "name":booking['name'], "surname": booking['surname'], "typeOfTicket": booking['typeOfTicket']}
                flight["_id"] = str(flight["_id"])
                return jsonify(y)
        
        return Response('no such flight found',status=500,mimetype='application/json')
    return Response('You are not logged in.',status=401,mimetype='application/json')
       
#book a ticket
@app.route('/bookTick/<id>', methods=['POST'])
def bookTick(id):

    if loggedIn() and isUser():
        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("Bad json content",status=400,mimetype='application/json')
        if data == None:
            return Response("Bad request",status=400,mimetype='application/json')
        if not "name" in data  or not "surname" in data or not "passportNumber" in data or not "dateOfBirth" in data  or not "email" in data or not "typeOfTicket" in data:
            return Response("Information incomplete",status=500,mimetype="application/json")

        user = users.find_one({"name": data['name'], "surname": data['surname'], "passportNumber": data['passportNumber'], "email": data['email']})

        if user != None:
        
            if id == None:
                return Response("Bad request", status=500, mimetype='application/json')
            
            flight = flights.find_one({"_id": ObjectId(id)})

            if flight != None:
                if int(flight["availableTicketsEconomy"]) > 0 or int(flight["availableTicketsBusiness"]) > 0:

                    booking = {"airportOfOrigin":flight['airportOfOrigin'],"airportOfDestination": flight['airportOfDestination'],"dateOfDeparture":flight['dateOfDeparture'],"name":data['name'], "surname": data['surname'], "passportNumber": data['passportNumber'],"dateOfBirth": data['dateOfBirth'],"email": data['email'],"typeOfTicket": data['typeOfTicket']}
                    
                    if booking['typeOfTicket'] == 'economy' and int(flight["availableTicketsEconomy"]) > 0:

                        bookings.insert_one(booking)

                        x = int(flight['availableTicketsEconomy'])-1
                        flights.update_one({'_id':ObjectId(id)},{'$set': {'availableTicketsEconomy': str(x)}})
                        return Response("Successful booking.",status=200,mimetype="application/json")
                    
                    elif booking['typeOfTicket'] == 'economy' and int(flight["availableTicketsEconomy"]) == 0:

                        return Response('No more ECONOMY tickets available for this flight',status=500,mimetype='application/json')
                    
                    elif booking['typeOfTicket'] == 'business' and int(flight["availableTicketsBusiness"]) > 0:
                    
                        bookings.insert_one(booking)

                        x = int(flight['availableTicketsBusiness'])-1
                        flights.update_one({'_id':ObjectId(id)},{'$set': {'availableTicketsBusiness': str(x)}})
                        return Response("Successful booking.",status=200,mimetype="application/json")
                        
                    elif booking['typeOfTicket'] == 'business' and int(flight["availableTicketsBusiness"]) == 0:

                        return Response('No more BUSINESS tickets available for this flight',status=500,mimetype='application/json')
                    elif booking['typeOfTicket'] != 'economy' and booking['typeOfTicket'] != 'business':

                        return Response('Wrong input of type of the ticket. Type "economy" or "business"',status=500,mimetype='application/json')
                    
                
                return Response('No more tickets available for this flight',status=500,mimetype='application/json')

            return Response('no such flight found',status=500,mimetype='application/json')
    
        return Response('no such user found',status=500,mimetype='application/json')
    return Response('You are not logged in.',status=401,mimetype='application/json')
       
#Show bookings
@app.route('/getBookings', methods=['GET'])
def getBookings():

    if loggedIn() and isUser():

        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("Bad json content",status=400,mimetype='application/json')
        if data == None:
            return Response("Bad request",status=400,mimetype='application/json')
        if  not "email" in data:
            return Response("Information incomplete. Please enter your email.",status=500,mimetype="application/json")
        
        user = users.find_one({"email": data['email']})
        users_bookings = []

        if user != None:

            iterable = bookings.find({})

            for booking in iterable:

                if booking['email'] == user['email']:
                    booking = ({"airportOfOrigin": booking['airportOfOrigin'],"airportOfDestination": booking['airportOfDestination'],"dateOfDeparture": booking['dateOfDeparture'],"name":user['name'],"surname":user['surname'],
                                "passportNumber": user['passportNumber'], "dateOfBirth": user['dateOfBirth'], "email": user['email'], "typeOfTicket": booking['typeOfTicket']})
                    users_bookings.append(booking)
                
            if users_bookings != []: 
                return jsonify(users_bookings)
            else:
                return Response('This user has no bookings.',status=500,mimetype='application/json')
        
        return Response('no user found',status=500,mimetype='application/json')
    
    return Response('You are not logged in.',status=401,mimetype='application/json')




# Show the booking details
@app.route('/getBookingDet/<id>', methods = ['GET'])
def getBookingDet(id) :

    if loggedIn() and isUser():

        if id == None:
            return Response("Bad request", status=500, mimetype='application/json')
        
        booking = bookings.find_one({"_id": ObjectId(id)})

        if booking != None:
            booking["_id"] = str(booking["_id"])
            return jsonify(booking)
        
        return Response('no such booking found',status=500,mimetype='application/json')
    
    return Response('You are not logged in.',status=401,mimetype='application/json')

#Delete booking
@app.route('/deleteBooking/<id>', methods=['DELETE'])
def deleteBooking(id):

    if loggedIn() and isUser():

        if id == None:
            return Response("Bad request", status=500, mimetype='application/json')
        
        booking = bookings.find_one({"_id": ObjectId(id)})
        if booking != None:
            
            bookings.delete_one(booking)

            iterable = flights.find({})

            for flight in iterable:

                if flight['airportOfOrigin'] == booking['airportOfOrigin'] and flight['airportOfDestination'] == booking['airportOfDestination'] and flight['dateOfDeparture'] == booking['dateOfDeparture']:

                    if booking['typeOfTicket'] == 'economy':
                       
                        x = int(flight['availableTicketsEconomy']) + 1
                        flights.update_one({'airportOfDestination':booking['airportOfDestination']},{'$set': {'availableTicketsEconomy': str(x)}})

                    elif booking['typeOfTicket'] == 'business':
                        
                        x = int(flight['availableTicketsBusiness']) + 1
                        flights.update_one({'airportOfDestination':booking['airportOfDestination']},{'$set': {'availableTicketsBusiness': str(x)}})
                    
            return Response("The booking has been deleted.",status=200,mimetype="application/json")

        return Response('no such booking found',status=500,mimetype='application/json')
    
    return Response('You are not logged in.',status=401,mimetype='application/json')

#delete user
@app.route('/deleteUser', methods = ['DELETE'])
def deleteUser():

    if loggedIn() and isUser():

        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("Bad json content",status=400,mimetype='application/json')
        if data == None:
            return Response("Bad request",status=400,mimetype='application/json')
        if  not "email" in data or not "password" in data:
            return Response("Information incomplete. Please enter your email or username.",status=500,mimetype="application/json")
        
        user = users.find_one({"email": data['email']})

        if user != None:
            users.delete_one(user)    
            return Response("User has been deleted.",status=200,mimetype="application/json")
        
        return Response('no such user found',status=500,mimetype='application/json')
        
    return Response('You are not logged in.',status=401,mimetype='application/json')

#create new flight
@app.route('/createNewFlight', methods=['POST'])
def createNewFlight():

    if loggedIn() and isAdmin():

        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("Bad json content",status=400,mimetype='application/json')
        if data == None:
            return Response("Bad request",status=400,mimetype='application/json')
        if not "airportOfOrigin" in data  or not "airportOfDestination" in data or not "dateOfDeparture" in data or not "availableTicketsEconomy" in data  or not "availableTicketsBusiness" in data or not "valueTicketEconomy" in data or not "valueTicketBusiness" in data  :
            return Response("Information incomplete",status=500,mimetype="application/json")
        
        
        flight = ({"airportOfOrigin": data['airportOfOrigin'], "airportOfDestination": data['airportOfDestination'],"dateOfDeparture": data['dateOfDeparture'], "availableTicketsEconomy": data['availableTicketsEconomy'], "availableTicketsBusiness": data['availableTicketsBusiness'], "valueTicketEconomy": data['valueTicketEconomy'], "valueTicketBusiness": data['valueTicketBusiness'] })
    
        if int(flight["availableTicketsEconomy"]) >= 0 and int(flight["availableTicketsBusiness"]) >= 0 and int(flight["valueTicketEconomy"]) >= 0 and int(flight["valueTicketBusiness"]):
            flights.insert_one(flight)
            return Response("New flight created.",status=200,mimetype="application/json")
        return Response('The tickets and prices must be greater or equal to 0. ',status=500,mimetype='application/json')
    
    elif loggedIn() and isUser():

        return Response('You dont have permission to perform this request.',status=403,mimetype='application/json')
    
    return Response('You are not logged in.',status=401,mimetype='application/json')
    
#update the value of the tickets
@app.route('/updateValue/<id>', methods= ['PATCH'])
def updateValue(id):
    
    if loggedIn() and isAdmin():

        data = None 
        try:
            data = json.loads(request.data)
        except Exception as e:
            return Response("Bad json content",status=400,mimetype='application/json')
        if data == None:
            return Response("Bad request",status=400,mimetype='application/json')
        if  not "valueTicketEconomy" in data or not "valueTicketBusiness" in data:
            return Response("Information incomplete. Please enter the value of the economy and business ticket that you wanna change.",status=500,mimetype="application/json")
    
        if id == None:
            return Response("Bad request", status=500, mimetype='application/json')
        
        flight = flights.find_one({"_id": ObjectId(id)})

        if flight != None:

            if int(flight["valueTicketEconomy"]) >= 0 and int(flight["valueTicketEconomy"]) >=0 :

                flights.update_one({'_id':ObjectId(id)},{'$set': {'valueTicketEconomy': data['valueTicketEconomy']}})
                flights.update_one({'_id':ObjectId(id)},{'$set': {'valueTicketBusiness': data['valueTicketBusiness']}})
                return Response("Values updated.",status=200,mimetype="application/json")
            
            return Response('The value of the ticket must be greater or equal to 0.',status=500,mimetype='application/json')
        return Response('no such flight found',status=500,mimetype='application/json')
    
    elif loggedIn() and isUser():

        return Response('You dont have permission to perform this request.',status=403,mimetype='application/json')
    
    return Response('You are not logged in.',status=401,mimetype='application/json')


# Delete flight
@app.route('/deleteFlight/<id>',methods=['DELETE'])
def deleteFlight(id):

    if loggedIn() and isAdmin():

        if id == None:
            return Response("Bad request", status=500, mimetype='application/json')
        
        flight = flights.find_one({"_id": ObjectId(id)})

        iteriable = bookings.find({})

        for booking in iteriable:
            if flight['airportOfOrigin'] == booking['airportOfOrigin'] and flight['airportOfDestination'] == booking['airportOfDestination'] and flight['dateOfDeparture'] == booking['dateOfDeparture']:
                #found a booking for this flight
                return Response('This flight cannot be deleted because there is at least one booking registered.',status=500,mimetype='application/json')
            
        flights.delete_one(flight)
        return Response("Flight deleted.",status=200,mimetype="application/json")
    
    elif loggedIn() and isUser():

        return Response('You dont have permission to perform this request.',status=403,mimetype='application/json')
    
    return Response('You are not logged in.',status=401,mimetype='application/json')    



# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
