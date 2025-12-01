// 閉じるボタンの関数 (メール用)
function hideModal() {
    $('#mail-modal-overlay').fadeOut(200);
}


// メールを開く
$(document).ready(function() {
    $('.email-link').on('click', function(e) {
        e.preventDefault();
        var emailUrl = $(this).data('url');

        $.ajax({
            url: emailUrl,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#mail-subject').text(data.subject);
                var formattedBody = data.body.replace(/\r?\n/g, '<br>');    //改行
                $('#mail-text').html(formattedBody);    //整形済みHTML文字列の格納
                $('#mail-modal-overlay').fadeIn(200);
        },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", status, error);
                 alert('メール本文の取得に失敗しました。');
             }
        });
     });
});
/* ============================================
   📌 メールモーダル（既存の機能）
============================================ */
function showMailModal(text) {
    $("#mail-text").text(text);
    $("#mail-modal-overlay").fadeIn(200);
}

function hideMailModal() {
    $("#mail-modal-overlay").fadeOut(200);
}
