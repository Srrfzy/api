#!/usr/bin/env python3
# 指定使用 Python 3 解释器运行此脚本

# 导入所需的模块
from flask import Flask, jsonify  # Flask 是一个轻量级的 Web 框架，jsonify 用于将 Python 字典转换为 JSON 响应
from flask_cors import CORS  # flask_cors 扩展用于处理跨域资源共享（CORS）
import mysql.connector  # mysql.connector 用于连接和操作 MySQL 数据库
from mysql.connector import Error  # Error 类用于捕获数据库操作中的错误

# 创建 Flask 应用实例
app = Flask(__name__)
# 启用 CORS，允许来自不同域的请求访问 API
CORS(app)

# 数据库配置信息
DB_CONFIG = {
    'host': 'localhost',  # 数据库服务器地址
    'user': 'root',  # 数据库用户名
    'password': 'fan',  # 数据库密码（请根据实际情况修改）
    'database': 'actors',  # 要连接的数据库名称
    'raise_on_warnings': True  # 当出现警告时抛出异常
}

# 定义获取数据库连接的函数
def get_db_connection():
    try:
        # 使用配置信息连接数据库
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():  # 如果连接成功
            return conn  # 返回连接对象
    except Error as e:  # 捕获数据库连接错误
        print(f"数据库连接错误: {e}")
        return None  # 连接失败时返回 None

# 定义路由 '/actors'，支持 GET 请求
@app.route('/actors', methods=['GET'])
def get_actors():
    # 获取数据库连接
    conn = get_db_connection()
    if not conn:  # 如果连接失败
        return jsonify({'error': '无法连接到数据库'}), 500  # 返回 500 错误和错误信息

    # 创建数据库游标（返回字典格式的结果）
    cursor = conn.cursor(dictionary=True)
    try:
        # 执行 SQL 查询：获取 characters 表中的所有数据
        cursor.execute("SELECT * FROM characters")
        actors = cursor.fetchall()  # 获取所有查询结果
        return jsonify(actors)  # 将结果转换为 JSON 格式返回
    except Error as e:  # 捕获查询过程中的错误
        return jsonify({'error': f'查询失败: {e}'}), 500  # 返回 500 错误和错误信息
    finally:
        cursor.close()  # 确保无论如何都关闭游标
        conn.close()  # 确保无论如何都关闭数据库连接

# 定义路由 '/actors/<name>'，支持 GET 请求，<name> 是 URL 参数
@app.route('/actors/<name>', methods=['GET'])
def get_actor_by_name(name):
    # 获取数据库连接
    conn = get_db_connection()
    if not conn:  # 如果连接失败
        return jsonify({'error': '无法连接到数据库'}), 500

    # 创建数据库游标（返回字典格式的结果）
    cursor = conn.cursor(dictionary=True)
    try:
        # 执行带参数的 SQL 查询：根据姓名查询演员信息
        cursor.execute("SELECT * FROM characters WHERE name = %s", (name,))
        actor = cursor.fetchone()  # 获取单条查询结果
        if actor:  # 如果找到结果
            return jsonify(actor)  # 返回 JSON 格式的演员信息
        else:  # 如果没有找到结果
            return jsonify({'error': '未找到该演员'}), 404  # 返回 404 错误和错误信息
    except Error as e:  # 捕获查询过程中的错误
        return jsonify({'error': f'查询失败: {e}'}), 500
    finally:
        cursor.close()  # 确保无论如何都关闭游标
        conn.close()  # 确保无论如何都关闭数据库连接

# 定义路由 '/api'，支持 GET 请求
@app.route('/api', methods=['GET'])
def list_apis():
    """列出所有可用的API端点"""
    # 定义 API 接口信息
    apis = {
        'available_endpoints': [
            {
                'path': '/actors',  # 接口路径
                'methods': ['GET'],  # 支持的 HTTP 方法
                'description': '获取所有演员信息'  # 接口描述
            },
            {
                'path': '/actors/<name>',  # 接口路径，包含 URL 参数
                'methods': ['GET'],  # 支持的 HTTP 方法
                'description': '根据姓名获取演员信息'  # 接口描述
            }
        ]
    }
    return jsonify(apis)  # 返回 JSON 格式的 API 文档

# 如果作为主程序运行，则执行以下代码
if __name__ == '__main__':
    app.run(debug=True)  # 启动 Flask 开发服务器，debug=True 表示开启调试模式