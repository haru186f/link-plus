document.addEventListener('DOMContentLoaded', function() {

  // ============================
  //  カレンダー（上段の月表示）
  // ============================
  const calendarEl = document.getElementById('calendar');

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'ja',
    timeZone: 'Asia/Tokyo',
    height: 'auto',
    weekends: false,
    businessHours: true,
    expandRows: true,
    headerToolbar: false,
  });

  calendar.render();

  // -----------------------------
  // ボタン（card-header）に追加
  // -----------------------------
  const headerButtons = document.getElementById('calendar-header-buttons');
  headerButtons.innerHTML = `
    <button class="btn btn-outline-secondary btn-sm me-1" id="fc-prev">
      <i class="bi bi-chevron-left"></i>
    </button>

    <button class="btn btn-outline-secondary btn-sm me-1" id="fc-next">
      <i class="bi bi-chevron-right"></i>
    </button>

    <button class="btn btn-outline-primary btn-sm" id="fc-today">今日</button>
  `;

  document.getElementById('fc-prev').onclick  = () => { calendar.prev(); updateTitle(); };
  document.getElementById('fc-next').onclick  = () => { calendar.next(); updateTitle(); };
  document.getElementById('fc-today').onclick = () => { calendar.today(); updateTitle(); };

  function updateTitle() {
    document.getElementById('calendar-title').textContent = calendar.view.title;
  }
  updateTitle();


  // ============================
  //  時間割（list view）
  // ============================
  const calendarEl2 = document.getElementById('calendar-list');

  const calendar2 = new FullCalendar.Calendar(calendarEl2, {
    initialView: 'listDay',
    locale: 'ja',
    timeZone: 'Asia/Tokyo',
    height: 'auto',
    weekends: false,
    businessHours: true,
    expandRows: true,

    noEventsContent: '本日の講義はありません',

    events: {
      url: '/api/lecture-events/',
      method: 'GET',
      failure: function() {
        alert('講義予定を読み込めませんでした。');
      }
    },

    eventClick: function(info) {
      alert(info.event.title + "\n" + info.event.extendedProps.room);
    }
  });

  calendar2.render();
});
