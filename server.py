from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps, load, loads
from  flask_jsonpify import jsonify
import sqlite3
import protobuf

sqlite_file = "a1.sqlite"
app = Flask(__name__)
api = Api(app)

class RFQ(Resource):
    def get(self):
        attributes = ['ID','accountid','productnumber','quantity', 'price', 'pricevalidationperiod']
        conn = sqlite3.connect(sqlite_file)  # connect to database
        c = conn.cursor()
        c.execute("select * from rfq")  # This line performs query and returns json result
        r = c.fetchall()
        for tuple in r:
            x = {'rfq': [dict({n: m for n, m in zip(attributes, tuple)})]}
            print (x)
            return jsonify(x)

    def post(self):

        data = request.get_json()
        print(data['ID'])
        conn = sqlite3.connect(sqlite_file)  # connect to database
        c = conn.cursor()
        c.execute(("INSERT into rfq (ID, AccountID, ProductNumber, Quantity) VALUES ({a},{b},{c},{d})").format(a=data['ID'], b=data['accountid'], c=data['productnumber'], d=data['quantity']))  # This line performs query and returns json result
        conn.commit()
        return ((data))


class Account(Resource):
    def get(self):
        conn = sqlite3.connect(sqlite_file)  # connect to database
        c = conn.cursor()
        c.execute("select trackid, name, composer, unitprice from tracks;")
        result = c.fetchall()
        return dumps(result)


class Product_Number(Resource):
    def get(self, tracks_id):
        conn = sqlite3.connect(sqlite_file)  # connect to database
        c = conn.cursor()
        c.execute("select * from tracks where TrackId =%d " % int(tracks_id))
        result = c.fetchall()
        return dumps(result)


class Quantity(Resource):
    def get(self, employee_id):
        conn = sqlite3.connect(sqlite_file)  # connect to database
        c = conn.cursor()
        c.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = c.fetchall()
        return dumps(result)

api.add_resource(RFQ, '/rfq') # Route_1

if __name__ == '__main__':
     app.run(port='5002')

