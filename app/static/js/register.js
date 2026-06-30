const input_cpf = document.querySelector("#cpf");

input_cpf.addEventListener('input', update_cpf);


const valores = ['1','2','3','4','5','6','7','8','9','.', '-']

function update_cpf(input){
    
    const input = input_cpf.value;
    
    if (input.length < 11) return;
    if (input.length > 11) return;

    for (let i = 0; i < input.length; i++) {
        
    }
    
}