const panZoom = document.querySelector("#map-modal-img");
let panZoomInstance = null;
// モーダル表示
function showMapModal(imgSrc) {
    $("#map-modal-img").attr("src", imgSrc);
    $("#map-modal-overlay").fadeIn(200);
    // Panzoom初期化
        if (panZoomInstance !== null) {
            panZoomInstance = null;
        }
        panZoomInstance = panzoom(panZoom, {
            bounds: true,
            boundsPadding: 0.4,
            maxScale: 5,
            minScale: 1
        });
}

// モーダル非表示
function hideMapModal() {
    $("#map-modal-overlay").fadeOut(200);
}

// マップを開く
$(document).ready(function () {
    // マップ画像をクリック → モーダル表示
    $("#map-image").on("click", function () {
        showMapModal($(this).attr("src"));
    });

    // モーダル背景クリック → 閉じる
    $("#map-modal-overlay").on("click", function (e) {
        if (e.target.id === "map-modal-overlay") {
            hideMapModal();
        }
    });
});
