// window.addEventListener("load", ()=>{
//     var bg = document.getElementById("crop_bg");
//     var border = document.getElementById("crop_border");
//     var fg = document.getElementById("crop_fg");

//     bg.width = border.width = fg.width = window.width;
//     bg.height = border.height = fg.height = window.height;
// })
// Pixel tối thiểu mọi chiều của 1 hình phải có
// Nếu có một trong 2 chiều nhỏ hơn thì chức năng crop không hoạt động
const minImageSize = 32
var cropImageWorking = false
// File hiện tại đang được trỏ tới
var currentSelectedFileCursor = null 
var currentSelectedFileContent = null

var cropWindow = {
    // Đơn vị là pixel
    top : 0,
    left : 0,
    right : minImageSize,
    down : minImageSize
}
var searchImage;
const cropWindowBorderThickness = 5;

function displayErrorMessage (msg) {
    $("#status_msg").text(msg)
    $("#status_msg").removeClass("status")
    $("#status_msg").addClass("error")
}

function displayStatusMessage (msg) {
    $("#status_msg").text(msg)
    $("#status_msg").removeClass("error")
    $("#status_msg").addClass("status")
}

// Set event khi nút chọn File được click vào
$("#file_input").change((event) => {
    let file = $("#file_input").prop('files')[0]
    searchImage = file;
    console.log(file)
    if (file) {
        currentSelectedFileCursor = file
        var reader = new FileReader()
        reader.readAsDataURL(currentSelectedFileCursor);
        reader.onload = function() {
            currentSelectedFileContent = reader.result
            //console.log(currentSelectedFileContent)
            updateCropImage()
        }
        reader.onerror = function() {
            displayErrorMessage("Error reading "+file.name)
        }
    }
})
$("#btn_open").click((event) => {
    $("#file_input").trigger('click')
})

async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: "POST",
        // headers: { "Content-Type": "application/json" },
        body: data
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

$("#btn_search").click((event) => {
    if (currentSelectedFileCursor) {
        displayStatusMessage("Searching... please wait warmly...")

        // const up
        const uploadData = new FormData();
        
        let wn=$("#crop_bg").prop('naturalWidth'), 
        hn=$("#crop_bg").prop('naturalHeight'), 
        wv=$("#crop_bg").prop('width'), 
        hv=$("#crop_bg").prop('height')
        console.log("wn, hn, wv, hv",wn,hn,wv,hv)
        let x1 = Math.round(cropWindow.left / wv * wn)
        // let x1 = cropWindow.left-cropWindowBorderThickness;
        let y1 = Math.round(cropWindow.top / hv * hn)
        // let y1 = cropWindow.top-cropWindowBorderThickness;
        let x2 = Math.round(cropWindow.right / wv * wn)
        // let x2 = cropWindow.right+cropWindowBorderThickness;
        let y2 = Math.round(cropWindow.bottom / hv * hn)
        // let y2 = cropWindow.bottom+cropWindowBorderThickness;
        
        uploadData.append("image", searchImage, searchImage.name);
        uploadData.append("x1", x1);
        uploadData.append("x2", x2);
        uploadData.append("y1", y1);
        uploadData.append("y2", y2);
        
        console.log("coor", x1, y1, x2, y2);
        
        // fetch("http://localhost:8000/search", {
        //     method: "POST",
        //     // headers: { "Content-Type": "application/json" },
        //     body: uploadData
        // })
        // response.json().then(res => {
        //     console.log(res)
        // })
        // .catch(error => console.log(error))
                
        postData("http://localhost:8000/search", uploadData)
        .then(data => displaySearchResult(data))
        .catch(error => console.log("postData error:",error))
    }
    else {
        displayErrorMessage("No image to search yet. Please open one.")
    }
})

function displaySearchResult (data) {
    // Only UTFString are allowed in sessionStorage
    sessionStorage.setItem('feir_result_data', JSON.stringify(data))
    sessionStorage.setItem('feir_query_image', JSON.stringify(currentSelectedFileContent))
    // Refirect
    location.href = 'result.html'
}

// Các hàm tiện ích về khoảng cách
// Nếu khoảng cách trong tầm này, thì xác định là click dính
const stickDistance = 20
function dist (x1, y1, x2, y2) {
    return Math.abs(x1-x2) + Math.abs(y1-y2)
}

