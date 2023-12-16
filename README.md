A simple async RCON library for Ark. Inspired by https://github.com/scottjones4k/ark_rcon

This RCON client is designed to work with Ark SE servers with the intention of integrating its features into a
Discord bot, or other asynchronous project.

Features:
1. saveworld - ability to send a save world command to your Ark SE server.
2. broadcast - Send a global broadcast message to your server.
3. chat - send chats to the global channel as server, can provide a username
4. chat history - *WIP* pull the chat history from the server



### Basic Usage

Getting a list of online players:
```py
import asyncio

from async_arkon import Client

host = "192.168.1.200"
port = 27015
password = "my_super_secret_admin_password"


async def main():
    async with Client(host=host, port=port, password=password) as client:
        players = await client.fetch_online_players()

        print(players)


asyncio.run(main())

```
This can also be done without using async context managers.
```py
import asyncio

from async_arkon import Client

host = "192.168.1.200"
port = 27015
password = "my_super_secret_admin_password"


async def main():

    client = Client(host=host, port=port, password=password)
    await client.login()

    players = await client.fetch_online_players()
    await client.close()

    print(players)


asyncio.run(main())

```

### Links:
- [docs](https://dlchamp.github.io/async_arkon/)
