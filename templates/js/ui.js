function renderTable(data, config) {
    const thead = document.getElementById('table-head');
    const tbody = document.getElementById('table-body');

    thead.innerHTML = '';
    tbody.innerHTML = '';

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="100%" style="text-align: center; padding: 40px;">No data available</td></tr>';
        return;
    }

    const headerRow = document.createElement('tr');
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement('th');
        th.textContent = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    data.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.onclick = () => selectRow(tr, row, index);
        
        Object.entries(row).forEach(([key, value]) => {
            const td = document.createElement('td');
            if (key === 'photo' && currentTable === 'caregivers' && value) {
                const img = document.createElement('img');
                img.src = `${API_BASE}/caregivers/${row.caregiver_user_id}/photo`;
                img.style.maxWidth = '300px';
                img.style.width = 'auto';
                img.style.height = 'auto';
                img.style.maxHeight = '200px';
                img.style.objectFit = 'cover';
                img.style.cursor = 'pointer';
                img.style.display = 'block';
                img.style.margin = '0 auto';
                img.onclick = (e) => {
                    e.stopPropagation();
                    window.open(`${API_BASE}/caregivers/${row.caregiver_user_id}/photo`, '_blank');
                };
                td.appendChild(img);
                td.style.padding = '10px';
                td.style.textAlign = 'center';
            } else {
                td.textContent = value !== null && value !== undefined ? value : '';
            }
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    });
}

function selectRow(tr, row, index) {
    document.querySelectorAll('#table-body tr').forEach(r => {
        r.style.backgroundColor = '';
    });
    
    tr.style.backgroundColor = '#ffebcd';
    selectedRow = row;
}

function openCreateModal() {
    isUpdateMode = false;
    document.getElementById('modal-title').textContent = 'Create ' + tableConfigs[currentTable].title.slice(0, -1);
    buildForm();
    document.getElementById('modal').style.display = 'block';
}

function openUpdateModal() {
    if (!selectedRow) {
        showMessage('Please select a row to update', 'error');
        return;
    }
    isUpdateMode = true;
    document.getElementById('modal-title').textContent = 'Update ' + tableConfigs[currentTable].title.slice(0, -1);
    buildForm(selectedRow);
    document.getElementById('modal').style.display = 'block';
}

function buildForm(data = null) {
    const formFields = document.getElementById('form-fields');
    formFields.innerHTML = '';
    
    const config = tableConfigs[currentTable];
    config.fields.forEach(field => {
        const div = document.createElement('div');
        div.className = 'form-group';

        const label = document.createElement('label');
        label.textContent = field.label;
        if (field.required && !(field.optionalInUpdate && isUpdateMode)) {
            label.textContent += ' *';
        }
        div.appendChild(label);

        let input;
        if (field.type === 'select') {
            input = document.createElement('select');
            field.options.forEach(opt => {
                const option = document.createElement('option');
                option.value = opt;
                option.textContent = opt;
                if (data && data[field.name] === opt) option.selected = true;
                input.appendChild(option);
            });
        } else if (field.type === 'textarea') {
            input = document.createElement('textarea');
        } else {
            input = document.createElement('input');
            input.type = field.type;
        }

        if (field.readonly) input.disabled = true;
        if (field.required && !field.readonly) {
            if (field.type === 'file' && field.optionalInUpdate && isUpdateMode) {
            } else {
                input.required = true;
            }
        }
        if (data && field.type !== 'file') {
            if (field.type === 'date' && data[field.name]) {
                const dateValue = new Date(data[field.name]);
                input.value = dateValue.toISOString().split('T')[0];
            } else if (field.type === 'time' && data[field.name]) {
                const timeValue = data[field.name];
                if (typeof timeValue === 'string') {
                    input.value = timeValue.substring(0, 5);
                }
            } else {
                input.value = data[field.name] || '';
            }
        }
        if (field.type === 'file' && data && data[field.name] && isUpdateMode) {
            const fileInfo = document.createElement('div');
            fileInfo.style.marginTop = '5px';
            fileInfo.style.fontSize = '12px';
            fileInfo.style.color = '#666';
            fileInfo.innerHTML = `Current: ${data[field.name]}<br>Select new file to replace`;
            div.appendChild(fileInfo);
        }

        input.name = field.name;
        div.appendChild(input);
        formFields.appendChild(div);
    });
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('data-form').reset();
}

function showMessage(message, type) {
    const msgDiv = document.getElementById('message');
    msgDiv.textContent = message;
    msgDiv.className = type;
    setTimeout(() => {
        msgDiv.textContent = '';
        msgDiv.className = '';
    }, 3000);
}

