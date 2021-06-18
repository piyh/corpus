let nav_collapse = document.getElementById("navbar_collapse")
nav_collapse.addEventListener('blur', function(e) {

    if (!e.target.classList.contains("collapsed")){
        e.target.click()        
    }

});
