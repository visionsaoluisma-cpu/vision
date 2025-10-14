from vision import db

if __name__ == "__main__":
    db.create_tables()
    print("Banco de dados inicializado em", db.DB_PATH)
