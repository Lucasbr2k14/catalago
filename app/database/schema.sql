CREATE TABLE IF NOT EXISTS user_roules (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    user_name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    nascimento TIMESTAMP NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES user_roules(id)
);

CREATE TABLE IF NOT EXISTS produto (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    preco INT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE IF NOT EXISTS composicao (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    preco INT NOT NULL,
    foto TEXT,
    user_id INT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE IF NOT EXISTS composicoes_produto (
    id SERIAL PRIMARY KEY,
    produto_id INT,
    composicao_id INT,
    user_id INT,
    FOREIGN KEY (produto_id) REFERENCES produto(id),
    FOREIGN KEY (composicao_id) REFERENCES composicao(id),
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);