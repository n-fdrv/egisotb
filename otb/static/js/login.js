document.getElementById('loginForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = this;
    const username = document.getElementById('id_username').value.trim();
    const password = document.getElementById('id_password').value.trim();

    // --- Проверка полей ---
    if (!username || !password) {
        form.classList.add('was-validated');
        return;
    }

    try {
        const res = await fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (data.success) {
            alert('✅ Добро пожаловать!');
            window.location.href = data.redirect_url;
        } else {
            alert(`❌ ${data.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('⚠️ Ошибка сети');
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}