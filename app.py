from flask import Flask, jsonify, request, make_response, Response
from flask_mysqldb import MySQL
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
from dicttoxml import dicttoxml

app = Flask(__name__)

# -------------------------
# DATABASE CONFIG
# -------------------------
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "110515"
app.config["MYSQL_DB"] = "hospital"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# -------------------------
# JWT CONFIG
# -------------------------
app.config["JWT_SECRET_KEY"] = "finals-secret-key"
jwt = JWTManager(app)

mysql = MySQL(app)

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def execute_query(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    return result


def format_response(data, status=200):
    response_format = request.args.get("format", "json")
    if response_format == "xml":
        xml = dicttoxml(data, custom_root="response", attr_type=False)
        return Response(xml, mimetype="text/xml", status=status)
    return make_response(jsonify(data), status)


# -------------------------
# HOME
# -------------------------
@app.route("/")
def index():
    return jsonify({
        "message": "Hospital Management REST API",
        "endpoints": [
            "POST /login",
            "GET /patients",
            "GET /patients/<id>",
            "POST /patients",
            "PUT /patients/<id>",
            "DELETE /patients/<id>",
            "GET /patients/search",
            "GET /patients/<id>/doctors",
            "GET /doctors",
            "GET /diagnosis"
        ]
    })


# -------------------------
# AUTHENTICATION
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return format_response({"error": "Missing credentials"}, 400)

    if data["username"] == "admin" and data["password"] == "1234":
        token = create_access_token(identity=data["username"])
        return format_response({"token": token})

    return format_response({"error": "Invalid credentials"}, 401)


# -------------------------
# PATIENTS CRUD
# -------------------------
@app.route("/patients", methods=["GET"])
def get_patients():
    data = execute_query("""
        SELECT p.idPatient, p.name, p.age,
               d.diagnosis_name, d.category
        FROM patient p
        JOIN diagnosis d ON p.Diagnosis_idDiagnosis = d.idDiagnosis
    """)
    return format_response(data)


@app.route("/patients/<int:idPatient>", methods=["GET"])
def get_patient(idPatient):
    data = execute_query("""
        SELECT p.idPatient, p.name, p.age,
               d.diagnosis_name, d.category
        FROM patient p
        JOIN diagnosis d ON p.Diagnosis_idDiagnosis = d.idDiagnosis
        WHERE p.idPatient = %s
    """, (idPatient,))

    if not data:
        return format_response({"error": "Patient not found"}, 404)

    return format_response(data)


@app.route("/patients", methods=["POST"])
@jwt_required()
def create_patient():
    data = request.json

    if not data:
        return format_response({"error": "No input data provided"}, 400)

    required = ("name", "age", "Diagnosis_idDiagnosis")
    if not all(k in data for k in required):
        return format_response({"error": "Missing required fields"}, 400)

    if not isinstance(data["age"], int):
        return format_response({"error": "Age must be an integer"}, 400)

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO patient (name, age, Diagnosis_idDiagnosis)
        VALUES (%s, %s, %s)
    """, (data["name"], data["age"], data["Diagnosis_idDiagnosis"]))
    mysql.connection.commit()
    cur.close()

    return format_response({"message": "Patient created"}, 201)


@app.route("/patients/<int:idPatient>", methods=["PUT"])
@jwt_required()
def update_patient(idPatient):
    data = request.json

    if not data:
        return format_response({"error": "No input data provided"}, 400)

    if "name" not in data or "age" not in data:
        return format_response({"error": "Missing fields"}, 400)

    if not isinstance(data["age"], int):
        return format_response({"error": "Age must be an integer"}, 400)

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE patient
        SET name = %s, age = %s
        WHERE idPatient = %s
    """, (data["name"], data["age"], idPatient))
    mysql.connection.commit()

    affected = cur.rowcount
    cur.close()

    if affected == 0:
        return format_response({"error": "Patient not found"}, 404)

    return format_response({"message": "Patient updated"})


@app.route("/patients/<int:idPatient>", methods=["DELETE"])
@jwt_required()
def delete_patient(idPatient):
    cur = mysql.connection.cursor()

    try:
        cur.execute("""
            DELETE FROM doctors_has_patient
            WHERE Patient_idPatient = %s
        """, (idPatient,))

        cur.execute("""
            DELETE FROM patient
            WHERE idPatient = %s
        """, (idPatient,))

        mysql.connection.commit()

        if cur.rowcount == 0:
            return format_response({"error": "Patient not found"}, 404)

        return format_response({"message": "Patient deleted successfully"})

    except Exception as e:
        mysql.connection.rollback()
        return format_response({"error": str(e)}, 500)

    finally:
        cur.close()


# -------------------------
# SEARCH
# -------------------------
@app.route("/patients/search", methods=["GET"])
def search_patients():
    name = request.args.get("name")
    age = request.args.get("age")

    query = """
        SELECT p.idPatient, p.name, p.age,
               d.diagnosis_name, d.category
        FROM patient p
        JOIN diagnosis d ON p.Diagnosis_idDiagnosis = d.idDiagnosis
        WHERE 1=1
    """
    params = []

    if name:
        query += " AND p.name LIKE %s"
        params.append(f"%{name}%")

    if age:
        query += " AND p.age = %s"
        params.append(age)

    data = execute_query(query, tuple(params))

    if not data:
        return format_response({"error": "No matching records found"}, 404)

    return format_response(data)


# -------------------------
# PATIENT DOCTORS
# -------------------------
@app.route("/patients/<int:idPatient>/doctors", methods=["GET"])
def get_patient_doctors(idPatient):
    data = execute_query("""
        SELECT d.iddoctors, d.doctor_name, d.specialization
        FROM doctors d
        JOIN doctors_has_patient dhp
        ON d.iddoctors = dhp.doctors_iddoctors
        WHERE dhp.Patient_idPatient = %s
    """, (idPatient,))

    if not data:
        return format_response({"error": "No doctors found"}, 404)

    return format_response(data)


# -------------------------
# DOCTORS & DIAGNOSIS
# -------------------------
@app.route("/doctors", methods=["GET"])
def get_doctors():
    return format_response(execute_query("SELECT * FROM doctors"))


@app.route("/diagnosis", methods=["GET"])
def get_diagnosis():
    return format_response(execute_query("SELECT * FROM diagnosis"))


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
