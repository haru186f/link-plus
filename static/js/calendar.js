document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ja',
        timeZone: 'Asia/Tokyo',
        weekends: true,
        height: 600,
        expandRows: true,
        headerToolbar: false,
        stickyHeaderDates: false,
        fixedWeekCount: true,
        dayMaxEventRows: 3,
        displayEventTime: true,
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

        eventDidMount: function(arg) {
          const status = arg.event.extendedProps.status;
          const subject = arg.event.extendedProps.subject;
          const eventDate = arg.event.startStr.split('T')[0];

          if (status === 1) {
              // --- ❌ 休講（赤色・斜線）の見た目設定 ---
              arg.el.style.setProperty('color', '#6c757d', 'important');

              // 休講は必ず表示する
              arg.el.style.setProperty('display', 'block', 'important');

          } else {
              // --- 🔵 通常授業（青色）の見た目設定 ---
              // 判定：今日、この科目の「休講(status:1)」がデータとして存在するか？
              const hasCancelToday = calendar.getEvents().some(ev =>
                  ev.extendedProps.status === 1 &&
                  ev.extendedProps.subject === subject &&
                  ev.startStr.split('T')[0] === eventDate
              );

              if (hasCancelToday) {
                  // 重複がある「その日」だけ、この要素を隠す
                  arg.el.style.setProperty('display', 'none', 'important');
              } else {
                  // 重複がない他の月曜日は青色で表示
                  arg.el.style.setProperty('display', 'block', 'important');
                  arg.el.style.setProperty('border-color', '#3788d8', 'important');
                  arg.el.style.setProperty('color', '#6c757d', 'important');
              }
          }
      }
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

  eventClassNames: function(arg) {
    if (arg.event.extendedProps.status === 1) {
      return ['event-canceled'];
    }
    return [];
  },

  eventDidMount: function(arg) {
          const status = arg.event.extendedProps.status;
          const subject = arg.event.extendedProps.subject;
          const eventDate = arg.event.startStr.split('T')[0];

          if (status === 1) {
              // --- ❌ 休講（赤色・斜線）の見た目設定 ---
              arg.el.style.setProperty('color', '#6c757d', 'important');
              arg.el.style.setProperty('border', '1px solid #dee2e6', 'important');

              // 休講は必ず表示する
              arg.el.style.setProperty('display', 'block', 'important');

          } else {
              // --- 🔵 通常授業（青色）の見た目設定 ---
              // 判定：今日、この科目の「休講(status:1)」がデータとして存在するか？
              const hasCancelToday = calendar.getEvents().some(ev =>
                  ev.extendedProps.status === 1 &&
                  ev.extendedProps.subject === subject &&
                  ev.startStr.split('T')[0] === eventDate
              );

              if (hasCancelToday) {
                  // 重複がある「その日」だけ、この要素を隠す
                  arg.el.style.setProperty('display', 'none', 'important');
              } else {
                  // 重複がない他の月曜日は青色で表示
                  arg.el.style.setProperty('display', 'block', 'important');
                  arg.el.style.setProperty('border-color', '#3788d8', 'important');
                  arg.el.style.setProperty('color', '#6c757d', 'important');
              }
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
