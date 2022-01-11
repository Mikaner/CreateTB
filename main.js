// Response for Uptime Robot
const http = require('http');
http.createServer(function(request, response) {
	response.writeHead(200, {'Content-Type': 'text/plain'});
	response.end('Discord bot is active now \n');
}).listen(8080);

// Discord bot implements
const discord = require('discord.js');
const client = new discord.Client();
const {prefix} = require('./config'); // prefixの設定
const musicCog = require('./services/music/cog');

client.on('ready', message => {
  client.user.setPresence({ game: { name: 'with discord.js' } });
	console.log('Logged in as');
  console.log(`${client.user.tag}`);
  /*client.user.setPresence({
      activities:[{ 
        name: 'with discord.js',
        type: 'COMPETING',
      }],
      status: 'idle',
  });*/
});


client.on('message', message => {
  //botに反応しなくなる奴
  if(message.author.bot) return;
  if(message.content === "にゃーん"){
    message.channel.send('にゃーん')
      .then(message => console.log(`Sent message: ${message.content}`))
      .catch(console.error);
  }
  //メンションが来たら｢呼びましたか？｣と返す
  /*
	if(message.isMemberMentioned(client.user)) {
		message.reply('呼びましたか？');
	}*/
  //argumentなどの処理
  if(message.content.indexOf(prefix) !== 0) return;
  
  const args = message.content.slice(prefix.length).trim().split(/ +/g);
  const command = args.shift().toLowerCase();
  
  //!pingと打ったらpong!が帰ってくる
  if(command === "ping") {
    message.channel.send('pong!')
  }
  //argumentを使ったこだま返し
  if(command === "echo") {
    const text = args.join(' ');
    message.channel.send(text)
  }
  if(message.content.startsWith(prefix)){
    musicCog.call(message);
  }
});

if(process.env.DISCORD_BOT_TOKEN == undefined) {
	console.log('please set ENV: DISCORD_BOT_TOKEN');
	process.exit(0);
}

client.login( process.env.DISCORD_BOT_TOKEN );