from datetime import datetime, timezone

from app.extensions import db


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
        }


class Position(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    asset_symbol = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    avg_price = db.Column(db.Float, nullable=False, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'asset_symbol': self.asset_symbol,
            'quantity': self.quantity,
            'avg_price': self.avg_price,
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    asset_symbol = db.Column(db.String(20), nullable=False)
    side = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='executed')
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'asset_symbol': self.asset_symbol,
            'side': self.side,
            'quantity': self.quantity,
            'price': self.price,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }