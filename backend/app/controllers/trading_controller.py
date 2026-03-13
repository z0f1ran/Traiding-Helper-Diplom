from app.extensions import db
from app.controllers.repositories import AssetRepository, PositionRepository, OrderRepository


class TradingController:
    def __init__(self):
        self.asset_repository = AssetRepository()
        self.position_repository = PositionRepository()
        self.order_repository = OrderRepository()

    def seed_data(self):
        if self.asset_repository.get_all():
            return

        self.asset_repository.create('BTCUSDT', 'Bitcoin', 68000.0)
        self.asset_repository.create('ETHUSDT', 'Ethereum', 3500.0)
        self.asset_repository.create('SOLUSDT', 'Solana', 160.0)
        self.position_repository.create('BTCUSDT', 0.1, 64000.0)
        db.session.commit()

    def get_assets(self):
        assets = self.asset_repository.get_all()
        return [asset.to_dict() for asset in assets]

    def get_portfolio(self):
        assets = {asset.symbol: asset for asset in self.asset_repository.get_all()}
        positions = self.position_repository.get_all()
        items = []
        total_value = 0.0

        for position in positions:
            current_price = assets.get(position.asset_symbol).price if assets.get(position.asset_symbol) else 0.0
            market_value = position.quantity * current_price
            pnl = (current_price - position.avg_price) * position.quantity
            total_value += market_value
            items.append({
                **position.to_dict(),
                'current_price': current_price,
                'market_value': market_value,
                'pnl': pnl,
            })

        return {
            'positions': items,
            'total_value': total_value,
        }

    def list_orders(self):
        orders = self.order_repository.get_all()
        return [order.to_dict() for order in orders]

    def create_order(self, payload):
        symbol = str(payload.get('symbol', '')).upper().strip()
        side = str(payload.get('side', '')).lower().strip()
        quantity = payload.get('quantity')

        if not symbol or side not in {'buy', 'sell'}:
            raise ValueError('Некорректные параметры ордера')

        try:
            quantity = float(quantity)
        except (TypeError, ValueError):
            raise ValueError('Количество должно быть числом')

        if quantity <= 0:
            raise ValueError('Количество должно быть больше 0')

        asset = self.asset_repository.get_by_symbol(symbol)
        if not asset:
            raise ValueError(f'Инструмент {symbol} не найден')

        position = self.position_repository.get_by_symbol(symbol)

        if side == 'buy':
            if position:
                new_quantity = position.quantity + quantity
                if new_quantity <= 0:
                    raise ValueError('Некорректный итоговый объём позиции')
                position.avg_price = ((position.quantity * position.avg_price) + (quantity * asset.price)) / new_quantity
                position.quantity = new_quantity
            else:
                self.position_repository.create(symbol, quantity, asset.price)
        else:
            if not position or position.quantity < quantity:
                raise ValueError('Недостаточный объём для продажи')
            position.quantity -= quantity
            if position.quantity == 0:
                self.position_repository.delete(position)

        order = self.order_repository.create(
            asset_symbol=symbol,
            side=side,
            quantity=quantity,
            price=asset.price,
        )
        db.session.commit()
        return order.to_dict()