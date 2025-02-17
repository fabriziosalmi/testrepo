import logging
from typing import Any
import os
import ipaddress
from mitmproxy import http

# Configure logging
logging.basicConfig(
    filename="proxy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

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
        client_ip = flow.client_address[0]
        try:
            if str(ipaddress.ip_address(client_ip)) == blocked_ip:
                logging.warning(f"Blocked request from {client_ip} to {flow.request.pretty_url}")
                flow.response = http.HTTPResponse.make(
                    403, b"Forbidden", {"Content-Type": "text/plain"}
                )
                return
            logging.info(f"Forwarding request from {client_ip} to {flow.request.pretty_url}")
        except ValueError:
            logging.error(f"Invalid client IP address: {client_ip}")

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Handle the HTTP response.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]
        try:
            logging.info(
                f"Received response from {flow.request.pretty_url} for {client_ip} (status code: {flow.response.status_code})"
            )
        except ValueError:
            logging.error(f"Invalid client IP address: {client_ip}")

addons = [TransparentProxy()]