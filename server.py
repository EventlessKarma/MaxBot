import http.server
import socketserver
import database_json
import datetime

PORT = 9999


# class handles the http requests
class Handler(http.server.SimpleHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.set_headers()

        print(self.path)

        # expect the path to be the user id
        try:
            user_id = int(self.path[1:])
        except ValueError:
            return

        # read in the website html template
        template = open('website/google_chart_template.html', 'r')
        template_text = template.read()
        template.close()

        # substitute the roll data for the specific user id into the html string
        to_send = template_text.replace('DATA_POINTS_IN', roll_to_text(user_id, 20, 'today'))

        # submit the html
        self.wfile.write(bytes(to_send, 'utf-8'))


# get string of roll data compatible with google charts format
def roll_to_text(user_id: int, dice: int, date: str) -> str:

    db_json = database_json.Database()

    # determine what data to retrieve
    if date == 'all':
        # rolls = database.get_all_rolls(user_id, dice)[1:-1]
        rolls = db_json.get(user_id, datetime.date.today(), dice)
    else:
        rolls = db_json.get(user_id, datetime.date.today(), dice)

    # format for google charts
    to_return = ""
    for i, roll in enumerate(rolls):
        to_return += "[ '{}', {}, 'blue' ],\n".format(i + 1, roll)

    return to_return


if __name__ == "__main__":
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print('Server started')
        httpd.serve_forever()
