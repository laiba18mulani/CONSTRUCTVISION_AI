# ============================================================
# CONSTRUCTVISION AI
# SHARED IoT SENSOR DATA
# ============================================================

from datetime import datetime, timedelta
import numpy as np


def get_sensor_data(building_w=12.0, building_d=16.0, wall_h=3.2):
    """
    Central sensor registry.

    3D Building page and IoT Monitoring page
    both use this same sensor data.
    """

    sensors = [
        {
            "id": "SNS-FND-01",
            "component": "Foundation Footing",
            "type": "Settlement",
            "value": 0.04,
            "unit": "deg",
            "status": "Normal",
            "pos": [
                -building_w / 2 + 0.5,
                0.2,
                -building_d / 2 + 0.5
            ],
            "location": "Foundation - Grid A1",
            "description": "Foundation settlement monitoring sensor"
        },

        {
            "id": "SNS-COL-03",
            "component": "Ground Columns",
            "type": "Strain",
            "value": 920,
            "unit": "µε",
            "status": "Warning",
            "pos": [
                building_w / 2 - 0.5,
                2.0,
                building_d / 2 - 0.5
            ],
            "location": "Ground Column - Grid C3",
            "description": "Structural column strain monitoring sensor"
        },

        {
            "id": "SNS-BM-04",
            "component": "Primary Beams",
            "type": "Vibration",
            "value": 4.1,
            "unit": "m/s²",
            "status": "Critical",
            "pos": [
                0.0,
                wall_h + 0.9,
                -building_d / 2
            ],
            "location": "Primary Beam - Grid B2",
            "description": "Primary beam vibration monitoring sensor"
        }
    ]

    return sensors


def get_sensor_status_color(status):
    if status == "Normal":
        return "#22C55E"

    if status == "Warning":
        return "#EAB308"

    if status == "Critical":
        return "#EF4444"

    return "#64748B"


def get_sensor_by_id(sensor_id, sensors=None):

    if sensors is None:
        sensors = get_sensor_data()

    for sensor in sensors:
        if sensor["id"] == sensor_id:
            return sensor

    return None


def get_component_sensors(component, sensors=None):

    if sensors is None:
        sensors = get_sensor_data()

    return [
        sensor
        for sensor in sensors
        if sensor["component"] == component
    ]


def create_sensor_history(sensor):

    sensor_id = sensor["id"]
    base_value = sensor["value"]
    status = sensor["status"]

    np.random.seed(hash(sensor_id) % (2**32))

    time_now = datetime.now()

    times = [
        (
            time_now - timedelta(seconds=i * 2)
        ).strftime("%H:%M:%S")
        for i in range(30, 0, -1)
    ]

    scale = base_value * (
        0.05
        if status == "Normal"
        else
        0.15
        if status == "Warning"
        else
        0.30
    )

    readings = np.random.normal(
        loc=base_value,
        scale=scale,
        size=30
    ).tolist()

    return {
        "Time": times,
        "Reading": readings
    }
