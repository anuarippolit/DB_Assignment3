const API_BASE = window.location.origin;

async function loadTable(table) {
    try {
        const config = tableConfigs[table];
        const response = await fetch(`${API_BASE}${config.endpoint}`);
        if (!response.ok) throw new Error('Failed to load data');
        
        currentData = await response.json();
        renderTable(currentData, config);
        showMessage('Data loaded successfully', 'success');
    } catch (error) {
        showMessage('Error loading data: ' + error.message, 'error');
        renderTable([], tableConfigs[table]);
    }
}

async function createRecord(formData, config) {
    const url = `${API_BASE}${config.endpoint}/`;
    
    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        let errorMessage = 'Failed to create record';
        try {
            const error = await response.json();
            errorMessage = error.detail || errorMessage;
        } catch (e) {
            errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    showMessage('Record created successfully', 'success');
    closeModal();
    loadTable(currentTable);
}

async function updateRecord(formData, config) {
    const idField = config.idField;
    const id = selectedRow[idField];
    
    if (currentTable === 'caregivers') {
        const photoFile = formData.get('photo');
        const hasPhoto = photoFile && photoFile instanceof File && photoFile.size > 0;
        
        const regularFields = new FormData();
        let hasRegularFields = false;
        formData.forEach((value, key) => {
            if (key !== 'photo' && value) {
                regularFields.append(key, value);
                hasRegularFields = true;
            }
        });

        const promises = [];

        if (hasPhoto) {
            const photoFormData = new FormData();
            photoFormData.append('photo', photoFile);
            promises.push(
                fetch(`${API_BASE}${config.endpoint}/${id}/photo`, {
                    method: 'PUT',
                    body: photoFormData
                }).then(async (response) => {
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Failed to update photo');
                    }
                    return response;
                })
            );
        }

        if (hasRegularFields) {
            const params = new URLSearchParams();
            regularFields.forEach((value, key) => {
                if (value) params.append(key, value);
            });
            promises.push(
                fetch(`${API_BASE}${config.endpoint}/${id}?${params}`, {
                    method: 'PUT'
                })
            );
        }

        if (promises.length === 0) {
            throw new Error('No fields to update');
        }

        try {
            const responses = await Promise.all(promises);
            
            for (const response of responses) {
                if (!response.ok) {
                    let errorMessage = 'Failed to update record';
                    try {
                        const error = await response.json();
                        errorMessage = error.detail || errorMessage;
                    } catch (e) {
                        errorMessage = `HTTP ${response.status}: ${response.statusText}`;
                    }
                    throw new Error(errorMessage);
                }
            }
        } catch (error) {
            throw error;
        }

        showMessage('Record updated successfully', 'success');
        closeModal();
        loadTable(currentTable);
        return;
    }

    let url;
    if (config.compositeKey) {
        const keys = config.compositeKey.map(k => selectedRow[k]);
        url = `${API_BASE}${config.endpoint}/caregiver/${keys[0]}/job/${keys[1]}`;
    } else {
        url = `${API_BASE}${config.endpoint}/${id}`;
    }

    const params = new URLSearchParams();
    formData.forEach((value, key) => {
        if (value && !(value instanceof File)) params.append(key, value);
    });

    const response = await fetch(`${url}?${params}`, {
        method: 'PUT'
    });

    if (!response.ok) {
        let errorMessage = 'Failed to update record';
        try {
            const error = await response.json();
            errorMessage = error.detail || errorMessage;
        } catch (e) {
            errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    showMessage('Record updated successfully', 'success');
    closeModal();
    loadTable(currentTable);
}

async function deleteSelected() {
    if (!selectedRow) {
        showMessage('Please select a row to delete', 'error');
        return;
    }

    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }

    try {
        const config = tableConfigs[currentTable];
        let url;
        
        if (config.compositeKey) {
            const keys = config.compositeKey.map(k => selectedRow[k]);
            url = `${API_BASE}${config.endpoint}/caregiver/${keys[0]}/job/${keys[1]}`;
        } else {
            const id = selectedRow[config.idField];
            url = `${API_BASE}${config.endpoint}/${id}`;
        }

        const response = await fetch(url, {
            method: 'DELETE'
        });

        if (!response.ok) {
            let errorMessage = 'Failed to delete record';
            try {
                if (response.status !== 204) {
                    const error = await response.json();
                    errorMessage = error.detail || errorMessage;
                } else {
                    errorMessage = `HTTP ${response.status}: ${response.statusText}`;
                }
            } catch (e) {
                errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }

        showMessage('Record deleted successfully', 'success');
        selectedRow = null;
        loadTable(currentTable);
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    }
}

