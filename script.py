class TransparentProxy:
    """
    A transparent proxy class to block requests from a specific IP address and log other requests.
    """

    def __init__(self, blocked_ip):
        self.blocked_ip = blocked_ip

    def process_request(self, request):
        if request.ip == self.blocked_ip:
            self.log_access(request)
            raise Exception("Access denied for blocked IP")
        else:
            self.log_access(request)

    def log_access(self, request):
        # Securely log the request details without exposing sensitive information
        print(f"Request from {request.ip}: {request.method} {request.path}")