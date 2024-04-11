import http.server
import json
from urllib.parse import urlparse
import sqlite3
import bcrypt
import jwt
import os

#load env variables from database
from dotenv import load_dotenv

load_dotenv('.env')

#Database configuration from the .env file
DB_NAME = os.getenv('DB_NAME')

sessions = {}

#Create a connection to the database
def connect_to_database():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  
    return conn


#Create database and tables if they don't exist for both the users and corresponding reservations
def create_database():
    try:
        #Connect to the created database
        return connect_to_database()
    except Exception as e:
        print(f"Error creating database: {e}")
        return None

def create_tables():
    connection = connect_to_database()  #get connection
    cursor = connection.cursor()
    try:
        #Create both users and reservations table
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT NOT NULL,
                          email TEXT NOT NULL,
                          password_hash TEXT NOT NULL
                          )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS reservations (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER NOT NULL,
                          date TEXT NOT NULL,
                          time TEXT NOT NULL,
                          party_size INTEGER NOT NULL,
                          FOREIGN KEY (user_id) REFERENCES users(id)
                          )""")
        connection.commit()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        if connection:
            connection.close()

#Create database and tables if they don't exist
create_database()
create_tables()

#server.http handle methods 
class RequestHandler(http.server.BaseHTTPRequestHandler):
    #function to handle cors, json, etc
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'content-type, Authorization')
        self.end_headers()

    #config of CORS
    def do_OPTIONS(self):
        self._set_headers()

    #this will create a token everytime the user logs in
    def generate_token(self, user_id):
        token = jwt.encode({'user_id': user_id}, '123', algorithm='HS256')
        return token
    
    #GET METHOD 
    def do_GET(self):
        # Get the token from the Authorization header
        token = self.headers.get('Authorization')
        if not token:
            self._set_headers(401)
            self.wfile.write(json.dumps({'message': 'No token provided'}).encode())
            return

        token = token.replace('Bearer ', '')

        #Check token
        user_id = sessions.get(token)
        if not user_id:
            self._set_headers(401)
            self.wfile.write(json.dumps({'message': 'Invalid token'}).encode())
            return

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        #if url request is '/reservations
        if path == '/reservations':
            #try block
            try:
                connection = connect_to_database()
                cursor = connection.cursor()
                #get reservations
                cursor.execute("SELECT * FROM reservations WHERE user_id = ?", (user_id,))
                reservations = cursor.fetchall()

                reservations = [dict(row) for row in reservations]

                self._set_headers(200)
                self.wfile.write(json.dumps(reservations).encode())
            except Exception as e:
                print(f"Error retrieving reservations from database: {e}")
                self._set_headers(500)
                self.wfile.write(json.dumps({'message': 'Internal server error'}).encode())
            finally:
                if connection:
                    connection.close()

    #POST METHOD
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        #if url is '/register
        if path == '/register':
            #Register new user
            try:
                connection = connect_to_database()
                cursor = connection.cursor()
                #check if there is already a user
                cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (data['username'], data['email']))
                existing_user = cursor.fetchone()
                if existing_user:
                    raise ValueError('Username or email already exists')

                #hash the password using bcrypt
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

                #save user
                sql = "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)"
                cursor.execute(sql, (data['username'], data['email'], hashed_password))
                connection.commit()
            except Exception as e:
                print(f"Error saving user data to database: {e}")
            finally:
                if connection:
                    connection.close()

            self._set_headers(201)
            self.wfile.write(json.dumps({'message': 'User registered successfully'}).encode())

        #if the url is '/login
        elif path == '/login':
            #generate token
            try:
                connection = connect_to_database()
                cursor = connection.cursor()
                #get user data
                cursor.execute("SELECT * FROM users WHERE username = ?", (data['username'],))
                user = cursor.fetchone()
                if not user:
                    raise ValueError('User not found')

                #check password
                if bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash']):
                    #generate token
                    token = self.generate_token(user['id'])
                    sessions[token] = user['id']

                    self._set_headers(200)
                    self.wfile.write(json.dumps({'message': 'Login successful', 'token': token, 'user_id': user['id']}).encode())
                else:
                    raise ValueError('Incorrect password')
            except Exception as e:
                print(f"Error logging in: {e}")
                self._set_headers(401)
                self.wfile.write(json.dumps({'message': 'Login failed'}).encode())
            finally:
                if connection:
                    connection.close()

        #if the url is '/reservations'
        elif path == '/reservations':
            #make reservation
            try:
                connection = connect_to_database()
                cursor = connection.cursor()
                #insert reservation data
                sql = "INSERT INTO reservations (user_id, date, time, party_size) VALUES (?, ?, ?, ?)"
                cursor.execute(sql, (data['user_id'], data['date'], data['time'], data['partySize']))
                connection.commit()
            except Exception as e:
                print(f"Error saving reservation to database: {e}")
            finally:
                if connection:
                    connection.close()

            self._set_headers(201)
            self.wfile.write(json.dumps({'message': 'Reservation made successfully'}).encode())

    #PUT METHOD
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data)

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/reservations'):
            #update reservations
            try:
                connection = connect_to_database()
                cursor = connection.cursor()
                #get the reservation id 
                reservation_id = path.split('/')[-1]

                #update reservation
                sql = "UPDATE reservations SET date = ?, time = ?, party_size = ? WHERE id = ?"
                cursor.execute(sql, (data['date'], data['time'], data['party_size'], reservation_id))
                connection.commit()
            except Exception as e:
                print(f"Error updating reservation in database: {e}")
            finally:
                if connection:
                    connection.close()

            self._set_headers(200)
            self.wfile.write(json.dumps({'message': 'Reservation updated successfully'}).encode())
    
    #DELETE METHOD
    def do_DELETE(self):
        #get token
        token = self.headers.get('Authorization')
        if not token:
            self._set_headers(401)
            self.wfile.write(json.dumps({'message': 'No token provided'}).encode())
            return

        token = token.replace('Bearer ', '')

        #check token = vaild
        user_id = sessions.get(token)
        if not user_id:
            self._set_headers(401)
            self.wfile.write(json.dumps({'message': 'Invalid token'}).encode())
            return

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/reservations/'):
            #get reservation_id
            reservation_id = path.split('/')[-1]

            #delete a reservation
            try:
                connection = connect_to_database()
                cursor = connection.cursor()
                #do action
                cursor.execute("DELETE FROM reservations WHERE id = ? AND user_id = ?", (reservation_id, user_id))
                connection.commit()

                self._set_headers(200)
                self.wfile.write(json.dumps({'message': 'Reservation deleted successfully'}).encode())
            except Exception as e:
                print(f"Error deleting reservation from database: {e}")
                self._set_headers(500)
                self.wfile.write(json.dumps({'message': 'Internal server error'}).encode())
            finally:
                if connection:
                    connection.close()

#Start the server
def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()