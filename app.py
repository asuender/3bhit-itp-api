from flask import Flask, request, jsonify
import webuntis

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    untis = webuntis.Session(
        username=username,
        password=password,
        server="neilo.webuntis.com",
        school="tgm",
        useragent="E-Sitzplaner"
    )

    try:
        untis.login()

        classes = [kl.name for kl in untis.klassen()]
        students = [st.full_name for st in untis.students()]
        rooms = [r.name for r in untis.rooms()]

        untis.logout()

        return jsonify({
            "code": 0,
            "data": {
                "classes": classes,
                "students": students,
                "rooms": rooms
            }
        })

    except webuntis.errors.BadCredentialsError:
        return jsonify({"code": 1, "message": "Invalid username or password."})

    except Exception as e:
        return jsonify({"code": 2, "message": "An error occurred during the login procedure.", "error": e})
