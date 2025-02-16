import os
import http.server
import socketserver
from urllib.parse import urlparse, unquote

# Function to validate if a file path exists
def validate_file_path(file_path):
    parsed_url = urlparse(file_path)
    # Convert "URL-like" path to a local file path
    local_path = unquote(parsed_url.path)
    if os.path.exists(local_path):
        print(f"File exists: {local_path}")
        return True
    else:
        print(f"File does not exist: {local_path}")
        return False

# Validate an example file path
example_path = "file:///path/to/your/example.txt"  # Replace with a real path
validate_file_path(example_path)

# Create a simple HTTP server
class HelloWorldHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Respond with "Hello, World!" for all GET requests
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

# Start the HTTP server
PORT = 8080
with socketserver.TCPServer(("", PORT), HelloWorldHandler) as httpd:
    print(f"Serving HTTP on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()
