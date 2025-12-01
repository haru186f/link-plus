// --- ⚙️ モーダル操作関数 ---

// モーダル表示
function showMailModal(subject, body) {
    // 件名を設定
    $('#mail-subject').text(subject);
    
    // 本文の改行を <br> に変換し、HTMLとして設定
    const formattedBody = body.replace(/\r?\n/g, '<br>');
    $('#mail-text').html(formattedBody);

    // モーダルをフェードイン表示
    $('#mail-modal-overlay').fadeIn(200);
}

// モーダル非表示
function hideMailModal() {
    $('#mail-modal-overlay').fadeOut(200);
}


// --- 🔗 イベントハンドラ ---

$(document).ready(function() {
    
    // 📧 メールリンクのクリックイベント
    $('.email-link').on('click', function(e) {
        e.preventDefault(); // リンクのデフォルト動作を停止
        const emailUrl = $(this).data('url');

        // $.getを使ってメール本文を取得
        $.get(emailUrl)
            .done(function(data) {
                // 取得成功時、モーダルを表示
                showMailModal(data.subject, data.body);
            })
            .fail(function(xhr, status, error) {
                // 取得失敗時
                console.error("AJAX Error:", status, error);
                alert('メール本文の取得に失敗しました。');
            });
    });

    // 🖱️ モーダル背景クリックで閉じるイベント
    $("#mail-modal-overlay").on("click", function (e) {
        // クリックされた要素がオーバーレイ自体（背景）であるか確認
        if (e.target.id === "mail-modal-overlay") {
            hideMailModal();
        }
    });

    // ※ 閉じるボタン（×ボタンなど）がある場合は、別途そのクリックイベントで hideMailModal() を呼び出してください。
});