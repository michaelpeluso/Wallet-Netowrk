from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        connection = pymysql.connect(host='localhost', user='root', password='', database='wallet_db')
        with connection.cursor() as cursor:
            query = "INSERT INTO users (Name, SSN, Email) VALUES (%s, %s, %s)"
            cursor.execute(query, (data['name'], data['ssn'], data['email']))
            connection.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
