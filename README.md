# Disaster
Disaster is a face search system for disasters using `dlib`, and what is written in `python`. How can you find a loved one in the event of a disaster? Disaster allows you to search for the face of the person you are looking for from the video taken by the camera installed in the shelter.

### Disasterの特徴
* シェルターに設置されているカメラの映像から、元の顔画像に復元不可能な数値データに変換します
Converts the image taken by a camera installed in the shelter into numerical data that cannot be restored to the original face image.
* 家族の写真をDisaster Webアプリケーションにアップロードすると、似ている人を自動的に探し、いつどのシェルターに被災者がいたかという情報を表示します When upload a family photo to the Disaster web application, it will automatically look for similar people and display information about when and in which shelter the victim was.
* 自治体や組織は自由にシステムを利用する事が可能です Local governments and organizations can freely use Disaster. 

![demo](https://user-images.githubusercontent.com/93259837/139436058-758f8c10-1dd2-4e67-ad23-5a9f6b2dbd7a.gif)

## プロジェクトの内容 Project content
災害が発生した状況に於いて最愛の人の安否が確認できない、この状況の解決方法を模索することは喫緊の課題です。現在様々な企業が実現可能な技術を持ち寄り課題の解決に取り組んでいます。しかしながら災害前の事前登録が必要であったり、前もって家族の話し合いが前提であったりするため、災害前に何らかの対策をしていない場合災害後に家族の安否を確認する事が困難になることが予想されます。被災者のスマートフォンが使用できない状況の場合、災害直後に被災者から家族へ連絡を試みることは困難です。  

It is an urgent task to find a solution to this situation where the safety of a loved one cannot be confirmed in a disaster situation. 
Currently, various companies are working to solve problems bringing together feasible technologies. 

However, pre-registration before the disaster is often required, and/or family discussions are a prerequisite in advance. 

So it is expected that it will be difficult to confirm the safety of the family after the disaster if some measures are not taken before the disaster. 
If the situation when victim cannot be used smartphone, it is difficult for the family to try to contact victim immediately after the disaster. 

こうした状況は自然災害だけではなく戦争や内戦によって、世界中で発生しています。

These situations are occurring all over the world not only natural disasters but also wars or civil wars. 

## 構成 Component
このシステムは3つのブロックから成り立っています。  

This system consists of three blocks.

### Webアプリケーション Web application
家族を探したい人が家族の写真をアップロードします。サーバーで復元不可能な数値データに変換し、シェルターのカメラから撮影された映像から似ている顔を検索します。スマートフォンには日時と避難所名が表示されます。  

People who want to find a family upload a family photo. It converts to non-recoverable numerical data on the server and searches for similar faces in the footage taken by the shelter's camera. Date, time and the shelter's name are displayed on the smartphone. 

### サーバー間のデータ同期 Data synchronization between servers
顔データファイルを各サーバー間で共有し、システム全体のダウンを防止します。  

The face data file is shared between each server to prevent the entire system from going down. 

### カメラから顔データを作成するアプリケーション The Application for creating numerical face data from camera
シェルターに設置されたカメラで撮影された大勢の顔を全てデータ化します。  

All the faces taken by the camera installed in the shelter are converted into numerical data. 

## ロードマップ Roadmap  
### 基本構造 Basic structure  
#### Web application  
```bash
disaster
└ web_app
    ├ main.py
    └ others
```
![web_application](https://user-images.githubusercontent.com/93259837/139513838-3e22fb8e-f9b7-4c88-aa7c-2ec4aa72cdd4.png)  
* アップロードページ作成 Upload page
* 顔領域切り抜き処理作成 Crop face area process
* 顔選択画面作成 Select a face
* 確認画面作成 Confirm page
* 類似度計算処理作成 Compute similarity
* 結果表示画面作成 Result page  

#### facial data application  
```bash
disaster
└ create_face_data
    ├ create_face_data_app.py
    └ others
```
![make_data_application](https://user-images.githubusercontent.com/93259837/139513900-7dd066a4-5295-4ae6-aa49-d3e6feb01cd6.png)  
* 映像データ入力 Video data input
* フレームごとに顔検出 Face detection for each frame
* 顔座標から128次元データを作成 Create 128-dimensional data from face coordinates
* 数値データと避難所データを作成 Create numerical face data and shelter's data

## Usage  
```bash
$ pip install -r requirements.txt
``` 
```bash
$ cd web_app
$ export FLASK_APP=main.py
$ flask run
 * Serving Flask app 'main.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
*** Access `http://127.0.0.1:5000/` ***

## プロジェクトの維持、貢献 Project maintenance and contribution
活動が広く広がることを願います。英訳出来る方がいらっしゃると大変助かります。  

I hope that the activities will spread widely. It would be very helpful if someone could translate it into English. 

Thankyou
