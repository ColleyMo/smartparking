# combined_code.py
import RPi.GPIO as GPIO
import time
from flask import Flask, render_template

app = Flask(__name__)

# Set GPIO pins for ultrasonic sensor
TRIG = 18
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2

    return distance

def check_parking_status():
    distance = measure_distance()

    # Trigger an error message if the distance is less than 5 (something covering the sensor)
    if distance < 5:
        return "Error: Obstacle detected!"
    else:
        return "Free" if distance > 20 else "Occupied"

@app.route('/')
def index():
    status = check_parking_status()
    return render_template('index.html', status=status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

