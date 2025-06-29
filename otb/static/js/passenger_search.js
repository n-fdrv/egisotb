document.addEventListener('DOMContentLoaded', function() {
    const docNumberInput = document.getElementById('id_doc_number');
    const passengerList = document.getElementById('passengerList');
    const passengerForm = document.getElementById('passengerForm');
    let debounceTimer;

    // Функция для отображения уведомлений
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        passengerList.prepend(alertDiv);

        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 3000);
    }

    // Функция для установки значений в select
    function setSelectValue(selectId, value) {
        if (!value) return;
        const select = document.getElementById(selectId);
        if (select) {
            for (let i = 0; i < select.options.length; i++) {
                if (select.options[i].value == value) {
                    select.selectedIndex = i;
                    break;
                }
            }
        }
    }

    // Функция поиска пассажиров
    const searchPassengers = async (query) => {
        if (query.length < 3) {
            passengerList.innerHTML = '<p class="text-muted">Введите минимум 3 символа</p>';
            return;
        }

        passengerList.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div></div>';

        try {
            const response = await fetch(`/api/passengers/?doc_number=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (data.length > 0) {
                let html = '<ul class="list-group">';
                data.forEach(passenger => {
                    html += `
                    <li class="list-group-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${passenger.surname} ${passenger.name} ${passenger.patronymic || ''}</strong><br>
                                <small class="text-muted">${passenger.doc_type}: ${passenger.doc_number}</small>
                            </div>
                            <button class="btn btn-sm btn-outline-primary select-passenger"
                                    data-passenger-id="${passenger.id}">
                                Выбрать
                            </button>
                        </div>
                    </li>`;
                });
                html += '</ul>';
                passengerList.innerHTML = html;

                // Добавляем обработчики для кнопок выбора
                document.querySelectorAll('.select-passenger').forEach(button => {
                    button.addEventListener('click', function() {
                        fillForm(this.getAttribute('data-passenger-id'));
                    });
                });
            } else {
                passengerList.innerHTML = '<p class="text-muted">Пассажиры не найдены</p>';
            }
        } catch (error) {
            console.error('Ошибка поиска:', error);
            showAlert('Ошибка загрузки данных', 'danger');
        }
    };

    // Функция заполнения формы данными пассажира
    const fillForm = async (passengerId) => {
        try {
            const response = await fetch(`/api/passengers/${passengerId}/`);
            const passengerData = await response.json();

            // Заполняем текстовые поля
            document.getElementById('id_surname').value = passengerData.surname || '';
            document.getElementById('id_name').value = passengerData.name || '';
            document.getElementById('id_patronymic').value = passengerData.patronymic || '';
            document.getElementById('id_doc_number').value = passengerData.doc_number || '';

            // Заполняем выпадающие списки
            setSelectValue('id_doc_type', passengerData.doc_type);
            setSelectValue('id_citizenship', passengerData.citizenship);
            setSelectValue('id_gender', passengerData.gender);

            // Заполняем дату рождения
            if (passengerData.birthday) {
                document.getElementById('id_birthday').value = passengerData.birthday.split('T')[0];
            }

            // Очищаем список найденных пассажиров
            passengerList.innerHTML = '<p class="text-muted">Данные загружены. Проверьте и нажмите "Добавить"</p>';

            // Показываем уведомление
            showAlert('Данные пассажира загружены в форму!', 'success');

        } catch (error) {
            console.error('Ошибка загрузки данных пассажира:', error);
            showAlert('Ошибка загрузки данных', 'danger');
        }
    };

    // Обработчик ввода номера документа (с дебаунсом)
    docNumberInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            searchPassengers(this.value);
        }, 300);
    });

    // Обработчик очистки формы (если нужно добавить кнопку)
    if (document.getElementById('clearFormBtn')) {
        document.getElementById('clearFormBtn').addEventListener('click', function() {
            passengerForm.reset();
            passengerList.innerHTML = '<p class="text-muted">Введите номер документа для поиска</p>';
        });
    }
});