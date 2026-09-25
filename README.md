# Waterlevel_Alart
Waterlevel Alart program

## Overview
Influxdbに接続し、取得した水位と気温を表示＆一定以上の水位の場合に特定の音声を再生するPythonスクリプト

## Requirement
以下のライブラリを使用しています
+ influxdb_client
+ Adafuruit_CircuitPython_ssd1306
+ Adafuruit Blinka

## Usage
### 必要なライブラリをインストールし、以下の箇所を環境に応じて変更します
~~~
url = "<YOUR_INFLUXDB_URL>"
token = "<YOUR_INFLUXDB_TOKEN>"
org = "<YOUR_INFLUXDB_ORG>"

waterlevel_query変数：<WATERLEVEL_BUCKET>,<YOUR_MEASUREMENT>
wether_query変数：<WEATHER_BUCKET>,<YOUR_MEASUREMENT>
~~~

スクリプトと同じディレクトリに再生したい音声ファイル(wav)を配置します(ファイル名はスクリプトと一致させる必要あり)
~~~
サンプル例：
01-ETWS.wav
02-J-Alart.wav
03-Tsunami.wav
~~~

### cronなどで10分に1回実行するように設定
cronなどの定期実行ツールを用いて10分に1回実行されるように設定しておきます。

## Features

Influxdbに接続し、取得した水位と気温を表示＆一定以上の水位の場合に特定の音声を再生するPythonスクリプトです。  
スクリプトが実行されるたびにI2C接続された液晶に最新の水位/気温を表示します。  
また設定した水位以上の場合、任意の音声ファイルを警報音として再生します。  

確認環境：Raspberry pi Zero W(Raspberry Pi OS 12 bookworm) + SSD1306 w/I2C + PCM5102 DAC w/I2S環境にて動作を確認済み

## Licence
MITライセンスとなります。
