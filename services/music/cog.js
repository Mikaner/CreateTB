const {prefix} = require('../../config.json');
const ytdl = require('ytdl-core');
const {}


module.exports = {
  call: call,
  play: play,
  isValidCommand: isValidCommand,
  handlePlay: handlePlay,
  handleSkip: handleSkip,
  handleStop: handleStop,
  handleStart: handleStart,
  handlePlayNow: handlePlayNow,
  handleDisconnect: handleDisconnect,
}

let servers = {};
let connections = {};
let is_pausing = false;

function call(message){
  const args = message.content.slice(prefix.length).trim().split(/ +/g);
  const command = args.shift().toLowerCase();
  
  switch(command) {
    case 'testplay':
      handleTestPlay(message);
      break;
    case 'play':
    case 'p':
      handlePlay(message,args[0]);
      break;
    case 'skip':
    case 's':
      handleSkip(message);
      break;
    case 'stop':
      handleStop(message);
      break;
    case 'start':
      handleStart(message);
      break
    case 'playnow':
      handlePlayNow(message, args[0]);
      break;
    case 'join':
      handleJoin(message);
      break;
    case 'np':
    case 'nowplaying':
      handleNp(message);
      break;
    case 'loopqueue':
    case 'lq':
      handleLoopQueue(message);
      break;
    case 'list':
    case 'queue':
    case 'q':
      handleList(message);
      break;
    case 'clear':
      handleClear(message);
      break;
    case 'disconnect':
    case 'dc':
      handleDisconnect(message);
      break;
  }
}

function isValidCommand(message, url){
  if(!message.member.voice.channel){
    message.reply('Voiceチャンネルに参加してください');
    return false;
  }
  
  if(!url) {
    message.reply('YoutubeのURLを入力してください');
    return false;
  }
  
  let reg = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/gm;
  if (!url.match(reg)) {
    message.reply('Youtubeのリンクを判別できませんでした');
    return false;
  }
  
  return true;
}


function getCurrentQueue(message){
  return servers[message.guild.id].now_playing;
  /*
  return queues.filter(function(queue) {
    return queue.status === 1;
  }).slice(-1)[0];
  */
}

function getFirstUnPlayedQueue(message){
  return servers[message.guild.id].queue[0];
  /*
  return queues.filter(function(queue) {
    return queue.status === 0;
  })[0];
  */
}

function popFirstUnPlayedQueue(message){
  return servers[message.guild.id].queue.shift();
}

function playNext(server, message){
  if(server.loopflag){
    server.queue.push(getCurrentQueue(message));
  }
  
  const next_music = getFirstUnPlayedQueue(message)
  if(next_music){
    play(connections[message.guild.id], message);
  } else {
    //handleDisconnect(message);
    console.log(`The ${message.guild.id} was finished to play!`);
    console.log(servers[message.guild.id].dispatcher);
    delete servers[message.guild.id];
  }
}

async function play(connection, message){
  let server = servers[message.guild.id];
  server.now_playing = popFirstUnPlayedQueue(message);
  //now_playing[message.guild.id] = popFirstUnPlayedQueue(message);
  
  if(server.now_playing.local){
    server.dispatcher = connection.play( server.now_playing.url );
  } else {
    const info = await ytdl.getInfo(server.now_playing.url);
    console.log(`info: ${info}`);
    server.dispatcher = connection.play(
      ytdl(server.now_playing.url),
      { volume: 0.2 }
    );
  }
  console.log('Playing '+ server.now_playing.url);
  //server.now_playing.status = 1;
  
  server.dispatcher.on('finish', ()=>playNext(server, message));
}

function handleJoin(message){
  if (!connections[message.guild.id]){
    message.member.voice.channel.join()
      .then(connection => {
        connections[message.guild.id] = connection;
        if(!servers[message.guild.id]) { servers[message.guild.id] = {queue: []}; }
        servers[message.guild.id].loopflag = false;
      })
      .catch(console.log);
  }
  console.log(connections[message.guild.id]);
}

function handleDisconnect(message){
  if(connections[message.guild.id]){
    connections[message.guild.id].disconnect();
    delete connections[message.guild.id];
  }
  console.log(connections);
  console.log(servers[message.guild.id]);
}

