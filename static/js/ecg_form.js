'use strict';

/**
 * ECG Form Submission Script
 * Handles ECG file upload and real-time analysis for NEW visit forms
 * This script is ONLY for form submission - NOT for editing existing visits
 */
class ECGFormSubmissionHandler {
  constructor() {
    // File inputs & main containers
    this.matFileInput      = null;
    this.heaFileInput      = null;
    this.analysisSection   = null;
    this.analysisResults   = null;
    this.analysisLoading   = null;
    this.analysisError     = null;

    // Waveform sub-components
    this.waveformContainer = null;
    this.waveformLoading   = null;
    this.waveformError     = null;
    this.waveformControls  = null;
    this.waveformChart     = null;

    // Data state
    this.currentECGData    = null;
    this.currentLead       = 0;
    this.ECG_LEADS         = [
      'Lead I', 'Lead II', 'Lead III', 'aVR', 'aVL', 'aVF',
      'V1', 'V2', 'V3', 'V4', 'V5', 'V6'
    ];

    this.init();
  }

  init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.initializeElements());
    } else {
      this.initializeElements();
    }
  }

  initializeElements() {
    // Grab DOM nodes
    this.matFileInput    = document.getElementById('ecg_mat_file');
    this.heaFileInput    = document.getElementById('ecg_hea_file');
    this.analysisSection = document.getElementById('ecg-analysis-section');

    if (!this.matFileInput || !this.heaFileInput || !this.analysisSection) {
      console.warn('ECG Form Submission: Required elements for analysis not found');
      return;
    }

    this.analysisResults = document.getElementById('ecg-analysis-results');
    this.analysisLoading = document.getElementById('ecg-analysis-loading');
    
    this.analysisError   = document.getElementById('ecg-analysis-error');

    // Waveform specific elements from static HTML
    this.waveformDisplayArea = document.getElementById('ecg-waveform-display-area');
    this.waveformLoading = document.getElementById('ecg-waveform-loading');
    this.waveformError = document.getElementById('ecg-waveform-error');
    this.waveformControls = document.getElementById('ecg-controls');
    this.waveformChartCanvas = document.getElementById('ecg-waveform-chart');
    this.ecgChart = null; // For Chart.js instance

    if (!this.waveformDisplayArea || !this.waveformLoading || !this.waveformError || !this.waveformControls || !this.waveformChartCanvas) {
        console.warn('ECG Form Submission: Required elements for waveform display not found. Ensure they exist in visit_form.html.');
        // Decide if this is a fatal error for the class or if it can proceed without waveform functionality.
        // For now, we'll allow it to proceed, but waveform features will not work.
    }

     // 1) Always keep the ECG panel visible
  this.analysisSection.style.display = 'block';

  // 2) Hide only the spinners & errors — but do NOT hide the waveform area or canvas
  if (this.analysisLoading) this.analysisLoading.style.display = 'none';
  if (this.analysisError)   this.analysisError.style.display   = 'none';
  if (this.waveformLoading) this.waveformLoading.style.display   = 'none';
  if (this.waveformError)   this.waveformError.style.display     = 'none';
  // *** Remove any this.hideWaveformDisplay() here ***

  this.showInstructionMessage();
  this.attachEventListeners();
  console.log('ECG Form Submission handler initialized');
  }

  attachEventListeners() {
    this.matFileInput.addEventListener('change', () => this.checkAndAnalyzeECG());
    this.heaFileInput.addEventListener('change', () => this.checkAndAnalyzeECG());
  }

  checkAndAnalyzeECG() {
    const matFile = this.matFileInput.files[0];
    const heaFile = this.heaFileInput.files[0];
    console.log('ECG files check – MAT:', !!matFile, 'HEA:', !!heaFile);

    if (matFile && heaFile) {
      this.showAnalysisSection();
      this.analyzeECGFiles(matFile, heaFile);
    } else if (matFile || heaFile) {
      this.showWaitingForBothFiles();
    } else {
      this.showInstructionMessage();
    }
  }

  showAnalysisSection() {
  this.analysisSection.style.display = 'block';
  this.analysisSection.querySelectorAll('*').forEach(el => el.style.removeProperty('display'));
}


  showWaitingForBothFiles() {
    this.clearError();
    this.hideLoading();
    this.analysisResults.innerHTML = `
      <div class="card border-warning">
        <div class="card-header bg-warning text-dark">
          <h6 class="mb-0"><i class="fas fa-clock"></i> Waiting for Complete ECG Upload</h6>
        </div>
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-md-8">
              <h6 class="text-warning">Almost Ready!</h6>
              <p class="mb-2">Please upload both ECG files (MAT and HEA) to start the heart rhythm analysis.</p>
              <small class="text-muted">
                <i class="fas fa-info-circle"></i> Both files work together to provide accurate ECG analysis - one contains the data, the other contains the header information.
              </small>
            </div>
            <div class="col-md-4 text-center">
              <i class="fas fa-hourglass-half fa-3x text-warning mb-2"></i>
              <br>
              <small class="text-muted">Upload remaining file</small>
            </div>
          </div>
        </div>
      </div>`;
  }
