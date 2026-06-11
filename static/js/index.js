const produtos = document.querySelectorAll(".produto");
const pesquisa = document.querySelector("#pesquisa");

function eventMenu(i) {
    const element_style = produtos[i].querySelector("table").style.display;
    if ( element_style == "") {
        produtos[i].querySelector("table").style.display = "block";
        produtos[i].querySelector(".seta").innerHTML = "&#9662;"
    } else {
        produtos[i].querySelector("table").style.display = "";
        produtos[i].querySelector(".seta").innerHTML = "&#9656;";
    }
}

function pesquisar(input) {
    const value = pesquisa.value.toLowerCase();

    for (let i = 0; i < produtos.length; i++) {
        
        const text = produtos[i].querySelector("h3").textContent.toLowerCase();
        
        if (text.includes(value)) {
            produtos[i].style.display = "block";
        } else {
            produtos[i].style.display = "none";
        }
    
    
    }

}


pesquisa.addEventListener("input", pesquisar);

for (let i = 0; i < produtos.length; i++) {
    const element = produtos[i];
    element.querySelector("p").addEventListener(
        "click", 
        (p) => { eventMenu(i) }
    );
}