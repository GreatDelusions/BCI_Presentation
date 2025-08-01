from flask import Flask, render_template_string, request, jsonify
import numpy as np
import random

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>BCI Ultrasonic System</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 30px; }
        canvas { margin: 20px auto; max-width: 90%; }
    </style>
</head>
<body>
    <h1>BCI + RF Ultrasonic Simulation</h1>
    <div>
        <p>Status: <span id="status">Idle</span></p>
        <label>Scan Interval (ms):
            <input id="interval" type="number" value="100" min="50" max="2000">
        </label>
        <button onclick="startScan()">Start</button>
        <button onclick="stopScan()">Stop</button>
    </div>
    <canvas id="fftChart"></canvas>
    <canvas id="doaChart" width="400" height="400"></canvas>

    <script>
        let running = false;
        let interval = 100;

        const fftCtx = document.getElementById('fftChart').getContext('2d');
        const doaCtx = document.getElementById('doaChart').getContext('2d');

        const fftChart = new Chart(fftCtx, {
            type: 'line',
            data: {
                labels: [...Array(128).keys()],
                datasets: [{
                    label: 'Simulated FFT',
                    data: Array(128).fill(0),
                    borderColor: 'blue',
                    borderWidth: 1
                }]
            },
            options: { animation: false, scales: { y: { beginAtZero: true } } }
        });

        const doaChart = new Chart(doaCtx, {
            type: 'polarArea',
            data: {
                labels: ['Direction'],
                datasets: [{
                    label: 'Beamforming Direction',
                    data: [0],
                    backgroundColor: ['rgba(255, 99, 132, 0.5)']
                }]
            },
            options: {
                animation: false,
                scales: { r: { beginAtZero: true, max: 360 } }
            }
        });

        function updateCharts(fft, doa) {
            fftChart.data.datasets[0].data = fft;
            fftChart.update();

            doaChart.data.datasets[0].data = [Math.abs(doa % 360)];
            doaChart.update();
        }

        function poll() {
            if (!running) return;
            fetch('/scan')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('status').innerText = 'Active';
                    updateCharts(data.fft, data.doa);
                    setTimeout(poll, interval);
                });
        }

        function startScan() {
            interval = parseInt(document.getElementById('interval').value) || 100;
            running = true;
            poll();
        }

        function stopScan() {
            running = false;
            document.getElementById('status').innerText = 'Idle';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan')
def scan():
    fft = [random.randint(0, 100) for _ in range(128)]
    doa = random.randint(0, 360)
    return jsonify({"fft": fft, "doa": doa})

if __name__ == "__main__":
    app.run(debug=True, port=5000)