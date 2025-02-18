import http.server
import os
import socketserver
from urllib.parse import urlparse, unquote


# Function to validate if a file path exists and is within the allowed directory
def validate_file_path(file_path: str, allowed_directory: str) -> bool:
    """
    Validates if the provided file path exists and is within the allowed directory.

    Args:
        file_path (str): The file path to validate.
        allowed_directory (str): The directory that is allowed.

    Returns:
        bool: True if the file exists and is within the allowed directory, False otherwise.
    """
    parsed_url = urlparse(file_path)
    # Convert "URL-like" path to a local file path
    local_path = unquote(parsed_url.path)
    
    # Ensure the path is within the allowed directory
    if not local_path.startswith(allowed_directory):
        return False
    
    # Check if the file exists
    return os.path.exists(local_path)


# Validate an example file path
allowed_directory = "/path/to/your/directory/"  # Replace with a real directory
example_path = "file:///path/to/your/example.txt"  # Replace with a real path
if validate_file_path(example_path, allowed_directory):
    print("File is valid.")
else:
    print("File is invalid.")


# Create a simple HTTP server that serves files from the allowed directory
class HelloWorldHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """
        Handles GET requests by responding with "Hello, World!".
        """
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