// Set event khi người ta click vào khung ảnh crop
// Để có thể kéo thả cái khung
var isDragging = {
    top : false,
    bottom : false,
    left : false,
    right : false
}
// Xử lý mouseleave và mouseevent sẽ làm ui mượt hơn chút
$("#crop_window").mouseleave((e) => {
    e.preventDefault()
    //console.log("mouse_leave")
})
$("#crop_window").mouseenter((e) => {
    e.preventDefault()
    //console.log("mouse_enter")
    if (e.buttons == 0) {
        isDragging.top = false
        isDragging.bottom = false
        isDragging.left = false
        isDragging.right = false
    }
})
$("#crop_window").mouseup((e) => {
    e.preventDefault()
    //console.log("mouse_up")
    isDragging.top = false
    isDragging.bottom = false
    isDragging.left = false
    isDragging.right = false
})
$("#crop_window").mousedown((e) => {
    e.preventDefault()
    //console.log("mouse_down")
    // Cạnh trên
    if (Math.abs(e.offsetY - cropWindow.top) <= stickDistance
    && cropWindow.left-stickDistance <= e.offsetX
    && e.offsetX <= cropWindow.right+stickDistance) {
        isDragging.top = true
    }
    else isDragging.top = false
    
    // Cạnh dưới
    if (Math.abs(e.offsetY - cropWindow.bottom) <= stickDistance
    && cropWindow.left-stickDistance <= e.offsetX
    && e.offsetX <= cropWindow.right+stickDistance) {
        isDragging.bottom = true
    }
    else isDragging.bottom = false

    // Cạnh trái
    if (Math.abs(e.offsetX - cropWindow.left) <= stickDistance
    && cropWindow.top-stickDistance <= e.offsetY
    && e.offsetY <= cropWindow.bottom+stickDistance) {
        isDragging.left = true
    }
    else isDragging.left = false

    // Cạnh phải
    if (Math.abs(e.offsetX - cropWindow.right) <= stickDistance
    && cropWindow.top-stickDistance <= e.offsetY
    && e.offsetY <= cropWindow.bottom+stickDistance) {
        isDragging.right = true
    }
    else isDragging.right = false
})
$("#crop_window").mousemove((e) => {
    e.preventDefault()
    //console.log("mouse_move")
    var changed = false
    if (isDragging.top) {
        if (e.offsetY + minImageSize <= cropWindow.bottom) {
            cropWindow.top = e.offsetY
            changed = true
        }
    } else if (isDragging.bottom) {
        if (cropWindow.top + minImageSize <= e.offsetY) {
            cropWindow.bottom = e.offsetY
            changed = true
        }
    }

    if (isDragging.left) {
        if (e.offsetX + minImageSize <= cropWindow.right) {
            cropWindow.left = e.offsetX
            changed = true
        }

    } else if (isDragging.right) {
        if (cropWindow.left + minImageSize <= e.offsetX) {
            cropWindow.right = e.offsetX
            changed = true
        }
    }

    if (changed) {
        updateCropWindowCss()
    }
})

// Cập nhật lại hình background và foreground của crop_window
function updateCropImage() {
    $("#crop_bg").attr('src', currentSelectedFileContent)
    $("#crop_fg").on('load', (e) => {
            if (e.target.width >= minImageSize
            && e.target.height >= minImageSize) {
                $("#crop_fg").removeClass("hide")
                cropImageWorking = true
                resetCropWindow(e)
            }
            else {
                cropImageWorking = false
                $("#crop_fg").addClass("hide")
            }
            displayStatusMessage("Load complete. Please drag border of image to crop as you please then press Submit.")
        })
    $("#crop_fg").attr('src', currentSelectedFileContent)
}

// Cập nhật lại css cái khung vẽ cho crop đúng chỗ
function updateCropWindowCss() {
    // Set the width and height so that 
    strb = "polygon(" +
        `${cropWindow.left-cropWindowBorderThickness}px ${cropWindow.top-cropWindowBorderThickness}px,` +
        `${cropWindow.right+cropWindowBorderThickness}px ${cropWindow.top-cropWindowBorderThickness}px,` +
        `${cropWindow.right+cropWindowBorderThickness}px ${cropWindow.bottom+cropWindowBorderThickness}px,` +
        `${cropWindow.left-cropWindowBorderThickness}px ${cropWindow.bottom+cropWindowBorderThickness}px)`
    str = "polygon(" +
        `${cropWindow.left}px ${cropWindow.top}px,` +
        `${cropWindow.right}px ${cropWindow.top}px,` +
        `${cropWindow.right}px ${cropWindow.bottom}px,` +
        `${cropWindow.left}px ${cropWindow.bottom}px)`

    // console.log(strb)
    $("#crop_border").css('clip-path', strb)
    $("#crop_fg").css('clip-path', str)
}

function updateCropBorderDimension(w,h) {
    $("#crop_border").css('width', `${w}px`)
    $("#crop_border").css('height', `${h}px`)
}

function resetCropWindow(e) {
    [w, h] = [e.target.width, e.target.height]
    cropWindow.top = 0
    cropWindow.left = 0
    cropWindow.right = w-1
    cropWindow.bottom = h-1
    updateCropBorderDimension(w,h)
    updateCropWindowCss()
}
