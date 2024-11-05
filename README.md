# BTC Pair Order Block Monitoring System

This project monitors order block levels for BTC trading pairs on Binance. It uses GitHub Actions to automate data updates and price checks, sending alerts via Telegram when an asset reaches a specified order block level.

## Directory Structure

```plaintext
.
├── .github
│   └── workflows
│       ├── update_raw_data.yml               # Updates raw BTC pair data from Binance
│       ├── update_order_block_data.yml       # Detects order blocks from raw data
│       └── check_order_block_price.yml       # Checks price against order blocks and sends alerts
├── data
│   ├── raw                                   # Stores raw 4-hour data for each BTC pair
│   └── orderblocks                           # Stores detected order blocks for each BTC pair
└── scripts
    ├── update_raw_data.py                    # Script to fetch and update raw data
    ├── update_order_block_data.py            # Script to detect order blocks from raw data
    └── check_order_block_price.py            # Script to check if prices have reached order block levels
```

## Setting Up Secrets
### Binance API Key and Secret
Create an API key in Binance under API Management.  
In GitHub, go to Settings > Secrets and variables > Actions, and add:  
`BINANCE_API_KEY`  
`BINANCE_API_SECRET`

### Telegram Bot Token and Chat ID
Create a Telegram bot using BotFather to obtain a Token.
Start a chat with your bot and retrieve your Chat ID using:

```bash
https://api.telegram.org/bot<YourBotToken>/getUpdates
```

In GitHub, add the following secrets:  
`TELEGRAM_TOKEN`  
`TELEGRAM_CHAT_ID`