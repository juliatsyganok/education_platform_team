from flask import Blueprint, jsonify

ugc_bp = Blueprint("ugc", __name__, url_prefix="/ugc")


@ugc_bp.route("/", methods=["GET"])
def list_ugc():
    return jsonify({"status": "ok", "data": [], "message": "Список UGC"})


@ugc_bp.route("/", methods=["POST"])
def create_ugc():
    return jsonify({"status": "ok", "message": "Создание UGC — в разработке"})