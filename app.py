from flask import Flask, jsonify, request
from database import Database

app = Flask(__name__)

@app.route("/personas", methods=["GET"])
def listar_personas():
    db = Database()

    data = db.execute(
        """
        SELECT id, nombre, apellido, fecha_nacimiento, fecha_fallecimiento, vigente, salario 
        FROM personas
        """
    )
    db.close()

    personas_procesadas = []
    for registro in data:
        if isinstance(registro, dict):
            p = registro.copy()
        else:
            p = {
                "id": registro[0],
                "nombre": registro[1],
                "apellido": registro[2],
                "fecha_nacimiento": registro[3],
                "fecha_fallecimiento": registro[4],
                "vigente": registro[5],
                "salario": registro[6]
            }
            
        p["fecha_nacimiento"] = str(p["fecha_nacimiento"])
        if p["fecha_fallecimiento"]:
            p["fecha_fallecimiento"] = str(p["fecha_fallecimiento"])
        p["salario"] = float(p["salario"])
        personas_procesadas.append(p)

    return jsonify(personas_procesadas)

@app.route("/personas/<int:id>", methods=["GET"])
def obtener_persona(id):
    db = Database()

    data = db.execute(
        """
        SELECT id, nombre, apellido, fecha_nacimiento, fecha_fallecimiento, vigente, salario 
        FROM personas WHERE id=%s
        """,
        (id,)
    )
    db.close()

    if data:
        registro = data[0] 
        if isinstance(registro, dict):
            p = registro.copy()
        else:
            p = {
                "id": registro[0],
                "nombre": registro[1],
                "apellido": registro[2],
                "fecha_nacimiento": registro[3],
                "fecha_fallecimiento": registro[4],
                "vigente": registro[5],
                "salario": registro[6]
            }

        p["fecha_nacimiento"] = str(p["fecha_nacimiento"])
        if p["fecha_fallecimiento"]:
            p["fecha_fallecimiento"] = str(p["fecha_fallecimiento"])
        p["salario"] = float(p["salario"])
        return jsonify(p)

    return jsonify({"error": "Persona no encontrada"}), 404

@app.route("/personas", methods=["POST"])
def crear_persona():
    data = request.json
    db = Database()

    db.execute(
        """
        INSERT INTO personas(nombre, apellido, fecha_nacimiento, fecha_fallecimiento, vigente, salario)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            data["nombre"],
            data["apellido"],
            data["fecha_nacimiento"],
            data.get("fecha_fallecimiento", None),
            data.get("vigente", True),
            data.get("salario", 0.00)
        )
    )
    db.close()

    return jsonify({
        "mensaje": "Persona creada exitosamente"
    }), 201

@app.route("/personas/<int:id>", methods=["PUT"])
def actualizar_persona(id):
    data = request.json
    db = Database()

    db.execute(
        """
        UPDATE personas
        SET nombre=%s,
            apellido=%s,
            fecha_nacimiento=%s,
            fecha_fallecimiento=%s,
            vigente=%s,
            salario=%s
        WHERE id=%s
        """,
        (
            data["nombre"],
            data["apellido"],
            data["fecha_nacimiento"],
            data.get("fecha_fallecimiento", None),
            data.get("vigente", True),
            data.get("salario", 0.00),
            id
        )
    )
    db.close()

    return jsonify({
        "mensaje": "Persona actualizada correctamente"
    })

@app.route("/personas/<int:id>", methods=["DELETE"])
def eliminar_persona(id):
    db = Database()

    db.execute(
        "DELETE FROM personas WHERE id=%s",
        (id,)
    )
    db.close()

    return jsonify({
        "mensaje": "Persona eliminada correctamente"
    })

if __name__ == "__main__":
    app.run(debug=True)
