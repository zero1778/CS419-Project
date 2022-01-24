
window.onload = function initializeResultGallery() {
    //let data = ['all_souls_000006.jpg', 'all_souls_000003.jpg', 'all_souls_000010.jpg', 'all_souls_000008.jpg', 'all_souls_000005.jpg', 'all_souls_000001.jpg', 'all_souls_000011.jpg', 'all_souls_000007.jpg', 'all_souls_000002.jpg', 'all_souls_000000.jpg']
    let data = JSON.parse(sessionStorage.getItem('feir_result_data'))
    sessionStorage.removeItem('feir_result_data')
    let queryImg = JSON.parse(sessionStorage.getItem('feir_query_image')) 
    if (queryImg) {
        sessionStorage.removeItem('feir_query_image')
        $("#gallery").append(searchElementFactory(queryImg, "Query image", false))
    }
    // Cho hiện các ảnh ở đây
    data.forEach((name, index) => {
        let divElem = searchElementFactory("http://localhost:8000/data/oxbuild_images/"+name, name)
        $("#gallery").append(divElem)
    })
}

function searchElementFactory (image_src, image_name, link=true) {
    // Mỗi phần tử gồm phần hình ở trên và phần text ở dưới

    // Phần hình
    let img = document.createElement('img')
    img.src = image_src
    
    // Phần văn bản
    let txt = document.createElement('a')
    txt.innerText = image_name
    if (link)
        txt.href = image_src

    let div = document.createElement('div')
    div.classList.add("element")
    div.appendChild(img)
    div.appendChild(txt)
    return div
}
