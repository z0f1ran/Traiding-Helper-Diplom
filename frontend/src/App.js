import { useEffect, useMemo, useState } from 'react';

const SCREENS = [
  { id: 'dashboard', label: 'Дашборд' },
  { id: 'markets', label: 'Рынок' },
  { id: 'trade', label: 'Торговля' },
  { id: 'portfolio', label: 'Портфель' },
  { id: 'orders', label: 'Ордера' },
];

function App() {
  const [activeScreen, setActiveScreen] = useState('dashboard');
  const [assets, setAssets] = useState([]);
  const [portfolio, setPortfolio] = useState({ positions: [], total_value: 0 });
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({ symbol: 'BTCUSDT', side: 'buy', quantity: '0.01' });

  const dashboardStats = useMemo(() => {
    const bestAsset = [...assets].sort((a, b) => b.price - a.price)[0];
    return {
      assetsCount: assets.length,
      positionsCount: portfolio.positions.length,
      ordersCount: orders.length,
      bestAsset,
    };
  }, [assets, portfolio.positions.length, orders]);

  const request = async (url, options = {}) => {
    const response = await fetch(url, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    });

    const body = await response.json();
    if (!response.ok || body.status !== 'success') {
      throw new Error(body.message || 'Ошибка запроса');
    }
    return body.data;
  };

  const loadAll = async () => {
    setLoading(true);
    setError('');
    try {
      const [assetsData, portfolioData, ordersData] = await Promise.all([
        request('/api/assets'),
        request('/api/portfolio'),
        request('/api/orders'),
      ]);
      setAssets(assetsData);
      setPortfolio(portfolioData);
      setOrders(ordersData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  const submitOrder = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      await request('/api/orders', {
        method: 'POST',
        body: JSON.stringify({
          symbol: form.symbol,
          side: form.side,
          quantity: Number(form.quantity),
        }),
      });
      await loadAll();
      setActiveScreen('orders');
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>Crypto Trading Platform</h1>
        <button className="secondary" onClick={loadAll} disabled={loading}>
          Обновить данные
        </button>
      </header>

      <nav className="navigation">
        {SCREENS.map((screen) => (
          <button
            key={screen.id}
            className={activeScreen === screen.id ? 'active' : ''}
            onClick={() => setActiveScreen(screen.id)}
          >
            {screen.label}
          </button>
        ))}
      </nav>

      {error ? <div className="error">Ошибка: {error}</div> : null}
      {loading ? <div className="loading">Загрузка...</div> : null}

      <main className="screen-wrapper">
        {activeScreen === 'dashboard' && (
          <section className="grid two">
            <article className="card">
              <h2>Сводка проекта</h2>
              <p>Инструментов: {dashboardStats.assetsCount}</p>
              <p>Позиции: {dashboardStats.positionsCount}</p>
              <p>Ордера: {dashboardStats.ordersCount}</p>
              <p>Стоимость портфеля: ${portfolio.total_value.toFixed(2)}</p>
            </article>
            <article className="card">
              <h2>Лидер по цене</h2>
              {dashboardStats.bestAsset ? (
                <>
                  <p>{dashboardStats.bestAsset.name}</p>
                  <p>{dashboardStats.bestAsset.symbol}</p>
                  <p>${dashboardStats.bestAsset.price.toFixed(2)}</p>
                </>
              ) : (
                <p>Данные недоступны</p>
              )}
            </article>
          </section>
        )}

        {activeScreen === 'markets' && (
          <section className="card">
            <h2>Рынок</h2>
            <table>
              <thead>
                <tr>
                  <th>Символ</th>
                  <th>Название</th>
                  <th>Цена</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((asset) => (
                  <tr key={asset.id}>
                    <td>{asset.symbol}</td>
                    <td>{asset.name}</td>
                    <td>${asset.price.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}

        {activeScreen === 'trade' && (
          <section className="card">
            <h2>Создание ордера</h2>
            <form onSubmit={submitOrder} className="trade-form">
              <label>
                Инструмент
                <select
                  value={form.symbol}
                  onChange={(event) => setForm((prev) => ({ ...prev, symbol: event.target.value }))}
                >
                  {assets.map((asset) => (
                    <option key={asset.id} value={asset.symbol}>
                      {asset.symbol}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Сторона
                <select
                  value={form.side}
                  onChange={(event) => setForm((prev) => ({ ...prev, side: event.target.value }))}
                >
                  <option value="buy">Покупка</option>
                  <option value="sell">Продажа</option>
                </select>
              </label>

              <label>
                Количество
                <input
                  type="number"
                  min="0"
                  step="0.0001"
                  value={form.quantity}
                  onChange={(event) => setForm((prev) => ({ ...prev, quantity: event.target.value }))}
                />
              </label>

              <button type="submit" disabled={loading}>
                Отправить ордер
              </button>
            </form>
          </section>
        )}

        {activeScreen === 'portfolio' && (
          <section className="card">
            <h2>Портфель</h2>
            {portfolio.positions.length === 0 ? (
              <p>Позиции отсутствуют</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Символ</th>
                    <th>Количество</th>
                    <th>Средняя цена</th>
                    <th>Текущая цена</th>
                    <th>Стоимость</th>
                    <th>PnL</th>
                  </tr>
                </thead>
                <tbody>
                  {portfolio.positions.map((position) => (
                    <tr key={position.id}>
                      <td>{position.asset_symbol}</td>
                      <td>{position.quantity.toFixed(4)}</td>
                      <td>${position.avg_price.toFixed(2)}</td>
                      <td>${position.current_price.toFixed(2)}</td>
                      <td>${position.market_value.toFixed(2)}</td>
                      <td>{position.pnl >= 0 ? '+' : ''}${position.pnl.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        )}

        {activeScreen === 'orders' && (
          <section className="card">
            <h2>История ордеров</h2>
            {orders.length === 0 ? (
              <p>Ордера пока не созданы</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Инструмент</th>
                    <th>Сторона</th>
                    <th>Количество</th>
                    <th>Цена</th>
                    <th>Статус</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((order) => (
                    <tr key={order.id}>
                      <td>{order.id}</td>
                      <td>{order.asset_symbol}</td>
                      <td>{order.side}</td>
                      <td>{order.quantity}</td>
                      <td>${order.price.toFixed(2)}</td>
                      <td>{order.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;