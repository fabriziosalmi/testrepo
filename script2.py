import http.server
import os
import socketserver
from urllib.parse import unquote, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    if os.path.exists(local_path):
        logging.info(f"File exists: {local_path}")
        return True
    else:
        logging.warning(f"File does not exist: {local_path}")
        return False


example_path = os.getenv("EXAMPLE_PATH", "file:///path/to/your/example.txt")  # Replace with a real path
validate_file_path(example_path)


class HelloWorldHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """
        Handles GET requests by responding with "Hello, World!".
        """
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello, World!")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            self.send_error(500, "Internal Server Error")


PORT = 8080
with socketserver.TCPServer(("", PORT), HelloWorldHandler) as httpd:
    logging.info(f"Serving HTTP on port {PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("\nShutting down server.")
        httpd.server_close()