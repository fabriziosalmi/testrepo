import http.server
import os
import socketserver
from urllib.parse import unquote, urlparse

def validate_file_path(file_path: str) -> bool:
    """
    Validates if the provided file path exists.

    Args:
        file_path (str): The file path to validate.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    parsed_url = urlparse(file_path)
    local_path = unquote(parsed_url.path)
    
    # Ensure the path is within a safe directory to prevent directory traversal
    safe_directory = "/safe/directory/path"  # Replace with a real safe directory path
    if not local_path.startswith(safe_directory):
        print("Attempted to access a file outside the safe directory.")
        return False
    
    if os.path.exists(local_path):
        print(f"File exists: {local_path}")
        return True
    else:
        print("File does not exist.")
        return False

class HelloWorldHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """
        Handles GET requests by responding with "Hello, World!".
        """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

PORT = 8080

# Implement a graceful shutdown mechanism
def run_server():
    with socketserver.TCPServer(("", PORT), HelloWorldHandler) as httpd:
        print(f"Serving HTTP on port {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()

if __name__ == "__main__":
    run_server()