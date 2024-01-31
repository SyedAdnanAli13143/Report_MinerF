from flask import Flask, request, Response, jsonify
import re
from collections import OrderedDict
import json

app = Flask(__name__)

def sanitize_column(column):
   
    forbidden_chars = {'.': '_', '&': 'and', ' ': '_'}
    for char, replacement in forbidden_chars.items():
        column = column.replace(char, replacement)

    
    column = re.sub(r'\W+', '', column)

    return column

def is_valid_row(row, columns):
    return all(sanitize_column(column) in row and row[sanitize_column(column)] is not None for column in columns)

@app.route('/extract_data', methods=['POST'])
def extract_data():
    try:
        data_text = request.json.get('data_text', '')
        lines = [line.strip() for line in data_text.strip().split('\n')]
        lines = [line for line in lines if line]

        columns = [sanitize_column(col) for col in re.split(r'\s{2,}', lines[0].strip())]

        data = []
        for line in lines[1:]:
            values = re.split(r'\s{2,}', line.strip())
            row = OrderedDict(zip(columns, values))

            if is_valid_row(row, columns):
                data.append(row)

        response = {"structuredData": data}
        json_response = json.dumps(response, default=str)

        return Response(json_response, content_type='application/json')

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
