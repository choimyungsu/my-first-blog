function showandhide() {/** 메뉴 숨기고 나타내기 */

    //미디어 쿼리 적용
    var x = document.getElementById("leftmenuinner");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
