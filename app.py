from flask import Flask, render_template, request, send_file
import os
import uuid
import pdfplumber
import openpyxl
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit

# Crear directorio de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return {
            'filename': filename,
            'message': 'File uploaded successfully'
        }
    
    return {'error': 'Invalid file type'}, 400

@app.route('/extract', methods=['POST'])
def extract_data():
    filename = request.form.get('filename')
    if not filename:
        return {'error': 'Filename is required'}, 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        # Extraer datos del PDF (simulación)
        # En una aplicación real, usarías pdfplumber o similar para extraer datos reales
        extracted_data = [
            {
                'nombre': 'Empresa Demo SA de CV',
                'rfc': 'EDM201505HJ7',
                'serieYFolio': 'A-12345',
                'folioFiscal': 'FOLIO-FISCAL-UUID-12345-67890',
                'cantidad': '10',
                'unidad': 'PZA',
                'claveSAT': '43211500',
                'concepto': 'Computadoras portátiles',
                'precioUnitario': '15000.00',
                'importe': '150000.00'
            },
            {
                'nombre': 'Empresa Demo SA de CV',
                'rfc': 'EDM201505HJ7',
                'serieYFolio': 'A-12345',
                'folioFiscal': 'FOLIO-FISCAL-UUID-12345-67890',
                'cantidad': '5',
                'unidad': 'PZA',
                'claveSAT': '43211900',
                'concepto': 'Monitores de computadora',
                'precioUnitario': '3500.00',
                'importe': '17500.00'
            }
        ]
        
        return {
            'data': extracted_data,
            'message': 'Data extracted successfully'
        }
    
    except Exception as e:
        return {'error': f'Error processing PDF: {str(e)}'}, 500

@app.route('/export', methods=['POST'])
def export_to_excel():
    data = request.get_json()
    if not data or 'data' not in data:
        return {'error': 'No data provided'}, 400
    
    try:
        # Crear un libro de Excel en memoria
        output = BytesIO()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
        # Encabezados
        headers = [
            'Nombre', 'RFC', 'Serie y Folio', 'Folio Fiscal', 
            'Cantidad', 'Unidad', 'Clave SAT', 'Concepto', 
            'Precio Unitario', 'Importe'
        ]
        sheet.append(headers)
        
        # Datos
        for row in data['data']:
            sheet.append([
                row.get('nombre', ''),
                row.get('rfc', ''),
                row.get('serieYFolio', ''),
                row.get('folioFiscal', ''),
                row.get('cantidad', ''),
                row.get('unidad', ''),
                row.get('claveSAT', ''),
                row.get('concepto', ''),
                row.get('precioUnitario', ''),
                row.get('importe', '')
            ])
        
        workbook.save(output)
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name='datos_extraidos.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        return {'error': f'Error generating Excel: {str(e)}'}, 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'pdf'

if __name__ == '__main__':
    app.run(debug=True)
