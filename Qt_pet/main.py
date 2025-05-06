import sys
import os
from PySide2.QtWidgets import   QHBoxLayout,QInputDialog, QMessageBox,QApplication, QMainWindow, QWidget, QVBoxLayout,QLabel, QTextEdit, QLineEdit, QPushButton, QSplitter
from PySide2.QtCore import Qt, QUrl,QTimer
from PySide2.QtWebEngineWidgets import QWebEngineView
from cat import get_ai_cat_reply,random_cat_phrase
import requests
#from fetch import fetch_sol

from PySide2.QtCore import QRunnable, QThreadPool, Signal, QObject

class AIWorkerSignals(QObject):
    finished = Signal(str)

class AIWorker(QRunnable):
    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input
        self.signals = AIWorkerSignals()

    def run(self):
        try:
            reply = get_ai_cat_reply(self.user_input)
            self.signals.finished.emit(reply)
        except Exception as e:
            self.signals.finished.emit(f"喵呜，出错啦~ {e}")



def query_sol(address):
    url = f"http://47.86.28.231:8000/sol?address={address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('info', '未找到相关信息')
    except requests.exceptions.RequestException as e:
        print("请求出错:", e)
        return "查询失败，请稍后重试。"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("桌宠AI")
        self.setFixedSize(400, 400)
        self.offset = None
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint |Qt.WindowStaysOnTopHint |Qt.Tool))
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.thread_pool = QThreadPool()

        # 创建一个覆盖层容器
        self.overlay_widget = QWidget(self)
        self.overlay_widget.setGeometry(0, 0, self.width(), self.height())
        self.overlay_widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.overlay_widget.setStyleSheet("background: transparent;")
        self.overlay_layout = QVBoxLayout(self.overlay_widget)
        self.overlay_layout.setContentsMargins(0, 0, 0, 0)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # 主部件
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        # Live2D显示
        self.web_view = QWebEngineView()
        html_path = os.path.abspath("live2d.html")
        self.web_view.load(QUrl.fromLocalFile(html_path))
        self.web_view.setFixedHeight(400)
        self.web_view.page().setBackgroundColor(Qt.transparent)

        # 提示圆按钮
        self.tip_button = QPushButton("SOL")
        self.tip_button.setFixedSize(100, 100)
        self.tip_button.setParent(self.overlay_widget)
        self.tip_button.move(self.width()+50, 0)
        self.tip_button.raise_()
        self.tip_button.show()
        self.tip_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 150);
                color: white;
                font-weight: bold;
            }
        """)

        #self.tip_button.hide()
        self.tip_button.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.tip_button.clicked.connect(self.open_input_dialog)
        QTimer.singleShot(0, self.raise_tip_button)

        # 对话
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(5, 5, 5, 5)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("对我说点什么吧~")
        self.input_line.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.send_button)

        layout.addWidget(self.web_view)
        layout.addWidget(input_widget)

        self.setCentralWidget(main_widget)

        self.overlay = QLabel(self)
        self.overlay.setGeometry(0, 0, 300, 300)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.overlay.mousePressEvent = self.mousePressEvent
        self.overlay.mouseMoveEvent = self.mouseMoveEvent
        self.overlay.mouseReleaseEvent = self.mouseReleaseEvent

        self.tip_button.setParent(self)
        self.tip_button.raise_()
        self.tip_button.show()





    def enterEvent(self, event):
        self.tip_button.show()

    def leaveEvent(self, event):
        self.tip_button.hide()

    def open_input_dialog(self):
        print("按钮被点击了")
        address, ok = QInputDialog.getText(self, "查询SOL余额", "请输入SOL地址：")
        if ok and address:
            info = query_sol(address)
            QMessageBox.information(self, "查询结果", info)


    def send_message(self):
        user_input = self.input_line.text().strip()
        if not user_input:
            self.show_chat_bubble("喵宝：正在思考中喵~💭")
            return

        self.show_chat_bubble("喵宝：正在思考中喵~💭")
        worker = AIWorker(user_input)
        worker.signals.finished.connect(self.display_reply)
        self.thread_pool.start(worker)

    def display_reply(self, reply):
        formatted_reply = reply.replace('\n', '<br>')
        self.show_chat_bubble(f"喵宝：{formatted_reply}")


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()


    def mouseMoveEvent(self, event):
        if self.offset and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None
        self.show_chat_bubble(random_cat_phrase())

    def show_chat_bubble(self, text):
        safe_text = text.replace('"', '\\"').replace("\n", "<br>")
        js_code = f'showBubble("{safe_text}");'
        self.web_view.page().runJavaScript(js_code)


    def raise_tip_button(self):
        self.tip_button.move(150, 150)  # 确保在合适位置
        self.tip_button.raise_()
        self.tip_button.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
