<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="Content-Style-Type" content="text/css">
  <title></title>
  <meta name="Generator" content="Cocoa HTML Writer">
  <meta name="CocoaVersion" content="2685.6">
  <style type="text/css">
    p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica; -webkit-text-stroke: #000000}
    p.p2 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Helvetica; -webkit-text-stroke: #000000; min-height: 14.0px}
    span.s1 {font-kerning: none}
  </style>
</head>
<body>
<p class="p1"><span class="s1">from flask import Flask, request, jsonify, render_template_string</span></p>
<p class="p1"><span class="s1">from datetime import datetime, timezone, timedelta</span></p>
<p class="p1"><span class="s1">app = Flask(__name__)</span></p>
<p class="p1"><span class="s1">measurements = []</span></p>
<p class="p2"><span class="s1"></span><br></p>
<p class="p1"><span class="s1">HTML = """</span></p>
<p class="p1"><span class="s1">&lt;!DOCTYPE html&gt;</span></p>
<p class="p1"><span class="s1">&lt;html lang="en"&gt;</span></p>
<p class="p1"><span class="s1">&lt;head&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;meta charset="UTF-8"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;meta</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>name="viewport"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>content="width=device-width, initial-scale=1.0"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;title&gt;Formaldehyde Map&lt;/title&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;link</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>rel="stylesheet"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;style&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>html,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>body {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>height: 100%;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>margin: 0;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>#map {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>width: 100%;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>height: 100%;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.info {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>position: absolute;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>z-index: 1000;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>top: 15px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>left: 15px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>background: white;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>padding: 15px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>border-radius: 8px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>box-shadow:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>0 2px 10px rgba(0,0,0,0.25);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>font-family: Arial, sans-serif;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.info h2 {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>margin: 0 0 8px 0;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>font-size: 18px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.legend {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>margin-top: 10px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>font-size: 13px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.legend-item {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>margin: 4px 0;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.color {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>display: inline-block;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>width: 14px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>height: 14px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>margin-right: 5px;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>vertical-align: middle;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>border-radius: 50%;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;/style&gt;</span></p>
<p class="p1"><span class="s1">&lt;/head&gt;</span></p>
<p class="p1"><span class="s1">&lt;body&gt;</span></p>
<p class="p1"><span class="s1">&lt;div id="map"&gt;&lt;/div&gt;</span></p>
<p class="p1"><span class="s1">&lt;div class="info"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;h2&gt;Formaldehyde Map&lt;/h2&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>Measurements:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;strong id="count"&gt;0&lt;/strong&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;div class="legend"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;div class="legend-item"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;span</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>class="color"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>style="background:#2ecc71"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&gt;&lt;/span&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&amp;le; 0.035 mg/m³</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;div class="legend-item"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;span</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>class="color"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>style="background:#f1c40f"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&gt;&lt;/span&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>0.036-0.05 mg/m³</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;div class="legend-item"&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&lt;span</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>class="color"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>style="background:#e74c3c"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&gt;&lt;/span&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>&amp;gt; 0.05 mg/m³</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>&lt;/div&gt;</span></p>
<p class="p1"><span class="s1">&lt;/div&gt;</span></p>
<p class="p2"><span class="s1"></span><br></p>
<p class="p1"><span class="s1">&lt;script</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"&gt;</span></p>
<p class="p1"><span class="s1">&lt;/script&gt;</span></p>
<p class="p1"><span class="s1">&lt;script&gt;</span></p>
<p class="p1"><span class="s1">const map = L.map("map").setView(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>[48.3794, 31.1656],</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>6</span></p>
<p class="p1"><span class="s1">);</span></p>
<p class="p1"><span class="s1">L.tileLayer(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>maxZoom: 19,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>attribution:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"&amp;copy; Created by Alex. 2026. OpenStreetMap contributors"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}</span></p>
<p class="p1"><span class="s1">).addTo(map);</span></p>
<p class="p1"><span class="s1">function getColor(mgm3) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if (mgm3 &lt;= 0.035) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return "#2ecc71";</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if (mgm3 &lt;= 0.05) {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return "#f1c40f";</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>return "#e74c3c";</span></p>
<p class="p1"><span class="s1">}</span></p>
<p class="p1"><span class="s1">function escapeHtml(value)</span></p>
<p class="p1"><span class="s1">{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>return String(value)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.replaceAll("&amp;", "&amp;amp;")</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.replaceAll("&lt;", "&amp;lt;")</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.replaceAll("&gt;", "&amp;gt;")</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.replaceAll('"', "&amp;quot;")</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>.replaceAll("'", "&amp;#039;");</span></p>
<p class="p1"><span class="s1">}</span></p>
<p class="p1"><span class="s1">async function loadMeasurements()</span></p>
<p class="p1"><span class="s1">{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>try</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const response =</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>await fetch("/api/data");</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>if (!response.ok)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>throw new Error(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>"Failed to load measurements"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>const data =</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>await response.json();</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>document.getElementById("count")</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>.textContent = data.length;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>data.forEach(measurement =&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const lat =</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>Number(measurement.lat);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const lon =</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>Number(measurement.lon);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const mgm3 =</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>Number(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>measurement.formaldehyde_mg_m3</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>const marker =</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>L.circleMarker(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>[lat, lon],</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>radius: 9,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>color: "#222",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>weight: 1,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>fillColor:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                            </span>getColor(mgm3),</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>fillOpacity: 0.8</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>marker.bindPopup(`</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;b&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>${escapeHtml(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>measurement.name ||</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                        </span>"Measurement"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>)}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;/b&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;br&gt;&lt;br&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;b&gt;Formaldehyde:&lt;/b&gt;&lt;br&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>${measurement.formaldehyde_mg_m3}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>mg/m³</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;br&gt;&lt;br&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;b&gt;Coordinates:&lt;/b&gt;&lt;br&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>${lat},</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>${lon}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;br&gt;&lt;br&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>&lt;b&gt;Time:&lt;/b&gt;&lt;br&gt;</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>${escapeHtml(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>measurement.timestamp ||</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                    </span>"Unknown"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>)}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>`);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>marker.addTo(map);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>});</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>catch(error)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>{</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>console.error(error);</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}</span></p>
<p class="p1"><span class="s1">}</span></p>
<p class="p1"><span class="s1">loadMeasurements();</span></p>
<p class="p1"><span class="s1">&lt;/script&gt;</span></p>
<p class="p1"><span class="s1">&lt;/body&gt;</span></p>
<p class="p1"><span class="s1">&lt;/html&gt;</span></p>
<p class="p1"><span class="s1">"""</span></p>
<p class="p1"><span class="s1">@app.route("/")</span></p>
<p class="p1"><span class="s1">def index():</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>return render_template_string(HTML)</span></p>
<p class="p1"><span class="s1">@app.route("/api/data", methods=["GET"])</span></p>
<p class="p1"><span class="s1">def get_data():</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>return jsonify(measurements)</span></p>
<p class="p1"><span class="s1">@app.route("/api/data", methods=["POST"])</span></p>
<p class="p1"><span class="s1">def add_data():</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>data = request.get_json(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>silent=True</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if data is None:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"success": False,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"error": "JSON body required"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}), 400</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>required = [</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"lat",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"lon",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"formaldehyde_mg_m3",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>]</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>missing = []</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>for field in required:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>if field not in data:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>missing.append(field)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if missing:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"success": False,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"error": "Missing fields",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"fields": missing</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}), 400</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>try:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>lat = float(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>data["lat"]</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>lon = float(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>data["lon"]</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>mgm3 = float(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>data["formaldehyde_mg_m3"]</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>except (ValueError, TypeError):</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"success": False,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"error": "Invalid numeric value"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}), 400</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if not -90 &lt;= lat &lt;= 90:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"success": False,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"error": "Invalid latitude"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}), 400</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if not -180 &lt;= lon &lt;= 180:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"success": False,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"error": "Invalid longitude"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}), 400</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if mgm3 &lt; 0:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"success": False,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"error": "Negative mg/m3"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>}), 400</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>name = data.get(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"name",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"Arduino UNO HCHO"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>timestamp = data.get("time") or data.get("timestamp")</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>if not timestamp:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>timestamp = (</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>datetime.now(timezone.utc) + timedelta(hours=3)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>).isoformat()</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>else:</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>pass</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>measurement = {</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"id":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>len(measurements) + 1,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"name":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>str(name),</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"lat":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>lat,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"lon":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>lon,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"formaldehyde_mg_m3":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>mgm3,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"timestamp":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>timestamp</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>measurements.append(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>measurement</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>)</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"success": True,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"message":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>"Measurement received",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"id":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>measurement["id"],</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"lat":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>measurement["lat"],</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"lon":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>measurement["lon"],</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"formaldehyde_mg_m3":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>measurement[</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">                </span>"formaldehyde_mg_m3"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">            </span>],</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}), 201</span></p>
<p class="p2"><span class="s1"></span><br></p>
<p class="p1"><span class="s1">@app.route("/api/status, methods=["GET"])</span></p>
<p class="p1"><span class="s1">def status():</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>return jsonify({</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"success": True,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>"server": "online"</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>}), 200</span></p>
<p class="p1"><span class="s1">if __name__ == "__main__":</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>app.run(</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>host="0.0.0.0",</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>port=5000,</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">        </span>debug=True</span></p>
<p class="p1"><span class="s1"><span class="Apple-converted-space">    </span>)</span></p>
</body>
</html>
