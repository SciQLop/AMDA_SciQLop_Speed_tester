import sys
import json
import pkg_resources
from pygments.lexers.data import JsonLexer
from pygments.formatters import HtmlFormatter
from pygments import highlight

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog, QPushButton,
                             QHBoxLayout, QLabel, QMainWindow, QToolBar, QVBoxLayout, QWidget, QTextBrowser)

from PyQt5.QtWebEngineWidgets  import QWebEnginePage, QWebEngineView

from amda_sciqlop_speed_tester.images import MainPage
from amda_sciqlop_speed_tester.speed_teser_sequence import TestSequence


class AMDA_SciQLop_Speed_tester(QMainWindow):

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super(AMDA_SciQLop_Speed_tester, self).__init__(parent)
        self.resize(1024, 768)
        self.setWindowTitle('AMDA_SciQLop_Speed_tester')
        window_icon = pkg_resources.resource_filename('amda_sciqlop_speed_tester.images',
                                                      'logo.png')
        self.setWindowIcon(QIcon(window_icon))

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)

        self.start_test_qpb = QPushButton("Start test")
        self.view = QWebEngineView()
        self.page = QWebEnginePage()
        self.view.setPage(self.page)
        self.html_page = MainPage()
        self.page.setHtml(self.html_page.html())
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.start_test_qpb)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)

        self.test_sequence = TestSequence()
        self.test_sequence.message.connect(self.status_bar.showMessage)
        self.test_sequence.done.connect(self.test_complete)
        self.test_sequence.update_progress.connect(self.progress_update)
        self.test_sequence.push_result.connect(self.show_result)
        self.start_test_qpb.clicked.connect(self.start_test)

    def start_test(self):
        self.start_test_qpb.setEnabled(False)
        self.test_sequence.start()

    def progress_update(self, task, value):
        self.html_page.update(**{task: value})
        self.page.setHtml(self.html_page.html())

    def show_result(self, result:dict):
        pretty_result = json.dumps(result, indent=4)
        html = highlight(pretty_result,JsonLexer(),HtmlFormatter())
        self.html_page.update(result=html)
        self.page.setHtml(self.html_page.html())

    def test_complete(self, success: bool):
        self.start_test_qpb.setEnabled(True)

    def send_result(self):
        QDesktopServices.openUrl(QUrl.fromEncoded(
            b"mailto:alexis.jeandet@lpp.polytechnique.fr?subject=Sending%20File&attachment=path/to/local/file.dat"))


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