async function handleTestPlay(message){
  const url = 'https://cdn.glitch.me/0c4da0ec-8148-4d59-b605-4b229d189f4f/MikeTest.mp3?v=1640168216964';
  
  if(!servers[message.guild.id]) { servers[message.guild.id] = {queue: []}; }
  await servers[message.guild.id].queue.push({
    url: url,
    status: 0,
    local: true
  });
  
  console.log(message.guild.id);
  console.log(servers[message.guild.id].queue);
  
  if (!connections[message.guild.id]) {
    message.member.voice.channel.join()
      .then(connection => {
        connections[message.guild.id] = connection;
        play(connections[message.guild.id], message);
      })
      .catch(console.log);
  } else if(!servers[message.guild.id].dispatcher){
    play(connections[message.guild.id], message);
  }
}

async function handlePlay(message, url){
  if(!isValidCommand(message, url)) { return; }
  
  if(!servers[message.guild.id]) { servers[message.guild.id] = {queue: []}; }
  await servers[message.guild.id].queue.push({
    url: url,
    status: 0,
    local: false
  });
  
  console.log(message.guild.id);
  console.log(servers[message.guild.id].queue);
  
  if (!connections[message.guild.id]) {
    message.member.voice.channel.join()
      .then(async connection => {
        connections[message.guild.id] = connection;
        await play(connections[message.guild.id], message);
      })
      .catch(console.log);
  } else if(!servers[message.guild.id].dispatcher){
    await play(connections[message.guild.id], message);
  }
}

function handleSkip(message){
  if (!servers[message.guild.id]) { return; }
  
  let server = servers[message.guild.id];
  if (server.dispatcher) {
    server.dispatcher.destroy();
    playNext(server, message);
  }
}

function handleStop(message){
  if (connections[message.guild.id]) {
    if(!is_pausing){
      is_pausing = true;
      servers[message.guild.id].dispatcher.pause(true);
    }
  }
}

function handleStart(message){
  if (connections[message.guild.id]) {
    if(is_pausing){
      is_pausing = false;
      servers[message.guild.id].dispatcher.resume();
    }
  }
}

function handleClear(message){
  if (servers[message.guild.id]){
    delete servers[message.guild.id].queue
    servers[message.guild.id].queue = [];
  }
}

function handleLoopQueue(message){
  servers[message.guild.id].loopflag = !servers[message.guild.id].loopflag;
}

function handlePlayNow(message, url){
  let server = servers[message.guild.id];
  if(!server){
    handlePlay(message, url);
    return;
  }
  
  server.queue.splice(1, 0, {
    url: url,
    status: 0
  });
  server.dispatcher.destroy();
}

async function handleNp(message){
  let server = servers[message.guild.id];
  if(!server || !server.queue){
    message.reply("何も再生していません");
    return;
  }
  let current_queue = getCurrentQueue(message);//server.queue);
  if(!server) {return;}
  ytdl.getBasicInfo(current_queue.url).then(info => {
    message.channel.send(getInfoMsg(info, current_queue.url));
  });
}

async function handleList(message){
  let server = servers[message.guild.id];
  if(!server || !server.queue) {
    message.reply("何もキューに入ってないです");
    return;
  }
  let msg = "";
  for (const [index, queue] of server.queue.entries()) {
    console.log(queue);
    if(!queue.local){
      const info = await ytdl.getBasicInfo(queue.url);
      msg += `${index===0?"Next":index}`+getInfoMsg(info, queue.url) + '\n -------------------------\n';
      console.log(msg);
    }else{
      msg += `${index===0?"Next":index} Title: MikeTest.mp3\n -------------------------\n`;
      console.log(msg);
    }
    console.log("test");
  };
  
  //await delay();
  
  if(msg===""){
    message.reply("何もキューに入ってないです");
  } else {
    message.channel.send(msg);
  }
}

function getInfoMsg(info, url){
  return ` Title: ${info.player_response.videoDetails.title}`;//` \n Link: ${url}`;
}

function delay(){
  return new Promise(resolve => setTimeout(resolve, 1000));
}