// Map abbreviations to full names and detailed explanations
getFullClassNameAndExplanation(abbr) {
  const classData = {
    'NSR': {
      fullName: 'Normal Sinus Rhythm',
      explanation: 'The patient\'s heart rhythm is completely normal and healthy. The electrical signals are working perfectly, creating regular heartbeats at a normal rate.',
      severity: 'normal',
      action: 'Patient should continue regular check-ups and maintain a healthy lifestyle.'
    },
    'AF': {
      fullName: 'Atrial Fibrillation',
      explanation: 'The patient\'s heart\'s upper chambers are beating irregularly, which can cause an uneven pulse. This is a common condition that can be managed with proper treatment.',
      severity: 'moderate',
      action: 'Patient should consult their doctor about treatment options to prevent complications.'
    },
    'STEMI': {
      fullName: 'ST-Elevation Myocardial Infarction (Major Heart Attack)',
      explanation: 'This indicates a serious heart attack where a major heart artery is completely blocked. The patient requires immediate emergency medical attention.',
      severity: 'critical',
      action: 'Patient needs emergency medical care immediately - call 911 or go to the nearest emergency room.'
    },
    'NSTEMI': {
      fullName: 'Non-ST-Elevation Myocardial Infarction (Heart Attack)',
      explanation: 'This shows signs of a heart attack where a heart artery is partially blocked. While less severe than STEMI, the patient still requires urgent medical attention.',
      severity: 'high',
      action: 'Patient should contact their doctor immediately or seek urgent medical care.'
    },
    'LBBB': {
      fullName: 'Left Bundle Branch Block',
      explanation: 'The electrical signals in the patient\'s heart are taking a detour, causing a slight delay in how the heart contracts. This can indicate heart muscle strain.',
      severity: 'moderate',
      action: 'Patient should follow up with their cardiologist for further evaluation and monitoring.'
    },
    'RBBB': {
      fullName: 'Right Bundle Branch Block',
      explanation: 'There\'s a delay in the electrical signal to the right side of the patient\'s heart. This is often harmless but may sometimes indicate underlying heart or lung conditions.',
      severity: 'low',
      action: 'Patient should discuss with their doctor, but this is often not a serious concern.'
    },
    'PVC': {
      fullName: 'Premature Ventricular Contractions',
      explanation: 'The patient\'s heart occasionally beats earlier than expected, creating extra heartbeats. This is very common and usually harmless, like hiccups of the heart.',
      severity: 'low',
      action: 'Usually no treatment needed, but patient should mention to their doctor during regular visits.'
    },
    'PAC': {
      fullName: 'Premature Atrial Contractions',
      explanation: 'The patient\'s heart\'s upper chambers occasionally beat early, causing extra heartbeats. This is very common and typically not dangerous.',
      severity: 'low',
      action: 'Generally harmless - patient should discuss with their doctor if they feel symptoms.'
    },
    'Tachycardia': {
      fullName: 'Rapid Heart Rate (Tachycardia)',
      explanation: 'The patient\'s heart is beating faster than normal. This can happen due to exercise, stress, fever, or underlying heart conditions.',
      severity: 'moderate',
      action: 'Monitor patient symptoms and consult their doctor to determine the cause.'
    },
    'Bradycardia': {
      fullName: 'Slow Heart Rate (Bradycardia)',
      explanation: 'The patient\'s heart is beating slower than normal. This can be normal for athletes or may indicate an issue with the patient\'s heart\'s electrical system.',
      severity: 'moderate',
      action: 'Patient should discuss with their doctor, especially if they experience dizziness or fatigue.'
    }
  };

  return classData[abbr] || {
    fullName: abbr,
    explanation: 'This heart rhythm pattern requires further evaluation by a medical professional.',
    severity: 'unknown',
    action: 'Please consult with the patient\'s doctor for interpretation of this result.'
  };
}
  showInstructionMessage() {
    this.clearError();
    this.hideLoading();
    this.analysisResults.innerHTML = `
      <div class="card border-info">
        <div class="card-header bg-info text-white">
          <h6 class="mb-0"><i class="fas fa-heartbeat"></i> ECG Analysis Ready</h6>
        </div>
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-md-8">
              <h6 class="text-info">Upload Your ECG Files</h6>
              <p class="mb-2">Upload both ECG files (MAT and HEA) above to get instant AI-powered heart rhythm analysis.</p>
              <small class="text-muted">
                <i class="fas fa-shield-alt"></i> Your ECG data is processed securely and analyzed using advanced AI technology.
              </small>
            </div>
            <div class="col-md-4 text-center">
              <i class="fas fa-file-upload fa-3x text-info mb-2"></i>
              <br>
              <small class="text-muted">Both files required</small>
            </div>
          </div>
        </div>
      </div>`;
  }

  showLoading() {
    this.clearError();
    this.analysisLoading.style.display = 'block';
  }

  hideLoading() {
    this.analysisLoading.style.display = 'none';
  }

  clearError() {
    this.analysisError.textContent = '';
    this.analysisError.style.display = 'none';
  }

  analyzeECGFiles(matFile, heaFile) {
    console.log('Sending ECG files for analysis…');
    this.showLoading();
    this.analysisResults.innerHTML = ''; 
    this.hideWaveformDisplay(); // Hide waveform display during analysis

    const formData = new FormData();
    formData.append('mat_file', matFile);
    formData.append('hea_file', heaFile);

    fetch('/analyze_ecg', { method: 'POST', body: formData })
      .then(response => {
        if (!response.ok) {
          // Try to parse error from server if it's JSON
          return response.json().then(errData => {
            throw new Error(errData.error || `Server returned ${response.status}`);
          }).catch(() => { // Fallback if error response is not JSON
            throw new Error(`Server returned ${response.status}`);
          });
        }
        return response.json();
      })
      .then(data => {
        this.hideLoading();
        if (data.success) {
          this.displayAnalysisResults(data);
          // Now, also fetch and display the waveform
          this.fetchAndDisplayWaveform(matFile, heaFile);
        } else {
          throw new Error(data.error || 'Unknown analysis error');
        }
      })
      .catch(err => {
        console.error('ECG analysis error:', err);
        this.hideLoading();
        this.displayError(err.message);
        // Clear results area if an error occurs to prevent showing stale/confusing info
        this.analysisResults.innerHTML = '';
      });
  }

  displayAnalysisResults(data) {
    const primaryAbbr = data.primary_diagnosis.abbreviation;
    const primaryProb = data.primary_diagnosis.probability;
    const summary = data.summary;
    const confidencePct = (primaryProb * 100).toFixed(1) + '%';

    // Get comprehensive class information
    const classInfo = this.getFullClassNameAndExplanation(primaryAbbr);
    const primaryName = classInfo.fullName;

    // Determine confidence styling and message
    let confidenceClass = 'text-danger';
    let confidenceMessage = 'Low confidence - requires further evaluation';
    if (primaryProb > 0.8) {
      confidenceClass = 'text-success';
      confidenceMessage = 'High confidence in diagnosis';
    } else if (primaryProb > 0.6) {
      confidenceClass = 'text-warning';
      confidenceMessage = 'Moderate confidence - consider additional testing';
    }

    // Determine severity styling
    let severityClass = 'badge-secondary';
    let severityIcon = 'fas fa-question-circle';
    switch(classInfo.severity) {
      case 'normal':
        severityClass = 'badge-success';
        severityIcon = 'fas fa-check-circle';
        break;
      case 'low':
        severityClass = 'badge-info';
        severityIcon = 'fas fa-info-circle';
        break;
      case 'moderate':
        severityClass = 'badge-warning';
        severityIcon = 'fas fa-exclamation-triangle';
        break;
      case 'high':
        severityClass = 'badge-danger';
        severityIcon = 'fas fa-exclamation-circle';
        break;
      case 'critical':
        severityClass = 'badge-danger';
        severityIcon = 'fas fa-times-circle';
        break;
    }

    const detailedProbsHtml = this.getDetailedProbabilitiesHtml(data.probabilities);

    this.analysisResults.innerHTML = `
      <div class="ecg-analysis-results">
        <!-- Primary Diagnosis Card -->
        <div class="card border-primary mb-3">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0"><i class="fas fa-heartbeat"></i> Primary Diagnosis</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-8">
                <h4 class="text-primary mb-2">${primaryName}</h4>
                <span class="badge ${severityClass} mb-2">
                  <i class="${severityIcon}"></i> ${classInfo.severity.charAt(0).toUpperCase() + classInfo.severity.slice(1)} Priority
                </span>
              </div>
              <div class="col-md-4 text-right">
                <div class="mb-2">
                  <small class="text-muted">Confidence Level</small>
                  <div class="h4 ${confidenceClass}">${confidencePct}</div>
                  <small class="${confidenceClass}">${confidenceMessage}</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Explanation Card -->
        <div class="card border-info mb-3">
          <div class="card-header bg-info text-white">
            <h6 class="mb-0"><i class="fas fa-info-circle"></i> What This Means (In Simple Terms)</h6>
          </div>
          <div class="card-body">
            <p class="mb-3">${classInfo.explanation}</p>
            <div class="alert alert-light border-left-info">
              <strong><i class="fas fa-stethoscope"></i> Recommended Action:</strong><br>
              ${classInfo.action}
            </div>
          </div>
        </div>

        <!-- AI Summary Card -->
        <div class="card border-secondary mb-3">
          <div class="card-header bg-secondary text-white">
            <h6 class="mb-0"><i class="fas fa-robot"></i> AI Analysis Summary</h6>
          </div>
          <div class="card-body">
            <p class="mb-0">${summary}</p>
            <hr>
            <small class="text-muted">
              <i class="fas fa-info-circle"></i> This is an AI-powered analysis. Always consult with a qualified healthcare professional for medical interpretation and treatment decisions.
            </small>
          </div>
        </div>

        <!-- Detailed Probabilities (Collapsible) -->
        <div class="card border-light">
          <div class="card-header bg-light">
            <h6 class="mb-0">
              <button class="btn btn-link text-decoration-none p-0" type="button" data-toggle="collapse" data-target="#detailedProbs" aria-expanded="false" aria-controls="detailedProbs">
                <i class="fas fa-chart-bar"></i> Detailed Analysis Results <i class="fas fa-chevron-down ml-2"></i>
              </button>
            </h6>
          </div>
          <div class="collapse" id="detailedProbs">
            <div class="card-body">
              <p class="text-muted mb-3">
                <small>The AI system evaluates multiple possible diagnoses. Here are all the probabilities:</small>
              </p>
              ${detailedProbsHtml}
            </div>
          </div>
        </div>
      </div>

      <style>
        .border-left-info {
          border-left: 4px solid #17a2b8 !important;
        }
        .ecg-analysis-results .card {
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          border-radius: 8px;
        }
        .ecg-analysis-results .progress {
          height: 8px;
          border-radius: 4px;
        }
      </style>
    `;
    
    console.log('Enhanced ECG analysis results displayed with comprehensive explanations');
  }

  // Enhanced detailed probabilities with full class names
  getDetailedProbabilitiesHtml(probabilities) {
    let html = '<div class="row">';
    
    // Sort probabilities by value (highest first)
    const sortedProbs = Object.entries(probabilities).sort(([,a], [,b]) => b - a);
    
    for (const [abbr, p] of sortedProbs) {
      const pct = (p * 100).toFixed(1);
      const classInfo = this.getFullClassNameAndExplanation(abbr);
      const displayName = classInfo.fullName;
      
      // Color coding based on probability
      let progressClass = 'bg-secondary';
      if (p > 0.7) progressClass = 'bg-success';
      else if (p > 0.4) progressClass = 'bg-warning';
      else if (p > 0.2) progressClass = 'bg-info';
      
      html += `
        <div class="col-md-6 mb-3">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <small class="font-weight-bold">${displayName}</small>
            <small class="text-muted">${pct}%</small>
          </div>
          <div class="progress" style="height:12px; border-radius: 6px;">
            <div class="progress-bar ${progressClass}" 
                 role="progressbar" 
                 style="width:${pct}%" 
                 aria-valuenow="${pct}" 
                 aria-valuemin="0" 
                 aria-valuemax="100">
            </div>
          </div>
          <small class="text-muted">${abbr}</small>
        </div>`;
    }
    html += '</div>';
    
    html += `
      <div class="mt-3 p-3 bg-light rounded">
        <small class="text-muted">
          <i class="fas fa-lightbulb"></i> <strong>Understanding These Results:</strong><br>
          • Higher percentages indicate stronger likelihood of that specific heart rhythm pattern<br>
          • Multiple conditions can have similar ECG patterns, which is why several options are shown<br>
          • Your doctor will consider these results along with your symptoms and medical history
        </small>
      </div>
    `;
    
    return html;
  }

  displayError(msg) {
    this.analysisError.textContent = msg;
    this.analysisError.style.display = 'block';
  }

  // === In your ECGFormSubmissionHandler class, replace displayECGWaveform: ===

