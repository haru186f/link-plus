// モーダル表示
function showMailModal(subject, body) {
    $('#mail-subject').text(subject);
    $('#mail-text').text(body);
    $('#mail-modal-overlay').fadeIn(200);
}

// モーダル非表示
function hideMailModal() {
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
                showMailModal(data.subject, data.body);
            },
            error: function(xhr, status, error) {
                console.error("AJAX Error:", status, error);
                alert('メール本文の取得に失敗しました。');
            }
        });
    });
});


$(".email-link").on("click", function () {
    const url = $(this).data("url");

    $.get(url, function (data) {
        // モーダルタイトルに件名
        $("#mail-modal-title").text(data.subject);

        // 本文中にも件名を入れる
        const fullText = `件名：${data.subject}\n\n${data.body}`;
        $("#mail-text").text(fullText);

        $("#mail-modal-overlay").show();
    });
        // モーダル背景クリック → 閉じる
    $("#mail-modal-overlay").on("click", function (e) {
        if (e.target.id === "mail-modal-overlay") {
            hideMailModal();
        }
    });
});
