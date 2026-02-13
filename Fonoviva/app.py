    from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

exercises = [
  "BOLA","PATO","CASA","SAPO","MALA",
  "DADO","FACA","VACA","GATO","RATO",
  "LUA","SOL","PIPA","TATU","BICO",
  "CAMA","FADA","VIDA","TOMATE","BANANA",
  "JANELA","PORTA","CARRO","PEIXE","FLOR",
  "PRATO","BRINCO","TRIGO","CRAVO","GRILO",
  "BLUSA","CLUBE","PLANO","FRUTA","DRAGÃO",
  "CHUVA","NARIZ","DEDAL","LIVRO","COPO"
]

def init_db():
    conn = sqlite3.connect("progresso.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY,
            etapa INTEGER
        )
    """)
    c.execute("INSERT OR IGNORE INTO progresso (id, etapa) VALUES (1, 0)")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/progresso")
def progresso():
    conn = sqlite3.connect("progresso.db")
    c = conn.cursor()
    c.execute("SELECT etapa FROM progresso WHERE id=1")
    etapa = c.fetchone()[0]
    conn.close()
    return jsonify({"etapa": etapa, "total": len(exercises)})

@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.json
    resposta = data.get("resposta").upper()

    conn = sqlite3.connect("progresso.db")
    c = conn.cursor()
    c.execute("SELECT etapa FROM progresso WHERE id=1")
    etapa = c.fetchone()[0]

    correta = exercises[etapa]

    if resposta == correta:
        etapa += 1
        c.execute("UPDATE progresso SET etapa=?", (etapa,))
        conn.commit()
        resultado = "correto"
    else:
        resultado = "errado"

    conn.close()

    return jsonify({
        "resultado": resultado,
        "etapa": etapa,
        "palavra": exercises[etapa] if etapa < len(exercises) else None,
        "total": len(exercises)
    })

@app.route("/reset")
def reset():
    conn = sqlite3.connect("progresso.db")
    c = conn.cursor()
    c.execute("UPDATE progresso SET etapa=0 WHERE id=1")
    conn.commit()
    conn.close()
    return jsonify({"status": "resetado"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
