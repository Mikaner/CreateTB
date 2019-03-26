from Replay import Replay
from datetime import datetime as dt
from discord.ext import commands
import discord
import json
import random
import re

client = discord.Client()
rp = Replay()
with open('./config/config.json','r',1,encoding='utf-8') as tokenCode:
	token = json.load(tokenCode)


channelID = [520936539757215755, 522337508571217931, 437952848097968130]
tyat = discord.Object(id=520936539757215755)#437952848097968130)
menshon = discord.Object(id=520808347449032705)
voiceChannelID = 520936539757215757#'437952848097968132'
channelObj = [None]*len(channelID)
voiceChannel = client.get_channel(voiceChannelID)

for i in range(len(channelID)):
	channelObj[i] = discord.Object(id=channelID[i])

ahokusa = ['わかる','わかんないや','思わないかな～','いいんじゃない？','んーノーコメントでっ！']


@client.event
async def on_ready():
	inTime = dt.now()
	print('Logged in as')
	print(client)
#	print(client.guilds)
	print(client.user.name)
	print(client.user.id)
	print(inTime)
	print('---message---')
	if inTime.hour < 4:
		msg = '夜遅くにこっそり...'
	elif inTime.hour < 12:
		msg = 'おはよーございまーす！'
	elif inTime.hour < 19:
		msg = 'こんにちわー！'
	else:
		msg = 'こんばんはー'
	#await client.send_message(discord.Object(id=554226307194421261), '( ͡° ͜ʖ ͡°)')
	#await client.send_message(tyat, f'てすとだよー {ユーザーにメンションしたい.user.menshon}')
	#for i in range(len(channelObj)):
		#await client.send_message(channelObj[i], msg)


