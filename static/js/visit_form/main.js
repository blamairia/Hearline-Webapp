/**
 * Visit Form Main Module
 * Coordinates all visit form functionality
 */

// Initialize all modules when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    console.log('Initializing Visit Form...');

    // Create module instances
    window.demoECGManager = new DemoECGManager();
    window.ecgAnalysis = new ECGAnalysis();
    window.formControls = new FormControls();

    // Initialize modules in correct order
    try {
        // 1. Initialize form controls first (patient/medication selects, date pickers)
        window.formControls.init();
        console.log('✓ Form controls initialized');

        // 2. Initialize ECG analysis module
        window.ecgAnalysis.init();
        console.log('✓ ECG analysis initialized');

        // 3. Initialize demo ECG manager last (will trigger file loading)
        window.demoECGManager.init();
        console.log('✓ Demo ECG manager initialized');

        console.log('Visit Form initialization complete!');
    } catch (error) {
        console.error('Error initializing visit form:', error);
        // Show user-friendly error message
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger alert-dismissible fade show';
        errorAlert.innerHTML = `
            <strong>Initialization Error:</strong> There was a problem loading the form. 
            Please refresh the page. If the problem persists, contact support.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('.page-container');
        if (container) {
            container.insertBefore(errorAlert, container.firstChild);
        }
    }
});
