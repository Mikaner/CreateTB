# CreateTB
* Discord Bot

## prerequisites
- discordapp
- discord bot token key
- python 3.7
- youtube-data-api key
- 

## Development environment for TB 
* python 3.7.3
* aiohttp 3.5.4
* async-timeout 3.0.1
* attrs 19.1.0
* beautifulsoup4 4.7.1
* cachetools 3.1.0
* certifi 2019.3.9
* cffi 1.12.2
* chardet 3.0.4
* discord 1.0.1
* discord.py 1.1.1
* google-api-python-client 1.7.9
* google-auth 1.6.3
* google-auth-httplib2 0.0.3
* httplib2 0.12.1
* idna 2.8
* multidict 4.5.2
* pafy 0.5.4
* pyasn1 0.4.5
* pyasn1-modules 0.2.4
* pycparser 2.19
* PyNaCl 1.2.1
* requests 2.21.0
* rsa 4.0
* six 1.12.0
* soupsieve 1.9
* uritemplate 3.0.0
* urllib3 1.24.1
* websockets 6.0
* yarl 1.3.0
* youtube-dl 2019.5.20

## How to use
* Clone or download this repository.
* Create .env file  under the top of the project.
  * You can copy or rename example.env
```
{
    "token":"",
    "APIKey":"",
    "prefix":"$"
}
```
* If you do not want to pollute the environment, use a virtual environment such as venv, pyenv, pipenv or others.
* Create environment.
```
pip install --upgrade pip
pip install discord.py[voice] google-api-python-client youtube-dl pafy
```
* Execution command under this.
```bash
python MainTB.py
```
or
```bash
python3 MainTB.py
```
or
```bash
py -3 MainTB.py
```
* If you get a response below, Your bot will have logged in your guild successfully.
```
Logged in as
bot name
bot id
----message----
```

## How to custom
* This bot can change the prefix. Do you want? In that case, change item of prefix in config.json file.
```:from
{
    "token":"",
    "APIKey":"",
    "prefix":"$"
}
```
```:to
{
    "token":"",
    "APIKey":"",
    "prefix":"&"
}
```