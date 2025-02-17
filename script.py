class TransparentProxy:
    """
    A transparent proxy class to block requests from a specific IP address and log other requests.
    """

    def __init__(self, blocked_ip):
        self.blocked_ip = blocked_ip

    def process_request(self, request):
        if request.ip == self.blocked_ip:
            self.log_event("Blocked request from", request.ip)
            return None
        response = self.forward_request(request)
        self.log_event("Processed request from", request.ip)
        return response

    def log_event(self, message, ip):
        with open("proxy_log.txt", "a") as log_file:
            log_file.write(f"{message} {ip}\n")

    def forward_request(self, request):
        # Placeholder for actual request forwarding logic
        pass