@client.event
async def on_message(message):
	voice = None
	if client.user == message.author:
		return

	if message.content.startswith('\TBexit'):
		exit()
	
	
	wer = re.compile(u'TB、(.+)の天気').search(message.content)
	tb = re.compile(u'TB').search(message.content)
	u = re.compile(u'占い').search(message.content)
	uranai = re.compile(u'占って').search(message.content)
	omikuji = re.compile(u'おみくじ').search(message.content)
	thinkSo = re.compile(u'ね？そう思うでしょTBちゃん？').search(message.content)
	thanks = re.compile(u'ありがとう').search(message.content)
	dice = re.compile(u'/d (.+)d(.+)').match(message.content)
	sleep = re.compile(u'おやすみ').search(message.content)
	TBplay = re.compile(u'/TBplay (.+)').match(message.content)
	notPlay = re.compile(u'/TBnotPlay').match(message.content)
	helpCommand = re.compile(u'/TBhelp').match(message.content)
	musicJoin = re.compile(u'!j').match(message.content)
	musicPlay = re.compile(u'!TBplay (.+)').match(message.content)

	if message.content.startswith('Iowa') or message.content.startswith('iowa') or message.content.startswith('あいおわ') or message.content.startswith('アイオワ'):
		await client.send_message(message.channel, 'MotivationNotFoundException')

	if TBplay:
		await client.change_presence(game=discord.Game(name=TBplay.group(1)))
	if notPlay:
		await client.change_presence(game=None)

	if helpCommand:
		reply = rp.TBhelp()
		await client.send_message(message.channel, reply)

	if thanks and tb:
		reply = 'どういたしまして！'
		await client.send_message(message.channel,reply)

	if wer:#TB、*の天気が入っていた場合
		# messageに今日or明日or明後日が入っているか判断。入ってたら各文それを入れる。ちなみに今日が一番強い
		day = 0 if '今日' in message.content else 1 if '明日' in message.content else 2 if '明後日' in message.content else -1
		now = dt.now()
		informationFlag = True if 'どう' in message.content or '情報' in message.content else False

		reply = rp.weatherReport(wer.group(1), day, informationFlag, now.hour)

		await client.send_message(message.channel,reply)

	elif message.content.startswith('TBかわいい'):# 始めからTBかわいいが入っていた場合
		reply = rp.shyTB()
		await client.send_message(message.channel, reply)

	elif thinkSo:# ね？そう思うでしょTBちゃん？が入っていた場合
		r = random.randrange(0, len(ahokusa))
		reply = ahokusa[r]
		await client.send_message(message.channel, reply)

	elif message.content.startswith('TB') or message.content.startswith('てぃーびー') or message.content.startswith('Hey TB') or client.user.id in message.content:# 始めに名前が入っていた場合
		reply = f'{message.author.mention} 呼んだ？'# message(受け取った文字の情報)の中にあるauthor(発言者)情報へmention(@だれだれ)する
		await client.send_message(message.channel, reply)

	if u or uranai or omikuji:# 占い
		reply = rp.luck()
		await client.send_message(message.channel, reply)


	if message.content.startswith('いま何時何分') or message.content.startswith('今何時何分'):# これあんま必要ない気がする
		now = dt.now()# 今のdatetime情報をnowに代入する
		reply = f'{now.hour}時{now.minute}分だよ'# now.hourでdatetimeの中のhour情報(時間)を取得。同様にnow.minuteで分を取得しreplyに代入
		await client.send_message(message.channel, reply)

	elif message.content.startswith('いま何時') or message.content.startswith('今何時'):
		now = dt.now()
		reply = f'いまは{now.hour}時だよ'
		await client.send_message(message.channel, reply)

	elif message.content.startswith('いま何分') or message.content.startswith('今何分'):
		now = dt.now()
		reply  =f'{now.minute}分だよ'
		await client.send_message(message.channel, reply)

	if dice:# dice計算用
		try:
			reply = dice.group()+':' # dice.group():受け取ったmessageのうち、判定に使った情報
			diceSum = 0 # 合計計算用の受け取り変数を用意
			if int(dice.group(1)) <= 992:
				for i in range(int(dice.group(1))):# 2d6だった場合、2回for文を回す
					r = random.randrange(0,int(dice.group(2)))+1 # 2d6だった場合、0~5をランダムで選択し、+1する
					diceSum += r
					reply += ' '+str(r)
				reply += ' ⇒ '+str(diceSum)
			else:
				reply = 'ちょ、多すぎ！もっとちっちゃくして！'
		except ValueError: # 大体変なことするとfor文の中のint()の部分で型のエラーが出るからそれをcatch
			reply = '数値じゃないと...わかんないのです....'
		finally: # どっちにしろこの文は起動するからfinally使ってます。正直いらないと思う。見やすいからいるかな？
			await client.send_message(message.channel, reply)


	if message.content.startswith('/neko') or message.content.startswith('にゃーん'):# にゃーん
		reply = rp.TBcat()
		await client.send_message(message.channel, reply)

	if message.content.startswith('おはよ'):
		now = dt.now()
		reply = rp.ohayo(now.hour)
		await client.send_message(message.channel, reply)

	if message.content.startswith('こんにちは') or message.content.startswith('こんにちわ') or message.content.startswith('ちわー'):#ちわー
		reply = rp.hello()
		await client.send_message(message.channel, reply)

	if message.content.startswith('こんばんは') or message.content.startswith('こんばんわ') or message.content.startswith('ばんわ'):#ばんわー
		now = dt.now()
		if now.hour in {19,20,21,22,23}:
			reply = 'こんばんはー'
		elif now.hour in {16,17,18}:
			reply = 'こんばんは'
		elif now.hour in {15}:
			reply = 'おやつの時間だよー'
		elif now.hour in {12,13,14}:
			reply = 'お昼だよー'
		elif now.hour in {6,7,8,9,10,11}:
			reply = 'おはよぉ。オールした？'
		elif now.hour in {4,5}:
			reply = '( ˘ω˘)ｽﾔｧ'
		elif now.hour in {1,2,3}:
			reply = 'もう寝ないと体に毒だよ'
		else:
			reply = 'こんばんは'
		await client.send_message(message.channel, reply)

	if sleep:#(つ∀-)ｵﾔｽﾐｰ
		reply = rp.goodNight()
		await client.send_message(message.channel, reply)
	
	if message.content.startswith('にゃんぱす'):#にゃんぱすー
		reply = 'にゃんぱすー'
		await client.send_message(message.channel, reply)

	if message.content.startswith('すっごーい'):#脳みそとけぅ
		reply = 'たーのしー！'
		await client.send_message(message.channel, reply)

	if message.content.startswith('がおー'):
		reply = 'がおー！'
		await client.send_message(message.channel, reply)

	if message.content.startswith('神々の'):
		print(message.author)
		reply = '遊び'
		await client.send_message(message.channel, reply)

	if musicJoin:
		voiceChannel = client.get_channel(voiceChannelID)
		if client.is_voice_connected(voiceChannel.server):
			voice = client.voice_client_in(channel.server)
		else:
			voice = await client.join_voice_channel(voiceChannel)
		#player = voice.create_ffmpeg_player('C:/Users/c0118259dc/Music/針原翼 (HarryP)/A HUNDRED MILLION LIGHTS/14 TODAY THE FUTURE Magical Mirai ver.wma')#'music/MikeTest.mp3')
		#player.start()
		print(voice)
	
	if musicPlay:
	#if client.is_voice_connected(voiceChannelID) == True:

		#player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=phNFXwRN1ZM')#musicPlay.group(1))
		player = voice.create_ffmpeg_player('music/MikeTest.mp3')
		player.start()


@client.event
async def on_member_update(before, after):
	#print(after.channel)
	if before.status != after.status:
		if after.display_name == 'Mikaner':
			return
			# reply = f'あ、Mikanerが{str(after.status)}になった。'
		else:
			reply = f'あ、{after.display_name}さんが{str(after.status)}になったみたい'
		await client.send_message(channelObj[0], reply) 

client.run(token["token"])