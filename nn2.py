import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Course Registration</title>
        </head>
        <body>
            <h2>Course Registration Form</h2>
            <form method="post">
                <label>Name:</label>
                <input type="text" name="student_name" required><br><br>

                <label>Course:</label>
                <select name="course_name">
                    <option value="Python Basics">Python Basics</option>
                    <option value="Web Development">Web Development</option>
                    <option value="Data Science">Data Science</option>
                </select><br><br>

                <input type="submit" value="Register">
            </form>
        </body>
        </html>
        '''

        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form = parse_qs(post_data)

        student_name = form.get('student_name', [''])[0]
        course_name = form.get('course_name', [''])[0]

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='16042006',
                database='coursedb'
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO course_registrations (student_name, course_name) VALUES (%s, %s)",
                (student_name, course_name)
            )
            conn.commit()
            cursor.close()
            conn.close()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h3>You are successfully registered for the course!</h3>")

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h3>Error: {str(e)}</h3>".encode('utf-8'))

def run():
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server running at http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
