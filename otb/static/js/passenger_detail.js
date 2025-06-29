document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('table tbody tr');

    rows.forEach(row => {
      row.style.cursor = 'pointer';
      row.addEventListener('click', function () {
        // Получаем данные из ячеек (порядок соответствует вашему шаблону)
        const cells = row.getElementsByTagName('td');
        const surname = cells[0].textContent.trim();
        const name = cells[1].textContent.trim();
        const patronymic = cells[2].textContent.trim();
        const birthday = cells[3].textContent.trim();
        const citizenship = cells[4].textContent.trim();
        const docType = cells[5].textContent.trim();
        const docNumber = cells[6].textContent.trim();

        // Заполняем модальное окно данными
        document.getElementById('passenger-surname').textContent = surname;
        document.getElementById('passenger-name').textContent = name;
        document.getElementById('passenger-patronymic').textContent = patronymic;
        document.getElementById('passenger-birthday').textContent = birthday;
        document.getElementById('passenger-citizenship').textContent = citizenship;
        document.getElementById('passenger-doc-type').textContent = docType;
        document.getElementById('passenger-doc-number').textContent = docNumber;

        // Открываем модальное окно
        const viewModal = new bootstrap.Modal(document.getElementById('viewPassengerModal'));
        viewModal.show();
      });
    });
  });