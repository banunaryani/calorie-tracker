food_elem = document.getElementById("food_id")

food_elem.addEventListener("input", showList)

qty_list = document.getElementById("quantity")

qty_list.addEventListener("focus", showQtyRecomList)

function focusQty() {
    qty_list.focus();
}

function showList() {
    keyword = food_elem.value
    search_result = document.getElementById("food-search-result")

    cleanSearchResult()
    
    if (keyword) {
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function () {
            resp = JSON.parse(this.response)
            console.log(resp)
            resp.forEach(r => {
                var single_list = document.createElement('li')
                text_node = document.createTextNode(r['food_name'])
                single_list.appendChild(text_node)
                
                search_result.appendChild(single_list)
                single_list.setAttribute('class', 'list-group-item')
                
                expand_btn = document.createElement('a')
                expand_text_node = document.createTextNode('Expand')
                expand_btn.appendChild(expand_text_node)
                single_list.appendChild(expand_btn)
                expand_btn.setAttribute('href', '#')
                expand_btn.setAttribute('class', 'expand-btn')
                expand_btn.setAttribute('onclick', 'expandFood(this)')
                expand_btn.style.cssText = "margin-left: 1.5rem"
            });
    
        }
        xhttp.open("GET", "api/food?q="+keyword);
        xhttp.send();
    }

}

function showQtyRecomList() {
    qty_recom_list=document.getElementById("qty-recom-list")
    qty = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    qty.forEach(q => {
        var single_list = document.createElement('button')
        text_node = document.createTextNode(q)
        single_list.appendChild(text_node)
        
        qty_recom_list.appendChild(single_list)
        single_list.setAttribute('type', 'button')
        single_list.setAttribute('class', 'list-group-item')
        
        // expand_btn = document.createElement('a')
        // expand_text_node = document.createTextNode('Expand')
        // expand_btn.appendChild(expand_text_node)
        // single_list.appendChild(expand_btn)
        // expand_btn.setAttribute('href', '#')
        // expand_btn.setAttribute('class', 'expand-btn')
        single_list.setAttribute('onclick', 'expandQty(this)')
        // expand_btn.style.cssText = "margin-left: 1.5rem"
    });
}

function showQtySatuanList() {
    qty_satuan_list=document.getElementById("qty-satuan-list")
    qty = [0,1,2,3,4,5,6,7,8,9]
    qty.forEach(q => {
        var single_list = document.createElement('button')
        text_node = document.createTextNode(q)
        single_list.appendChild(text_node)
        
        qty_satuan_list.appendChild(single_list)
        single_list.setAttribute('type', 'button')
        single_list.setAttribute('class', 'list-group-item btnQtySatuan')
        
        // expand_btn = document.createElement('a')
        // expand_text_node = document.createTextNode('Expand')
        // expand_btn.appendChild(expand_text_node)
        // single_list.appendChild(expand_btn)
        // expand_btn.setAttribute('href', '#')
        // expand_btn.setAttribute('class', 'expand-btn')
        single_list.setAttribute('onclick', 'expandSatuan(this)')
        // expand_btn.style.cssText = "margin-left: 1.5rem"
    });
}

function expandFood(e) {
    raw_text = e.parentNode.textContent

    clean_text= raw_text.substring(0,raw_text.length-6)
    
    document.getElementById("food_id").value = clean_text
    
    document.querySelector("input#quantity").focus()
}

function expandQty(e) {
    clean_text = e.textContent
    
    document.getElementById("quantity").value = clean_text
    
    document.getElementById("qty-recom-list").innerHTML = ""

    showQtySatuanList()
}

function expandSatuan(e) {
    clean_text = e.textContent
    
    document.getElementById("qty-satuan-list").innerHTML = ""
    
    qty = document.getElementById("quantity").value
    intQty = parseInt(qty)
    document.getElementById("quantity").value = intQty + parseInt(clean_text)
    
}

$('.select2-input').select2({
    theme: 'bootstrap4',
});