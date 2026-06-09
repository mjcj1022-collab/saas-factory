"""
Fleet Maintenance Optimizer — predictive maintenance engine.
"""
from __future__ import annotations
import json
from typing import List, Dict


# OBD-II / telematics fault code severity mapping
CRITICAL_CODES = {
    "P0300": "Random/Multiple Cylinder Misfire",
    "P0171": "System Too Lean Bank 1",
    "P0420": "Catalyst System Efficiency Below Threshold",
    "P0715": "Input/Turbine Speed Sensor Circuit",
    "P0562": "System Voltage Low",
    "U0100": "Lost Communication with ECM/PCM",
}

HIGH_CODES = {
    "P0101": "Mass Air Flow Sensor Circuit",
    "P0113": "Intake Air Temperature Sensor High",
    "P0217": "Engine Coolant Over Temperature",
    "P0523": "Engine Oil Pressure Sensor High",
}


class PredictiveMaintenanceEngine:
    """
    Analyzes vehicle telemetry history to predict failures.
    Uses rule-based + AI hybrid approach.
    """

    def analyze(self, vehicle_id: str) -> List[Dict]:
        from apps.fleet.models import Vehicle, TelemetryEvent

        vehicle = Vehicle.objects.get(id=vehicle_id)
        recent_events = TelemetryEvent.objects.filter(
            vehicle=vehicle
        ).order_by("-timestamp")[:200]

        predictions = []
        code_counts: Dict[str, int] = {}
        for event in recent_events:
            code_counts[event.code] = code_counts.get(event.code, 0) + 1

        for code, count in code_counts.items():
            if code in CRITICAL_CODES:
                predictions.append({
                    "component": CRITICAL_CODES[code],
                    "fault_code": code,
                    "confidence": min(0.6 + count * 0.1, 0.99),
                    "predicted_days": max(1, 14 - count * 2),
                    "severity": "critical",
                })
            elif code in HIGH_CODES:
                predictions.append({
                    "component": HIGH_CODES[code],
                    "fault_code": code,
                    "confidence": min(0.5 + count * 0.08, 0.95),
                    "predicted_days": max(3, 21 - count * 2),
                    "severity": "high",
                })

        # Mileage-based predictions
        mileage = vehicle.odometer
        if mileage % 5000 < 500:
            predictions.append({
                "component": "Engine Oil & Filter",
                "fault_code": "SCHEDULED",
                "confidence": 0.99,
                "predicted_days": 7,
                "severity": "medium",
            })
        if mileage % 30000 < 1000:
            predictions.append({
                "component": "Transmission Fluid",
                "fault_code": "SCHEDULED",
                "confidence": 0.95,
                "predicted_days": 14,
                "severity": "medium",
            })

        return predictions

    def save_predictions(self, vehicle_id: str):
        from apps.fleet.models import MaintenancePrediction
        predictions = self.analyze(vehicle_id)
        saved = []
        for p in predictions:
            obj = MaintenancePrediction.objects.create(
                vehicle_id=vehicle_id,
                predicted_failure=p["component"],
                component=p.get("fault_code", ""),
                confidence=p["confidence"],
                predicted_days=p["predicted_days"],
            )
            saved.append(obj)
        return saved


class InventoryAutomation:
    """
    When a prediction is created, check inventory and trigger reorder.
    """

    PARTS_MAP = {
        "Engine Oil & Filter": ["OIL-5W30-5QT", "FILTER-OIL-STD"],
        "Transmission Fluid": ["FLUID-ATF-1QT"],
        "Catalyst System Efficiency Below Threshold": ["SENSOR-O2-UNIV"],
        "Mass Air Flow Sensor Circuit": ["SENSOR-MAF-UNIV"],
    }

    def check_and_reorder(self, prediction) -> List[str]:
        from apps.fleet.models import InventoryPart
        skus = self.PARTS_MAP.get(prediction.predicted_failure, [])
        reorder_triggered = []
        for sku in skus:
            try:
                part = InventoryPart.objects.get(
                    organization_id=prediction.vehicle.organization_id, sku=sku
                )
                if part.quantity <= part.reorder_point:
                    reorder_triggered.append(sku)
                    # In production: trigger PO via integrations hub
            except InventoryPart.DoesNotExist:
                reorder_triggered.append(sku)
        return reorder_triggered
