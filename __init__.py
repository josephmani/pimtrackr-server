import psycopg2
import urllib.parse as up

from flask import Flask,g,request
from flask import render_template,jsonify
from flask_cors import CORS,cross_origin

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(os.path.dirname(os.path.realpath(__file__)), '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")

up.uses_netloc.append("postgres")
url = up.urlparse(DATABASE_URL)
dbconn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)



def create_app():
#create_app is a keyword.
	app= Flask(__name__)
	#CORS(app)
	app.config.from_mapping(
		DATABASE= "pimdb"
	)
		
	@app.route("/")
	#@cross_origin()
	def index():
		response = jsonify(message="Simple server is running")
		return response
		
	
	@app.route("/login", methods=["POST"])
	#@cross_origin())
	def loginpage():
		cursor = dbconn.cursor()
		print('haha')
		#print(request.form)
		username= request.json['username']
		password= request.json['password']
		cursor.execute("SELECT id,pwd from users where uname=%s",(username,))
		temp= cursor.fetchone()
		if temp:
			deets,passcode=temp
			if passcode==password:
				return jsonify(temp)
			else:
				return jsonify(message="Incorrect password")
		else:
			return jsonify(message="Incorrect username")
				

	
	@app.route("/register", methods=["POST"])
	def registration():
		cursor = dbconn.cursor()
		username= 'lee'
		name='Lenoah'
		password='manipwoli'
		cursor.execute("INSERT INTO users (name, uname, pwd) VALUES(%s, %s, %s)",(name, username, password))
		dbconn.commit()
		return "details entered"
	

	@app.route("/fillnote", methods=["POST"])
	def fillnotes():
		cursor = dbconn.cursor()
		userid= 2
		ntitle='internship'
		description='shakthiman foundation'
		hashtag_ids='hustle'
		hash_id=hashtag_ids.split(',')
		
				
		cursor.execute("INSERT INTO notes (title,dcp,hids,uid) VALUES(%s, %s, %s, %s)",(ntitle, description, hashtag_ids, userid))
		dbconn.commit()
		
		#to get notesid 
		cursor = dbconn.cursor()
		cursor.execute("SELECT MAX(nid) from notes")
		notesid= cursor.fetchall()[0]
		dbconn.commit()
		
		for hashes in hash_id:	
				cursor = dbconn.cursor()
				cursor.execute("INSERT INTO hashtags (label,nid,uid) VALUES (%s, %s, %s)",(hashes, notesid, userid))
				dbconn.commit()
		
		cursor = dbconn.cursor()
		cursor.execute("SELECT title,dcp,hids from notes where uid= %s",(userid,))
		values= cursor.fetchall()
		return f"Note Entered:\n{values}"


	@app.route("/getallnotes", methods=["GET"])
	def getnotes():
		cursor = dbconn.cursor()
		userid= 2
		cursor.execute("SELECT * from notes where uid= %s",(userid,))
		values= cursor.fetchall()
		dbconn.commit()
		response = jsonify(values)
		return response

		
	@app.route("/update", methods=["PUT"])
	def updatenote():
		cursor = dbconn.cursor()
		userid=3
		old_title='gaming'
		ntitle='Complete Genskill assignment'
		description='Intro to Javascript'
		hashtag_ids='study,hustle'
		hash_id=hashtag_ids.split(',')
		
		#get notesid to update
		cursor.execute("SELECT nid from notes where title=%s and uid=%s",(old_title,userid))
		notesid= cursor.fetchall()[0]
		dbconn.commit()
		
		cursor = dbconn.cursor()
		cursor.execute("UPDATE notes SET title=%s, dcp=%s, hids=%s where nid=%s and uid=%s",(ntitle, description, hashtag_ids, notesid, userid))
		cursor.execute("DELETE FROM hashtags where nid=%s and uid=%s",(notesid, userid))
		dbconn.commit()
		
		
		for hashes in hash_id:	
				cursor = dbconn.cursor()
				cursor.execute("INSERT INTO hashtags (label,nid,uid) VALUES (%s, %s, %s)",(hashes, notesid, userid))
				dbconn.commit()
		
		cursor = dbconn.cursor()
		cursor.execute("SELECT title,dcp,hids from notes where nid= %s and uid=%s",(notesid,userid))
		values= cursor.fetchall()
		dbconn.commit()
		return f"Note Updated as:\n{values}"	
		
	
	@app.route("/delete", methods=["DELETE"])
	def deletenote():
		cursor = dbconn.cursor()
		userid=3
		old_title='Complete Genskill assignment'
		
		#get notesid to delete
		cursor.execute("SELECT nid from notes where title=%s and uid=%s",(old_title, userid))
		notesid= cursor.fetchall()[0]

		cursor.execute("DELETE FROM hashtags where nid=%s and uid=%s",(notesid, userid))
		cursor.execute("DELETE FROM notes where nid=%s and uid=%s",(notesid, userid))
		
		dbconn.commit()
		return "Note Deleted"


	
	@app.route("/hashtags", methods=["GET"])
	def gethashtags():
		cursor = dbconn.cursor()
		userid= 2
		cursor.execute("SELECT label from hashtags where uid= %s",(userid,))
		values= cursor.fetchall()
		dbconn.commit()
		response = jsonify(values)
		return response		
	
	return app	

