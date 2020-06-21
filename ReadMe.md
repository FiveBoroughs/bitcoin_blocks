# Bitcoin Blocks to telegram

Simply waits for new Bitcoin Blocks and forwards them to you on telegram

Currently forwarding to https://t.me/Bitcoin_Blocks

Useful for when you're waiting for that transaction to go through

```bash
cp config.sample.yml config.yml
```

Update the details inside `config.yml` :

* Blockcypher token here https://accounts.blockcypher.com/tokens
* Telegram Token here https://t.me/botfather
* Telegram channel id https://api.telegram.org/botYOURTOKENHERE/getUpdates

```bash
virtualenv bitcoin_blocks_venv -p $(which python3)
source bitcoin_blocks_venv/bin/activate
pip install -r requirements.txt
python BitcoinBlocks.py
```
