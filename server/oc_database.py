'''
This file is going to handle everything regarding the database
'''
import sqlite3
import json
import os 
from tabulate import tabulate


class Database:
    def __init__(self) -> None:
        self.location = "./serverdb.db"
        self.cur = None # Database cursor (needed to execute SQL queries)
        self.con = self.connectToDatabase() # Connection instance 

    # If the database didn't exist create all the tables. 
    def buildDatabase(self) -> None:
        
        # Enable foreign keys
        self.query("PRAGMA foreign_keys = ON") 

        # Create the user table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY, 
                name VARCHAR(16), 
                created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
                version VARCHAR(45), 
                status VARCHAR(45), 
                room INTEGER, 
                FOREIGN KEY (room) REFERENCES room(id)          
            )
            ''')
                            
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS room (
            id      INTEGER PRIMARY KEY NOT NULL, 
            created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            name    VARCHAR(45)      
           ) 
            ''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS message (
                id      INTEGER  PRIMARY KEY,
                date    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                text    LONGTEXT, 
                data    LONGBLOB,  
                room_id INTEGER, 
                user_id INTEGER,
                FOREIGN KEY(room_id) REFERENCES room(id), 
                FOREIGN KEY(user_id) REFERENCES user(id) 
            )         
            ''')
        
    
        tables = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        for table in tables:
            print(table)
    
    
    def checkUser(self, user):
        sql =f"""
        SELECT
            CASE
            WHEN EXISTS (
                SELECT 1
                FROM user
                WHERE name = '{user}'
            )
            THEN 1
            ELSE 0
            END AS value_exists;
        """
        response = self.query(sql)
        return response.fetchone()
    
    def insertUser(self, user):
        sql = f"""
            INSERT INTO user (name) VALUES ('{user}')
        """
        self.query(sql)
        
        
        
    
    

    # Check if the database exists already and connect. If it doens't exist create the db file. 
    def connectToDatabase(self) -> None:
        exists = os.path.exists(self.location)
        self.con = sqlite3.connect(self.location, check_same_thread=False)
        self.cur = self.con.cursor()
        if not exists: # If the database didn't exist create the tables
            print("DB Doesn't Exist. Creating the db...")
            self.buildDatabase()
        return self.con
        


        


    

    # Load the database
    def load_database():
        pass
        
    def sanitizedQuery(self, command, parameters=None):
        command = self.cur.execute(command, parameters)
        self.con.commit()
        return command
    
    
    # Query the database
    def query(self, command):
        command = self.cur.execute(command)
        self.con.commit()
        # print(f"Command: {command}")
        return command
