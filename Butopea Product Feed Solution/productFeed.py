import sqlite3

dbconnection= sqlite3.connect("data.sqlite")
cursor = dbconnection.cursor()