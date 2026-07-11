import "./menu.js"

function $(a){
    return document.querySelector(a);
}


class Dashboard {
    
    constructor () {
        this.prod_div = $("#produtos");
        this.prod_inp = $("#pesq-prod");
        this.dialog = $("#janela");
        this.add_prod_buton = $("#add-prod-btn");
        this.add_event();
        this.start_dash();  
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
                <input type="file" id="imagem" accept="image/*">
            </label>
        `

        const btns = `
            <button id="ok">ok</button>
            <button id="cancelar">cancelar</button>
        `;

        content.innerHTML = inputs;
        buttons.innerHTML = btns;

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

    try {
        const response = await fetch("/api/product", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome,
                preco,
                quantidade
            })
        });

        if (!response.ok) {
            throw new Error(`Erro ${response.status}`);
        }

        const data = await response.json();
        this.dialog.close();
        await this.start_dash();

    } catch (error) {
        console.error("Erro ao cadastrar produto:", error);
        alert("Não foi possível cadastrar o produto.");
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
            tbody += `
            <tr>
                <td class="prod-name" >${p.name}</td>
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
}

const dash = new Dashboard();