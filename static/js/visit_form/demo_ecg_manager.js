/**
 * Demo ECG Files Manager Module
 * Handles loading, rendering, and selecting demo ECG files
 * Includes drag-and-drop functionality and prevents infinite loading loops
 */

class DemoECGManager {
    constructor() {
        this.demoFilesData = [];
        this.isLoading = false;
        this.hasLoaded = false; // Prevent multiple loads
        this.grid = null;
        this.uploadSection = null;
        this.dropZone = null;
    }

    /**
     * Initialize the demo ECG manager
     */
    init() {
        // Get DOM elements
        this.grid = document.getElementById('demo-files-grid');
        this.uploadSection = document.getElementById('manual-upload-section');
        this.dropZone = document.getElementById('ecg-drop-zone');

        if (!this.grid) {
            console.error('Demo files grid element not found');
            return;
        }

        // Set up event listeners
        this.setupEventListeners();

        // Load demo files only once
        if (!this.hasLoaded && !this.isLoading) {
            this.loadDemoFiles();
        }
    }

    /**
     * Load demo files from server with proper error handling
     */
    async loadDemoFiles() {
        // Prevent multiple simultaneous loads (fixes infinite loop)
        if (this.isLoading || this.hasLoaded) {
            console.log('Demo files already loading or loaded, skipping...');
            return;
        }

        this.isLoading = true;
        console.log('Loading demo ECG files...');

        try {
            const response = await fetch(window.DEMO_FILES_URL || '/api/demo_ecg_files');

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Validate response data
            if (!data || !Array.isArray(data.demo_files)) {
                throw new Error('Invalid response format from server');
            }

            this.demoFilesData = data.demo_files;
            this.renderDemoFiles(this.demoFilesData);
            this.hasLoaded = true;

            console.log(`Successfully loaded ${this.demoFilesData.length} demo files`);
        } catch (error) {
            console.error('Error loading demo files:', error);
            this.showError('Failed to load demo files. Please refresh the page.');
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Render demo files as cards
     */
    renderDemoFiles(files) {
        if (!this.grid) return;

        if (files.length === 0) {
            this.grid.innerHTML = '<div class="col-12"><div class="alert alert-warning">No demo files available.</div></div>';
            return;
        }

        // Group files by class
        const groupedFiles = {};
        files.forEach(file => {
            if (!groupedFiles[file.class_abbr]) {
                groupedFiles[file.class_abbr] = {
                    name: file.class_name,
                    description: file.description,
                    color: file.color,
                    files: []
                };
            }
            groupedFiles[file.class_abbr].files.push(file);
        });

        // Render cards - one card per class with variant toggle
        let html = '';
        for (const [abbr, classData] of Object.entries(groupedFiles)) {
            const variants = classData.files;
            const firstFile = variants[0];

            html += `
                <div class="col-md-6 col-lg-4">
                    <div class="demo-file-card card h-100 border-${firstFile.color}" 
                         draggable="true" 
                         data-file-id="${firstFile.id}"
                         data-class-abbr="${abbr}"
                         data-class-name="${firstFile.class_name}"
                         data-variants='${JSON.stringify(variants.map(v => v.id))}'
                         data-current-variant="0"
                         style="cursor: grab;">
                        <div class="card-body p-3">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <span class="badge bg-${firstFile.color}">${abbr}</span>
                                <i class="fas fa-grip-vertical text-muted"></i>
                            </div>
                            <h6 class="card-title mb-1">${firstFile.class_name}</h6>
                            <p class="card-text small text-muted mb-2">${firstFile.description}</p>
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <div class="small text-muted">
                                    <i class="fas fa-file me-1"></i><span class="file-id-display">${firstFile.id}</span>
                                </div>
                                ${variants.length > 1 ? `
                                <div class="btn-group btn-group-sm" role="group">
                                    ${variants.map((v, idx) => `
                                        <button type="button" class="btn btn-outline-secondary variant-toggle ${idx === 0 ? 'active' : ''}" data-variant-idx="${idx}">
                                            ${idx + 1}
                                        </button>
                                    `).join('')}
                                </div>
                                ` : ''}
                            </div>
                            <button type="button" class="btn btn-sm btn-outline-primary w-100 use-demo-file">
                                <i class="fas fa-check me-1"></i>Use This File
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }

        this.grid.innerHTML = html;

        // Attach event listeners to newly created elements
        this.attachCardListeners();
    }

    /**
     * Show error message in the grid
     */
    showError(message) {
        if (!this.grid) return;

        this.grid.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>${message}
                </div>
            </div>
        `;
    }

    /**
     * Attach event listeners to demo file cards
     */
    attachCardListeners() {
        // Variant toggle buttons
        document.querySelectorAll('.variant-toggle').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const card = e.target.closest('.demo-file-card');
                const variantIdx = parseInt(e.target.dataset.variantIdx);
                const variants = JSON.parse(card.dataset.variants);

                // Update active button
                card.querySelectorAll('.variant-toggle').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');

                // Update card data
                card.dataset.currentVariant = variantIdx;
                card.dataset.fileId = variants[variantIdx];
                card.querySelector('.file-id-display').textContent = variants[variantIdx];
            });
        });

