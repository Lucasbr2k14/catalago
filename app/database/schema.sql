
CREATE TABLE IF NOT EXISTS user_roules (
    id   SERIAL PRIMARY KEY,
    nome VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS "users" (
    id         SERIAL PRIMARY KEY,
    uuid       TEXT NOT NULL UNIQUE,
    "name"     VARCHAR(150) NOT NULL,
    user_name  VARCHAR(100) NOT NULL UNIQUE,
    email      VARCHAR(100) NOT NULL UNIQUE,
    nascimento TIMESTAMP NOT NULL,
    "password" TEXT NOT NULL,
    create_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id    INT,

    FOREIGN KEY (role_id) REFERENCES user_roules(id)
);

CREATE TABLE IF NOT EXISTS produto (
    id        SERIAL PRIMARY KEY,
    uuid      TEXT NOT NULL UNIQUE,
    nome      TEXT NOT NULL UNIQUE,
    preco     INT NOT NULL,
    quant     INT DEFAULT 0,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id   INT,
    FOREIGN KEY (user_id) REFERENCES "users"(id)
);

CREATE TABLE IF NOT EXISTS tipo_composicao (
    id   SERIAL PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS composicao (
    id              SERIAL PRIMARY KEY,
    nome            TEXT NOT NULL,
    preco           INT NOT NULL,
    foto            TEXT,
    user_id         INT,
    tipo_composicao INT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_composicao) REFERENCES "tipo_composicao"(id),
    FOREIGN KEY (user_id) REFERENCES "users"(id)
);

CREATE TABLE IF NOT EXISTS composicoes_produto (
    id            SERIAL PRIMARY KEY,
    produto_id    INT,
    composicao_id INT,
    user_id       INT,
    FOREIGN KEY (produto_id) REFERENCES produto(id),
    FOREIGN KEY (composicao_id) REFERENCES composicao(id),
    FOREIGN KEY (user_id) REFERENCES "users"(id)
);