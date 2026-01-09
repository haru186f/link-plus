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
    expandRows: true,
    headerToolbar: false,
    stickyHeaderDates: false,
    fixedWeekCount: true,
    height: 500,
// --- ここを追加：時刻（数字）の表示を消す ---
    displayEventTime: false,

    noEventsContent: '本日の講義はありません',

    events: {
      url: '/api/lecture-events/',
      method: 'GET',
      failure: function() {
        alert('講義予定を読み込めませんでした。');
      }
    },

    eventDataTransform: function(eventData) {
      if (eventData.extendedProps && eventData.extendedProps.full_title) {
        eventData.title = eventData.extendedProps.full_title;
      }
      return eventData;
    },

    eventClick: function(info) {
      alert(
        "講義名: " + info.event.title + "\n" +
        "時限: " + (info.event.extendedProps.period || "未設定") + "\n" +
        "教室: " + (info.event.extendedProps.room || "未定")
      );
    }
  });
    eventSources: [
      // 終日イベント
      {
        url: '/api/all-day-events/',
        method: 'GET',
      },
      // 時間割
      {
        url: '/api/lecture-events/',
        method: 'GET',
      }
    ],
      eventClick(info) {
        if (info.event.allDay) {
          alert('【行事】\n' + info.event.title);
        } else {
          alert(
            '【講義】\n' +
            info.event.title + '\n' +
            info.event.extendedProps.room
          );
        }
      },
    }
  );

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
    weekends: true,
    headerToolbar: false,
    businessHours: true,
    expandRows: true,

    noEventsContent: '本日の講義はありません',

    eventSources: [
      // 終日イベント
      {
        url: '/api/all-day-events/',
        method: 'GET',
      },
      // 時間割
      {
        url: '/api/lecture-events/',
        method: 'GET',
      }
    ],

    eventDidMount(info) {
      // 行事を目立たせる
      if (info.event.allDay) {
        info.el.classList.add('fw-bold');
      }
    },

    eventClick(info) {
      if (info.event.allDay) {
        alert('【行事】\n' + info.event.title);
      } else {
        alert(
          '【講義】\n' +
          info.event.title + '\n' +
          info.event.extendedProps.room
        );
      }
    }
  }
);

  calendar2.render();

    // ---- 時間割のボタン ----
  const ttButtons = document.getElementById('timetable-header-buttons');
  ttButtons.innerHTML = `
    <button class="btn btn-outline-secondary btn-sm me-1" id="tt-prev">
      <i class="bi bi-chevron-left"></i>
    </button>

    <button class="btn btn-outline-secondary btn-sm me-1" id="tt-next">
      <i class="bi bi-chevron-right"></i>
    </button>

    <button class="btn btn-outline-primary btn-sm" id="tt-today">今日</button>
  `;

  document.getElementById('tt-prev').onclick  = () => { calendar2.prev(); updateTtTitle(); };
  document.getElementById('tt-next').onclick  = () => { calendar2.next(); updateTtTitle(); };
  document.getElementById('tt-today').onclick = () => { calendar2.today(); updateTtTitle(); };

  function updateTtTitle() {
    document.getElementById('timetable-title').textContent = calendar2.view.title;
  }
  updateTtTitle();
});
