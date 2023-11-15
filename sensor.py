from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO setup for PIR sensor
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 18  # Replace with the actual GPIO pin connected to your PIR sensor
GPIO.setup(GPIO_PIR, GPIO.IN)

@app.route('/')
def index():
    return render_template('index.html', status=get_parking_status())

def get_parking_status():
    if GPIO.input(GPIO_PIR):
        return 'Occupied'
    else:
        return 'Free'

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except KeyboardInterrupt:
        print("App stopped by user")
        GPIO.cleanup()
