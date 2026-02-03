const uploadSection = document.getElementById('uploadSection');
const fileInput = document.getElementById('fileInput');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const resultSection = document.getElementById('resultSection');
const previewImage = document.getElementById('previewImage');

uploadSection.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadSection.classList.add('dragover');
});

uploadSection.addEventListener('dragleave', () => {
    uploadSection.classList.remove('dragover');
});

uploadSection.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        processFile(file);
    } else {
        showError('Por favor, selecciona una imagen válida (JPG/PNG)');
    }
});

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

async function processFile(file) {
    hideError();
    hideResults();
    showLoading();

    previewImage.src = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/invoices/extract', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Error al procesar la factura');
        }

        displayResults(data.invoice);
    } catch (err) {
        showError(err.message);
    } finally {
        hideLoading();
    }
}

function displayResults(invoice) {
    document.getElementById('invoiceNumber').textContent = invoice.invoice_number || '-';
    document.getElementById('invoiceDate').textContent = invoice.invoice_date || '-';
    document.getElementById('dueDate').textContent = invoice.due_date || '-';
    document.getElementById('vendorName').textContent = invoice.vendor_name || '-';
    document.getElementById('vendorTaxId').textContent = invoice.vendor_tax_id || '-';

    const totalAmount = invoice.total_amount;
    const currency = invoice.currency || '';
    document.getElementById('totalAmount').textContent = totalAmount ? `${totalAmount} ${currency}` : '-';
    document.getElementById('currency').textContent = currency || '-';
    document.getElementById('taxAmount').textContent = invoice.tax_amount ? `${invoice.tax_amount} ${currency}` : '-';

    if (invoice.line_items && invoice.line_items.length > 0) {
        document.getElementById('lineItemsSection').style.display = 'block';
        const tbody = document.getElementById('itemsTableBody');
        tbody.innerHTML = '';

        invoice.line_items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.description || '-'}</td>
                <td>${item.quantity || 0}</td>
                <td>${item.unit_price ? item.unit_price.toFixed(2) : '-'}</td>
                <td>${item.amount ? item.amount.toFixed(2) : '-'}</td>
            `;
            tbody.appendChild(row);
        });
    } else {
        document.getElementById('lineItemsSection').style.display = 'none';
    }

    resultSection.classList.add('show');
}

async function downloadCSV() {
    try {
        const response = await fetch('/api/invoices/csv');
        if (!response.ok) {
            throw new Error('No hay facturas para descargar');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'invoices.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (err) {
        showError(err.message);
    }
}

function showLoading() {
    loading.classList.add('show');
}

function hideLoading() {
    loading.classList.remove('show');
}

function showError(message) {
    error.textContent = message;
    error.classList.add('show');
}

function hideError() {
    error.classList.remove('show');
}

function hideResults() {
    resultSection.classList.remove('show');
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Factura OCR - Aplicación cargada');
});