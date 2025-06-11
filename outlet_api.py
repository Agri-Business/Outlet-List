
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
data = pd.read_csv("Beat and Outlet.csv")
data.columns = data.columns.str.strip()

@app.route('/get_outlets', methods=['GET'])
def get_outlets():
    contact = request.args.get('contact')
    beat = request.args.get('beat')

    if not contact or not beat:
        return jsonify({'error': 'Missing required parameters: contact and beat'}), 400

    data['contact'] = data['contact'].astype(str).str.strip()
    data['Beat Name'] = data['Beat Name'].astype(str).str.strip()

    filtered = data[
        (data['contact'] == contact.strip()) & 
        (data['Beat Name'] == beat.strip())
    ]

    if filtered.empty:
        return jsonify({'error': 'No matching outlets found'}), 404

    outlet_list = filtered['Outlet Name'].dropna().unique().tolist()
    return jsonify({'Outlets': outlet_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
