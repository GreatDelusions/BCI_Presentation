from flask import Flask, render_template, jsonify, request
import random
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['GET'])
def scan():
    # Simulated data response
    mode = request.args.get('mode', 'ultrasonic')
    user_detected = random.choice([True, False])
    doa = random.randint(0, 360) if user_detected else None
    fft_data = [random.randint(0, 100) for _ in range(128)]
    signal_strength = random.randint(20, 100) if user_detected else 0
    leds = [0] * 12
    if user_detected:
        led_index = int(doa / 30) % 12
        leds[led_index] = 1

    return jsonify({
        'fft': fft_data,
        'doa': doa,
        'signal_strength': signal_strength,
        'user_detected': user_detected,
        'leds': leds,
        'mode': mode
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host='0.0.0.0', port=port)
