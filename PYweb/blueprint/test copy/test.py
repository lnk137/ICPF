from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from tkinter import filedialog

test = Blueprint('test', __name__)

@test.route('/login', methods=['GET'])
def login():
    return "12345"

@test.route('/getModelPath', methods=['POST'])
def getModelPath():
    # 打开文件选择对话框，并返回选择的文件路径
    file_path = filedialog.askopenfilename()
    # 输出选择的文件路径
    print(f"选择的文件路径: {file_path}")
    # 返回文件路径，使用 JSON 格式
    return jsonify({"file_path": file_path})

@test.route('/register', methods=['POST'])
def register():
    return "789"

