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
- playnow (実装中)(使用可能)
- testplay (実装中)(使用可能)
- skip
  - s
- stop
- start
- np
  - nowplaying
- list (実装中)(使用可能)
  - queue
  - q
- loopqueue (実装中)(使用可能)
  -lq
- clear (実装中)(使用不可)(バグ有)
- remove (未実装)
  - rm

## タスク
要件 実装 検証
- Playの初期音量設定(20%) ☐ ☐
- Join後のplayが動かないバグ除去 ☑ ☐
- Skipのdestroy後にunplayed musicの呼び出し ☑ ☐
- handleListの順番を固定化 ☐ ☐
- Queueの割り込み ☐ ☐
- Queueの個別削除 ☐ ☐
- Queueの全削除 ☐ ☐
- MikeTestのURLをplayNextが呼ぶと死ぬ
- https://www.youtube.com/watch?v=gNp4VNr44hg ←これが再生されない ←410 Gone
- handleListのindex情報の実装改善 ←処理速度の違いからずれてるっぽい ←awaitでできるかごにょってみたけど全然無理。どうすればええかわからん。
  - →forEachからforに直したらawaitが仕事し始めた ☑ ☐
- handleListの表示改善(embedの利用) ☐ ☐
- loopqueueの実装 ☑ ☐
- 検索機能の実装 ☐ ☐

# 参考URL
https://qiita.com/HungTran/items/98e2b07a0fdd9e9b37fd

.pyの方<br>
https://github.com/Mikaner/CreateTB