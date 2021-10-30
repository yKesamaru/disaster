# disaster
How can you find a loved one in the event of a disaster? A system that allows you to search for the face of the person you are looking for from a camera installed in the shelter may help you. I propose a face search system for disasters using dlib. 

![demo](https://user-images.githubusercontent.com/93259837/139436058-758f8c10-1dd2-4e67-ad23-5a9f6b2dbd7a.gif)

## プロジェクトの内容 Project content
災害が発生した状況に於いて最愛の人の安否が確認できない、この状況の解決方法を模索することは喫緊の課題です。現在様々な企業が実現可能な技術を持ち寄り課題の解決に取り組んでいます。しかしながら災害前の事前登録が必要であったり、前もって家族の話し合いが前提であったりするため、災害前に何らかの対策をしていない場合災害後に家族の安否を確認する事が困難になることが予想されます。また被災者のスマートフォンが使用できない状況の場合、災害直後に被災者から家族へ連絡を試みることは困難です。  

It is an urgent task to find a solution to this situation where the safety of a loved one cannot be confirmed in a disaster situation. 
Currently, various companies are working to solve problems bringing together feasible technologies. 

However, pre-registration before the disaster is often required, and/or family discussions are a prerequisite in advance. 

So it is expected that it will be difficult to confirm the safety of the family after the disaster if some measures are not taken before the disaster. 
Also, if the victim's smartphone cannot be used, it is difficult for the victim to try to contact family immediately after the disaster. 

こうした災害は世界中で発生しています。このプロジェクトでは世界中の人々が自由にシステムを構築できるようにするためgithubで公開します。  

These disasters are occurring all over the world. In this project, I'll publish it on github so that people who lived all over the world can build the system for free.

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

今回githubに公開したのはwebアプリケーションの基本部分です。これを改良することで使えるようになるでしょう。カメラから顔データを作成するアプリケーションを次に作成します。  

This time, I published the basic part of the web application on github. It will be possible to use it by improving this. Next, I'll create an application that creates face numerical data from the camera. 

## ロードマップ Roadmap  
### 基本構造 Basic structure  
#### Web application  
![web_application](https://user-images.githubusercontent.com/93259837/139513838-3e22fb8e-f9b7-4c88-aa7c-2ec4aa72cdd4.png)  
* アップロードページ作成 Upload page
* 顔領域切り抜き処理作成 Crop face area process
* 顔選択画面作成 Select a face
* 確認画面作成 Confirm page
* 類似度計算処理作成 Compute similarity
* 結果表示画面作成 Result page  

#### facial data application  
![make_data_application](https://user-images.githubusercontent.com/93259837/139513900-7dd066a4-5295-4ae6-aa49-d3e6feb01cd6.png)  
* 映像データ入力 Video data input
* フレームごとに顔検出 Face detection for each frame
* 顔座標から128次元データを作成 Create 128-dimensional data from face coordinates
* 数値データと避難所データを作成 Create numerical face data and shelter's data

## ユーザーがプロジェクトを開始する方法 How the user starts the project  
```bash
$ pip install -r requirements.txt
``` 

使用するPythonライブラリはrequirements.txtに書いてあります。pipを使い一括でインストールしてください。足りないライブラリがある場合はrequirements.txtに追記して頂けると助かります。  

現在Webアプリケーションの基本部分のみ作成されています。  

Currently only the basic part of the web application has been created.
```python
import os
import random

import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template, request
from PIL import Image
```

## プロジェクトの維持、貢献 Project maintenance and contribution
活動が広く広がることを願います。英訳出来る方がいらっしゃると大変助かります。  

I hope that the activities will spread widely. It would be very helpful if someone could translate it into English. 

Thankyou
