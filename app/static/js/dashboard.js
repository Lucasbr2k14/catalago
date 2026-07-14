import "./menu.js"
import "./createTable.js"


function $(a){
    return document.querySelector(a);
}


function data(gmt) {
    const data = new Date(gmt);
    return data.toLocaleDateString("pt-BR");
}


class Dashboard {
    constructor () {
        this.prod_div = $("#produtos");
        this.prod_inp = $("#pesq-prod");
        this.dialog = $("#janela");
        this.add_prod_buton = $("#add-prod-btn");
        this.add_event();
        this.start_dash();

        this.product_by_name = {};
    }


    async start_dash() {
        this.create_table(
            await this.get_products(0)
        );
    }


    add_event() {
        this.prod_inp.addEventListener("input", (e) => {
            this.search_product(this.prod_inp.value);
        });

        this.add_prod_buton.addEventListener("click", (e) => {
            this.add_prod_menu();
        });
    }

    
    // Menus com os dialog
    
    async prod_menu(uuid) {
        const prod = await this.get_product(uuid);

        const title   = this.dialog.querySelector("h2");
        const content = this.dialog.querySelector("#dia-content");
        const buttons = this.dialog.querySelector("#dia-buttons");
        const ok = document.querySelector("#ok");
        const cancelar = document.querySelector("#cancelar");
        

        title.innerText = prod.name;

        console.log(prod);
        
        this.dialog.showModal();

        content.innerHTML = `
        <div id="div-prod-menu">

            <div id="div-prod-menu-image">
                <img id="prod-menu-image" src="${prod.image_url}"></img>
            </div>
            <div id="div-prod-menu-info">
                <p>
                    <span>
                        Nome: 
                    </span>
                    ${prod.name}
                </p>
                <p>
                    <span>
                        Quantidade:  
                    </span>
                    ${prod.quantidade}
                </p>
                <p>
                    <span>
                        Preço: 
                    </span>
                    R$${prod.preco.replace(".", ",")}
                </p>
                <p>
                    <span>
                        Criado em: 
                    </span>
                    ${data(prod.create_at)}
                </p>
            </div>
        </div>
        
        `

        
        
        ok.addEventListener("click", () => {
            this.add_prod();
        });

        cancelar.addEventListener("click", () => {
            this.dialog.close();
        });

    }


    add_prod_menu() {
        const title = this.dialog.querySelector("h2");
        const content = this.dialog.querySelector("#dia-content");
        const buttons = this.dialog.querySelector("#dia-buttons");

        title.innerText = "Adicionar produto";

        const inputs = `
            <label>
                Nome
                <input type="text" id="prod-name-add">
            </label>

            <label>
                Quantidade
                <input type="number" id="prod-quant-add">
            </label>

            <label>
                Preço
                <div class="money-input">
                    <span>R$</span>
                    <input id="prod-price-add" type="number" step="0.01" min="0">
                </div>
            </label>
            <label>
                Foto
                <input type="file" id="image" accept="image/*">
            </label>
        `

        content.innerHTML = inputs;

        this.dialog.showModal();

        const ok = document.querySelector("#ok");
        const cancelar = document.querySelector("#cancelar");
        
        ok.addEventListener("click", () => {
            this.add_prod();
        });

        cancelar.addEventListener("click", () => {
            this.dialog.close();
        });
    }


    async search_product(name) {
        this.get_products(0, 10, name).then( res => {
            console.log(res);
            this.create_table(res);
        });
    }


    async add_prod() {
        const nome = document.querySelector("#prod-name-add").value.trim();
        const quantidade = Number(document.querySelector("#prod-quant-add").value);
        const preco = Number(document.querySelector("#prod-price-add").value);
        const foto = document.querySelector("#image");

        if (!nome) {
            alert("Informe o nome do produto.");
            return;
        }

        if (quantidade < 0 || Number.isNaN(quantidade)) {
            alert("Quantidade inválida.");
            return;
        }

        if (preco < 0 || Number.isNaN(preco)) {
            alert("Preço inválido.");
            return;
        }

        if (foto.files.length != 1) {
            alert("Foto inválida");
            return;
        }

        try {
            const url_image = await this.sand_file(foto);

            const response = await fetch("/api/product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    nome: nome,
                    preco:preco,
                    quantidade:quantidade,
                    image: url_image.url
                })
            });

            if (!response.ok) {
                throw new Error(`Erro ${response.status}`);
            }
            
            const data = await response.json();
            
            this.dialog.close();
            await this.start_dash();

        } catch (error) {
            alert(`Não foi possível cadastrar o produto. ${error}`);
        }

    }


    async sand_file(file_input) {

        const file = file_input.files[0];
        const formData = new FormData();

        formData.append("image", file);

        try {
            const res = await fetch('/api/image', {
                method: 'POST',
                body:formData
            });
        
            if (!res.ok) {
                throw new Error(`Error: ${res.status}`);
            }

            return res.json();
        } catch (e) {
            alert("Foto inválida");
        }

    }


    create_table(prod) {

        const products = prod.products;

        const thead = `
        <thead>
            <tr>
                <th>Nome</th>
                <th>Qt.</th>
                <th>Preço</th>
            </tr>
        </thead>
        `;

        let tbody = "<tbody>\n";

        for (let i in products) {
            const p = products[i];

            this.product_by_name[p.name] = {
                img: p.image_path,
                uuid: p.uuid
            } 
            
            tbody += `
            <tr>
                <td class="prod-name" ><p class="p-name">${p.name}</p></td>
                <td class="prod-quat" >${p.quantidade}</td>
                <td class="prod-prec" >R$${p.preco.replace(".", ",")}</td>
            </tr>
            `;
        }

        tbody += "</tbody>"

        const table = `
        <table>
        ${thead}
        ${tbody}
        </table>
        `;

        this.prod_div.innerHTML = table;
        this.set_events();
    }
    

    set_events() {
        const name = document.querySelectorAll('.p-name');
        const preview_img = document.querySelector("#preview img");
        const preview = document.querySelector("#preview");

        name.forEach( (element) => {
            element.addEventListener("mouseenter", (e) => {
                preview_img.setAttribute("src",  this.product_by_name[element.innerText].img);
                preview.style.display = 'block';
            });
        
            element.addEventListener("mouseleave", (e) => {
                preview.style.display = 'none';
                preview_img.setAttribute("src", "");
            });
        
            element.addEventListener("mousemove", (e) => {
                preview.style.left = `${e.clientX + 20}px`
                preview.style.top  = `${e.clientY + 20}px` 
            });
        
            element.addEventListener("click", (e) => {
                this.prod_menu(this.product_by_name[element.innerText].uuid);
            });

        });
        
    }


    async get_products(page, limit=10, name='') {
        let url = `/api/products?page=${page}&limit=${limit}`;

        if (name != '') {
            url += `&search=${name}`
        }

        const prod = await fetch(url);
        
        if (prod.status != 200) {
            return null;
        }

        const json = prod.json();

        return json;
    }


    async get_product(uuid) {
        let url = `/api/product/${uuid}`

        try{
            const prod = await fetch(url);
            if (prod.status == 200){
                return prod.json();
            }
        } catch(e) {
            return null
        }
    }

}

const dash = new Dashboard();

