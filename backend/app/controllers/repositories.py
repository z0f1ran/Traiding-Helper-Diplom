from app.extensions import db
from app.models import Asset, Position, Order


class AssetRepository:
    def get_all(self):
        return Asset.query.order_by(Asset.symbol.asc()).all()

    def get_by_symbol(self, symbol):
        return Asset.query.filter_by(symbol=symbol).first()

    def create(self, symbol, name, price):
        asset = Asset(symbol=symbol, name=name, price=price)
        db.session.add(asset)
        return asset


class PositionRepository:
    def get_all(self):
        return Position.query.order_by(Position.asset_symbol.asc()).all()

    def get_by_symbol(self, symbol):
        return Position.query.filter_by(asset_symbol=symbol).first()

    def create(self, symbol, quantity, avg_price):
        position = Position(asset_symbol=symbol, quantity=quantity, avg_price=avg_price)
        db.session.add(position)
        return position

    def delete(self, position):
        db.session.delete(position)


class OrderRepository:
    def get_all(self):
        return Order.query.order_by(Order.created_at.desc()).all()

    def create(self, asset_symbol, side, quantity, price, status='executed'):
        order = Order(
            asset_symbol=asset_symbol,
            side=side,
            quantity=quantity,
            price=price,
            status=status,
        )
        db.session.add(order)
        return order