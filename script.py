import logging
from typing import Any
import ipaddress
from mitmproxy import http

# Configure logging with log rotation and size limit
logging.basicConfig(
    filename="proxy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode='a',
    maxBytes=1024*1024,  # 1 MB
    backupCount=5
)

blocked_ip = "1.2.3.4"

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

        try:
            if self.is_valid_ip(client_ip) and client_ip == blocked_ip:
                logging.info(f"Blocked request from {client_ip} to {self.mask_url(flow.request.url)}")
                flow.response = http.HTTPResponse.make(
                    403, b"Forbidden", {"Content-Type": "text/plain"}
                )  # Or just drop: flow.kill()
                return  # Stop processing the request

            # Log the request (optional)
            logging.info(f"Forwarding request from {client_ip} to {self.mask_url(flow.request.url)}")
        except Exception as e:
            logging.error(f"Error processing request: {e}")

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Handle the HTTP response.

        Args:
            flow (http.HTTPFlow): The HTTP flow object containing the request and response information.
        """
        client_ip = flow.client_address[0]
        try:
            logging.info(
                f"Received response from {self.mask_url(flow.request.url)} for {client_ip} "
                f"(status code: {flow.response.status_code})"
            )
        except Exception as e:
            logging.error(f"Error processing response: {e}")

    def is_valid_ip(self, ip):
        """
        Validate the IP address format.
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def mask_url(self, url):
        """
        Mask the URL to avoid logging sensitive information.
        """
        # Example: mask the query parameters
        from urllib.parse import urlparse, urlunparse

        parsed_url = urlparse(url)
        masked_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        return masked_url

addons = [TransparentProxy()]