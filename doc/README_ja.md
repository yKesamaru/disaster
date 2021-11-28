<div style="text-align: right"><a href="https://github.com/yKesamaru/disaster#disaster">[en]</a></div>  

***最新のドキュメントは<a href="https://github.com/yKesamaru/disaster#disaster">英語版</a>になります。ご注意下さい。***

# Disaster（ディザスター）
Disasterとは`dlib`, `face_recognition`, `flask`, `PySimpleGUI`他を使った災害時安否確認用顔認証システムであり`Python`言語で書かれています。

災害が起こった時どうやって最愛の人を探しますか？Disasterを使うと避難所のカメラから家族の顔を検索することができます。

Disasterはプライバシーに最も配慮しています。顔情報は復元不可能な数値データに置き換えられ、たとえ開発者であっても元の顔画像に復元できません。  

* Disaster webアプリケーションのデモ  
![demo](../img/demo.gif)  
![screenshot](https://user-images.githubusercontent.com/93259837/139792630-06f66eef-2b41-4bbf-8c00-6c57ac811974.png)  

* 様々な顔から128Dベクトルデータを作成するDisasterアプリケーションウィンドウ  
![create_face_data](../img/demo3.gif)   

## Disaster Webアプリケーションを体験できます
DisasterをHEROKU上に構築しました。
https://disaster-application.herokuapp.com/
  
***無料プランを使用しているためインスタンスの起動に30秒ほどかかります。***

## 背景
災害が発生した状況に於いて最愛の人の安否が確認できない、この状況の解決方法を模索することは喫緊の課題です。現在様々な企業が実現可能な技術を持ち寄り課題の解決に取り組んでいます。  

しかしながら災害前の事前登録が必要であったり、前もって家族の話し合いが前提であったりするため、災害前に何らかの対策をしていない場合災害直後に家族の安否を確認する事は困難であると予想されます。  

もし被災者のスマートフォンが使用できない状況の場合、災害直後に被災者から家族へ連絡を試みることは困難です。  

こうした状況は自然災害だけではなく戦争や内戦によって、世界中で発生しています。


## 特徴
* シェルターに設置されているカメラの映像から元の顔画像に復元不可能な数値データに変換します。プライバシーを最重要視するため被災者の顔画像は表示もされず、またすぐに破棄されます。  

* 家族の写真をDisaster Webアプリケーションにアップロードすると、似ている人を自動的に探し、いつどのシェルターに被災者がいたかという情報を表示します  

* 自治体や組織は自由にシステムを利用する事が可能です  

## システム要件
* Ubuntuか類似したLinuxディストリビューション
* NVIDIA GeForce GTX 1660 Ti +
  * Disasterを試すだけの場合は必要ありません。その場合は処理速度がかなり遅くなります。
  * もしGPUを使用したい場合、ドライバなどのインストールは[こちら](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-docker-ce)に紹介されている方法でインストールして下さい。
* Python 3.7 +
* git
* Docker 19.03 +
* ネットワークカメラやWebカメラ
  * Disasterを試すだけなら必要ありません。その様な場合に備えてmp4ファイルが添付されています。
```bash
実行環境例 (私の開発環境)
Kernel	Linux 5.4.0-89-generic (x86_64)
Version	#100~18.04.1-Ubuntu SMP Wed Sep 29 10:59:42 UTC 2021
C Library	GNU C Library / (Ubuntu GLIBC 2.27-3ubuntu1.4) 2.27
Distribution	Ubuntu 18.04.6 LTS
Renderer	NVIDIA GeForce GTX 1660 Ti/PCIe/SSE2
Version	4.6.0 NVIDIA 470.63.01
AMD Ryzen 5 1400 Quad-Core Processor
Total Memory	16389096 KiB
Python 3.7.11(pyenv)
```
  
## 使用方法  
### Dockerを使う方法
Dockerを使う場合は<a href="Build_python_runtime_environment.md">こちら</a>を参照して下さい。  
もしnvidia-docker2パッケージをインストールしていない場合、実行速度はかなり遅くなります。しかしながら、もしDisasterを試す場合だけだった場合はそのままで良いと思います。  
もしDisasterを標準的な処理速度で動かしたい場合でnvidia-docker2パッケージをインストールしていない場合、以下を参照して下さい。
```bash:Install nvidia-docker2 package
# For Ubuntu 18.04
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && \
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - && \
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```
各ディストリビューションにおけるインストールの方法は、公式ドキュメントをご参照下さい。  
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-docker-ce  


### Dockerを使わない方法
<a href="./Build_python_runtime_environment.md">こちら</a>を参照してPython実行環境等を構築して下さい。  
```bash
$ git clone https://github.com/yKesamaru/disaster.git
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
*** `http://127.0.0.1:5000/`にアクセスして下さい ***

### 顔データ作成を試すには
DisasterではネットワークカメラやWebカメラを使用することが出来ます。  
ここでは簡単な例としてmp4ファイルを使います。  
オプション：前もってPython仮想環境を立ち上げて下さい。
```bash
$ cd create_face_data/shelter01
$ python create_face_data_app.py 
$ cd ../
$ python marge_npKnown.py
```

## 構成
このシステムは3ブロックで構成されます。
### 1. Webアプリケーション  
![web_application](https://user-images.githubusercontent.com/93259837/139513838-3e22fb8e-f9b7-4c88-aa7c-2ec4aa72cdd4.png)  
```bash
Disaster
└ web_app
    ├ main.py
    └ others
```
家族を探したい人が家族の写真をアップロードします。サーバーで復元不可能な数値データに変換し、シェルターのカメラから撮影された映像から似ている顔を検索します。スマートフォンには日時と避難所名が表示されます。  

### 2. 顔データ作成アプリケーション
![make_data_application](https://user-images.githubusercontent.com/93259837/139513900-7dd066a4-5295-4ae6-aa49-d3e6feb01cd6.png)  
```bash
Disaster
└ create_face_data
    ├ marge_npKnown.py
    ├ npKnown_root.npz
    ├ shelter01
    │  ├ create_face_data_app.py
    │  ├ shelter01.mp4    
    │  └ npKnown.npz
    └ shelter02
        ├ create_face_data_app.py
        ├ shelter02.mp4    
        └ npKnown.npz
```
シェルターに設置されたカメラで撮影された大勢の顔を全てデータ化します。  

複数のシェルターを表現するためshelter01, shelter02ディレクトリを設けています。  
より詳しい説明は<a href="./How_to_operate.md">こちら</a>からご参照下さい。   

### 3. サーバ間データ同期
顔データファイルを各サーバー間で共有し、システム全体のダウンを防止します。  
この機能はまだ実装されていません。

## プロジェクトの維持・貢献
Disasterのメンテナンスは袈裟丸喜嗣が行っています。  
同様の活動が広く広がることを期待します。  
英語が得意ではありませんので英語の誤りがありましたら指摘して頂けると大変ありがたいです。  
  
ありがとうございました。

<!-- ## ToDo
*  -->