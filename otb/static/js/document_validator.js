// static/js/document_validator.js

document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, есть ли нужные элементы на странице
    if (!document.getElementById('id_doc_type') || !document.getElementById('id_doc_number')) {
        return; // Если элементов нет, прекращаем выполнение
    }

    const docTypeSelect = document.getElementById('id_doc_type');
    const docNumberInput = document.getElementById('id_doc_number');
    let feedbackElement = docNumberInput.nextElementSibling;

    // Создаем элемент для отображения ошибок, если его нет
    if (!feedbackElement || !feedbackElement.classList.contains('invalid-feedback')) {
        feedbackElement = document.createElement('div');
        feedbackElement.className = 'invalid-feedback';
        docNumberInput.parentNode.appendChild(feedbackElement);
    }

    // Типы документов и их валидация
    const DOCUMENT_TYPES = {
        'Паспорт РФ': {
            pattern: /^\d{0,10}$/,
            fullPattern: /^\d{10}$/,
            message: 'Введите ровно 10 цифр',
            maxLength: 10,
            placeholder: 'Пример: 1234567890'
        },
        'Свидетельство о рождении': {
            pattern: /^[IVXLCDM]{0,3}[А-ЯЁ]{0,2}\d{0,6}$/i,
            fullPattern: /^[IVXLCDM]{1,3}[А-ЯЁ]{2}\d{6}$/i,
            message: 'Формат: 1-3 римские цифры, 2 буквы, 6 цифр (XIIАБ123456)',
            maxLength: 11,
            placeholder: 'Пример: XIIАБ123456'
        }
    };

    // Инициализация при загрузке
    function init() {
        updateInputRestrictions();
        setupEventListeners();
    }

    // Обновление ограничений ввода
    function updateInputRestrictions() {
        const selectedOption = docTypeSelect.options[docTypeSelect.selectedIndex];
        const docType = selectedOption ? selectedOption.text : '';
        const rules = DOCUMENT_TYPES[docType] || {};

        docNumberInput.maxLength = rules.maxLength || 20;
        docNumberInput.placeholder = rules.placeholder || '';
        docNumberInput.value = '';
        docNumberInput.pattern = rules.fullPattern?.source || '';

        // Сбрасываем состояние валидации
        docNumberInput.classList.remove('is-invalid');
        feedbackElement.textContent = '';
    }

    // Настройка обработчиков событий
    function setupEventListeners() {
        docTypeSelect.addEventListener('change', updateInputRestrictions);

        docNumberInput.addEventListener('input', function(e) {
            validateInput();
        });

        docNumberInput.addEventListener('keydown', function(e) {
            // Разрешаем служебные клавиши
            if ([8, 9, 13, 16, 17, 18, 20, 27, 37, 38, 39, 40, 46].includes(e.keyCode)) {
                return;
            }

            const selectedOption = docTypeSelect.options[docTypeSelect.selectedIndex];
            const docType = selectedOption ? selectedOption.text : '';
            const rules = DOCUMENT_TYPES[docType];

            if (!rules) return;

            const currentValue = docNumberInput.value;
            const cursorPos = docNumberInput.selectionStart;
            const newValue = currentValue.slice(0, cursorPos) + e.key + currentValue.slice(cursorPos);

            // Проверяем, соответствует ли новый ввод шаблону
            if (!rules.pattern.test(newValue)) {
                e.preventDefault();
                showFeedback(rules.message);
            }
        });

        // Валидация при отправке формы
        const form = docNumberInput.closest('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                if (!validateInput(true)) {
                    e.preventDefault();
                    docNumberInput.focus();
                }
            });
        }
    }

    // Валидация ввода
    function validateInput(checkFull = false) {
        const selectedOption = docTypeSelect.options[docTypeSelect.selectedIndex];
        const docType = selectedOption ? selectedOption.text : '';
        const rules = DOCUMENT_TYPES[docType];

        if (!rules) return true;

        const isValid = checkFull
            ? rules.fullPattern.test(docNumberInput.value)
            : rules.pattern.test(docNumberInput.value);

        if (!isValid) {
            docNumberInput.classList.add('is-invalid');
            showFeedback(rules.message);
            return false;
        }

        docNumberInput.classList.remove('is-invalid');
        feedbackElement.textContent = '';
        return true;
    }

    // Показ сообщения об ошибке
    function showFeedback(message) {
        feedbackElement.textContent = message;
        feedbackElement.style.display = 'block';
    }

    // Запускаем инициализацию
    init();
});