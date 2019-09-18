
# CreateTB

Discord Bot

## prerequisites

- discord app
- discord bot token key
- python 3.7
- youtube-data-api key
- docker
- docker-compose

## How to use

- Clone or download this repository.
- Create .env file  under the top of the project.
  - You can copy or rename example.env

```env
REDIS_URL=redis://redis
BOT_TOKEN=<DISCORD_BOT_TOKEN_HERE>
GOOGLE_API_KEY=<GOOGLE_API_KEY_HERE>
PREFIX=$
```

- Let's Start Bot
  - under the top of the project
  - enter this command

```bash
docker-compose up -d --build
```

and

```bash
docker-compose run workspace python MainTB.py
```

If you get a response below, Your bot will have logged in your guild successfully.

```bash
Logged in as
bot name
bot id
----message----
```

## How to custom

If you want to change command prefix, change the value of prefix in .env

For example, If you want to change prefix from "$" to "#", change .env from

```:from
PREFIX=$
```

to

```:to
PREFIX=#
```
