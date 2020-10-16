import sys, os
import json
from tempfile import NamedTemporaryFile
import pkg_resources
from pygments.lexers.data import JsonLexer
from pygments.formatters import HtmlFormatter
from pygments import highlight

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog, QPushButton,
                             QHBoxLayout, QLabel, QMainWindow, QToolBar, QVBoxLayout, QWidget, QTextBrowser,
                             QSizePolicy)

from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

from amda_sciqlop_speed_tester.images import MainPage
from amda_sciqlop_speed_tester.speed_teser_sequence import TestSequence


class AMDA_SciQLop_Speed_tester(QMainWindow):

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super(AMDA_SciQLop_Speed_tester, self).__init__(parent)
        self.setWindowTitle('AMDA_SciQLop_Speed_tester')
        window_icon = pkg_resources.resource_filename('amda_sciqlop_speed_tester.images',
                                                      'logo.png')
        self.setWindowIcon(QIcon(window_icon))

        self.widget = QWidget()
        self.main_layout = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)

        self._result = {"None": None}

        self.start_test_qpb = QPushButton("Start test")
        self.send_result_qpb = QPushButton("Send result")
        self.send_result_qpb.setDisabled(True)
        self.save_result_qpb = QPushButton("Save result")
        self.save_result_qpb.setDisabled(True)

        self.start_test_qpb.setStyleSheet(
            "font: bold;background-color: #90EE90;font-size: 36px;height: 48px;width: 120px;")
        self.send_result_qpb.setStyleSheet(
            "font: bold;background-color: #90EE90;font-size: 36px;height: 48px;width: 120px;")
        self.save_result_qpb.setStyleSheet(
            "font: bold;background-color: #90EE90;font-size: 36px;height: 48px;width: 120px;")
        self.view = QWebEngineView()
        self.page = QWebEnginePage()
        self.view.setPage(self.page)
        self.html_page = MainPage()
        self.page.setHtml(self.html_page.html())
        self.main_layout.addWidget(self.view)
        self.buttons_layout = QHBoxLayout()
        button_wdgt = QWidget()
        button_wdgt.setLayout(self.buttons_layout)
        button_wdgt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.main_layout.addWidget(button_wdgt)
        self.buttons_layout.addWidget(self.start_test_qpb)
        self.buttons_layout.addWidget(self.send_result_qpb)
        self.buttons_layout.addWidget(self.save_result_qpb)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')

        self.test_sequence = TestSequence()
        self.test_sequence.message.connect(self.status_bar.showMessage)
        self.test_sequence.done.connect(self.test_complete)
        self.test_sequence.update_progress.connect(self.progress_update)
        self.test_sequence.push_result.connect(self.show_result)
        self.start_test_qpb.clicked.connect(self.start_test)
        self.send_result_qpb.clicked.connect(self.send_result)
        self.save_result_qpb.clicked.connect(self.save_result)

        self.resize(1024, 900)

    def start_test(self):
        self.start_test_qpb.setEnabled(False)
        self.send_result_qpb.setEnabled(False)
        self.save_result_qpb.setEnabled(False)
        self.test_sequence.start()

    def progress_update(self, task, value):
        self.html_page.update(**{task: value})
        self.page.setHtml(self.html_page.html())

    def show_result(self, result: dict):
        self._result = result
        pretty_result = json.dumps(result, indent=4)
        html = highlight(pretty_result, JsonLexer(), HtmlFormatter())
        self.html_page.update(result=html)
        self.page.setHtml(self.html_page.html())

    def test_complete(self, success: bool):
        self.start_test_qpb.setEnabled(True)
        self.send_result_qpb.setEnabled(True)
        self.save_result_qpb.setEnabled(True)

    def save_result(self):
        if self._result is not None:
            fname = QFileDialog.getSaveFileName(self, "Save test result", "",
                                                "JSON files (*.json)")
            if fname:
                fname = fname[0]
                fname = fname + '.json' if fname.split('.')[-1] != 'json' else fname
                with open(fname, 'w+b') as data_file:
                    data_file.write(json.dumps(self._result, indent=4).encode())

    def send_result(self):
        if self._result is not None:
            data_file = NamedTemporaryFile(mode="w+b")
            data_file.write(json.dumps(self._result, indent=4).encode())
            QDesktopServices.openUrl(QUrl.fromEncoded(
                f"mailto:alexis.jeandet@lpp.polytechnique.fr?subject=AMDA and SciQLop speed test results&attachment={data_file.name}".encode()))


def main():
    application = QApplication(sys.argv)
    window = AMDA_SciQLop_Speed_tester()
    desktop = QDesktopWidget().availableGeometry()
    width = int((desktop.width() - window.width()) / 2)
    height = int((desktop.height() - window.height()) / 2)
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
