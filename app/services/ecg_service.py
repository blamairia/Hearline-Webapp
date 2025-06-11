# app/services/ecg_service.py

import os
import torch
import numpy as np
import wfdb
import tempfile
from flask import current_app

# Import ResNet architecture
from resnet import resnet34


class ECGService:
    """Service class for ECG analysis and processing."""
    
    def __init__(self):
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.model = None
        self.class_names = {
            "SNR": "Sinus Rhythm",
            "AF": "Atrial Fibrillation",
            "IAVB": "AV Block",
            "LBBB": "Left Bundle Branch Block",
            "RBBB": "Right Bundle Branch Block",
            "PAC": "Premature Atrial Contraction",
            "PVC": "Premature Ventricular Contraction",
            "STD": "ST Depression",
            "STE": "ST Elevation"
        }
        self.class_abbreviations = ["SNR", "AF", "IAVB", "LBBB", "RBBB", "PAC", "PVC", "STD", "STE"]
        # Don't load model immediately - wait for app context
    
    def load_model(self):
        """Load the ECG analysis model."""
        if self.model is not None:
            return  # Already loaded
            
        try:
            model_path = current_app.config['ECG_MODEL_PATH']
            
            # Instantiate the ResNet34 architecture (12 input channels, 9 classes)
            self.model = resnet34(input_channels=12, num_classes=9)
            
            # Load the saved state_dict
            if os.path.exists(model_path):
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                
                # Move to device and switch to eval mode
                self.model.to(self.device)
                self.model.eval()
                
                current_app.logger.info(f"ECG model loaded successfully from {model_path}")
            else:
                current_app.logger.warning(f"Model file not found at {model_path}. ECG inference will be disabled.")
                self.model = None
        except Exception as e:
            current_app.logger.error(f"Error loading ECG model: {e}. ECG inference will be disabled.")
            self.model = None
    
    def preprocess_ecg_signal(self, signal, target_length=5000):
        """Preprocess ECG signal for model input."""
        try:
            # Convert to numpy if needed
            if not isinstance(signal, np.ndarray):
                signal = np.array(signal)
            
            # Handle different signal shapes
            if len(signal.shape) == 1:
                # Single lead, expand to 12 leads by repeating
                signal = np.tile(signal.reshape(1, -1), (12, 1))
            elif signal.shape[0] > signal.shape[1]:
                # Transpose if samples x leads instead of leads x samples
                signal = signal.T
            
            # Ensure we have exactly 12 leads
            if signal.shape[0] < 12:
                # Pad with zeros if fewer than 12 leads
                padding = np.zeros((12 - signal.shape[0], signal.shape[1]))
                signal = np.vstack([signal, padding])
            elif signal.shape[0] > 12:
                # Take first 12 leads if more than 12
                signal = signal[:12, :]
            
            # Resize to target length
            current_length = signal.shape[1]
            if current_length != target_length:
                # Simple resampling by interpolation
                indices = np.linspace(0, current_length - 1, target_length)
                resampled_signal = np.zeros((12, target_length))
                for i in range(12):
                    resampled_signal[i, :] = np.interp(indices, np.arange(current_length), signal[i, :])
                signal = resampled_signal
            
            # Normalize
            signal = (signal - np.mean(signal, axis=1, keepdims=True)) / (np.std(signal, axis=1, keepdims=True) + 1e-8)
            
            # Convert to tensor
            signal_tensor = torch.FloatTensor(signal).unsqueeze(0)  # Add batch dimension
            
            return signal_tensor
            
        except Exception as e:
            current_app.logger.error(f"Error preprocessing ECG signal: {e}")
            return None
      def analyze_ecg_files(self, mat_path, hea_path):
        """Analyze ECG files and return predictions."""
        self.load_model()  # Ensure model is loaded
        
        if not self.model:
            raise Exception("ECG model not loaded")
        
        try:
            # Read ECG data using wfdb
            rec_basename = os.path.splitext(os.path.basename(hea_path))[0]
            rec_dir = os.path.dirname(hea_path)
            record_path = os.path.join(rec_dir, rec_basename)
            
            record = wfdb.rdrecord(record_path)
            signal = record.p_signal.T  # Transpose to get leads x samples
            
            # Preprocess signal
            processed_signal = self.preprocess_ecg_signal(signal)
            if processed_signal is None:
                raise Exception("Failed to preprocess ECG signal")
            
            # Move to device
            processed_signal = processed_signal.to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(processed_signal)
                probabilities = torch.softmax(outputs, dim=1)
                probs_np = probabilities.cpu().numpy()[0]
            
            # Create prediction dictionary
            predictions = {abbr: float(probs_np[i]) for i, abbr in enumerate(self.class_abbreviations)}
            
            return predictions
            
        except Exception as e:
            current_app.logger.error(f"Error analyzing ECG files: {e}")
            raise
    
    def get_ecg_waveform_data(self, hea_path):
        """Extract ECG waveform data for visualization."""
        try:
            rec_basename = os.path.splitext(os.path.basename(hea_path))[0]
            rec_dir = os.path.dirname(hea_path)
            record_path = os.path.join(rec_dir, rec_basename)
            
            record = wfdb.rdrecord(record_path)
            sig_all = record.p_signal
            nsteps, nleads = sig_all.shape
            
            fs = float(record.fs) if hasattr(record, 'fs') and record.fs else 250.0
            time_duration = nsteps / fs
            time_data = np.linspace(0, time_duration, nsteps).tolist()
            
            signals_list = []
            lead_names = record.sig_name if hasattr(record, 'sig_name') and record.sig_name else [f"Lead {i+1}" for i in range(nleads)]

            for lead_idx in range(nleads):
                lead_signal = sig_all[:, lead_idx]
                signals_list.append(lead_signal.tolist())

            ecg_data = {
                "time": time_data,
                "signals": signals_list,
                "sampling_rate": fs,
                "duration": time_duration,
                "lead_names": lead_names,
                "n_leads": nleads
            }
            
            return ecg_data
            
        except Exception as e:
            current_app.logger.error(f"Error extracting ECG waveform data: {e}")
            raise
    
    def get_analysis_summary(self, predictions):
        """Get a human-readable summary of ECG analysis."""
        if not predictions:
            return "No analysis available"
        
        # Find primary diagnosis
        max_prob_abbr = max(predictions, key=predictions.get)
        max_prob_value = predictions[max_prob_abbr]
        primary_name = self.class_names.get(max_prob_abbr, max_prob_abbr)
        
        return f"Primary finding: {primary_name} ({max_prob_value:.1%} confidence)"
