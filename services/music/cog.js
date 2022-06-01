const {prefix} = require('../../config.json');
const ytdl = require('ytdl-core');
const yts = require('yt-search');
//const {handleTestSearch} = require('utils.js');


module.exports = {
  call: call,
  play: play,
  isValidCommand: isValidCommand,
  handlePlay: handlePlay,
  handlePlayTop: handlePlayTop,
  handleSkip: handleSkip,
  handleStop: handleStop,
  handleStart: handleStart,
  handleRemove: handleRemove,
  handleDisconnect: handleDisconnect,
}

const servers = {};
const connections = {};

function call(message){
  const args = message.content.slice(prefix.length).trim().split(/ +/g);
  const command = args.shift().toLowerCase();
  
  switch(command) {
    case 'testplay':
      handleTestPlay(message);
      break;
    case 'join':
      handleJoin(message);
      break;
    case 'play':
    case 'p':
      handlePlay(message,args);
      break;
    case 'playtop':
    case 'pt':
      handlePlayTop(message, args);
      break;
    case 'search':
      handleSearch(message, args);
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
    case 'np':
    case 'nowplaying':
      handleNp(message);
      break;
    case 'loopqueue':
    case 'lq':
      handleLoopQueue(message);
      break;
    case 'list':
    case 'ls':
    case 'queue':
    case 'q':
      handleList(message);
      break;
    case 'clear':
      handleClear(message);
      break;
    case 'remove':
    case 'rm':
      handleRemove(message, args[0]);
      break;
    case 'move':
    case 'mv':
      handleMove(message, args[0], args[1]);
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
  
  return true;
}

function isYoutubeUrl(message, url){
  let reg = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/gm;
  if (!url.match(reg)) {
    //message.reply('Youtubeのリンクを判別できませんでした');
    return false;
  }
  
  return true;
}

function makeServerStatus(){
  return {queue: [], loopflag: false, is_pausing: false};
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

function getTitleByInfo(info, url){  // 削除候補
  return `${info.player_response.videoDetails.title}`;//` \n Link: ${url}`;
}

async function getTitleByUrl(url){
  const info = await ytdl.getBasicInfo(url);
  return getTitleByInfo(info, url);
}

function popFirstUnPlayedQueue(message){
  return servers[message.guild.id].queue.shift();
}

function playNext(server, message){
  if(server.loopflag){
    server.queue.push(getCurrentQueue(message));
  }
  
  const next_music = getFirstUnPlayedQueue(message);
  if(next_music){
    play(connections[message.guild.id], message);
  } else {
    //handleDisconnect(message);
    //console.log(servers[message.guild.id].dispatcher);
    console.log(`The ${message.guild.id} was finished to play!`);
    servers[message.guild.id].dispatcher.destroy();
    delete servers[message.guild.id].now_playing;
  }
}

async function play(connection, message){
  let server = servers[message.guild.id];
  server.now_playing = popFirstUnPlayedQueue(message);
  console.log(server.now_playing);
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
        if(!servers[message.guild.id]) { servers[message.guild.id] = makeServerStatus(); }
      })
      .catch(console.log);
  }
  console.log(connections[message.guild.id]);
}

function handleDisconnect(message){
  if(connections[message.guild.id]){
    connections[message.guild.id].disconnect();
    delete connections[message.guild.id];
    delete servers[message.guild.id];
  }
  console.log(connections);
  console.log(servers[message.guild.id]);
}

