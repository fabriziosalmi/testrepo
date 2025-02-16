import mitmproxy
from mitmproxy import http
import logging

# Configure logging
logging.basicConfig(filename='proxy.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

blocked_ip = "1.2.3.4"

class TransparentProxy:
    def request(self, flow: http.HTTPFlow):
        client_ip = flow.client_address[0]  # Get client IP

        if client_ip == blocked_ip:
            logging.info(f"Blocked request from {client_ip} to {flow.request.url}")
            flow.response = http.HTTPResponse.make(403, b"Forbidden", {"Content-Type": "text/plain"}) # Or just drop: flow.kill()
            return  # Stop processing the request

        # Log the request (optional)
        logging.info(f"Forwarding request from {client_ip} to {flow.request.url}")

        # No modification needed for transparent proxy.  mitmproxy handles forwarding.
        # You can inspect/modify flow.request here if needed.

    def response(self, flow: http.HTTPFlow):
       client_ip = flow.client_address[0]
       logging.info(f"Received response from {flow.request.url} for {client_ip} (status code: {flow.response.status_code})")
       # You can inspect/modify flow.response here if needed.


addons = [TransparentProxy()]

# To run: mitmproxy -T --host  (The -T makes it transparent)
# Note: You'll likely need root privileges for transparent proxying.
# On Linux, you'll need to set up iptables rules to redirect traffic to mitmproxy. Example:
# iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-ports 8080  (For HTTP)
# iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-ports 8080 (For HTTPS)
# (Adjust eth0 and 8080 (mitmproxy's default port) as needed)
#  You'll also need to enable IP forwarding:
#  echo 1 > /proc/sys/net/ipv4/ip_forward

#  For HTTPS interception, you'll need to install the mitmproxy CA certificate as a trusted root CA in your browser/system.
