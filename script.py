import logging
from typing import Any, Dict
import os
from mitmproxy import http

# Configure logging
logging.basicConfig(
    filename="proxy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load blocked IP from environment variable or default to a safe value
blocked_ip = os.getenv("BLOCKED_IP", "1.2.3.4")

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
        client_ip = self.validate_ip(flow.client_address[0])  # Get and validate client IP

        if not client_ip:
            logging.error(f"Invalid client IP address: {flow.client_address[0]}")
            flow.response = http.HTTPResponse.make(
                400, b"Bad Request", {"Content-Type": "text/plain"}
            )
            return  # Stop processing the request

        if client_ip == blocked_ip:
            logging.info(f"Blocked request from {client_ip} to {flow.request.url}")
            flow.response = http.HTTPResponse.make(
                403, b"Forbidden", {"Content-Type": "text/plain"}
            )  # Or just drop: flow.kill()
            return  # Stop processing the request

        # Log the request (optional)
        logging.info(f"Forwarding request from {client_ip} to {flow.request.url}")

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Handle the HTTP response.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = self.validate_ip(flow.client_address[0])
        if not client_ip:
            logging.error(f"Invalid client IP address: {flow.client_address[0]}")
            return  # Stop processing the response

        logging.info(
            f"Received response from {flow.request.url} for {client_ip} (status code: {flow.response.status_code})"
        )

    def validate_ip(self, ip: str) -> str:
        """
        Validate the IP address format.

        Args:
            ip (str): The IP address to validate.

        Returns:
            str: The validated IP address or an empty string if invalid.
        """
        parts = ip.split(".")
        if len(parts) != 4:
            return ""
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return ""
        return ip

addons = [TransparentProxy()]