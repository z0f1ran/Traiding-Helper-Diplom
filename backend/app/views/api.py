from flask import Blueprint, jsonify, request

from app.controllers import TradingController


api_bp = Blueprint('api', __name__, url_prefix='/api')
controller = TradingController()


def success_response(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


def error_response(message, status_code=400):
    return jsonify({'status': 'error', 'message': message}), status_code


@api_bp.get('/health')
def health():
    return success_response({'service': 'crypto-trading-api', 'state': 'ok'})


@api_bp.get('/assets')
def assets():
    return success_response(controller.get_assets())


@api_bp.get('/portfolio')
def portfolio():
    return success_response(controller.get_portfolio())


@api_bp.get('/orders')
def orders():
    return success_response(controller.list_orders())


@api_bp.post('/orders')
def create_order():
    payload = request.get_json(silent=True) or {}
    try:
        order = controller.create_order(payload)
        return success_response(order, 201)
    except ValueError as exc:
        return error_response(str(exc), 400)