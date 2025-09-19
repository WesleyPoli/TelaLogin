// Configuração da API
const API_BASE_URL = 'http://localhost:8000';

// Elementos DOM
let currentTab = 'login';

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    // Formulário de login
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Formulário de registro
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
}

function showTab(tabName) {
    // Remover classe active de todos os tabs e forms
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.form-container').forEach(form => form.classList.remove('active'));
    
    // Ativar tab e form selecionados
    event.target.classList.add('active');
    document.getElementById(tabName + '-form').classList.add('active');
    
    currentTab = tabName;
    clearMessages();
}

async function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    try {
        showLoading(true);
        clearMessages();
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Salvar token no localStorage
            localStorage.setItem('access_token', data.access_token);
            showMessage('Login realizado com sucesso!', 'success');
            
            // Redirecionar ou mostrar área protegida
            setTimeout(() => {
                showProtectedArea();
            }, 1500);
        } else {
            showMessage(data.detail || 'Erro no login', 'error');
        }
    } catch (error) {
        showMessage('Erro de conexão. Verifique se o servidor está rodando.', 'error');
        console.error('Erro:', error);
    } finally {
        showLoading(false);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    
    // Validar senhas
    if (password !== confirmPassword) {
        showMessage('As senhas não coincidem', 'error');
        return;
    }
    
    const registerData = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: password
    };
    
    try {
        showLoading(true);
        clearMessages();
        
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registerData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Usuário registrado com sucesso! Faça login para continuar.', 'success');
            
            // Limpar formulário
            event.target.reset();
            
            // Mudar para aba de login
            setTimeout(() => {
                showTab('login');
            }, 2000);
        } else {
            showMessage(data.detail || 'Erro no registro', 'error');
        }
    } catch (error) {
        showMessage('Erro de conexão. Verifique se o servidor está rodando.', 'error');
        console.error('Erro:', error);
    } finally {
        showLoading(false);
    }
}

async function showProtectedArea() {
    try {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            showMessage('Token não encontrado', 'error');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/auth/protected`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Criar área protegida
            const protectedHTML = `
                <div class="protected-area">
                    <h2>Área Protegida</h2>
                    <p>${data.message}</p>
                    <div class="user-info">
                        <h3>Informações do Usuário</h3>
                        <p><strong>Token:</strong> ${token.substring(0, 20)}...</p>
                    </div>
                    <button onclick="logout()" class="btn btn-primary">Logout</button>
                </div>
            `;
            
            document.querySelector('.login-card').innerHTML = protectedHTML;
        } else {
            showMessage('Erro ao acessar área protegida', 'error');
        }
    } catch (error) {
        showMessage('Erro de conexão', 'error');
        console.error('Erro:', error);
    }
}

function logout() {
    localStorage.removeItem('access_token');
    location.reload();
}

function showMessage(message, type = 'info') {
    const messageArea = document.getElementById('message-area');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    messageArea.appendChild(messageDiv);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.parentNode.removeChild(messageDiv);
        }
    }, 5000);
}

function clearMessages() {
    const messageArea = document.getElementById('message-area');
    messageArea.innerHTML = '';
}

function showLoading(show) {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        if (show) {
            btn.disabled = true;
            btn.innerHTML = '<span class="loading"></span>Carregando...';
        } else {
            btn.disabled = false;
            if (currentTab === 'login') {
                btn.innerHTML = 'Entrar';
            } else {
                btn.innerHTML = 'Registrar';
            }
        }
    });
}

// Verificar se já está logado
document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('access_token');
    if (token) {
        showProtectedArea();
    }
});
