1. gnuradio-companionでプロジェクトファイル gr_ble_goal9.grc を開く
2. FMComms2/3/4 Sourceに IIO context URI: にip:192.168.1.10(例) を設定する 
3. 上側の ZMQ PUB Message Sinkset Address: に tcp://127.0.0.1.3333(例)を設定する 
4. 下側の ZMQ PUB Message Sinkset Address: にtcp://127.0.0.1.3334(例)を設定する 
5. Python スクリプトを実行する: $ python3 receive_pdu.py
6. フローグラフを実行する
