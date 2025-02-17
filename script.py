import logging
from typing import Any
import ipaddress  # For IP validation
import mitmproxy
from mitmproxy import http

# Configure logging
logging.basicConfig(
    filename="proxy.log",
    level=logging.DEBUG,  # Increased to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Validate the blocked IP address
try:
    blocked_ip = ipaddress.ip_address("1.2.3.4")  # Ensure it's a valid IP
except ValueError:
    raise ValueError("Invalid blocked IP address")

class TransparentProxy:
    """
    A transparent proxy class to block requests from a specific IP address and log other requests.
    """

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Handle the HTTP request.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]  # Get client IP

        if client_ip == str(blocked_ip):
            logging.info(f"Blocked request from {client_ip} to {flow.request.url}")
            flow.response = http.HTTPResponse.make(
                403, b"Forbidden", {"Content-Type": "text/plain"}
            )  # Or just drop: flow.kill()
            return  # Stop processing the request

        # Log the request (optional)
        logging.debug(f"Forwarding request from {client_ip} to {flow.request.url}")

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Handle the HTTP response.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]
        logging.debug(
            f"Received response from {flow.request.url} for {client_ip} "
            f"(status code: {flow.response.status_code})"
        )

    def error(self, flow: http.HTTPFlow) -> None:
        """
        Handle any errors that occur during request or response processing.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]
        logging.error(
            f"Error processing request from {client_ip} to {flow.request.url}: {str(flow.error)}"
        )

addons = [TransparentProxy()]