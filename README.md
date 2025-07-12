# 演员信息管理系统 API

## 项目简介
本项目是一个基于 Flask 的演员信息管理系统 API，提供对演员信息的查询功能。

## 技术栈
- Python 3
- Flask
- MySQL
- flask-cors

## 数据库配置
- 主机: localhost
- 用户: root
- 数据库: actors

## API 接口

### 获取所有演员信息
- **路径**: `/actors`
- **方法**: GET
- **描述**: 获取数据库中存储的所有演员信息。

### 根据姓名查询演员信息
- **路径**: `/actors/<name>`
- **方法**: GET
- **描述**: 根据演员姓名查询对应的演员信息。

### 获取 API 接口列表
- **路径**: `/api`
- **方法**: GET
- **描述**: 获取当前系统提供的所有 API 接口信息。

## 运行说明
1. 确保已安装依赖: `pip install flask flask-cors mysql-connector-python`
2. 启动服务: `python app.py`
3. 默认运行在 `http://127.0.0.1:5000/`

## 注意事项
- 请确保 MySQL 服务已经启动
- 请根据实际情况修改数据库密码