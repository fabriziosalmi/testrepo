import http.server
import os
import socketserver
from urllib.parse import unquote, urlparse

def validate_file_path(file_path: str) -> bool:
    """Validates if the provided file path exists and is within a safe directory.

    Args:
        file_path (str): The file path to validate.

    Returns:
        bool: True if the file exists and is within a safe directory, False otherwise.
    """
    parsed_url = urlparse(file_path)
    local_path = unquote(parsed_url.path)

    # Define a safe directory
    safe_directory = "/path/to/safe/directory"  # Replace with the actual safe directory
    if not local_path.startswith(safe_directory):
        print("Invalid file path: Attempted to access a directory outside the safe directory.")
        return False

    if os.path.exists(local_path):
        print("File exists and is within the safe directory.")
        return True
    else:
        print("File does not exist or is outside the safe directory.")
        return False

example_path = "file:///path/to/safe/directory/example.txt"  # Replace with a real path
validate_file_path(example_path)

class HelloWorldHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """Handles GET requests by responding with "Hello, World!"."""
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello, World!")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

PORT = 8080
with socketserver.TCPServer(("", PORT), HelloWorldHandler) as httpd:
    print(f"Serving HTTP on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()