displayECGWaveform() {
  const data      = this.currentECGData;
  const container = this.waveformDisplayArea;
  if (!data || !container) {
    this.showWaveformError('No ECG data or container available.');
    return;
  }

  // 1 mm = 4 px
  const PX_PER_MM  = 4;
  const SMALL_BOX  = PX_PER_MM;        // 1 mm
  const LARGE_BOX  = PX_PER_MM * 5;    // 5 mm

  // Margins (px) for labels
  const M_LEFT   = LARGE_BOX * 4;
  const M_RIGHT  = LARGE_BOX * 1.5;
  const M_TOP    = LARGE_BOX * 1.5;
  const M_BOTTOM = LARGE_BOX * 3;

  // Plot dimensions (px)
  const totalSec  = data.duration;             // e.g. 15.0 s
  const boxesHorz = totalSec / 0.04;           // small boxes across
  const plotW     = boxesHorz * SMALL_BOX;     // px width
  const plotH     = 30 * SMALL_BOX;            // ±1.5 mV => 30 mm

  // Overall SVG size
  const svgW = M_LEFT + plotW + M_RIGHT;
  const svgH = M_TOP  + plotH + M_BOTTOM;

  // Clear prior content
  container.innerHTML = '';

  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');

  // FIXED size on SVG
  svg.setAttribute('width',  svgW);
  svg.setAttribute('height', svgH);
  svg.setAttribute('viewBox', `0 0 ${svgW} ${svgH}`);

  // 1) Background
  const bg = document.createElementNS(NS, 'rect');
  bg.setAttribute('x',      M_LEFT);
  bg.setAttribute('y',      M_TOP);
  bg.setAttribute('width',  plotW);
  bg.setAttribute('height', plotH);
  bg.setAttribute('fill',   '#FFF8DC');
  svg.appendChild(bg);

  // 2) Grid (small & large)
  // small lines
  for (let i = 0; i <= plotW/SMALL_BOX; i++) {
    const x = M_LEFT + i * SMALL_BOX;
    [ [x, M_TOP, x, M_TOP+plotH], [M_LEFT, M_TOP + i*SMALL_BOX, M_LEFT+plotW, M_TOP + i*SMALL_BOX] ]
      .forEach(coords => {
        const line = document.createElementNS(NS, 'line');
        line.setAttribute('x1', coords[0]);
        line.setAttribute('y1', coords[1]);
        line.setAttribute('x2', coords[2]);
        line.setAttribute('y2', coords[3]);
        line.setAttribute('stroke','black');
        line.setAttribute('stroke-width','0.5');
        line.setAttribute('stroke-opacity','0.1');
        svg.appendChild(line);
      });
  }
  // large lines
  for (let i = 0; i <= plotW/LARGE_BOX; i++) {
    const x = M_LEFT + i * LARGE_BOX;
    [ [x, M_TOP, x, M_TOP+plotH], [M_LEFT, M_TOP + i*LARGE_BOX, M_LEFT+plotW, M_TOP + i*LARGE_BOX] ]
      .forEach(coords => {
        const line = document.createElementNS(NS, 'line');
        line.setAttribute('x1', coords[0]);
        line.setAttribute('y1', coords[1]);
        line.setAttribute('x2', coords[2]);
        line.setAttribute('y2', coords[3]);
        line.setAttribute('stroke','black');
        line.setAttribute('stroke-width','1');
        line.setAttribute('stroke-opacity','0.25');
        svg.appendChild(line);
      });
  }

  // 3) ECG trace
  const pts = data.time.map((t,i) => {
    const x = M_LEFT + (t/totalSec) * plotW;
    const y = M_TOP + plotH - ((data.signals[this.currentLead][i] + 1.5)/3) * plotH;
    return `${x},${y}`;
  }).join(' ');
  const trace = document.createElementNS(NS,'polyline');
  trace.setAttribute('points', pts);
  trace.setAttribute('fill',   'none');
  trace.setAttribute('stroke', 'black');
  trace.setAttribute('stroke-width','1.5');
  svg.appendChild(trace);

  // 4) X-axis ticks & labels (0.2 s steps)
  for (let i = 0; i <= boxesHorz; i += 5) {
    const x = M_LEFT + i * SMALL_BOX;
    const tick = document.createElementNS(NS,'line');
    tick.setAttribute('x1', x); tick.setAttribute('y1', M_TOP+plotH);
    tick.setAttribute('x2', x); tick.setAttribute('y2', M_TOP+plotH+8);
    tick.setAttribute('stroke','black');
    svg.appendChild(tick);
    const text = document.createElementNS(NS,'text');
    text.setAttribute('x', x); 
    text.setAttribute('y', M_TOP+plotH+25);
    text.setAttribute('font-size','10');
    text.setAttribute('text-anchor','middle');
    text.textContent = ((i/5)*0.2).toFixed(1);
    svg.appendChild(text);
  }

  // 5) Y-axis ticks & labels (0.5 mV steps)
  const rows = Math.ceil(plotH / LARGE_BOX);
  for (let j = 0; j <= rows; j++) {
    const y = M_TOP + plotH - j * LARGE_BOX;
    const tick = document.createElementNS(NS,'line');
    tick.setAttribute('x1', M_LEFT); tick.setAttribute('y1', y);
    tick.setAttribute('x2', M_LEFT-8); tick.setAttribute('y2', y);
    tick.setAttribute('stroke','black');
    svg.appendChild(tick);
    const text = document.createElementNS(NS,'text');
    text.setAttribute('x', M_LEFT-12);
    text.setAttribute('y', y+4);
    text.setAttribute('font-size','10');
    text.setAttribute('text-anchor','end');
    text.textContent = ( (j*0.5) - (rows*0.5)/2 ).toFixed(1) + ' mV';
    svg.appendChild(text);
  }

  // 6) Axis titles
  const xlabel = document.createElementNS(NS,'text');
  xlabel.setAttribute('x', M_LEFT + plotW/2);
  xlabel.setAttribute('y', M_TOP + plotH + 40);
  xlabel.setAttribute('font-size','14');
  xlabel.setAttribute('text-anchor','middle');
  xlabel.textContent = 'Time (s)';
  svg.appendChild(xlabel);

  const ylabel = document.createElementNS(NS,'text');
  ylabel.setAttribute('x', M_LEFT-60);
  ylabel.setAttribute('y', M_TOP + plotH/2);
  ylabel.setAttribute('font-size','14');
  ylabel.setAttribute('text-anchor','middle');
  ylabel.setAttribute('transform', `rotate(-90 ${M_LEFT-60},${M_TOP+plotH/2})`);
  ylabel.textContent = 'Voltage (mV)';
  svg.appendChild(ylabel);

  // 7) Inject SVG
  container.appendChild(svg);
}


