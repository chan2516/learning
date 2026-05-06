
from __future__ import annotations

import json
import os
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional during bootstrap
    load_dotenv = None


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"
ENV_FILE = BASE_DIR / ".env"


if load_dotenv is not None:
    load_dotenv(ENV_FILE)


def get_mongo_collection():
    """Create a MongoDB collection using environment settings."""
    mongo_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONGODB_DATABASE", "first_project")
    collection_name = os.getenv("MONGODB_COLLECTION", "submissions")

    if not mongo_uri:
        raise RuntimeError(
            "MONGODB_URI is not set. Add your MongoDB Atlas connection string to the environment."
        )

    client = MongoClient(mongo_uri)
    database = client[database_name]
    return database[collection_name]


def load_data() -> list[dict]:
    """Load a JSON list from the backend file."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    if not isinstance(data, list):
        raise ValueError("data.json must contain a JSON list.")

    return data


def filter_data(records: list[dict], query: str) -> list[dict]:
    """Return records whose text fields match the search query."""
    normalized_query = query.strip().lower()
    if not normalized_query:
        return records

    filtered_records: list[dict] = []
    for record in records:
        values = (str(value).lower() for value in record.values())
        if any(normalized_query in value for value in values):
            filtered_records.append(record)

    return filtered_records


def build_submission_document(form_data: dict[str, str]) -> dict[str, str]:
    """Build a clean MongoDB document from submitted form values."""
    return {
        "name": form_data.get("name", "").strip(),
        "email": form_data.get("email", "").strip(),
        "message": form_data.get("message", "").strip(),
    }


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    @app.get("/")
    def index() -> str:
        search_query = request.args.get("q", "")
        records = filter_data(load_data(), search_query)
        return render_template(
            "index.html",
            records=records,
            search_query=search_query,
            form_data={"name": "", "email": "", "message": ""},
            error_message=None,
        )

    @app.post("/submit")
    def submit() -> str:
        search_query = request.form.get("q", "")
        records = filter_data(load_data(), search_query)
        form_data = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "message": request.form.get("message", "").strip(),
        }

        try:
            if not form_data["name"] or not form_data["email"] or not form_data["message"]:
                raise ValueError("All fields are required.")

            collection = get_mongo_collection()
            collection.insert_one(build_submission_document(form_data))
        except Exception as error:  # noqa: BLE001 - return the exact failure to the form
            return render_template(
                "index.html",
                records=records,
                search_query=search_query,
                form_data=form_data,
                error_message=str(error),
            ), 400

        return redirect(url_for("success"))

    @app.get("/success")
    def success() -> str:
        return render_template("success.html")

    @app.get("/api")
    def api() -> tuple:
        return jsonify(load_data())

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)