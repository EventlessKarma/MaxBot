import http.server
import socketserver
import database

PORT = 9999


class Handler(http.server.SimpleHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.set_headers()

        print(self.path)

        try:
            user_id = int(self.path[1:])
        except ValueError:
            return

        template = open('website/google_chart_template.html', 'r')
        template_text = template.read()
        template.close()
        to_send = template_text.replace('DATA_POINTS_IN', roll_to_text(user_id, 20, 'all'))

        self.wfile.write(bytes(to_send, 'utf-8'))


def roll_to_text(user_id: int, dice: int, date: str) -> str:

    if date == 'all':
        rolls = database.get_all_rolls(user_id, dice)[1:-1]
    else:
        rolls = database.RollDatabase().get_rolls(user_id, dice)[1:-1]

    to_return = ""
    for i, roll in enumerate(rolls):
        to_return += "[ '{}', {} ],\n".format(i + 1, roll)

    return to_return


with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print('Server started')
    httpd.serve_forever()
