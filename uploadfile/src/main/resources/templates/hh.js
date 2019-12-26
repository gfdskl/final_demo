container = document.getElementById("container");

// window.onload(addpicture);

function addpicture() {
    alert(3);
    var num = 20;
    var i;
    for (i = 0;i < num;i++)
    {
        // div_ = document.createElement("div");
        img_ = document.createElement("img");
        img_.src = "file:///C:\Users\86137\Desktop\cj.jpg";
        // img.style.max = max-width: 100%;
        // img.style.max-width = 100%;
        // div_.addpenChild(img_);
        container.addpenChild(img_);
    }
}

add = document.getElementById("add");
add.addEventListener("click",function() {
    img = document.getElementById("img");
    img.src = "file:///‪E:/cj.jpg";
    img.style.width = "400px";
    img.style.height = "300px";
    var container = document.getElementById("container");
    var num = 20;
    var i;
    for (i = 0;i < num;i++)
    {
        img_ = document.createElement("img");
        img_.src = "‪file:///E:/cj.jpg";
        // img.style.max = max-width: 100%;
        // img.style.max-width = 100%;
        // div_.addpenChild(img_);

        container.appendChild(img_);
        // alert(1);
    }
})