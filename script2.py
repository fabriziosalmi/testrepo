import http.server
import os
import socketserver
from urllib.parse import unquote, urlparse

# Define a safe directory for file operations
SAFE_DIRECTORY = "/path/to/safe/directory"  # Replace with a real path

def validate_file_path(file_path: str) -> bool:
    """
    Validates if the provided file path exists within a safe directory.

    Args:
        file_path (str): The file path to validate.

    Returns:
        bool: True if the file exists within the safe directory, False otherwise.
    """
    parsed_url = urlparse(file_path)
    local_path = unquote(parsed_url.path)

    # Ensure the path is within the safe directory
    full_path = os.path.abspath(os.path.join(SAFE_DIRECTORY, local_path))
    if not os.path.commonpath([full_path, SAFE_DIRECTORY]) == SAFE_DIRECTORY:
        print("Attempted to access a file outside the safe directory.")
        return False

    if os.path.exists(full_path):
        print(f"File exists: {full_path}")
        return True
    else:
        print(f"File does not exist: {full_path}")
        return False

example_path = "file:///path/to/safe/example.txt"  # Replace with a real path
validate_file_path(example_path)


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
with socketserver.TCPServer(("", PORT), HelloWorldHandler) as httpd:
    print(f"Serving HTTP on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()