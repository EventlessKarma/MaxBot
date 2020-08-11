from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from io import BytesIO
import send_graphs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            user_id = self.path[1:]
        except:
            return

        self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.end_headers()

        #with open('Reinforce.html', 'rb') as file:
        #    self.wfile.write(file.read())

        self.wfile.write(bytes(send_graphs.send_graphs(user_id), 'ascii'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


#httpd.socket = ssl.wrap_socket (httpd.socket, 
#        keyfile="./key.pem", 
#        certfile='./cert.pem', server_side=True)


if __name__ == "__main__":
    httpd = HTTPServer(('', 9999), SimpleHTTPRequestHandler)
    httpd.serve_forever()



