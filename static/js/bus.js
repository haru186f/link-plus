/**
 * bus.js - バス情報取得・表示管理スクリプト
 */

// --- 1. 定数・グローバル設定 ---
const BASE_API_URL = '/api/next/';
const PREFIX_ID = 'bus_info_'; 
const REFRESH_INTERVAL_MS = 60000; // 1分ごとに自動更新

// Djangoから渡される変数、またはデフォルト値
const SELECTED_BUS_STOP = typeof SELECTED_BUS_STOP_NAME !== 'undefined' ? SELECTED_BUS_STOP_NAME : '八王子';
const HACHIOJI_ID = typeof USER_BUS_STOP_ID !== 'undefined' ? USER_BUS_STOP_ID : 2;

// 内部状態
let currentDirection = 'campus'; // 'campus' (行き) または 'station' (帰り)
let latestBusData = null;      // APIから取得した最新のJSON

// --- 2. 初期化処理 ---
document.addEventListener('DOMContentLoaded', () => {
    // 方向に切り替えボタン
    const toggleBtn = document.getElementById('toggle_direction_btn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', handleDirectionToggle);
    }
    
    // 初回表示のセットアップ
    updateToggleButtonDisplay();
    fetchAndUpdateBusInfo();
    
    // 定期更新タイマー
    setInterval(fetchAndUpdateBusInfo, REFRESH_INTERVAL_MS);
    
    // 時計の開始
    updateClock();
    setInterval(updateClock, 1000);

    // 時刻表一覧モーダル (jQuery)
    initScheduleModal();
});

/**
 * ボタンクリック時の方向切り替え処理
 */
function handleDirectionToggle() {
    console.log("Direction toggle clicked");
    currentDirection = (currentDirection === 'campus') ? 'station' : 'campus';
    
    updateToggleButtonDisplay();
    
    // すでにデータがあれば即座にHTMLに反映。なければ取得しにいく
    if (latestBusData) {
        updateHtml(latestBusData);
    } else {
        fetchAndUpdateBusInfo();
    }
}

// --- 4. API・データ処理 ---

/**
 * APIからバス情報を取得
 */
async function fetchAndUpdateBusInfo() {
    try {
        const url = `${BASE_API_URL}?bus_stop=${encodeURIComponent(SELECTED_BUS_STOP)}`;
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) throw new Error(`HTTPエラー: ${response.status}`);

        const data = await response.json();
        latestBusData = data;
        updateHtml(latestBusData);
        displayErrorMessage(""); // エラーをクリア

    } catch (error) {
        console.error("データ取得失敗:", error);
        displayErrorMessage("情報の取得に失敗しました。");
    }
}

// --- 5. DOM更新（表示制御） ---

/**
 * トグルボタンのテキスト更新
 */
function updateToggleButtonDisplay() {
    const iconElement = document.getElementById('direction_icon');
    const busElement = document.getElementById('bus');
    if (!iconElement) return;

    // もし方向によって画像を変えたい場合はここで src を切り替えます
    if (currentDirection === 'campus') {
        iconElement.alt = "駅 → キャンパス";
        busElement.style.transform = "scaleX(-1)";
    } else {
        iconElement.alt = `${SELECTED_BUS_STOP} → 駅`;
        busElement.style.transform = "scaleX(1)";
    }
}

/**
 * メインのバス情報エリアを更新
 */
function updateHtml(data) {
    for (const busStopName in data) {
        if (!data.hasOwnProperty(busStopName)) continue;
        
        const info = data[busStopName];
        const elementId = `${PREFIX_ID}${busStopName}`;

        const isCampus = currentDirection === 'campus';
        const displayValue = isCampus ? info.departure_to_campus : info.return_to_station;
        const targetLabel = isCampus ? "駅発" : "キャンパス発";

        // ラベル更新
        const labelEl = document.getElementById(`${elementId}_direction_label`);
        if (labelEl) labelEl.textContent = targetLabel;

        // 時刻・分後 コンテンツ更新
        updateElementContent(`${elementId}_content`, displayValue, info.label);
    }
}

/**
 * 残り時間やステータスの表示を整形して挿入
 */
function updateElementContent(elementId, value, busStopLabel) {
    const element = document.getElementById(elementId);
    if (!element) return;

    let displayStr;
    const isNumber = typeof value === 'number';

    if (isNumber) {
        displayStr = value === 0 ? "間もなく出発" : `${value}分後`;
    } else {
        displayStr = value === '-' ? "情報なし" : (value || "エラー");
    }

    // 数値（残り時間）の場合は強調、それ以外は通常表示
    element.innerHTML = isNumber 
        ? `<p style="font-size: 1.2em; color: #1e88e5; font-weight: bold;">${displayStr}</p>`
        : `<p>${displayStr}</p>`;
}

/**
 * 現在時刻の表示
 */
function updateClock() {
    const clockEl = document.getElementById("clock");
    if (!clockEl) return;
    const now = new Date();
    const timeStr = now.toLocaleTimeString('ja-JP', { hour12: false });
    clockEl.textContent = `現在時刻：${timeStr}`;
}

/**
 * エラーメッセージの表示
 */
function displayErrorMessage(msg) {
    const container = document.getElementById('error_message_container');
    if (container) {
        container.innerHTML = msg ? `<p style="color: red;">${msg}</p>` : "";
    }
}

// --- 6. モーダル（jQuery） ---

function initScheduleModal() {
    if (typeof $ === 'undefined') return;

    const BUS_STOP_MAP = { 1: '八王子みなみ野', 2: '八王子' };
    const formatTime = (time) => time ? time.substring(0, 5) : '----';

    $('#openModalBtn').on('click', function() {
        $.ajax({
            url: '/api/bus-schedules',
            type: 'GET',
            success: function(response) {
                const $tableBody = $('#modalTableBody').empty();
                response.forEach(item => {
                    const f = item.fields;
                    if (f.bus_stop === HACHIOJI_ID) {
                        const row = `<tr>
                            <td>${BUS_STOP_MAP[f.bus_stop] || '不明'}</td>
                            <td>${f.is_saturday ? '土曜' : '平日'}</td>
                            <td>${formatTime(f.campus_departure)}</td>
                            <td>${formatTime(f.station_departure)}</td>
                            <td>${formatTime(f.campus_arrival)}</td>
                            <td>${f.note || ''}</td>
                        </tr>`;
                        $tableBody.append(row);
                    }
                });
                $('#dataModal').modal('show');
            },
            error: (xhr) => alert('時刻表の取得に失敗しました。')
        });
    });
}