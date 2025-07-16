<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PDF a Excel - Extractor de Datos</title>
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  
  <!-- Toastify JS for notifications -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">
  <script src="https://cdn.jsdelivr.net/npm/toastify-js"></script>
  
  <style>
    .drag-area {
      border: 2px dashed #4F46E5;
      transition: all 0.3s ease;
    }
    
    .drag-area.active {
      border: 2px solid #4F46E5;
      background-color: rgba(79, 70, 229, 0.1);
    }
    
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.8);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      flex-direction: column;
    }
    
    .spinner {
      border: 4px solid rgba(0, 0, 0, 0.1);
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border-left-color: #4F46E5;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }

    .data-table-container {
      max-height: 400px;
      overflow-y: auto;
    }
  </style>
</head>
<body class="bg-gray-50 min-h-screen">
  <header class="bg-indigo-600 text-white p-4 shadow-md">
    <div class="container mx-auto flex justify-between items-center">
      <h1 class="text-2xl font-bold">PDF a Excel - Extractor de Datos</h1>
      <div>
        <a href="javascript:void(0)" class="text-white hover:text-indigo-200 text-sm">
          <i class="fas fa-question-circle mr-1"></i> Ayuda
        </a>
      </div>
    </div>
  </header>
  
  <main class="container mx-auto p-4 mt-6">
    <div id="upload-section" class="mb-8">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold mb-4">Subir PDF para extracción</h2>
        
        <div id="drag-area" class="drag-area p-8 rounded-lg cursor-pointer flex flex-col items-center justify-center">
          <i class="fas fa-file-pdf text-5xl text-indigo-600 mb-4"></i>
          <p class="text-gray-700 text-center mb-2">Arrastra y suelta tu archivo PDF aquí</p>
          <p class="text-gray-500 text-sm mb-4">O</p>
          <label for="file-input" class="bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded cursor-pointer transition">
            Seleccionar archivo
          </label>
          <input type="file" id="file-input" accept=".pdf" class="hidden">
          <p class="text-gray-500 text-sm mt-4">Tamaño máximo: 50MB</p>
        </div>
      </div>
    </div>
    
    <div id="document-section" class="hidden mb-8">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Documento PDF</h2>
          <div>
            <span id="file-name" class="text-sm text-gray-600 mr-2">nombre-del-archivo.pdf</span>
            <button id="change-file" class="text-indigo-600 hover:text-indigo-800 text-sm">
              <i class="fas fa-exchange-alt"></i> Cambiar
            </button>
          </div>
        </div>
        
        <div class="flex flex-col gap-6">
          <div class="w-full">
            <iframe id="pdf-preview" class="w-full h-96 border rounded-lg" style="display: none;"></iframe>
            <div id="no-preview" class="text-center py-8 text-gray-500">
              <i class="fas fa-file-pdf text-4xl mb-2"></i>
              <p>Vista previa no disponible</p>
            </div>
          </div>
          
          <div class="w-full">
            <button id="extract-data" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 px-4 rounded-lg mb-4 flex items-center justify-center transition">
              <i class="fas fa-magic mr-2"></i> Extraer Datos
            </button>
            
            <div id="extraction-info" class="hidden">
              <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <i class="fas fa-info-circle text-blue-400"></i>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm text-blue-700">
                      Los datos han sido extraídos. Revisa y edita cualquier información incorrecta en la tabla a continuación.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div id="data-section" class="hidden mb-20">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold mb-4">Datos Extraídos</h2>
        
        <div class="data-table-container">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">RFC</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Serie y Folio</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Folio Fiscal</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidad</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Clave SAT</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Concepto</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Precio Unitario</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Importe</th>
              </tr>
            </thead>
            <tbody id="data-table-body" class="bg-white divide-y divide-gray-200">
              <!-- Data will be inserted here -->
            </tbody>
          </table>
        </div>
        
        <div id="no-data-message" class="py-8 text-center">
          <p class="text-gray-500">No hay datos disponibles. Primero extrae la información del PDF.</p>
        </div>
      </div>
    </div>
  </main>
  
  <footer class="fixed bottom-0 left-0 w-full bg-white border-t shadow-md p-4">
    <div class="container mx-auto flex justify-between items-center">
      <div>
        <p class="text-sm text-gray-600">Los datos extraídos son procesados en el servidor.</p>
      </div>
      <button id="export-excel" class="bg-green-600 hover:bg-green-700 text-white py-2 px-6 rounded-lg flex items-center transition disabled:opacity-50 disabled:cursor-not-allowed" disabled>
        <i class="fas fa-file-excel mr-2"></i> Exportar a Excel
      </button>
    </div>
  </footer>
  
  <div id="loading-overlay" class="loading-overlay hidden">
    <div class="spinner mb-4"></div>
    <p id="loading-text" class="text-gray-700">Procesando documento...</p>
  </div>

  <script>
    // DOM elements
    const dragArea = document.getElementById('drag-area');
    const fileInput = document.getElementById('file-input');
    const uploadSection = document.getElementById('upload-section');
    const documentSection = document.getElementById('document-section');
    const dataSection = document.getElementById('data-section');
    const fileName = document.getElementById('file-name');
    const changeFileBtn = document.getElementById('change-file');
    const extractDataBtn = document.getElementById('extract-data');
    const exportExcelBtn = document.getElementById('export-excel');
    const dataTableBody = document.getElementById('data-table-body');
    const noDataMessage = document.getElementById('no-data-message');
    const extractionInfo = document.getElementById('extraction-info');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    const pdfPreview = document.getElementById('pdf-preview');
    const noPreview = document.getElementById('no-preview');
    
    // State variables
    let currentPdfFile = null;
    let extractedData = null;
    
    // Event Listeners
    dragArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      dragArea.classList.add('active');
    });
    
    dragArea.addEventListener('dragleave', () => {
      dragArea.classList.remove('active');
    });
    
    dragArea.addEventListener('drop', (e) => {
      e.preventDefault();
      dragArea.classList.remove('active');
      
      const file = e.dataTransfer.files[0];
      handleFileUpload(file);
    });
    
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        handleFileUpload(file);
      }
    });
    
    dragArea.addEventListener('click', () => {
      fileInput.click();
    });
    
    changeFileBtn.addEventListener('click', () => {
      resetApp();
      uploadSection.classList.remove('hidden');
      documentSection.classList.add('hidden');
      dataSection.classList.add('hidden');
    });
    
    extractDataBtn.addEventListener('click', async () => {
      if (!currentPdfFile) return;
      
      showLoading('Extrayendo datos del PDF...');
      
      try {
        const formData = new FormData();
        formData.append('filename', currentPdfFile.name);
        
        const response = await fetch('/extract', {
          method: 'POST',
          body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
          extractedData = result.data;
          populateDataTable(extractedData);
          dataSection.classList.remove('hidden');
          extractionInfo.classList.remove('hidden');
          exportExcelBtn.disabled = false;
          
          showNotification('Datos extraídos correctamente', 'success');
        } else {
          throw new Error(result.error || 'Error al extraer datos');
        }
      } catch (error) {
        console.error('Error extracting data:', error);
        showNotification(error.message, 'error');
      } finally {
        hideLoading();
      }
    });
    
    exportExcelBtn.addEventListener('click', async () => {
      if (!extractedData || extractedData.length === 0) return;
      
      showLoading('Generando archivo Excel...');
      
      try {
        const response = await fetch('/export', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ data: extractedData })
        });
        
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'datos_extraidos.xlsx';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          a.remove();
          
          showNotification('Excel generado y descargado correctamente', 'success');
        } else {
          const error = await response.json();
          throw new Error(error.error || 'Error al generar Excel');
        }
      } catch (error) {
        console.error('Error exporting to Excel:', error);
        showNotification(error.message, 'error');
      } finally {
        hideLoading();
      }
    });
    
    // Functions
    function handleFileUpload(file) {
      if (!file) return;
      
      // Check if the file is a PDF
      if (!file.type.match('application/pdf')) {
        showNotification('Por favor, sube solo archivos PDF', 'error');
        return;
      }
      
      // Check file size (max 50MB)
      if (file.size > 50 * 1024 * 1024) {
        showNotification('El archivo excede el tamaño máximo de 50MB', 'error');
        return;
      }
      
      currentPdfFile = file;
      fileName.textContent = file.name;
      
      // Show loading
      showLoading('Subiendo PDF...');
      
      // Upload the file to the server
      const formData = new FormData();
      formData.append('file', file);
      
      fetch('/upload', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          throw new Error(data.error);
        }
        
        // Try to show preview (not all browsers support PDF preview)
        try {
          const fileUrl = URL.createObjectURL(file);
          pdfPreview.src = fileUrl;
          pdfPreview.style.display = 'block';
          noPreview.style.display = 'none';
        } catch (e) {
          pdfPreview.style.display = 'none';
          noPreview.style.display = 'block';
        }
        
        // Update UI
        uploadSection.classList.add('hidden');
        documentSection.classList.remove('hidden');
      })
      .catch(error => {
        console.error('Error uploading file:', error);
        showNotification(error.message, 'error');
        currentPdfFile = null;
      })
      .finally(() => {
        hideLoading();
      });
    }
    
    function populateDataTable(data) {
      // Clear existing data
      dataTableBody.innerHTML = '';
      
      if (!data || data.length === 0) {
        noDataMessage.classList.remove('hidden');
        return;
      }
      
      noDataMessage.classList.add('hidden');
      
      // Add data rows
      data.forEach((item, index) => {
        const row = document.createElement('tr');
        
        // Create editable cells for each field
        const fields = [
          'nombre', 'rfc', 'serieYFolio', 'folioFiscal', 
          'cantidad', 'unidad', 'claveSAT', 'concepto', 
          'precioUnitario', 'importe'
        ];
        
        fields.forEach(field => {
          const cell = document.createElement('td');
          cell.className = 'px-6 py-4 whitespace-nowrap';
          
          const div = document.createElement('div');
          div.className = 'editable-cell text-sm text-gray-900 p-1 rounded';
          div.setAttribute('contenteditable', 'true');
          div.setAttribute('data-index', index);
          div.setAttribute('data-field', field);
          div.textContent = item[field] || '';
          
          // Add event listener for editing
          div.addEventListener('blur', (e) => {
            const idx = parseInt(e.target.getAttribute('data-index'));
            const fld = e.target.getAttribute('data-field');
            const newValue = e.target.textContent.trim();
            
            // Update data
            extractedData[idx][fld] = newValue;
          });
          
          cell.appendChild(div);
          row.appendChild(cell);
        });
        
        dataTableBody.appendChild(row);
      });
    }
    
    function showLoading(message) {
      loadingText.textContent = message;
      loadingOverlay.classList.remove('hidden');
    }
    
    function hideLoading() {
      loadingOverlay.classList.add('hidden');
    }
    
    function showNotification(message, type) {
      const bgColor = type === 'success' ? '#10B981' : '#EF4444';
      
      Toastify({
        text: message,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "right",
        backgroundColor: bgColor,
        stopOnFocus: true
      }).showToast();
    }
    
    function resetApp() {
      currentPdfFile = null;
      extractedData = null;
      
      // Reset file input
      fileInput.value = '';
      
      // Clear data table
      dataTableBody.innerHTML = '';
      
      // Disable export button
      exportExcelBtn.disabled = true;
      
      // Hide extraction info
      extractionInfo.classList.add('hidden');
      
      // Hide PDF preview
      pdfPreview.style.display = 'none';
      noPreview.style.display = 'block';
    }
  </script>
</body>
</html>
