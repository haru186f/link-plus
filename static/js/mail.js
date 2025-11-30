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
