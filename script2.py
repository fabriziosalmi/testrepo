import http.server
import os
import socketserver
from urllib.parse import urlparse

# Define a safe base directory for file operations
SAFE_BASE_DIR = "/path/to/safe/directory"  # Replace with a real path

def validate_file_path(file_path: str) -> bool:
    """Validates if the provided file path exists within a safe directory.

    Args:
        file_path (str): The file path to validate.

    Returns:
        bool: True if the file exists within the safe directory, False otherwise.
    """
    parsed_url = urlparse(file_path)
    local_path = os.path.abspath(os.path.join(SAFE_BASE_DIR, parsed_url.path))
    
    # Ensure the path is within the safe directory
    if not local_path.startswith(SAFE_BASE_DIR):
        print("Invalid file path.")
        return False
    
    if os.path.exists(local_path):
        print(f"File exists: {local_path}")
        return True
    else:
        print("File does not exist.")
        return False

# Example usage
example_path = "file:///path/to/safe/directory/example.txt"  # Replace with a real path
validate_file_path(example_path)

class HelloWorldHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """Handles GET requests by responding with "Hello, World!". """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

PORT = 8080
with socketserver.TCPServer(("", PORT), HelloWorldHandler) as httpd:
    print(f"Serving HTTP on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()