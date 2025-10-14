import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List
import numpy as np

DB_DIR = Path("data")
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "vision.sqlite3"

CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Faces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        imagem BLOB NOT NULL,
        encoding BLOB NOT NULL,
        data_captura DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES Usuarios(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS LogsAcesso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL,
        imagem_capturada BLOB
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS ErrosSistema (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        erro TEXT NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        status_corrigido BOOLEAN DEFAULT 0
    );
    """
]

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def create_tables() -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        for sql in CREATE_TABLES_SQL:
            cur.execute(sql)
        conn.commit()

def create_user(nome: str, email: str, senha_hash: str) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash),
        )
        conn.commit()
        return cur.lastrowid

def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE email = ?", (email,))
        return cur.fetchone()

def insert_face(usuario_id: int, imagem_bytes: bytes, encoding_vec: np.ndarray) -> int:
    encoding_f32 = encoding_vec.astype(np.float32).tobytes()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Faces (usuario_id, imagem, encoding) VALUES (?, ?, ?)",
            (usuario_id, sqlite3.Binary(imagem_bytes), sqlite3.Binary(encoding_f32)),
        )
        conn.commit()
        return cur.lastrowid

def list_all_face_encodings() -> List[Tuple[int, np.ndarray]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT usuario_id, encoding FROM Faces")
        out: List[Tuple[int, np.ndarray]] = []
        for row in cur.fetchall():
            enc = np.frombuffer(row["encoding"], dtype=np.float32)
            out.append((row["usuario_id"], enc))
        return out

def insert_log_acesso(usuario_id: Optional[int], status: str, imagem_bytes: Optional[bytes]) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO LogsAcesso (usuario_id, status, imagem_capturada) VALUES (?, ?, ?)",
            (usuario_id, status, sqlite3.Binary(imagem_bytes) if imagem_bytes else None),
        )
        conn.commit()
        return cur.lastrowid

def insert_erro_sistema(erro: str) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO ErrosSistema (erro) VALUES (?)", (erro,))
        conn.commit()
        return cur.lastrowid
