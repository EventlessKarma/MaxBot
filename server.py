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

        try:
            user_id = int(self.path[1:])
        except ValueError:
            return

        template = open('website/stats_template.html', 'r')
        text = template.read()
        text.replace('DATA_POINTS_IN', roll_to_text(user_id, 20, 'all'))
        self.wfile.write(bytes(text, 'utf-8'))


def roll_to_text(user_id: int, dice: int, date: str) -> str:

    if date == 'all':
        rolls = database.get_all_rolls(user_id, dice)
    else:
        rolls = database.RollDatabase().get_rolls(user_id, dice)

    to_return = "dataPoints: [ "
    for i, roll in enumerate(rolls):
        to_return += "{{ y: {}, label: '{}' }},".format(roll, i + 1)
    to_return = to_return[:-1]

    return to_return


with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print('Server started')
    httpd.serve_forever()