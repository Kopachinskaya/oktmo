from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from flask_cors import CORS
import os
import uuid
import openpyxl
from comparison import get_data
from openpyxl import Workbook
import io

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])

def upload_file():

    global last_dict1

    file = request.files.get('file')
    if file and file.filename.endswith('.xlsx'):
        filename = f"{uuid.uuid4()}.xlsx"
        filepath = os.path.join(UPLOAD_FOLDER, 'поручения.xlsx')
        file.save(filepath)

        # Simulated processing - return two dictionarier
        data = get_data(r'/home/lira/Документы/OKTMO/uploads/поручения.xlsx')
        last_dict1 = data[0]

        return jsonify({'dict1': data[0], 'dict2': data[1]})
    return jsonify({'error': 'Invalid file'}), 400


@app.route('/download-dict1')
def download_dict1():
    global last_dict1

    if not last_dict1:
        return 'No data to export', 400

    wb = Workbook()
    ws = wb.active
    ws.title = "Поручения субъектам"
    ws.append(["Key", "Value"])

    for key, value in last_dict1.items():
        ws.append([key, value])

    # Save to memory
    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return send_file(file_stream, as_attachment=True,
                     download_name="Поручения субъектам.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == '__main__':
    app.run(debug=True)