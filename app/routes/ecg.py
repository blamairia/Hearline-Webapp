# app/routes/ecg.py

import os
from flask import Blueprint, render_template, jsonify, current_app
from flask_login import login_required
from app.decorators.auth import any_role_required
from app.models.visit import Visit
from app.services.visit_service import VisitService

ecg_bp = Blueprint('ecg', __name__)


@ecg_bp.route("/history")
@login_required
@any_role_required
def ecg_history():
    """Display comprehensive ECG history table with filtering and sorting capabilities."""
    # Get all visits that have ECG data
    visits_with_ecg = Visit.query.filter(
        Visit.ecg_prediction.isnot(None)
    ).order_by(Visit.visit_date.desc()).all()
    
    return render_template("ecg_history.html", visits=visits_with_ecg)


@ecg_bp.route("/api/details/<int:visit_id>")
@login_required
@any_role_required
def api_ecg_details(visit_id):
    """API endpoint to get detailed ECG analysis for a specific visit."""
    try:
        visit_service = VisitService()
        visit = visit_service.get_visit_by_id(visit_id)
        
        if not visit.has_ecg_prediction():
            return jsonify({"success": False, "error": "No ECG prediction data available for this visit"}), 404
        
        primary_diagnosis = visit.get_primary_diagnosis()
        
        analysis = {
            "probabilities": visit.ecg_prediction,
            "class_names": visit_service.ecg_service.class_names,
            "primary_diagnosis": primary_diagnosis,
            "summary": visit_service.ecg_service.get_analysis_summary(visit.ecg_prediction)
        }
        
        return jsonify({"success": True, "analysis": analysis})
        
    except Exception as e:
        current_app.logger.error(f"Error in /ecg/api/details/{visit_id}: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500


@ecg_bp.route("/api/waveform/<int:visit_id>")
@login_required
@any_role_required
def get_visit_ecg_waveform(visit_id):
    """Get ECG waveform data for visualization."""
    try:
        visit_service = VisitService()
        ecg_data = visit_service.get_visit_ecg_waveform(visit_id)
        
        return jsonify({
            "success": True,
            "ecg_data": ecg_data
        })
        
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404
    except Exception as e:
        current_app.logger.error(f"Error in /ecg/api/waveform/{visit_id}: {e}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to load ECG waveform: {str(e)}"}), 500
