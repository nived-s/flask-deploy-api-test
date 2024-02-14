from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time

# initialization
app = Flask(__name__)


## HOME PAGE
@app.route('/')
def home():
    return "home page"


# ................................
# LIGHT FUNCTIONALITY TO RasbPI
# ................................

# Set up GPIO
led_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)


# ON LED
def on_LED():
    # set light to HIGH
    GPIO.output(led_pin, GPIO.HIGH)

    print("Status is true")
    

# OFF LED
def off_LED():
    # set light to LOW
    GPIO.output(led_pin, GPIO.LOW)

    print("Status is false")

# UPDATE LIGHT STATUS API
@app.route('/light_status', methods=['POST'])
def process_status():
    try:
        data = request.get_json()

        if 'status' not in data:
            return jsonify({'error': 'Invalid request. Missing "status" field.'}), 400

        status = data['status']

        if status.lower() == 'true':
            on_LED()
            
        elif status.lower() == 'false':
            off_LED()
            
        else:
            return jsonify({'error': 'Invalid status value. Must be "true" or "false".'}), 400

        return jsonify({'message': 'Status processed successfully.'}), 200
    
    finally:
        # Clean up GPIO
        GPIO.cleanup()

# ..............................................................................#


# driver code
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
