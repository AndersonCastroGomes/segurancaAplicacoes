import sqlite3

# Criar conexão com o banco de dados
con = sqlite3.connect('biblioteca.db')
cursor = con.cursor()

# Criar tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('aluno', 'professor', 'admin'))
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn TEXT NOT NULL UNIQUE,
    disponivel INTEGER NOT NULL DEFAULT 1
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_devolucao TEXT,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(livro_id) REFERENCES livros(id)
)
''')

# Inserir dados de exemplo
usuarios = [
    ('Anderson Castro', 'AC2023001', 'senha123', 'aluno'),
    ('Andersen Facundo', 'AF2023002', 'facundo456', 'professor'),
    ('Luis Fernando', 'LF2023003', 'fernando789', 'admin')
]

livros = [
    ('Dom Casmurro', 'Machado de Assis', '978-8535902775'),
    ('O Senhor dos Anéis', 'J.R.R. Tolkien', '978-8533613379'),
    ('1984', 'George Orwell', '978-8535914846')
]

cursor.executemany('INSERT INTO usuarios (nome, matricula, senha, tipo) VALUES (?, ?, ?, ?)', usuarios)
cursor.executemany('INSERT INTO livros (titulo, autor, isbn) VALUES (?, ?, ?)', livros)

con.commit()
con.close()