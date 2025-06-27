"""
ECG Analysis Service for Heartline Desktop Application

This service handles ECG analysis using ONNX Runtime and provides
the same functionality as the web application.
"""

import os
import numpy as np
import onnxruntime as ort
import wfdb
from typing import Dict, List, Optional, Tuple
import tempfile
import logging

from ..core.config import Config, config
from ..core.exceptions import ECGAnalysisError

logger = logging.getLogger(__name__)

class ECGAnalysisService:
    """Service for ECG analysis using ONNX Runtime"""
    
    # ECG condition classes (same as web app)
    ECG_CLASSES = [
        "SNR",   # Sinus Rhythm (Normal)
        "AF",    # Atrial Fibrillation
        "IAVB",  # Atrioventricular Block
        "LBBB",  # Left Bundle Branch Block
        "RBBB",  # Right Bundle Branch Block
        "PAC",   # Premature Atrial Contraction
        "PVC",   # Premature Ventricular Contraction
        "STD",   # ST Depression
        "STE"    # ST Elevation
    ]
    
    def __init__(self):
        self.session: Optional[ort.InferenceSession] = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the ONNX model"""
        try:
            model_path = Config.get_model_path()
            if not model_path.exists():
                raise ECGAnalysisError(f"ONNX model not found at {model_path}")
            
            # Create ONNX Runtime session
            self.session = ort.InferenceSession(
                str(model_path),
                providers=['CPUExecutionProvider']  # Use CPU for compatibility
            )
            
            self.model_loaded = True
            logger.info("ECG analysis model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load ECG model: {e}")
            raise ECGAnalysisError(f"Model loading failed: {e}")
    
    def analyze_ecg_files(self, mat_file_path: str, hea_file_path: str) -> Dict:
        """
        Analyze ECG files and return prediction results
        
        Args:
            mat_file_path: Path to .mat file
            hea_file_path: Path to .hea file
            
        Returns:
            Dictionary with analysis results
        """
        if not self.model_loaded:
            raise ECGAnalysisError("ECG model not loaded")
        
        try:
            # Read ECG signal using wfdb
            signal_data = self._read_ecg_signal(mat_file_path, hea_file_path)
            
            # Preprocess signal
            processed_signal = self._preprocess_signal(signal_data)
            
            # Run inference
            predictions = self._run_inference(processed_signal)
            
            # Format results
            results = self._format_results(predictions)
            
            logger.info("ECG analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"ECG analysis failed: {e}")
            raise ECGAnalysisError(f"Analysis failed: {e}")
    
    def _read_ecg_signal(self, mat_file_path: str, hea_file_path: str) -> np.ndarray:
        """Read ECG signal from files"""
        try:
            # Extract base name without extension
            base_path = os.path.splitext(mat_file_path)[0]
            
            # Read the signal using wfdb
            record = wfdb.rdrecord(base_path)
            signal = record.p_signal
            
            if signal is None or len(signal) == 0:
                raise ECGAnalysisError("No signal data found in ECG files")
            
            return signal
            
        except Exception as e:
            raise ECGAnalysisError(f"Failed to read ECG signal: {e}")
    
    def _preprocess_signal(self, signal: np.ndarray) -> np.ndarray:
        """Preprocess ECG signal for model input"""
        try:
            # Convert to float32
            signal = signal.astype(np.float32)
            
            # Take first lead if multiple leads
            if signal.ndim > 1:
                signal = signal[:, 0]
            
            # Normalize signal
            signal = (signal - np.mean(signal)) / (np.std(signal) + 1e-8)
            
            # Ensure fixed length (example: 5000 samples)
            target_length = 5000
            if len(signal) > target_length:
                signal = signal[:target_length]
            else:
                # Pad with zeros if too short
                signal = np.pad(signal, (0, target_length - len(signal)), 'constant')
            
            # Reshape for model input (batch_size, channels, length)
            signal = signal.reshape(1, 1, -1)
            
            return signal
            
        except Exception as e:
            raise ECGAnalysisError(f"Signal preprocessing failed: {e}")
    
    def _run_inference(self, signal: np.ndarray) -> np.ndarray:
        """Run ONNX model inference"""
        try:
            # Get input name
            input_name = self.session.get_inputs()[0].name
            
            # Run inference
            outputs = self.session.run(None, {input_name: signal})
            
            # Get predictions (assuming single output)
            predictions = outputs[0]
            
            # Apply softmax to get probabilities
            predictions = self._softmax(predictions)
            
            return predictions[0]  # Remove batch dimension
            
        except Exception as e:
            raise ECGAnalysisError(f"Model inference failed: {e}")
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Apply softmax function"""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
    
    def _format_results(self, predictions: np.ndarray) -> Dict:
        """Format prediction results"""
        try:
            # Create results dictionary
            results = {
                "predictions": {},
                "primary_diagnosis": "",
                "confidence": 0.0,
                "analysis_successful": True
            }
            
            # Map predictions to class names
            for i, class_name in enumerate(self.ECG_CLASSES):
                results["predictions"][class_name] = float(predictions[i])
            
            # Find primary diagnosis (highest probability)
            max_idx = np.argmax(predictions)
            results["primary_diagnosis"] = self.ECG_CLASSES[max_idx]
            results["confidence"] = float(predictions[max_idx])
            
            return results
            
        except Exception as e:
            raise ECGAnalysisError(f"Results formatting failed: {e}")
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        if not self.model_loaded:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "model_path": str(Config.get_model_path()),
            "input_shape": self.session.get_inputs()[0].shape,
            "output_shape": self.session.get_outputs()[0].shape,
            "classes": self.ECG_CLASSES
        }
