#!/usr/bin/env python3
# pyright: reportOptionalSubscript=false

from flask import Flask, request, g, jsonify
from flask_cors import CORS
from decorators.error import catch_errors
from classes.Error import AccessError, InputError

from services.auth import auth_register_user, auth_login_user, auth_logout_user
from services.game import (
    game_update,
    game_getall,
    game_mutate,
    game_session_results,
    game_session_status,
)
from services.player import (
    player_add,
    player_retrieve_status,
    player_get_question,
    player_submit_answers,
    player_get_answers,
    get_player_results, 
)

from core.auth_core import authorise_user
import re

IGNORE_AUTH_PATHS = [
    "/admin/auth/register",
    "/admin/auth/login",
]
GAME_PLAY_REGEX_PATH = r"^/play/"   

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def bypass_auth_check(request):
    if request.path in IGNORE_AUTH_PATHS:
        return True
    elif re.match(GAME_PLAY_REGEX_PATH, request.path):
        return True

    return False

@app.before_request
@catch_errors
def flask_middle_auth():
    if request.method == "OPTIONS":
        return "", 200

    if bypass_auth_check(request):
        return

    # TODO: Extract and validate session token from Authorization header
    # TODO: Extract and validate CSRF token from X-CSRF-Token header
    # TODO: Implement authorization check for protected routes
    session_token = request.headers.get("Authorization")

    if not isinstance(session_token, str):
        raise AccessError("Invalid session token")
    session_token = session_token.strip()
    if session_token == "":
        raise AccessError("Invalid session token")
    
    csrf_token = request.headers.get("X-CSRF-Token")

    if not authorise_user(session_token, csrf_token):
        raise AccessError("Invalid session token")
    
    # TODO: Store validated tokens in Flask's g object for request context
    g.session_token = session_token

@app.route("/admin/auth/register", methods=["POST"])
@catch_errors
def admin_auth_register():
    data = request.json
    if not data or "email" not in data or "password" not in data or "name" not in data:
        raise InputError("Missing required fields: email, password, and name")
    email = data["email"]
    password = data["password"]
    name = data["name"]

    session_token, csrf_token = auth_register_user(email, password, name)
    # TODO: Include CSRF token in response 
    #response = jsonify({"session_token": session_token, "csrf_token": csrf_token})
    #response.set_cookie("session_token", session_token, httponly=True, samesite="Lax", secure=True)
    #response.set_cookie("csrf_token", csrf_token, httponly=True, samesite="Lax", secure=True)
    response = jsonify({"csrf_token": csrf_token})
    response.set_cookie("session_token", session_token, httponly=True, samesite="Lax", secure=True)
    return response, 200


@app.route("/admin/auth/login", methods=["POST"])
@catch_errors
def admin_auth_login():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        raise InputError("Missing required fields: email and password")
    email = data["email"]
    password = data["password"]

    session_token, csrf_token = auth_login_user(email, password)
    # TODO: Include CSRF token in response
    #response = jsonify({"session_token": session_token, "csrf_token": csrf_token})
    #response.set_cookie("session_token", session_token, httponly=True, samesite="Lax", secure=True)
    #response.set_cookie("csrf_token", csrf_token, httponly=True, samesite="Lax", secure=True)
    response = jsonify({"csrf_token": csrf_token})
    response.set_cookie("session_token", session_token, httponly=True, samesite="Lax", secure=True)

    return response, 200


@app.route("/admin/auth/logout", methods=["POST"])
@catch_errors
def admin_auth_logout():
    auth_logout_user(g.session_token)
    return {}, 200


@app.route("/admin/games", methods=["GET"])
@catch_errors
def admin_get_games():
    admin_games_list = game_getall(g.session_token)
    return {"games": admin_games_list}, 200


@app.route("/admin/games", methods=["PUT"])
@catch_errors
def admin_put_games():
    data = request.json
    if not data or "games" not in data:
        raise InputError("Missing required field: games")
    updated_games_list = data["games"]
    game_update(updated_games_list, g.session_token)

    return {}, 200


@app.route("/admin/game/<game_id>/mutate", methods=["POST"])
@catch_errors
def admin_mutate_game(game_id):
    data = request.json
    if not data or "mutationType" not in data:
        raise InputError("Missing required field: mutationType")
    mutation_type = data["mutationType"]
    mutate = game_mutate(game_id, mutation_type, g.session_token)
    return {"data": mutate}, 200


@app.route("/admin/session/<session_id>/status", methods=["GET"])
@catch_errors
def admin_get_game_session_status(session_id):
    status = game_session_status(session_id)
    return {"results": status}, 200


@app.route("/admin/session/<session_id>/results", methods=["GET"])
@catch_errors
def admin_get_game_session_results(session_id):
    results = game_session_results(session_id)
    return {"results": results}, 200


@app.route("/play/join/<session_id>", methods=["POST"])
@catch_errors
def player_join_game_session(session_id):
    data = request.json
    if not data or "name" not in data:
        raise InputError("Missing required field: name")
    name = data["name"]
    player_id = player_add(session_id, name)
    return {"playerId": player_id}, 200


@app.route("/play/<player_id>/status", methods=["GET"])
@catch_errors
def player_status(player_id):
    status = player_retrieve_status(player_id)
    return {"started": status}, 200


@app.route("/play/<player_id>/question", methods=["GET"])
@catch_errors
def player_question_details(player_id):
    question = player_get_question(player_id)
    return {"question": question}, 200


@app.route("/play/<player_id>/answer", methods=["PUT"])
@catch_errors
def player_question_answer_submit(player_id):
    data = request.json
    if not data or "answers" not in data:
        raise InputError("Missing required field: answers")
    answers = data["answers"]
    player_submit_answers(player_id, answers)
    return {}, 200


@app.route("/play/<player_id>/answer", methods=["GET"])
@catch_errors
def player_show_correct_answer(player_id):
    answers = player_get_answers(player_id)
    return {"answers": answers}, 200


@app.route("/play/<player_id>/results", methods=["GET"])
@catch_errors
def player_results(player_id):
    results = get_player_results(player_id)
    return {"results": results}, 200


@app.route("/quiz/template", methods=["GET"])
@catch_errors
def get_quiz_template():
    template = {
        "name": "Sample Quiz Template",
        "questions": [
            {
                "id": "q1",
                "text": "Sample Single Choice Question",
                "type": "Single-Choice",
                "summary": "Choose one correct answer",
                "visual": "",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correctAnswers": ["Option A"],
                "duration": 60,
                "points": 10
            },
            {
                "id": "q2", 
                "text": "Sample Multiple Choice Question",
                "type": "Multi-Choice",
                "summary": "Choose all correct answers",
                "visual": "",
                "options": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
                "correctAnswers": ["Choice 1", "Choice 3"],
                "duration": 90,
                "points": 15
            },
            {
                "id": "q3",
                "text": "Sample Judgement Question",
                "type": "Judgement",
                "summary": "Provide the correct answer",
                "visual": "",
                "options": [],
                "correctAnswers": ["Correct Answer"],
                "duration": 45,
                "points": 5
            }
        ]
    }
    return template, 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)
