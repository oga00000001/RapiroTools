RAPIRO　コントロールボード　簡易テストプログラム

ボード単体で、各ポートをテストする事を目的に作りました。
使用は自己責任でお願いします。

概要
サーボを接続するポートをデジタル出力にし、１ポート毎にON/OFFします。
I2Cポート（A4,A5）は、センサー用ポート（A6,A7）、アナログ入力にしています。

サーボ用ポートと、A4～A7を接続し、電源を入れると、下記のようなレポートが
シリアルモニタに出力されます。
A4～A7に接続されている、サーボ用ポートに対応する場所が*で表示され、それ以外は-が表示されます。
3回、接続しなおす必要がありますが、全てのポートのON/OFFが確認できます。
PWMのチェックはできませんが、ボードのオープン/ショートぐらいは確認できると思います。

Check Serov port output & Analog read 
A4 - - * - - - - - - - - - 
A5 - - - * - - - - - - - - 
A6 * - - - - - - - - - - - 
A7 - * - - - - - - - - - - 

サーボ用の電源と、A6又はA7を接続すると、サーボ用電源と、電源スイッチのON/OFFが確認出来ます。
注）DCDC電源が壊れていて、ACアダプターの電圧がスルーする様な事があれば、コントローラが壊れるおそれがあります。
ボード上のDCDCが正常であれば、出力電圧は4.8Vぐらいです。

コントローラのA3ピンがHIGHになると、A6またはA7が、1023ぐらいに上がります。その後、A3をLOWにした後、
１秒毎に、電圧を測定しします。チャージした電荷が抜けるのに時間がかかるの、徐々に数値が下がり、
どこかで0になります。

Check Serov power switch and output voltage.
ON0 1023　　　；電源ON
0 0 925     ；電源OFF
1 0 817
2 0 715
3 0 615
4 0 517
5 0 421
6 0 326
7 0 234
8 0 144
9 0 58
10 0 0
11 0 0
12 0 0
13 0 0
14 0 0
15 0 0
16 0 0
17 0 0
18 0 0
19 0 0
