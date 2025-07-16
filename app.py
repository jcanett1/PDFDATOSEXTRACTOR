import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO
import base64

# Configuración de la página
st.set_page_config(
    page_title="PDF a Excel - Extractor de Datos",
    page_icon="📄",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .stFileUploader > div > div > div > button {
        background-color: #4F46E5;
        color: white;
    }
    .stButton > button {
        background-color: #4F46E5;
        color: white;
        width: 100%;
    }
    .stDownloadButton > button {
        background-color: #10B981;
        color: white;
        width: 100%;
    }
    .dataframe {
        width: 100%;
    }
    .notification {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success {
        background-color: #D1FAE5;
        color: #065F46;
        border-left: 4px solid #10B981;
    }
    .error {
        background-color: #FEE2E2;
        color: #B91C1C;
        border-left: 4px solid #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# Función para mostrar notificaciones
def show_notification(message, type="success"):
    st.markdown(f"""
    <div class="notification {type}">
        <i class="fas fa-{'check-circle' if type == 'success' else 'exclamation-circle'}"></i> {message}
    </div>
    """, unsafe_allow_html=True)

# Función para extraer datos del PDF (simulada)
def extract_data_from_pdf(pdf_file):
    # Esta es una función simulada - en una aplicación real usarías pdfplumber
    # para extraer datos reales del PDF
    
    sample_data = [
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
    
    return sample_data

# Función para crear un archivo Excel
def create_excel_file(data):
    output = BytesIO()
    df = pd.DataFrame(data)
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Interfaz de la aplicación
st.title("📄 PDF a Excel - Extractor de Datos")

# Sección de carga de archivos
with st.expander("📤 Subir PDF para extracción", expanded=True):
    uploaded_file = st.file_uploader(
        "Arrastra y suelta tu archivo PDF aquí o haz clic para seleccionar",
        type=["pdf"],
        help="Tamaño máximo: 50MB"
    )

# Procesamiento del archivo
if uploaded_file is not None:
    st.success(f"Archivo cargado: {uploaded_file.name}")
    
    # Mostrar PDF (solo visualización)
    with st.expander("👁️ Vista previa del PDF", expanded=False):
        # Convertir a base64 para mostrar en iframe
        base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    # Botón para extraer datos
    if st.button("🔍 Extraer Datos", help="Extraer datos del PDF"):
        with st.spinner("Extrayendo datos del PDF..."):
            try:
                # Extraer datos (aquí iría tu lógica real de extracción)
                extracted_data = extract_data_from_pdf(uploaded_file)
                
                # Mostrar datos en un DataFrame editable
                st.session_state.extracted_data = extracted_data
                st.success("Datos extraídos correctamente")
                
            except Exception as e:
                st.error(f"Error al extraer datos: {str(e)}")

# Mostrar datos extraídos si existen
if 'extracted_data' in st.session_state:
    st.subheader("📊 Datos Extraídos")
    
    # Crear DataFrame editable
    df = pd.DataFrame(st.session_state.extracted_data)
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    # Actualizar datos editados
    st.session_state.extracted_data = edited_df.to_dict('records')
    
    # Botón para exportar a Excel
    excel_data = create_excel_file(st.session_state.extracted_data)
    st.download_button(
        label="💾 Exportar a Excel",
        data=excel_data,
        file_name="datos_extraidos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Nota al pie
st.caption("Los datos extraídos se mantienen durante la sesión actual.")
