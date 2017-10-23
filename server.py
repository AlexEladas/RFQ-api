from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import flask_jsonpify as jsonify

db_connect = create_engine('sqlite:///a1.db')
app = Flask(__name__)
api = Api(app)

class RFQ(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from employees")  # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID


class Account(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return dumps(result)


class Product_Number(Resource):
    def get(self, tracks_id):
        conn = db_connect.connect()
        query = conn.execute("select * from tracks where TrackId =%d " % int(tracks_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return dumps(result)


class Quantity(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return dumps(result)

