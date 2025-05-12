import sys
import os
from PySide2.QtWidgets import   QHBoxLayout,QInputDialog, QMessageBox,QApplication, QMainWindow, QWidget, QVBoxLayout,QLabel, QTextEdit, QLineEdit, QPushButton, QSplitter
from PySide2.QtCore import Qt, QUrl,QTimer
from PySide2.QtWebEngineWidgets import QWebEngineView
from cat import get_ai_cat_reply,random_cat_phrase
import requests
from utils import fetch

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



# def query_sol(address):
#     url = f"http://47.86.28.231:8000/sol?address={address}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         return data.get('info', '未找到相关信息')
#     except requests.exceptions.RequestException as e:
#         print("请求出错:", e)
#         return "查询失败，请稍后重试。"

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
        self.tip_button.setFixedSize(60, 60)
        self.tip_button.setParent(self.overlay_widget)
        self.tip_button.move(self.width() - 70, 10)
        self.tip_button.raise_()
        self.tip_button.show()
        self.tip_button.setStyleSheet("""
            QPushButton {
                border-radius: 30px;
                background-color: rgba(0, 0, 0, 150);
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid white;
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
            res = fetch.sol(address, port="7897") # 使用代理
            if res.get("success"):
                data = res["data"]
                # 显示余额和代币信息
                overview_info = f"账户余额: {data['overview']['account']['余额']} SOL\n\n"
                if data['overview']['token']['数量'] > 0:
                    token_info = data['overview']['token']['当前持有'][0]
                    overview_info += f"代币信息:\n"
                    overview_info += f"名称: {token_info['tokenName']}\n"
                    overview_info += f"符号: {token_info['tokenSymbol']}\n"
                    overview_info += f"数量: {token_info['balance']}\n"
                    overview_info += f"价值: {token_info['value']} USDT"
                
                QMessageBox.information(self, "账户概览", overview_info)
                
                # 历史交易按钮
                history_button = QPushButton("查看历史交易", self)
                history_button.clicked.connect(lambda: self.show_transaction_history(data['history']['transaction']))
                history_button.setFixedSize(60, 60)
                history_button.setStyleSheet("""
                    QPushButton {
                        border-radius: 30px;
                        background-color: #4CAF50;
                        color: white;
                        font-weight: bold;
                        font-size: 12px;
                        border: 2px solid rgba(255, 255, 255, 0.5);
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                        border: 2px solid white;
                    }
                """)
                # 将历史交易按钮放在SOL按钮的下方
                history_button.move(self.tip_button.x(), self.tip_button.y() + 70)
                history_button.raise_()
                history_button.show()
            else:
                QMessageBox.warning(self, "查询失败", f"Error: {res.get('error')}")

    def show_transaction_history(self, transactions):
        history_text = "历史交易记录:\n\n"
        for tx in transactions:
            time_str = self.format_timestamp(tx['time'])
            history_text += f"时间: {time_str}\n"
            history_text += f"交易方: {', '.join(tx['by'])}\n"
            history_text += f"交易额: {tx['value']} SOL\n"
            history_text += f"手续费: {tx['fee']}\n"
            history_text += "-" * 40 + "\n"
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("交易历史")
        msg_box.setText(history_text)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                min-width: 400px;
            }
        """)
        msg_box.exec_()

    def format_timestamp(self, timestamp):
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


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
        self.tip_button.move(self.width() - 70, 10)  # 放在右上角
        self.tip_button.raise_()
        self.tip_button.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
