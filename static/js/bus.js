document.addEventListener('DOMContentLoaded', function() {
var flag=0;
const documentButton=document.querySelector('#busBT');
const busButton =() => {
    if (flag===0) {
        document.querySelector('#goTo').textContent='八王子行き';
        document.querySelector('.bus-times span').innerText='08:00';
        document.querySelector('#bus').style = "transform: scale(-1, 1);"
        flag=1;
    } else {
        document.querySelector('#goTo').textContent='キャンパス行き';
        document.querySelector('.bus-times span').innerText='15:00';
        document.querySelector('#bus').style = ""
        flag=0;
    }
};
documentButton.addEventListener('click',busButton);
console.log(documentButton.value);
});

$(document).ready(function() {
    // 💡 BusStopモデルのPKと名前のマッピングを定義
    // ここは、BusStopに登録されているデータに合わせて修正してください。
    // 例: 八王子 (PK=1), 八王子みなみ野 (PK=2) の場合
    const BUS_STOP_MAP = {
        1: '八王子',
        2: '八王子みなみ野'
        // 実際のPKと名前のペアを記述
    };

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
                    
                    // バス停IDを名前に変換
                    const busStopName = BUS_STOP_MAP[fields.bus_stop] || '不明'; 

                    const row = `<tr>
                                   <td>${busStopName}</td> 
                                   <td>${fields.is_saturday ? '土曜' : '平日'}</td>
                                   <td>${formatTime(fields.station_departure)}</td>
                                   <td>${formatTime(fields.campus_departure)}</td>
                                   <td>${fields.note || ''}</td>
                                 </tr>`;
                    $tableBody.append(row);
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