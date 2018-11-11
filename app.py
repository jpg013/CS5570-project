#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request, send_from_directory, jsonify
from data_generation import DataGeneration
from history import History
from history_query_builder import HistoryQueryBuilder
from recovery_engine import RecoveryEngine
from build_graphs import build_graphs
import os
import json

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

app = Flask(__name__, static_folder='web-ui/build')
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Serve index.html for root
#----------------------------------------------------------------------------#

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("web-ui/build/" + path):
        return send_from_directory('web-ui/build', path)
    else:
        return send_from_directory('web-ui/build', 'index.html')

@app.route('/health')
def health():
    return "Healthy!", 200

@app.route('/generate_history')
def generate_history():
    data_generation = DataGeneration()
    history = History(data_generation.generate_transactions())
    history.interleave_transaction_schedule()
    return jsonify(history.serialize()), 200

@app.route('/build_history', methods=['POST'])
def build_history():
    try:
        history = HistoryQueryBuilder(request.json['input']).process()
        return jsonify(history.serialize()), 200
    except:
        resp = {}
        resp['message'] = 'error'
        return jsonify(resp), 500

@app.route('/recovery_report', methods=['POST'])
def get_recovery():
    try:
        history = HistoryQueryBuilder(request.json['input']).process()
        recovery_engine = RecoveryEngine(history)
        report = recovery_engine.get_report()
        return jsonify(report.serialize()), 200
    except:
        resp = {}
        resp['message'] = 'error'
        return jsonify(resp), 500

@app.route('/generate_graphs', methods=['GET'])
def get_graphs():
    try:
        results = build_graphs()
        return jsonify(results), 200
    except:
        resp = {}
        resp['message'] = 'error'
        return jsonify(resp), 500
        

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True, use_reloader=True)

