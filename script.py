import ipaddress

def request(self, flow: http.HTTPFlow) -> None:
    try:
        client_ip = flow.client_address[0]
        if not ipaddress.ip_address(client_ip):  # Validate IP address
            logging.error(f"Invalid client IP address: {client_ip}")
            return
        if client_ip == blocked_ip:
            logging.info(f"Blocked request from {client_ip} to {flow.request.url}")
            flow.response = http.HTTPResponse.make(
                403, b"Forbidden", {"Content-Type": "text/plain"}
            )
            return
        logging.info(f"Forwarding request from {client_ip} to {flow.request.url}")
    except ValueError:
        logging.error(f"Invalid client IP address: {client_ip}")