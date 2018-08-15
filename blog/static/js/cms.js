function showandhide() {/** 메뉴 숨기고 나타내기 */
    var x = document.getElementById("leftmenuinner");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
