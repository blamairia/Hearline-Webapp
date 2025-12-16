/**
 * ECG Analysis Module
 * Handles live ECG analysis and waveform visualization
 */

class ECGAnalysis {
    constructor() {
        this.ecgChart = null;
        this.resultsPanel = null;
        this.loadingDiv = null;
        this.contentDiv = null;
        this.errorDiv = null;
    }

    /**
     * Initialize the ECG analysis module
     */
    init() {
        this.resultsPanel = document.getElementById('live-analysis-results');
        this.loadingDiv = document.getElementById('analysis-loading');
        this.contentDiv = document.getElementById('analysis-content');
        this.errorDiv = document.getElementById('analysis-error');
    }

    /**
     * Perform live ECG analysis for a demo file
     */
    async performLiveAnalysis(fileId) {
        if (!this.resultsPanel || !this.loadingDiv || !this.contentDiv || !this.errorDiv) {
            console.error('Analysis panel elements not found');
            return;
        }

        // Show panel and loading state
        this.resultsPanel.classList.remove('d-none');
        this.loadingDiv.classList.remove('d-none');
        this.contentDiv.classList.add('d-none');
        this.errorDiv.classList.add('d-none');

        try {
            const response = await fetch(`/api/analyze_demo_ecg/${fileId}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.displayAnalysisResults(data);
            } else {
                this.showAnalysisError(data.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showAnalysisError('Failed to analyze ECG. Please try again.');
        }
    }

    /**
     * Display analysis results
     */
    displayAnalysisResults(data) {
        // Hide loading, show content
        this.loadingDiv.classList.add('d-none');
        this.contentDiv.classList.remove('d-none');

        // Plot ECG waveform
        if (data.ecg_data) {
            this.plotECG(data.ecg_data);
        }

        // Display primary diagnosis
        const primary = data.primary_diagnosis;
        const primaryNameEl = document.getElementById('primary-diagnosis-name');
        const primaryPercentEl = document.getElementById('primary-diagnosis-percent');
        const primaryBarEl = document.getElementById('primary-diagnosis-bar');

        if (primaryNameEl) primaryNameEl.textContent = primary.name;

        const percentage = (primary.probability * 100).toFixed(1);
        if (primaryPercentEl) primaryPercentEl.textContent = `${percentage}%`;
        if (primaryBarEl) {
            primaryBarEl.style.width = `${percentage}%`;

            // Color code based on confidence
            if (primary.probability >= 0.8) {
                primaryBarEl.className = 'progress-bar bg-success';
            } else if (primary.probability >= 0.5) {
                primaryBarEl.className = 'progress-bar bg-warning';
            } else {
                primaryBarEl.className = 'progress-bar bg-danger';
            }
        }

        // Display all predictions sorted by probability
        const allPredictionsEl = document.getElementById('all-predictions');
        if (allPredictionsEl) {
            const sortedPredictions = Object.entries(data.prediction)
                .sort((a, b) => b[1] - a[1])
                .map(([abbr, prob]) => {
                    const percent = (prob * 100).toFixed(1);
                    return `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span><strong>${abbr}</strong> - ${data.class_names[abbr]}</span>
                        <span class="badge bg-secondary">${percent}%</span>
                    </div>
                `;
                }).join('');

            allPredictionsEl.innerHTML = sortedPredictions;
        }

        // Scroll to results
        setTimeout(() => {
            this.resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }

    /**
     * Show analysis error
     */
    showAnalysisError(message) {
        this.loadingDiv.classList.add('d-none');
        this.errorDiv.classList.remove('d-none');

        const errorMessageEl = document.getElementById('error-message');
        if (errorMessageEl) {
            errorMessageEl.textContent = message;
        }
    }

    /**
     * Plot ECG waveform using Chart.js
     */
    plotECG(ecgData) {
        const canvas = document.getElementById('ecg-canvas');
        if (!canvas) {
            console.error('ECG canvas not found');
            return;
        }

        const ctx = canvas.getContext('2d');

        // Destroy previous chart if exists
        if (this.ecgChart) {
            this.ecgChart.destroy();
        }

        // Prepare datasets - display all 12 leads overlaid with offset
        const leads = ecgData.leads;
        const signals = ecgData.signals;
        const timeAxis = ecgData.time;

        // Colors for each lead
        const leadColors = {
            'I': '#e74c3c', 'II': '#3498db', 'III': '#2ecc71',
            'aVR': '#f39c12', 'aVL': '#9b59b6', 'aVF': '#1abc9c',
            'V1': '#e67e22', 'V2': '#34495e', 'V3': '#16a085',
            'V4': '#c0392b', 'V5': '#8e44ad', 'V6': '#27ae60'
        };

        // Create datasets with vertical offset for each lead (stacked view)
        const verticalSpacing = 3; // mV spacing between leads
        const datasets = leads.map((lead, idx) => {
            const offset = -(idx * verticalSpacing); // Stack from top to bottom
            return {
                label: lead,
                data: signals[idx].map((value, i) => ({
                    x: timeAxis[i],
                    y: value + offset
                })),
                borderColor: leadColors[lead],
                borderWidth: 1.5,
                fill: false,
                pointRadius: 0,
                tension: 0
            };
        });

        // Create chart with realistic ECG paper appearance
        this.ecgChart = new Chart(ctx, {
            type: 'line',
            data: { datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            boxWidth: 15,
                            font: { size: 11 },
                            padding: 10
                        }
                    },
                    title: {
                        display: true,
                        text: `ECG Recording (${ecgData.duration.toFixed(1)}s at ${ecgData.sample_rate}Hz)`,
                        font: { size: 14, weight: 'bold' }
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        display: true,
                        title: {
                            display: true,
                            text: 'Time (seconds)',
                            font: { size: 12, weight: 'bold' }
                        },
                        grid: {
                            color: '#ffcccc',  // Light red grid like ECG paper
                            lineWidth: 0.5
                        },
                        ticks: {
                            stepSize: 0.2,  // 200ms grid (standard ECG)
                            font: { size: 10 }
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        title: {
                            display: true,
                            text: 'Amplitude (mV)',
                            font: { size: 12, weight: 'bold' }
                        },
                        grid: {
                            color: '#ffcccc',  // Light red grid like ECG paper
                            lineWidth: 0.5
                        },
                        ticks: {
                            stepSize: 0.5,  // 0.5mV grid (standard ECG)
                            font: { size: 10 }
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
}

// Export for use in main script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ECGAnalysis;
}
