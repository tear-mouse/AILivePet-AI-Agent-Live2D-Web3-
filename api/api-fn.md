## 接口文档：GET /sol

### 请求说明
- 方法：GET
- 路径：`/sol`
- 参数：
  - `address`（string，可选）：查询的钱包地址

### 示例请求
```
GET /sol?address=7nyhQzUMjcj7fEnG5WqMbTbC8e3Z5m6fub2NDAu7E2Nz
```

### 返回结构（JSON）
```json
{
  "message": {
    "account": {
      "余额": 0.074049826
    },
    "token": {
      "数量": 1,
      "当前持有": [
        {
          "address": "Norannmx2UceenktR1r2c3DF3zRqGNHoAhtQi3Cnp79",
          "tokenAddress": "Grass7B4RdKfBCjTKgSqnXkqjwiGvQyFbuSCUJr3XXjs",
          "amount": 25250000000,
          "decimals": 9,
          "owner": "7nyhQzUMjcj7fEnG5WqMbTbC8e3Z5m6fub2NDAu7E2Nz",
          "reputation": "neutral",
          "priceUsdt": 1.63,
          "tokenName": "Grass",
          "tokenSymbol": "GRASS",
          "tokenIcon": "https://static.grassfoundation.io/grass-logo.png",
          "tokenType": "token",
          "balance": 25.25,
          "value": 41.1575
        }
      ]
    }
  }
}
```

### 字段说明

#### account
- `余额`：float，账户原生 SOL 余额

#### token
- `数量`：int，Token 数量
- `当前持有`：list，每个元素为一个 Token 对象，字段如下：

| 字段 | 类型 | 说明 |
|------|------|------|
| `address` | string | Token 账户地址 |
| `tokenAddress` | string | Token 合约地址 |
| `amount` | int | 原始数量（未除以 decimals） |
| `decimals` | int | 精度 |
| `owner` | string | 持有者地址 |
| `reputation` | string | 声誉评分，如 neutral |
| `priceUsdt` | float | 价格，单位 USDT |
| `tokenName` | string | 名称 |
| `tokenSymbol` | string | 符号缩写 |
| `tokenIcon` | string | 图标 URL |
| `tokenType` | string | 类型，如 token/nft |
| `balance` | float | 可读 Token 数量（浮点） |
| `value` | float | 折算 USD 价值 |
