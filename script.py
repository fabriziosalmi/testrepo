class TransparentProxy:
    """
    A transparent proxy class to block requests from a specific IP address and log other requests.
    """

    def __init__(self, blocked_ip):
        self.blocked_ip = blocked_ip

    def handle_request(self, request):
        if request.ip == self.blocked_ip:
            # Log the blocked request
            self.log_request(request)
            return "Request blocked"
        else:
            # Process and log the allowed request
            response = self.process_request(request)
            self.log_request(request)
            return response

    def process_request(self, request):
        # Placeholder for request processing logic
        return f"Processed {request}"

    def log_request(self, request):
        # Placeholder for logging logic
        print(f"Logged: {request}")