// ===============================
// ボタンによるバスの向き切り替え
// ===============================
document.addEventListener('DOMContentLoaded', function () {
    var flag = 0;
    const documentButton = document.querySelector('#busBT');

    const busButton = () => {
        if (flag === 0) {
            document.querySelector('#goTo').textContent = '八王子行き';
            document.querySelector('.bus-times span').innerText = '08:00';
            document.querySelector('#bus').style = "transform: scale(-1, 1);";
            flag = 1;
        } else {
            document.querySelector('#goTo').textContent = 'キャンパス行き';
            document.querySelector('.bus-times span').innerText = '15:00';
            document.querySelector('#bus').style = "";
            flag = 0;
        }
    };

    documentButton.addEventListener('click', busButton);
    console.log(documentButton.value);
});

// ===============================
// API からデータ取得
// ===============================
let busData = null;

function loadBusInfo() {
    fetch("/api/bus/next/")
        .then(response => response.json())
        .then(data => {
            busData = data; // ← 保存しておく

            updateDisplay();
        })
        .catch(error => console.error("Error:", error));
}

// ===============================
// 画面表示更新
// ===============================
function updateDisplay() {
    if (!busData) return;

    document.getElementById("bus-hachiouji-to-campus").textContent =
        `八王子 → キャンパス：${busData.hachiouji.departure_to_campus} 分`;

    document.getElementById("bus-hachiouji-to-station").textContent =
        `キャンパス → 八王子：${busData.hachiouji.return_to_station} 分`;

    document.getElementById("bus-minamino-to-campus").textContent =
        `みなみ野 → キャンパス：${busData.minamino.departure_to_campus} 分`;

    document.getElementById("bus-minamino-to-station").textContent =
        `キャンパス → みなみ野：${busData.minamino.return_to_station} 分`;
}

// ===============================
// PC 時刻の「分が変わる瞬間」に同期して更新
// ===============================
function syncEveryMinute(callback) {
    const now = new Date();
    const msToNextMinute = (60 - now.getSeconds()) * 1000;

    // 次の00秒で1回実行
    setTimeout(() => {
        callback();

        // 以降は毎分ぴったり実行（ズレなし）
        setInterval(callback, 60000);

    }, msToNextMinute);
}

// ===============================
// 初回ロード
// ===============================
window.onload = () => {
    loadBusInfo(); // まずAPIから取得
};

// ===============================
// APIは30分に1回だけ再取得（任意）
// ===============================
setInterval(loadBusInfo, 1800000); // 30分

// ===============================
// 表示だけは毎分PC時刻の00秒で更新
// ===============================
syncEveryMinute(() => {
    if (!busData) return;

    // 1分減らす
    busData.hachiouji.departure_to_campus--;
    busData.hachiouji.return_to_station--;
    busData.minamino.departure_to_campus--;
    busData.minamino.return_to_station--;

    updateDisplay();
});

// ===============================
// バス時刻表の一覧
// ===============================
$(document).ready(function() {
    // 💡 BusStopモデルのPKと名前のマッピングを定義
    const BUS_STOP_MAP = {
        1: '八王子みなみ野',
        2: '八王子'
    };

    // htmlからIDを取得
    const HACHIOJI_ID = USER_BUS_STOP_ID;

    // 時刻文字列を "HH:MM" 形式に整形するヘルパー関数
    const formatTime = (timeStr) => timeStr ? timeStr.substring(0, 5) : '----';

    $('#openModalBtn').on('click', function() {
        // 1. Ajax通信でデータを取得
        $.ajax({
            url: '/api/bus-schedules', // urls.pyで設定した名前
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                const $tableBody = $('#modalTableBody');
                $tableBody.empty(); // テーブルをクリア

                // 2. 取得したデータを行ごとに処理し、テーブルに追加
                response.forEach(function(item) {
                    const fields = item.fields;
                    // 八王子か八王子みなみ野を判定
                    if (fields.bus_stop === HACHIOJI_ID){
                    // バス停IDを名前に変換
                        const busStopName = BUS_STOP_MAP[fields.bus_stop] || '不明'; 

                        const row = `<tr>
                                   <td>${busStopName}</td> 
                                   <td>${fields.is_saturday ? '土曜' : '平日'}</td>
                                   <td>${formatTime(fields.station_departure)}</td>
                                   <td>${formatTime(fields.campus_arrival)}</td>
                                   <td>${formatTime(fields.campus_departure)}</td>
                                   <td>${fields.note || ''}</td>
                                 </tr>`;
                        $tableBody.append(row);
                    }
                });

                // 3. モーダルを表示
                $('#dataModal').modal('show');
            },
            error: function(xhr, status, error) {
                // エラー処理（例：サーバー側でNot Foundなどのエラーが発生した場合）
                alert('データの取得に失敗しました: ' + (error || status));
            }
        });
    });
});

// ===============================
// 現在時刻
// ===============================
function updateClock() {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2, "0");
    const mm = String(now.getMinutes()).padStart(2, "0");
    const ss = String(now.getSeconds()).padStart(2, "0");

    document.getElementById("clock").textContent =
        `現在時刻：${hh}:${mm}:${ss}`;
}

// 1秒ごとに表示更新
setInterval(updateClock, 1000);
updateClock();
