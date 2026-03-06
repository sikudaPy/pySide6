import sys
from PySide6.QtCore import QCoreApplication, QUrl, Slot
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QSslError

class NetworkManager:
    def __init__(self):
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.handle_finished)

    def fetch_url(self, url):
        request = QNetworkRequest(QUrl(url))
        reply = self.manager.get(request)
        # Connect error and ssl signals specifically for this reply
        reply.errorOccurred.connect(self.handle_error)
        reply.sslErrors.connect(self.handle_ssl_errors)
        reply.finished.connect(reply.deleteLater) # Clean up the reply object later

    @Slot(QNetworkReply)
    def handle_finished(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            print("Request finished successfully.")
            # Read data here: reply.readAll().data().decode('utf-8')
        else:
            # This case is usually handled by handle_error, but good practice to check
            print(f"Finished with error: {reply.errorString()} ({reply.error()})")
        # reply.deleteLater() # Already connected above, but must be called once

    @Slot(QNetworkReply.NetworkError)
    def handle_error(self, code):
        reply = self.sender() # Get the object that sent the signal
        print("-" * 20)
        print(f"Error occurred!")
        print(f"Error Code: {code}")
        print(f"Error String: {reply.errorString()}")
        print("-" * 20)
        
    @Slot(list) # The signal passes a list of QSslErrors
    def handle_ssl_errors(self, errors):
        print("-" * 20)
        print("SSL Errors occurred:")
        for error in errors:
            print(f"SSL Error: {error.errorString()}")
        # Call ignoreSslErrors() to proceed with caution if you trust the site (e.g., self-signed certs)
        # self.sender().ignoreSslErrors() 
        print("-" * 20)


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    network_manager = NetworkManager()
    
    # Test a URL that might cause an error, for example an invalid one
    # Use a valid HTTP/HTTPS URL for a real test
    network_manager.fetch_url("https://php1c.ru/catalogs/api?format=json") 
    
    sys.exit(app.exec())
