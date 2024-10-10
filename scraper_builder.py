import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from lxml import html

class WebScraperUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout and window
        self.setWindowTitle('Scrapy XPath Extractor')
        self.setGeometry(200, 200, 1200, 800)

        # Input field for the URL
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter a URL to scrape")
        self.url_input.setFixedHeight(30)

        # Button to load the webpage
        self.load_button = QPushButton("Load Webpage", self)
        self.load_button.setFixedSize(120, 40)
        self.load_button.clicked.connect(self.load_webpage)

        # Webview to display the webpage
        self.browser = QWebEngineView(self)
        self.browser.setMinimumSize(800, 600)

        # Textbox to display the extracted XPath
        self.xpath_output = QTextEdit(self)
        self.xpath_output.setPlaceholderText("XPath will be displayed here...")
        self.xpath_output.setFixedHeight(100)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.browser)
        layout.addWidget(self.xpath_output)
        self.setLayout(layout)

        # Set up the web channel for communication between Python and JavaScript
        self.channel = QWebChannel()
        self.com = Communicate()
        self.channel.registerObject('pyObj', self.com)
        self.browser.page().setWebChannel(self.channel)

        # Connect the element clicked signal to the function that displays XPath
        self.com.elementClicked.connect(self.display_xpath)

        # Use loadFinished instead of loadStarted
        self.browser.page().loadFinished.connect(self.page_loaded)

    def load_webpage(self):
        url = self.url_input.text()
        self.browser.setUrl(QUrl(url))

    def page_loaded(self):
        # Inject the QWebChannel script first
        self.browser.page().runJavaScript('''
            var script = document.createElement('script');
            script.src = 'qrc:///qtwebchannel/qwebchannel.js';  // Load the QWebChannel library from Qt
            script.onload = function() {
                console.log("QWebChannel script loaded successfully");

                // Initialize the QWebChannel
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.pyObj = channel.objects.pyObj;
                    console.log("QWebChannel initialized!");

                    // Add a click event listener
                    document.addEventListener('click', function(event) {
                        event.preventDefault(); // Prevent default action for all clicks

                        // If the clicked element is a link (anchor), do not follow it
                        if (event.target.tagName === 'A') {
                            console.log("Link clicked, but navigation is disabled.");
                            return; // Stop further execution for link clicks
                        }

                        console.log("Element clicked!");
                        if (window.pyObj && window.pyObj.onElementClicked) {
                            window.pyObj.onElementClicked(event.target.outerHTML);
                        } else {
                            console.error("window.pyObj.onElementClicked is not a function");
                        }
                    });
                });
            };
            document.head.appendChild(script);  // Add the script to the head of the document
        ''')

    
    def display_xpath(self, html_content):
        # Parse the clicked element's HTML and generate XPath
        tree = html.fromstring(html_content)
        xpath = tree.getroottree().getpath(tree)
        self.xpath_output.setPlainText(xpath)

class Communicate(QObject):
    # This signal is emitted when an element is clicked in the webview
    elementClicked = pyqtSignal(str)

    @pyqtSlot(str)
    def onElementClicked(self, element_html):
        # Emit the signal with the clicked element's HTML content
        self.elementClicked.emit(element_html)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initialize the main window
    window = WebScraperUI()
    window.show()

    sys.exit(app.exec_())
