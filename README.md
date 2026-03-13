# Execution Flow

## AI plan creation stage ↓

1. `conversation/views.py`
2. `conversation/services.py`
3. `llm/orchestrator.py`
4. `llm/council.py`
5. `lnn/judge.py`

## Trading stage ↓

1. `execution/pipeline.py`
2. `blockchain/signer.py`
3. `blockchain/registry.py`
4. `risk/router.py`
5. `monitoring/reputation.py`

## API Endpoints

### Chat

**POST** `/api/chat/`

Request body:

```json
{
  "conversation_id": "uuid",
  "message": "Swap 1500 USDT to ETH if volatility is acceptable"
}
```

### Approve Trade

**POST** `/api/trade/approve/`

Request body:

```json
{
  "plan": {
    "...": "..."
  },
  "user_address": "0x...",
  "chain_id": 1
}
```

## Trade platform

```json
https://api.dex-trade.com/v1/public/symbols
https://api.dex-trade.com/v1/public/ticker?pair=BTCUSD
```

## OpenAI

```json
https://developers.openai.com/api/reference/overview

and 

https://gemini.google.com/
https://github.com/googleapis/python-genai
```

## Required file for project

```json
\trading_agent\.env

SECRET_KEY = ""
DEBUG = 1
ALLOWED_HOSTS = "localhost 127.0.0.1"
```

## Requirments

```json
\trading_agent\requirements.txt

pip install -r .\requirements.txt
```
