# 概要
音楽再生用関連。
cog.js : 音楽再生用のコマンド実装
MikeTest.mp3 : 再生チェック用音声ファイル(assetsにも存在する) ← assetsの参照ができなさそうだったからここに入れた。

# cog.js
## コマンド
- join
- disconnect
  - dc
- play (実装中)(使用可能)
  - p
- playtop
  - pt
- testplay
- search
- skip
  - s
- stop
- start
- nowplaying
  - np
- list (実装中)(使用可能)
  - ls
  - queue
  - q
- loopqueue
  -lq
- clear
- remove (実装中)(使用可能)
  - rm
- move (実装中)(使用可能)
  - mv

## タスク
要件 実装 検証
- Playの初期音量設定(20%) ☑ ☑
- Join後のplayが動かないバグ除去 ☑ ☑
- Skipのdestroy後にunplayed musicの呼び出し ☑ ☑
- handleListの順番を固定化 ☑ ☑
- rmの実装 ☑ ☑
- Queueの全削除 ☑ ☐
- Queueの個別削除 ☑ ☐
- MikeTestのURLをplayNextが呼ぶと死ぬ ☑ ☐
- handleListのindex情報の実装改善 ←処理速度の違いからずれてるっぽい ←awaitでできるかごにょってみたけど全然無理。どうすればええかわからん。
  - →forEachからforに直したらawaitが仕事し始めた ☑ ☐
- loopqueueの実装 ☑ ☐
- 検索機能の実装 ☑ ☐
- loopqueueを設定したときのリアクション実装 ☑ ☐
- moveの実装 ☑ ☐
- handleListの表示改善(embedの利用) ☐ ☐
- playした際に再生されずにqueueに入る。(queueから押し出されない)バグ除去
- 曲がぷつぷつになる原因の除去

再生不可能リスト(StatusCode:410)
- https://www.youtube.com/watch?v=gNp4VNr44hg
- https://youtube.com/watch?v=x8VYWazR5mE

# 参考URL
https://qiita.com/HungTran/items/98e2b07a0fdd9e9b37fd

ソースコードの方:<br>
<a href="https://github.com/Mikaner/CreateTB">Github</a>