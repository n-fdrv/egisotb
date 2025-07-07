document.getElementById('registerForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();
    const form = this;

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const username = document.getElementById('username').value.trim();
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;

    let valid = true;

    // --- Валидация ---
    if (!firstName) {
        document.getElementById('firstName').classList.add('is-invalid');
        valid = false;
    }

    if (!lastName) {
        document.getElementById('lastName').classList.add('is-invalid');
        valid = false;
    }

    if (!username) {
        document.getElementById('username').classList.add('is-invalid');
        valid = false;
    }

    if (!password1 || password1.length < 8) {
        document.getElementById('password1').classList.add('is-invalid');
        valid = false;
    }

    if (password1 !== password2) {
        document.getElementById('password2').classList.add('is-invalid');
        valid = false;
    }

    if (!valid) {
        form.classList.add('was-validated');
        return;
    }

    // --- Отправка данных ---
    try {
        const res = await fetch('/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ first_name: firstName, last_name: lastName, username, password1, password2 })
        });

        const data = await res.json();

        if (data.success) {
            alert(`✅ Добро пожаловать, ${data.user.name}`);
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