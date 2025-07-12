#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'fan',  # 请根据实际情况修改密码
    'database': 'actors',
    'raise_on_warnings': True
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

@app.route('/actors', methods=['GET'])
def get_actors():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': '无法连接到数据库'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM characters")
        actors = cursor.fetchall()
        return jsonify(actors)
    except Error as e:
        return jsonify({'error': f'查询失败: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/actors/<name>', methods=['GET'])
def get_actor_by_name(name):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': '无法连接到数据库'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM characters WHERE name = %s", (name,))
        actor = cursor.fetchone()
        if actor:
            return jsonify(actor)
        else:
            return jsonify({'error': '未找到该演员'}), 404
    except Error as e:
        return jsonify({'error': f'查询失败: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api', methods=['GET'])
def list_apis():
    """列出所有可用的API端点"""
    apis = {
        'available_endpoints': [
            {
                'path': '/actors',
                'methods': ['GET'],
                'description': '获取所有演员信息'
            },
            {
                'path': '/actors/<name>',
                'methods': ['GET'],
                'description': '根据姓名获取演员信息'
            }
        ]
    }
    return jsonify(apis)

if __name__ == '__main__':
    app.run(debug=True)