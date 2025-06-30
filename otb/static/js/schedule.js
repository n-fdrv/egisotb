document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('schedule-body');
    let currentPage = 1;

    async function loadSchedules(page = 1) {
        const url = new URL('/api/schedules/', window.location.origin);
        url.searchParams.set('page', page);

        const date = document.getElementById('dateFilter').value.trim();
        const ferryId = document.getElementById('ferryFilter').value;

        if (date) url.searchParams.set('departure_date', date);
        if (ferryId) url.searchParams.set('ferry_id', ferryId);

        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error('Ошибка сети');
            const data = await res.json();
            renderTable(data.results);
            renderPagination(data.count, page, data.next ? page + 1 : null);
        } catch (err) {
            console.error(err);
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Ошибка загрузки данных</td></tr>';
        }
    }


    async function loadSchedules() {
        try {
            const res = await fetch('/api/schedules/');
            if (!res.ok) throw new Error('Ошибка загрузки');
            const data = await res.json();
            renderTable(data);
        } catch (err) {
            console.error(err);
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Ошибка загрузки данных</td></tr>';
        }
    }

    function renderTable(schedules) {
        tbody.innerHTML = '';
        if (!schedules.length) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">Нет данных</td></tr>';
            return;
        }

        schedules.forEach(s => {
            const tr = document.createElement('tr');
            const ferryName = s.ferry ? s.ferry.name : 'Неизвестен';
            tr.innerHTML = `
                <td>${s.name}</td>
                <td>${new Date(s.departure_date).toLocaleDateString()} ${s.departure_time}</td>
                <td>${ferryName}</td>
                <td>${s.departure_port}-${s.arrival_port}</td>
                <td>${s.passenger_count || 0}</td>   <!-- Количество пассажиров -->
                <td>${s.crew_count || 0}</td>       <!-- Количество экипажа -->
                <td>
                    <a href="#" class="btn btn-sm btn-success me-1"><img src="{% static 'svg/pencil.svg' %}" width="20" height="20"></a>
                    <a href="#" class="btn btn-sm btn-danger"><img src="{% static 'svg/trash.svg' %}" width="20" height="20"></a>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    loadSchedules();
});