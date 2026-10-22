from flask import Flask, request, jsonify, render_template_string
from datetime import datetime, timezone, timedelta
app = Flask(__name__)
measurements = []

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >
    <title>Formaldehyde Map</title>
    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    >
    <style>
        html,
        body {
            height: 100%;
            margin: 0;
        }
        #map {
            width: 100%;
            height: 100%;
        }
        .info {
            position: absolute;
            z-index: 1000;
            top: 15px;
            left: 15px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow:
                0 2px 10px rgba(0,0,0,0.25);
            font-family: Arial, sans-serif;
        }
        .info h2 {
            margin: 0 0 8px 0;
            font-size: 18px;
        }
        .legend {
            margin-top: 10px;
            font-size: 13px;
        }
        .legend-item {
            margin: 4px 0;
        }
        .color {
            display: inline-block;
            width: 14px;
            height: 14px;
            margin-right: 5px;
            vertical-align: middle;
            border-radius: 50%;
        }
    </style>
</head>
<body>
<div id="map"></div>
<div class="info">
    <h2>Formaldehyde Map</h2>
    <div>
        Measurements:
        <strong id="count">0</strong>
    </div>
    <div class="legend">
        <div class="legend-item">
            <span
                class="color"
                style="background:#2ecc71"
            ></span>
            &le; 0.035 mg/m³
        </div>
        <div class="legend-item">
            <span
                class="color"
                style="background:#f1c40f"
            ></span>
            0.036-0.05 mg/m³
        </div>
        <div class="legend-item">
            <span
                class="color"
                style="background:#e74c3c"
            ></span>
            &gt; 0.05 mg/m³
        </div>
    </div>
</div>

<script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
</script>
<script>
const map = L.map("map").setView(
    [48.3794, 31.1656],
    6
);
L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution:
            "&copy; Created by Alex. 2026. OpenStreetMap contributors"
    }
).addTo(map);
function getColor(mgm3) {
    if (mgm3 <= 0.035) {
        return "#2ecc71";
    }
    if (mgm3 <= 0.05) {
        return "#f1c40f";
    }
    return "#e74c3c";
}
function escapeHtml(value)
{
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}
async function loadMeasurements()
{
    try
    {
        const response =
            await fetch("/api/data");
        if (!response.ok)
        {
            throw new Error(
                "Failed to load measurements"
            );
        }
        const data =
            await response.json();
        document.getElementById("count")
            .textContent = data.length;
        data.forEach(measurement =>
        {
            const lat =
                Number(measurement.lat);
            const lon =
                Number(measurement.lon);
            const mgm3 =
                Number(
                    measurement.formaldehyde_mg_m3
                );
            const marker =
                L.circleMarker(
                    [lat, lon],
                    {
                        radius: 9,
                        color: "#222",
                        weight: 1,
                        fillColor:
                            getColor(mgm3),
                        fillOpacity: 0.8
                    }
                );
            marker.bindPopup(`
                <b>
                    ${escapeHtml(
                        measurement.name ||
                        "Measurement"
                    )}
                </b>
                <br><br>
                <b>Formaldehyde:</b><br>
                ${measurement.formaldehyde_mg_m3}
                mg/m³
                <br><br>
                <b>Coordinates:</b><br>
                ${lat},
                ${lon}
                <br><br>
                <b>Time:</b><br>
                ${escapeHtml(
                    measurement.timestamp ||
                    "Unknown"
                )}
            `);
            marker.addTo(map);
        });
    }
    catch(error)
    {
        console.error(error);
    }
}
loadMeasurements();
</script>
</body>
</html>
"""
@app.route("/")
def index():
    return render_template_string(HTML)
@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(measurements)
@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.get_json(
        silent=True
    )
    if data is None:
        return jsonify({
            "success": False,
            "error": "JSON body required"
        }), 400
    required = [
        "lat",
        "lon",
        "formaldehyde_mg_m3",
    ]
    missing = []
    for field in required:
        if field not in data:
            missing.append(field)
    if missing:
        return jsonify({
            "success": False,
            "error": "Missing fields",
            "fields": missing
        }), 400
    try:
        lat = float(
            data["lat"]
        )
        lon = float(
            data["lon"]
        )
        mgm3 = float(
            data["formaldehyde_mg_m3"]
        )
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Invalid numeric value"
        }), 400
    if not -90 <= lat <= 90:
        return jsonify({
            "success": False,
            "error": "Invalid latitude"
        }), 400
    if not -180 <= lon <= 180:
        return jsonify({
            "success": False,
            "error": "Invalid longitude"
        }), 400
    if mgm3 < 0:
        return jsonify({
            "success": False,
            "error": "Negative mg/m3"
        }), 400
    name = data.get(
        "name",
        "Arduino UNO HCHO"
    )
    timestamp = data.get("time") or data.get("timestamp")
    if not timestamp:
        timestamp = (
            datetime.now(timezone.utc) + timedelta(hours=3)
        ).isoformat()
    else:
        pass
    measurement = {
        "id":
            len(measurements) + 1,
        "name":
            str(name),
        "lat":
            lat,
        "lon":
            lon,
        "formaldehyde_mg_m3":
            mgm3,
        "timestamp":
            timestamp
    }
    measurements.append(
        measurement
    )
    return jsonify({
        "success": True,
        "message":
            "Measurement received",
        "id":
            measurement["id"],
        "lat":
            measurement["lat"],
        "lon":
            measurement["lon"],
        "formaldehyde_mg_m3":
            measurement[
                "formaldehyde_mg_m3"
            ],
    }), 201

@app.route("/api/status, methods=["GET"])
def status():
    return jsonify({
        "success": True,
        "server": "online"
    }), 200
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