        // Drag start
        document.querySelectorAll('.demo-file-card').forEach(card => {
            card.addEventListener('dragstart', (e) => {
                e.dataTransfer.effectAllowed = 'copy';
                e.dataTransfer.setData('text/plain', card.dataset.fileId);
                card.style.opacity = '0.5';
            });

            card.addEventListener('dragend', (e) => {
                card.style.opacity = '1';
            });
        });

        // Click "Use This File" button
        document.querySelectorAll('.use-demo-file').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = e.target.closest('.demo-file-card');
                this.selectDemoFile(card.dataset.fileId, card.dataset.className);
            });
        });
    }

    /**
     * Set up event listeners for drag and drop
     */
    setupEventListeners() {
        if (!this.uploadSection || !this.dropZone) return;

        // Drop zone handling
        this.uploadSection.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
            this.uploadSection.classList.add('drag-over-active');
        });

        this.uploadSection.addEventListener('dragleave', (e) => {
            // Only remove if leaving the upload section entirely
            if (!this.uploadSection.contains(e.relatedTarget)) {
                this.uploadSection.classList.remove('drag-over-active');
            }
        });

        this.uploadSection.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadSection.classList.remove('drag-over-active');

            const fileId = e.dataTransfer.getData('text/plain');
            if (fileId) {
                const file = this.demoFilesData.find(f => f.id === fileId);
                if (file) {
                    this.selectDemoFile(file.id, file.class_name);
                }
            }
        });

        // Toggle demo files visibility
        const toggleBtn = document.getElementById('toggle-demo-files');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const container = document.getElementById('demo-files-container');
                const icon = toggleBtn.querySelector('i');

                if (container.classList.contains('show')) {
                    container.classList.remove('show');
                    icon.classList.remove('fa-chevron-down');
                    icon.classList.add('fa-chevron-up');
                } else {
                    container.classList.add('show');
                    icon.classList.remove('fa-chevron-up');
                    icon.classList.add('fa-chevron-down');
                }
            });
        }

        // Clear selection button
        const clearBtn = document.getElementById('clear-demo-selection');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearSelection());
        }

        // Clear demo selection when user manually selects files
        const ecgMatInput = document.getElementById('ecg_mat_input');
        const ecgHeaInput = document.getElementById('ecg_hea_input');

        if (ecgMatInput) {
            ecgMatInput.addEventListener('change', () => {
                if (ecgMatInput.value) {
                    this.clearSelection();
                }
            });
        }

        if (ecgHeaInput) {
            ecgHeaInput.addEventListener('change', () => {
                if (ecgHeaInput.value) {
                    this.clearSelection();
                }
            });
        }
    }

    /**
     * Select a demo file
     */
    selectDemoFile(fileId, className) {
        // Clear any manual file selections
        const ecgMatInput = document.getElementById('ecg_mat_input');
        const ecgHeaInput = document.getElementById('ecg_hea_input');

        if (ecgMatInput) ecgMatInput.value = '';
        if (ecgHeaInput) ecgHeaInput.value = '';

        // Set hidden field
        const hiddenField = document.getElementById('demo_file_id');
        if (hiddenField) {
            hiddenField.value = fileId;
        }

        // Show selection indicator
        const selectedNameSpan = document.getElementById('selected-demo-name');
        const indicator = document.getElementById('demo-selection-indicator');

        if (selectedNameSpan) {
            selectedNameSpan.textContent = `${fileId} (${className})`;
        }

        if (indicator) {
            indicator.classList.remove('d-none');
        }

        // Disable manual upload inputs
        if (ecgMatInput) ecgMatInput.disabled = true;
        if (ecgHeaInput) ecgHeaInput.disabled = true;

        // Trigger live ECG analysis (will be handled by ECGAnalysis module)
        if (window.ecgAnalysis && typeof window.ecgAnalysis.performLiveAnalysis === 'function') {
            window.ecgAnalysis.performLiveAnalysis(fileId);
        }

        // Scroll to indicator
        if (indicator) {
            indicator.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    /**
     * Clear demo file selection
     */
    clearSelection() {
        const hiddenField = document.getElementById('demo_file_id');
        const indicator = document.getElementById('demo-selection-indicator');
        const ecgMatInput = document.getElementById('ecg_mat_input');
        const ecgHeaInput = document.getElementById('ecg_hea_input');
        const resultsPanel = document.getElementById('live-analysis-results');

        if (hiddenField) hiddenField.value = '';
        if (indicator) indicator.classList.add('d-none');
        if (ecgMatInput) ecgMatInput.disabled = false;
        if (ecgHeaInput) ecgHeaInput.disabled = false;
        if (resultsPanel) resultsPanel.classList.add('d-none');
    }
}

// Export for use in main script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DemoECGManager;
}
