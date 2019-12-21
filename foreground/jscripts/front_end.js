var video = document.getElementById("video");
var div1 = document.getElementById("div1");
var input = document.getElementById("file");
var canvas = document.getElementById("canvas");
var img = document.getElementById("img");
var div3 = document.getElementById("div3");
var button2 = document.getElementById("button2");
var text1 = document.getElementById("text1");
var text2 = document.getElementById("text2");
var text3 = document.getElementById("text3");
var text4 = document.getElementById("text4");
var process = document.getElementById("process");
var return_ans = document.getElementById("return_ans");
var submit2 = document.getElementById("submit2");

var point_num = 0;
var point = new Array();
var Point = new Object();

var global_img;

input.addEventListener("change",function() {
    // 如果网页上已有video元素，就删除原来的video。
    // if (document.getElementById("video")) {
    //     document.getElementById("video").remove();
    // }
    var file = this.files[0];
    if (window.FileReader) {
            var reader = new FileReader();
            reader.readAsDataURL(file);    
            //监听文件读取结束后事件    
            reader.onloadend = function (e) {
            video.src = e.target.result;
            video.controls = "controls";
            video.width = "700";
            video.height = "300";
            video.id = "video";
                //e.target.result就是最后的路径地址
            };
        }
});


// function fun(x){
//     var file = x.files[0];
//       if (window.FileReader) {    
//                var reader = new FileReader();    
//                reader.readAsDataURL(file);    
//                //监听文件读取结束后事件    
//              reader.onloadend = function (e) {
//                video.src = e.target.result;
//                alert(video.src);
//                    //e.target.result就是最后的路径地址
//                };
//           }
// }


video.addEventListener('loadeddata', function () {
    // if (document.getElementById("canvas")) {
    //     document.getElementById("canvas").remove();
    // }
    var scale = 0.4;
    // var canvas = document.createElement("canvas");
    // var img = document.createElement("img");
    canvas.strokeStyle = "red";
    canvas.width = this.videoWidth*scale;
    canvas.height = this.videoHeight*scale;
    alert(this.videoWidth);
    alert(this.videoHeight);
    // canvas.width = 400;
    // canvas.height = 280;
    canvas.getContext("2d").drawImage(this,0,0,canvas.width,canvas.height);
    global_img = canvas.toDataURL("image/png");
    document.getElementById("img1").src = global_img;
    img.src = global_img;
    alert(img.width);
    alert(img.height);
    canvas.getContext("2d").strokeStyle = "red";
    canvas.getContext("2d").strokeRect(0,0,canvas.width,canvas.height);//对边框的设置
    // div1.appendChild(canvas);
    // canvas.appendChild(img);
    // div1.appendChild(img);
});


canvas.addEventListener("click",function() {
    if (point_num == 4) {
        alert("请点击确认或者清除,当前point_num"+point_num);
        return;
    }
    // alert(point_num);
    var p = this.getBoundingClientRect();
    var x = event.clientX - p.left * (this.width / p.width);
    var y = event.clientY - p.top * (this.height / p.height);
    // alert("x:"+x+",y:"+y);
    var ctx = this.getContext("2d");
    // ctx.clearRect(0,0,500,500);
    ctx.beginPath();
    ctx.fillStyle="red";
    ctx.arc(x,y,2,0,180);
    ctx.fill();
    Point.x = x;
    Point.y = y;
    point[point_num++] = Point;
    addCoorValue(point_num,Point);
});


function addCoorValue(num,p) {
    var whichText = "text"+num;
    var text = document.getElementById(whichText);
    var strXY = "x:"+p.x.toFixed(1)+" y:"+p.y.toFixed(1);
    // var strXY = "x:"+int(p.x)+" y:"+p.y.toFixed(1);
    text.value = strXY;
}


button2.addEventListener("click",function() {
    var ctx = canvas.getContext("2d");
    img.src = global_img;
    point_num = 0;
    ctx.drawImage(img,0,0,canvas.width,canvas.height);
    text1.value = "";
    text2.value = "";
    text3.value = "";
    text4.value = "";
})



submit2.addEventListener("click",function() {
    process.style.display = "block";
    $.ajax({
        url : "newsservlet",//请求地址
        dataType : "json",//数据格式 
        type : "post",//请求方式
        async : false,//是否异步请求
        success : function(data) {   //如何发送成功
        for(var i=0;i<data.length;i++){    //遍历data数组
                var ls = data[i];    
                alert(ls);
                
            }

            // $("#div5").html(html); //在html页面id=ulul的标签里显示html内容
        }

})
})



submit2.addEventListener("click",function() {
    div5 = document.getElementById("div5")
    url = "jscripts/zz.jpg"
    img1 = document.getElementById("img1")
    img1.src = url
});