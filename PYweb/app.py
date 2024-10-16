import threading
import webview
from flask import Flask
from flask_cors import CORS

# pyinstaller app.spec
app = Flask(__name__)
CORS(app)

# 注册蓝图
from blueprints.image_processing import image_processing_bp
from blueprints.parameters import parameters_bp
from blueprints.k_img import k_img_bp
app.register_blueprint(k_img_bp)
app.register_blueprint(image_processing_bp)
app.register_blueprint(parameters_bp)

def start_flask():
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    # 启动Flask应用程序线程
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 创建Webview窗口
    # http://localhost:5173/
    # web/index.html
    # .\.venv\Scripts\activate 
    webview.create_window("智算优先流软件", "web/index.html", width=1000, height=800, resizable=False)
    webview.start(debug=True)
    # webview.start()


