from flask import Flask, render_template_string, request, jsonify
import numpy as np
import random
import time

app = Flask(__name__)

# HTML Template with basic JS and Chart.js for frontend rendering
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BCI RF Ultrasonic Web Simulation</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; text-align: center; margin: 40px; }
        canvas { max-width: 600px; margin: 20px auto; }
    </style>
</head>
<body>
    <h1>BCI + RF Ultrasonic GUI (Web Sim)</h1>
    <p>Status: <span id="status">Idle</span></p>
    <button onclick="startScan()">Start Scan</button>
    <button onclick="stopScan()">Stop Scan</button>
    <canvas id="fftChart"></canvas>
    <canvas id="doaChart" width="400" height="400"></canvas>

    <script>
        let running = false;
        const fftCtx = document.getElementById('fftChart').getContext('2d');
        const doaCtx = document.getElementById('doaChart').getContext('2d');

        const fftChart = new Chart(fftCtx, {
            type: 'line',
            data: {
                labels: Array.from({length: 128}, (_, i) => i),
                datasets: [{
                    label: 'Simulated FFT',
                    data: Array(128).fill(0),
                    borderColor: 'blue',
                    borderWidth: 1
                }]
            },
            options: { animation: false }
        });

        const doaChart = new Chart(doaCtx, {
            type: 'polarArea',
            data: {
                labels: ['DOA'],
                datasets: [{
                    label: 'DoA Estimate',
                    data: [0],
                    backgroundColor: ['rgba(75, 192, 192, 0.2)']
                }]
            },
            options: { animation: false }
        });

        function updateCharts(fftData, doa) {
            fftChart.data.datasets[0].data = fftData;
            fftChart.update();

            doaChart.data.datasets[0].data = [Math.abs(doa % 360)];
            doaChart.update();
        }

        function poll() {
            if (!running) return;
            fetch('/scan')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').innerText = 'Active';
                    updateCharts(data.fft, data.doa);
                    setTimeout(poll, 100);
                });
        }

        function startScan() {
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
    # Simulate FFT data and DoA
    fft_data = [random.randint(0, 100) for _ in range(128)]
    doa = random.randint(0, 360)
    return jsonify({"fft": fft_data, "doa": doa})

if __name__ == '__main__':
    app.run(debug=True, port=0.0.0.0)
