let currentTable = 'users';
let currentData = [];
let selectedRow = null;
let isUpdateMode = false;

function setupTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const table = tab.getAttribute('data-table');
            switchTable(table);
        });
    });
}

function switchTable(table) {
    currentTable = table;
    selectedRow = null;
    isUpdateMode = false;

    document.querySelectorAll('.tab').forEach(t => {
        t.classList.remove('active');
    });
    document.querySelector(`[data-table="${table}"]`).classList.add('active');

    document.getElementById('table-title').textContent = tableConfigs[table].title;

    loadTable(table);
}

document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    loadTable('users');

    document.getElementById('data-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData();
        const config = tableConfigs[currentTable];

        config.fields.forEach(field => {
            if (field.readonly && !isUpdateMode) return;
            const input = form.querySelector(`[name="${field.name}"]`);
            if (input && !input.disabled) {
                if (input.type === 'file') {
                    if (input.files.length > 0) {
                        formData.append(field.name, input.files[0]);
                    } else if (field.optional && isUpdateMode) {
                        formData.append(field.name, '');
                    }
                } else {
                    if (input.value) {
                        formData.append(field.name, input.value);
                    }
                }
            }
        });

        try {
            if (isUpdateMode) {
                await updateRecord(formData, config);
            } else {
                await createRecord(formData, config);
            }
        } catch (error) {
            showMessage('Error: ' + error.message, 'error');
        }
    });

    window.onclick = (event) => {
        const modal = document.getElementById('modal');
        if (event.target === modal) {
            closeModal();
        }
    }
});

