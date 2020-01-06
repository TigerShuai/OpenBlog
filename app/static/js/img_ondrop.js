function getEditormd(edit,httpUrl) {
    window.onload = function () {
        var codeEditor = $(".CodeMirror-wrap")[0];
        codeEditor.ondragenter = function (e) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        };
        codeEditor.ondragover = function (e) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        };
        codeEditor.ondrop = function (e) {
            e.preventDefault();
            e.stopPropagation();
            var files = e.dataTransfer.files // 这里获取到用户拖放的文件
            // 其中 ajaxUpload是Ajax上传文件的函数
            var formData = new FormData();
            formData.append("editormd-image-file", files[0]);
            // uploadUrl是后端提供的上传地址, uploadCallback是上传后的回调函数，用于生成代码片段并插入编辑器
            _ajax(httpUrl, formData, uploadCallback)
        };
    };

    // ajax上传图片 可自行处理
    var _ajax = function (url, data, callback) {
        $.ajax({
            "type": 'post',
            "cache": false,
            "url": url,
            "data": data,
            "dateType": "json",
            "processData": false,
            "contentType": false,
            "mimeType": "multipart/form-data",
            success: function (ret) {
                callback(JSON.parse(ret));
            },
            error: function (err) {
                console.log('js请求失败')
            }
        })
    }


    function uploadCallback(ret) {
        var url = ret.url; // 依据后端返回的数据格式而定
        var link = url;
        if (!url) return false;
        var alt = "";
        var cm = edit; // myEditormd是用editormd函数创建的编辑器对象，这里假设myEditor是全局变量
        var cursor = cm.getCursor(); // 获取光标位置
        if (url.endsWith(".mp4")) { // 如果是是视频
            var videoHtml = '<video class="video-js" controls preload="auto" width="100%" poster="" data-setup=\'{"aspectRatio":"16:9"}\'>\
<source src="' + url + '" type=\'video/mp4\' >\
<p class="vjs-no-js">\
To view this video please enable JavaScript\
</p>\
</video>';
            videoHtml = "\n" + videoHtml + "\n"; // videoHtml是生成的HTML视频代码片段
            cm.replaceSelection(videoHtml); // 插入到编辑器中
            cm.setCursor(cursor.line, cursor.ch + 2);
            return;
        }
        // 以下是对图片上传结果的处理，引用原image-upload插件的代码
        var altAttr = (alt !== "") ? " \"" + alt + "\"" : "";
        if (link === "" || link === "http://") {
            cm.replaceSelection("![" + alt + "](" + url + altAttr + ")");
        }
        else {
            cm.replaceSelection("[![" + alt + "](" + url + altAttr + ")](" + link + altAttr + ")");
        }

        if (alt === "") {
            cm.setCursor(cursor.line, cursor.ch + 2);
        }

    }

}


