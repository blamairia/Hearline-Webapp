# ECG Demo Files

This directory contains representative ECG sample files for demonstration and testing purposes.

## File Organization

Each ECG record consists of two files:
- `.mat` - Signal data (WFDB format)
- `.hea` - Header file with metadata

## ECG Class Mapping

| File ID | ECG Class | Full Name | Clinical Description |
|---------|-----------|-----------|---------------------|
| A0002, A0016 | **SNR** | Sinus Rhythm | Normal heart rhythm |
| A0003, A0004 | **AF** | Atrial Fibrillation | Irregular, rapid atrial activation |
| A0039, A0042 | **IAVB** | AV Block | Impaired conduction between atria and ventricles |
| A0011, A0018 | **LBBB** | Left Bundle Branch Block | Delayed left ventricular activation |
| A0001, A0006 | **RBBB** | Right Bundle Branch Block | Delayed right ventricular activation |
| A0047, A0049 | **PAC** | Premature Atrial Contraction | Early atrial beats |
| A0005, A0012 | **PVC** | Premature Ventricular Contraction | Early ventricular beats |
| A0008, A0013 | **STD** | ST Depression | Potential ischemia indicator |
| A0021, A0032 | **STE** | ST Elevation | Potential myocardial infarction indicator |

## Usage

These files are automatically available in the visit creation form under the "Demo ECG Files" section. Users can:
1. **Drag and drop** a demo file card to the ECG upload area
2. **Click "Use This File"** button on any demo card
3. Both .mat and .hea files are bundled together in each card

## Source

Files are sourced from the CPSC 2018 ECG Challenge dataset and selected based on their ground truth labels from `labels.csv`.

## Adding More Demo Files

To add additional demo files:
1. Identify the file ID and its ECG class from the CPSC dataset
2. Copy both `.mat` and `.hea` files to this directory
3. Update the mapping table above
4. Update the backend API in `app.py` if needed

## Technical Notes

- Files are read-only copies
- ECG analysis uses the ResNet34 ONNX model
- Expected input: 12-lead ECG with 15,000 samples
