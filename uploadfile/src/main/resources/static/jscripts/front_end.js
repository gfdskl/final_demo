// 路径不能有中文
var video = document.getElementById("video");
var div = document.getElementById("div");
var div1 = document.getElementById("div1");
var input = document.getElementById("file");
var canvas = document.getElementById("canvas");
var img = document.getElementById("img");
var img1 = document.getElementById("img1");
var img6 = document.getElementById("img6");
var div2 = document.getElementById("div2");
var div3 = document.getElementById("div3");
var div4 = document.getElementById("div4");
var div6 = document.getElementById("div6");
var div7 = document.getElementById("div7");
var form = document.getElementById("form");
var button1 = document.getElementById("button1");
var button2 = document.getElementById("button2");
var process = document.getElementById("process");
var return_ans = document.getElementById("return_ans");

var div6_p = document.getElementById("div6_p");

var point_num = 0;
var point = new Array();
var Point = new Object();

var global_img;

input.addEventListener("change",function() {
    // 如果网页上已有video元素，就删除原来的video。

    var file = this.files[0];
    if (window.FileReader) {
        var reader = new FileReader();
        reader.readAsDataURL(file);
        //监听文件读取结束后事件
        reader.onloadend = function (e) {
            video.style.display = "block";
            img1.style.display = "none";
            video.src = e.target.result;
            video.controls = "controls";
            video.id = "video";
        };
    }
});

video.addEventListener('loadeddata', function () {
    var scale = 0.7;
    canvas.strokeStyle = "red";
    canvas.width = this.videoWidth*scale;
    canvas.height = this.videoHeight*scale;
    canvas.getContext("2d").drawImage(this,0,0,canvas.width,canvas.height);
    global_img = canvas.toDataURL("image/png");
    img.src = global_img;
    canvas.getContext("2d").strokeStyle = "red";
    canvas.getContext("2d").strokeRect(0,0,canvas.width,canvas.height);//对边框的设置
});


canvas.addEventListener("click",function() {
    if (point_num == 4) {
        alert("请点击确认或者清除,当前point_num"+point_num);
        return;
    }
    var p = this.getBoundingClientRect();
    var x = event.clientX - p.left * (this.width / p.width);
    var y = event.clientY - p.top * (this.height / p.height);
    var ctx = this.getContext("2d");

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
    p.x /= 0.7;
    p.y /= 0.7;
    var strXY = p.x.toFixed(0)+","+p.y.toFixed(0);
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

button1.addEventListener("click",function() {
    var context = canvas.getContext("2d");
    context.clearRect(0,0,canvas.width,canvas.height);
    form.reset();
    video.src = "";
    img1.style.display = "block";
    video.style.display = "none";
    div7.style.display = "none";
    div6.style.display = "none";
    form.style.display = "block";
    div.style.display = "block";
    div1.style.display = "block";
    div2.style.display = "block";
    div3.style.display = "block";
    button1.setAttribute("hidden",true);
    div4.style.display = "block";
    process.style.display = "none";
    // process.innerText = "你看不见我";
    div4.style.textAlign = "left";
    process.style.fontSize = 20+"px";
})

// window.onload = function () {

    var input1 = document.getElementById('text1');    //获取输入框中内容
    var input2 = document.getElementById('text2');    //获取输入框中内容
    var input3 = document.getElementById('text3');    //获取输入框中内容
    var input4 = document.getElementById('text4');    //获取输入框中内容
    //button点击事件
    document.getElementById('submit2').onclick = function () {
        point_num = 0;
        div4.style.textAlign = "center";
        process.style.fontSize = 30+"px";
        hidden_some_page();
        process.innerText = "正在处理中。。。";
        sendMsg();
        // img6.style.display = "none";
        // video2.style.display = "block";
        // video2.src = "file:///";
        // process.innerHTML = "处理完成";
    }

    function sendMsg() {
        var input1 = document.getElementById('text1');    //获取输入框中内容
        var input2 = document.getElementById('text2');    //获取输入框中内容
        var input3 = document.getElementById('text3');    //获取输入框中内容
        var input4 = document.getElementById('text4');    //获取输入框中内容
        // var url = document.getElementById('img1');    //获取队列为插入做准备

        ajax({
            url : '/form?text1=' + input1.value + '&text2=' + input2.value  + '&text3=' + input3.value +  '&text4=' + input4.value,
            success : function (res) {
                process.innerText = "处理完成";
                // for(var i=0; i<res.size;i++){

                // }
                video2.src = res;
                img6.style.display = "none";
                video2.style.display = "block";
                process.innerHTML = "处理完成";

            }
        });
        input1.value = "";
        input2.value = "";
        input3.value = "";
        input4.value = "";
    }
    
    function hidden_some_page() {
        process.style.display = "block";        div7.style.display = "block";
        div6_p.style.display = "block";
        // img6.style.display = "block";
        form.style.display = "none";
        div.style.display = "none";
        div1.style.display = "none";
        div2.style.display = "none";
        div3.style.display = "none";
        div4.style.display = "block";
        div6.style.display = "block";
        button1.removeAttribute("hidden");
        // div6.style.display = "block";
    }

    function ajax(obj) {
        var xhr = null;
        if (window.XMLHttpRequest) {    //检查浏览器是否支持XMLHTTPRequest
            //创建异步对象(用于在后台与服务器交换数据 是ajax的基础)
            xhr = new XMLHttpRequest();
        }
        else {  //IE5和IE6等部分浏览器不支持XMLHTTPRequest 用ActiveXObject替代
            xhr = new ActiveXObject('Microsoft.XMLHTTP');
        }
        if (obj.method) {
            xhr.open(obj.method, obj.url, true);
        }
        else {
            xhr.open('get', obj.url, true);
        }
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {  //请求已完成，且响应已就绪
                if (xhr.status == 200) {    //响应返回成功
                    //console.log('请求成功',xhr.responseText)
                    if (obj.success) {
                        obj.success(xhr.responseText);
                    }
                }
                else {
                    //console.log(xhr.status,'请求出错')
                    if (obj.failure) {
                        obj.failure('请求失败');
                    }
                }
            }
        };
        //设置请求体(前端传给后台服务器的参数)
        if (obj.method == undefined || obj.method.toLowerCase() == 'get') {
            //get方法的参数包含在url中 所以请求体设为空 即null
            xhr.send(null);
        }
        else {
            xhr.send(obj.params);
        }
    }
// }