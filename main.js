
let running = false;
let currentMode = "ultrasonic";

const fftCtx = document.getElementById('fftChart').getContext('2d');
const doaCtx = document.getElementById('doaChart').getContext('2d');
const beamSlider = document.getElementById('beamAngle');
const beamVal = document.getElementById('beamVal');
const modeSelect = document.getElementById('modeSelect');
const threatFeed = document.getElementById('threatFeed');
const ledDisplay = document.getElementById('ledDisplay');

beamSlider.addEventListener('input', () => {
    beamVal.textContent = beamSlider.value + '°';
});

modeSelect.addEventListener('change', () => {
    currentMode = modeSelect.value;
});

const fftChart = new Chart(fftCtx, {
    type: 'line',
    data: {
        labels: Array.from({length: 128}, (_, i) => i),
        datasets: [{
            label: 'FFT Spectrum',
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
        labels: ['DoA'],
        datasets: [{
            label: 'DoA Estimate',
            data: [0],
            backgroundColor: ['rgba(255, 99, 132, 0.4)']
        }]
    },
    options: { animation: false }
});

function updateCharts(fftData, doa, leds) {
    fftChart.data.datasets[0].data = fftData;
    fftChart.update();

    doaChart.data.datasets[0].data = [Math.abs(doa % 360)];
    doaChart.update();

    ledDisplay.innerHTML = '';
    for (let i = 0; i < leds.length; i++) {
        let led = document.createElement('div');
        led.className = 'led';
        if (leds[i]) led.classList.add('active');
        ledDisplay.appendChild(led);
    }
}

function logThreat(msg) {
    const entry = document.createElement('li');
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    threatFeed.appendChild(entry);
    if (threatFeed.children.length > 10) {
        threatFeed.removeChild(threatFeed.firstChild);
    }
}

function poll() {
    if (!running) return;
    fetch(`/scan?mode=${currentMode}`)
        .then(response => response.json())
        .then(data => {
            updateCharts(data.fft, data.doa || 0, data.leds);
            if (!data.user_detected) {
                logThreat("No user detected");
            } else {
                logThreat(`Signal detected (${data.mode.toUpperCase()})`);
            }
            setTimeout(poll, 500);
        });
}

function startScan() {
    running = true;
    poll();
}

function stopScan() {
    running = false;
}