async function handleTestPlay(message){
  const url = 'https://cdn.glitch.me/0c4da0ec-8148-4d59-b605-4b229d189f4f/MikeTest.mp3?v=1640168216964';
  const title = 'MikeTest.mp3';
  
  if(!servers[message.guild.id]) { servers[message.guild.id] = makeServerStatus(); }
  await servers[message.guild.id].queue.push({
    url: url,
    status: 0,
    local: true
  });
  
  message.channel.send(`${title}を追加しました。`); 
  
  console.log(message.guild.id);
  console.log(servers[message.guild.id]);
  
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

async function handlePlay(message, args){
  let url = args[0];
  let title;
  if(!isValidCommand(message, url)) { return; }
  
  if(!isYoutubeUrl(message, url)){
    const r = await yts(args.join(' '));
    const video = await r.videos.slice(0, 1)[0];
    //console.log('------- video:-----------');
    //console.log(video);
    url = video.url;
    title = video.title;
  } else {
    const info = await ytdl.getBasicInfo(url);
    title = getTitleByInfo(info, url);// getInfoByUrlに変更候補
  }
  
  if(!servers[message.guild.id]) { servers[message.guild.id] = makeServerStatus(); }
  
  const server = servers[message.guild.id];
  await server.queue.push({
    url: url,
    status: 0,
    local: false
  });
  
  message.channel.send(`${title}を追加しました。`); 
  
  //console.log(message.guild.id);
  //console.log(servers[message.guild.id]);
  
  if (!connections[message.guild.id]) {
    message.member.voice.channel.join()
      .then(async connection => {
        connections[message.guild.id] = connection;
        await play(connections[message.guild.id], message);
      })
      .catch(console.log);
  } else if(!server.dispatcher){
    await play(connections[message.guild.id], message);
  }
}

async function handlePlayTop(message, args){
  const server = servers[message.guild.id];
  if(!server || !server.queue){
    handlePlay(message, args);
    return;
  }
  
  let url = args[0];
  
  if(!isValidCommand(message, url)) { return; }
  
  let title;
  
  if(!isYoutubeUrl(message, url)){
    const r = await yts(args.join(' '));
    const video = await r.videos.slice(0, 1)[0];
    console.log('------- video:-----------');
    console.log(video);
    url = video.url;
    title = video.title;
  } else {
    const info = await ytdl.getBasicInfo(url);
    title = getTitleByInfo(info, url);
  }
  
  server.queue.splice(0, 0, {
    url: url,
    status: 0,
    local: false
  });
  
  message.channel.send(`${title}を次の曲に追加しました。`); // getInfoByUrlに変更候補
  
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
    const server = servers[message.guild.id];
    if(!server.is_pausing){
      server.is_pausing = true;
      server.dispatcher.pause(true);
    }
  }
}

function handleStart(message){
  if (connections[message.guild.id]) {
    const server = servers[message.guild.id];
    if(server.is_pausing){
      server.is_pausing = false;
      server.dispatcher.resume();
    }
  }
}

function handleRemove(message, index_num){
  let index = Number(index_num);
  if(index_num.toLowerCase()==="next"){index=0}
  if(index===NaN){message.reply("数値を入力してください。");return;}
  const server = servers[message.guild.id];
  if (server && server.queue.length){
    message.reply(`${server.queue.splice(index%server.queue.length, 1)[0].url} was removed !`);
  }
}

function handleMove(message, from_index, to_index){
  let f_i = Number(from_index);
  let t_i = Number(to_index);
  if(from_index.toLowerCase()==="next"){f_i=0}
  if(to_index.toLowerCase()==="next"){t_i=0}
  if(f_i===NaN || t_i===NaN){message.reply("数値を入力してください。");return;}
  
  const server = servers[message.guild.id];
  
  if(server && server.queue.length){
    f_i = f_i%server.queue.length;
    t_i = t_i%server.queue.length;
  
    const target = server.queue.splice(f_i, 1)[0];
    console.log(`f_i is ${f_i} \nt_i is ${t_i}\ntarget is ${target}`);
    server.queue.splice(t_i, 0, target);
    message.reply(`${target.url} was moved from ${f_i} to ${t_i}`);
  }
}

function handleClear(message){
  if (servers[message.guild.id]){
    delete servers[message.guild.id].queue;
    servers[message.guild.id].queue = [];
  }
}

function handleLoopQueue(message){
  const loopflag = !servers[message.guild.id].loopflag;
  servers[message.guild.id].loopflag = loopflag;
  message.channel.send(`Turned ${loopflag?"on":"off"} the loop.`);
}

/*
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
*/

async function handleNp(message){
  let server = servers[message.guild.id];
  if(!server || !server.now_playing){
    message.reply("何も再生していません");
    return;
  }
  let current_queue = getCurrentQueue(message);//server.queue);
  if(!server) {return;}
  if(current_queue.local){
    message.channel.send(" Title: MikeTest.mp3");
  } else {
    ytdl.getBasicInfo(current_queue.url).then(info => {
      message.channel.send(" Title: "+getTitleByInfo(info, current_queue.url));
    });
  }
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
      msg += `${index===0?"Next":index} Title: `+getTitleByInfo(info, queue.url) + '\n -------------------------\n';  // getTitleByUrlに変更候補
      console.log(msg);
    }else{
      msg += `${index===0?"Next":index} Title: MikeTest.mp3\n -------------------------\n`;
      console.log(msg);
    }
    console.log("test");
  };
  
  
  if(msg===""){
    message.reply("何もキューに入ってないです");
  } else {
    message.channel.send(msg);
  }
}

async function handleSearch(message, args){
  console.log(args);
  
  const video_max_length = 3;
  
  const r = await yts(args.join(' '));
  const videos = r.videos.slice(0, video_max_length);
  
  let msg = "検索結果:\n========== \n";
  videos.forEach( (v) => {
    const views = String(v.views).padStart(10, ' ');
    msg += (`${ v.title } (${v.timestamp}) | ${v.author.name}\n`);
    msg += (`url: ${v.url}\n---------- \n`);
  });
  
  message.channel.send(msg);
}