// === drawGrid: small & large ECG boxes ===

drawGrid(ctx, width, height, offsetX, offsetY, small, large) {
  ctx.save();
  ctx.translate(offsetX, offsetY);

  // Small boxes
  ctx.strokeStyle = 'rgba(0,0,0,0.1)';
  ctx.lineWidth   = 0.5;
  for (let x = 0; x <= width; x += small) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }
  for (let y = 0; y <= height; y += small) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }

  // Large boxes
  ctx.strokeStyle = 'rgba(0,0,0,0.25)';
  ctx.lineWidth   = 1;
  for (let x = 0; x <= width; x += large) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }
  for (let y = 0; y <= height; y += large) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }

  ctx.restore();
}

// === drawAxes: time & voltage labels ===



  fetchAndDisplayWaveform(matFile, heaFile) {
    console.log('Fetching ECG waveform data...');
    this.showWaveformLoading();
    this.waveformDisplayArea.style.display = 'block'; // Show the area

    const formData = new FormData();
    formData.append('mat_file', matFile);
    formData.append('hea_file', heaFile);

    fetch('/ecg_waveform_data', { method: 'POST', body: formData })
      .then(response => {
        if (!response.ok) {
          return response.json().then(errData => {
            throw new Error(errData.error || `Server returned ${response.status} for waveform`);
          }).catch(() => {
            throw new Error(`Server returned ${response.status} for waveform`);
          });
        }
        return response.json();
      })
      .then(data => {
        this.hideWaveformLoading();
        if (data.success && data.ecg_data) {
          this.currentECGData = data.ecg_data;
          this.currentLead = 0; // Default to first lead
          this.createLeadControls(this.currentECGData.n_leads, this.currentECGData.lead_names);
          this.displayECGWaveform();
        } else {
          throw new Error(data.error || 'Unknown error fetching waveform data');
        }
      })
      .catch(err => {
        console.error('Waveform data error:', err);
        this.hideWaveformLoading();
        this.showWaveformError(err.message);
      });
  }

  showWaveformLoading() {
    if (this.waveformLoading) this.waveformLoading.style.display = 'block';
    if (this.waveformError) this.waveformError.style.display = 'none';
    if (this.waveformChartCanvas) this.waveformChartCanvas.style.display = 'none';
    if (this.waveformControls) this.waveformControls.innerHTML = '';
  }

  hideWaveformLoading() {
    if (this.waveformLoading) this.waveformLoading.style.display = 'none';
  }

  showWaveformError(msg) {
    if (this.waveformError) {
      this.waveformError.textContent = 'Error loading waveform: ' + msg;
      this.waveformError.style.display = 'block';
    }
    if (this.waveformChartCanvas) this.waveformChartCanvas.style.display = 'none';
    if (this.waveformControls) this.waveformControls.innerHTML = '';
  }
  
  hideWaveformDisplay() {
    if (this.waveformDisplayArea) this.waveformDisplayArea.style.display = 'none';
    if (this.waveformError) this.waveformError.style.display = 'none';
    if (this.waveformLoading) this.waveformLoading.style.display = 'none';
    if (this.waveformChartCanvas) this.waveformChartCanvas.style.display = 'none';
    if (this.waveformControls) this.waveformControls.innerHTML = '';
     if (this.ecgChart) {
        this.ecgChart.destroy();
        this.ecgChart = null;
    }
  }

  

  createLeadControls(numberOfLeads, leadNames) {
    if (!this.waveformControls) return;
    
    let controlsHTML = `
      <div class="row align-items-center">
        <div class="col-md-4">
          <label for="lead-selector" class="form-label mb-1"><strong>Select ECG Lead:</strong></label>
          <select id="lead-selector" class="form-control form-control-sm">
    `;
    
    for (let i = 0; i < numberOfLeads; i++) {
      const leadName = leadNames[i] || `Lead ${i + 1}`;
      controlsHTML += `<option value="${i}" ${this.currentLead === i ? 'selected' : ''}> ${leadName}</option>`;
    }
    
    controlsHTML += `
          </select>
        </div>
      </div>
    `;
    
    this.waveformControls.innerHTML = controlsHTML;
    
    const leadSelector = document.getElementById('lead-selector');
    if (leadSelector) {
      leadSelector.addEventListener('change', (event) => {
        this.currentLead = parseInt(event.target.value, 10);
        this.displayECGWaveform();
      });
    }
  }

  // Make sure to call hideWaveformDisplay in initializeElements or constructor if it should be hidden initially
  // ... (rest of the class) ...
}

// Auto-initialize
window.ECGFormSubmissionHandler = ECGFormSubmissionHandler;
let ecgFormHandler = null;
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    ecgFormHandler = new ECGFormSubmissionHandler();
  });
} else {
  ecgFormHandler = new ECGFormSubmissionHandler();
}
