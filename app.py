from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='newsfeed_db',
            user='your_username',
            password='your_password'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Post CRUD operations
@app.route('/post', methods=['POST'])
def add_post():
    data = request.json
    user_id = data.get('user_id')
    content = data.get('content')

    if not user_id or not content:
        return jsonify({"error": "Missing required fields"}), 400

    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO posts (user_id, content) VALUES (%s, %s)"
            cursor.execute(query, (user_id, content))
            connection.commit()
            return jsonify({"message": "Post created successfully", "post_id": cursor.lastrowid}), 201
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    content = data.get('content')

    if not content:
        return jsonify({"error": "Missing content field"}), 400

    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE posts SET content = %s WHERE id = %s"
            cursor.execute(query, (content, post_id))
            connection.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Post not found"}), 404
            return jsonify({"message": "Post updated successfully"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM posts WHERE id = %s"
            cursor.execute(query, (post_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Post not found"}), 404
            return jsonify({"message": "Post deleted successfully"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM posts WHERE id = %s"
            cursor.execute(query, (post_id,))
            post = cursor.fetchone()
            if post:
                return jsonify(post), 200
            else:
                return jsonify({"error": "Post not found"}), 404
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)