const API_URL = 'http://localhost:5000/users';

const userForm = document.getElementById('userForm');
const userName = document.getElementById('userName');
const userEmail = document.getElementById('userEmail');
const userId = document.getElementById('userId');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');
const formTitle = document.getElementById('formTitle');
const usersList = document.getElementById('usersList');
const alertBox = document.getElementById('alertBox');

// Mostrar notificaciones
function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = `alert active ${type}`;
    setTimeout(() => {
        alertBox.className = 'alert';
    }, 3000);
}

// Obtener Usuarios
async function fetchUsers() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Error al obtener usuarios');
        const users = await response.json();
        
        usersList.innerHTML = '';
        if (users.length === 0) {
            usersList.innerHTML = '<tr><td colspan="4" style="text-align:center;">No hay usuarios registrados</td></tr>';
            return;
        }

        users.forEach(user => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td style="display:flex; gap:0.5rem;">
                    <button onclick="editUser(${user.id}, '${user.name}', '${user.email}')">Editar</button>
                    <button class="delete" onclick="deleteUser(${user.id})">Eliminar</button>
                </td>
            `;
            usersList.appendChild(tr);
        });
    } catch (error) {
        console.error(error);
        showAlert('No se pudo conectar con la API Flask.', 'error');
    }
}

// Guardar o Actualizar Usuario
userForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const uId = userId.value;
    const name = userName.value;
    const email = userEmail.value;

    const method = uId ? 'PUT' : 'POST';
    const url = uId ? `${API_URL}/${uId}` : API_URL;

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email })
        });

        if (!response.ok) {
            const resData = await response.json();
            throw new Error(resData.error || 'Error en la solicitud');
        }

        showAlert(`Usuario ${uId ? 'actualizado' : 'creado'} correctamente`, 'success');
        resetForm();
        fetchUsers();
    } catch (error) {
        console.error(error);
        showAlert(error.message, 'error');
    }
});

// Preparar edición
window.editUser = function(id, name, email) {
    userId.value = id;
    userName.value = name;
    userEmail.value = email;
    formTitle.textContent = 'Editar Usuario';
    submitBtn.textContent = 'Actualizar Cambios';
    cancelBtn.style.display = 'block';
};

// Cancelar edición
cancelBtn.addEventListener('click', resetForm);

function resetForm() {
    userForm.reset();
    userId.value = '';
    formTitle.textContent = 'Crear Nuevo Usuario';
    submitBtn.textContent = 'Guardar Usuario';
    cancelBtn.style.display = 'none';
}

// Eliminar Usuario
window.deleteUser = async function(id) {
    if (!confirm('¿Seguro que deseas eliminar este usuario?')) return;
    
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Error al eliminar usuario');
        }

        showAlert('Usuario eliminado', 'success');
        fetchUsers();
    } catch (error) {
        console.error(error);
        showAlert(error.message, 'error');
    }
}

// Inicializar
fetchUsers();
