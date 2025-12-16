/**
 * Form Controls Module
 * Handles Tom Select initialization, Flatpickr, and dynamic form rows
 */

class FormControls {
    constructor() {
        this.patientSelect = null;
        this.medicationSelects = [];
        this.prescriptionCount = 0;
        this.documentCount = 0;
    }

    /**
     * Initialize all form controls
     */
    init() {
        this.initPatientSelect();
        this.initMedicationSelects();
        this.initFlatpickr();
        this.initDynamicFields();

        // Initialize counters
        this.prescriptionCount = document.querySelectorAll('.prescription-row').length || 0;
        this.documentCount = document.querySelectorAll('.document-row').length || 0;
    }

    /**
     * Initialize patient selection with Tom Select
     */
    initPatientSelect() {
        const selectElement = document.getElementById('patient-select');
        if (!selectElement) {
            console.warn('Patient select element not found');
            return;
        }

        this.patientSelect = new TomSelect('#patient-select', {
            valueField: 'id',
            labelField: 'text',
            searchField: 'text',
            placeholder: "Search for a patient...",
            maxOptions: 10,
            load: function (query, callback) {
                const url = window.SEARCH_PATIENTS_URL || '/search_patients_api';
                fetch(`${url}?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(json => {
                        callback(json.results || []);
                    })
                    .catch((error) => {
                        console.error('Error loading patients:', error);
                        callback();
                    });
            },
            dropdownParent: 'body',
            render: {
                option: function (data, escape) {
                    return '<div>' +
                        '<span class="title">' + escape(data.text) + '</span>' +
                        '</div>';
                },
                item: function (data, escape) {
                    return '<div>' + escape(data.text) + '</div>';
                }
            }
        });
    }

    /**
     * Initialize medication selection with Tom Select
     */
    initMedicationSelects() {
        const selects = document.querySelectorAll('.medication-select');
        selects.forEach(element => {
            this.initSingleMedicationSelect(element);
        });
    }

    /**
     * Initialize a single medication select element
     */
    initSingleMedicationSelect(element) {
        if (!element || element.tomselect) {
            return; // Already initialized
        }

        const select = new TomSelect(element, {
            valueField: 'id',
            labelField: 'text',
            searchField: 'text',
            placeholder: "Search for a medication...",
            maxOptions: 15,
            load: function (query, callback) {
                const url = window.SEARCH_MEDICATIONS_URL || '/search_medications_api';
                fetch(`${url}?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(json => {
                        callback(json.results || []);
                    })
                    .catch((error) => {
                        console.error('Error loading medications:', error);
                        callback();
                    });
            },
            dropdownParent: 'body',
            render: {
                option: function (data, escape) {
                    return '<div>' +
                        '<span class="title">' + escape(data.text) + '</span>' +
                        '</div>';
                },
                item: function (data, escape) {
                    return '<div>' + escape(data.text) + '</div>';
                }
            }
        });

        this.medicationSelects.push(select);
    }

    /**
     * Initialize Flatpickr date/time pickers
     */
    initFlatpickr() {
        if (typeof flatpickr === 'undefined') {
            console.warn('Flatpickr not loaded');
            return;
        }

        flatpickr(".flatpickr-datetime", {
            enableTime: true,
            dateFormat: "Y-m-d\\TH:i",  // Changed from "Y-m-d H:i" to match WTForms format %Y-%m-%dT%H:%M
            time_24hr: true
        });
    }

    /**
     * Initialize dynamic prescription and document fields
     */
    initDynamicFields() {
        // Add prescription button
        const addPrescriptionBtn = document.getElementById('add-prescription');
        if (addPrescriptionBtn) {
            addPrescriptionBtn.addEventListener('click', () => this.addPrescription());
        }

        // Add document button
        const addDocumentBtn = document.getElementById('add-document');
        if (addDocumentBtn) {
            addDocumentBtn.addEventListener('click', () => this.addDocument());
        }

        // Remove buttons (event delegation)
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-prescription')) {
                e.target.closest('.prescription-row').remove();
            }
            if (e.target.classList.contains('remove-document')) {
                e.target.closest('.document-row').remove();
            }
        });
    }

    /**
     * Add a new prescription row
     */
    addPrescription() {
        const template = document.getElementById('prescription-template');
        if (!template) {
            console.error('Prescription template not found');
            return;
        }

        const container = document.getElementById('prescriptions-container');
        if (!container) {
            console.error('Prescriptions container not found');
            return;
        }

        // Get template HTML and replace prefix
        let html = template.innerHTML.replace(/__prefix__/g, this.prescriptionCount);

        // Create new element
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html;
        const newRow = wrapper.firstElementChild;

        container.appendChild(newRow);

        // Initialize Tom Select on the new medication dropdown
        const newSelect = newRow.querySelector('.medication-select');
        if (newSelect) {
            // Small delay to ensure DOM is ready
            setTimeout(() => {
                this.initSingleMedicationSelect(newSelect);
            }, 100);
        }

        this.prescriptionCount++;
    }

    /**
     * Add a new document row
     */
    addDocument() {
        const template = document.getElementById('document-template');
        if (!template) {
            console.error('Document template not found');
            return;
        }

        const container = document.getElementById('documents-container');
        if (!container) {
            console.error('Documents container not found');
            return;
        }

        // Get template HTML and replace prefix
        let html = template.innerHTML.replace(/__prefix__/g, this.documentCount);

        // Create new element
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html;

        container.appendChild(wrapper.firstElementChild);

        this.documentCount++;
    }
}

// Export for use in main script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FormControls;
}
