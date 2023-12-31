#必用なライブラリをインポートします
import array, utime, math, machine
from machine import Pin, ADC
import rp2
from rp2 import PIO, StateMachine, asm_pio
import cvt_col

# クロック周波数を250MHzにしています。（オーバークロックです）
machine.freq(250_000_000)

#AD変換のポート(GP26~GP28)を割り当てて、vr0~vr2のインスタンスを生成します。
vr0 = ADC(26)
vr1 = ADC(27)
vr2 = ADC(28)

# 変換係数です
K_speed = 6.0 / (65535)
K_val = 20.0 / (65535)
K_sat = 150.0 / (65535)

#WS2812 のLEDの数を指定します
NUM_LEDS = 100
# Pico特有のstate machine を用いてWS2812の制御を行っています
# PIO State Machine to display ws2812
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True,\
         pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1)                .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")    .side(1)    [T1 - 1]
    jmp("bitloop")           .side(1)    [T2 - 1]
    label("do_zero")
    nop()                    .side(0)    [T2 - 1]

# Create the StateMachine with the ws2812 program, outputting on Pin(16)().
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(16))

# start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

#position の位置のＬＥＤをred, green, blue の値にて指定します
def ar_color(position, red, green, blue):
    ar[position] = (green<<16) + (red<<8) + blue

#全てのＬＥＤを消灯する関数です
def clear_all():
    for i in range(NUM_LEDS):
        ar[i] = 0
    sm.put(ar,8)

#ここから処理がスタートします
if __name__ == '__main__':
    # Process arguments
    print('Press Ctrl-C to quit.')
    
    r_max = 4.5 * math.sqrt(2)
    color = 0.0
    try:
        # 無限ループです
        while True:
            # A/D変換により値を読み取っています。
            # 変数変換をしています。
            # speed: -3.0~3.0
            speed = vr0.read_u16() * K_speed - 3.0
            color = (color - speed) % 60.0
            # v: 0~20
            v = int(vr1.read_u16() * K_val)
            # s:105~255
            s = int(vr2.read_u16() * K_sat) + 105

            # Neopixelを同心円上に色を変化させて表示するための計算です
            for i in range(NUM_LEDS):
                # 左から何列目かを計算し、4.5を引いています
                x = float(i % 10) - 4.5
                # 下から何段目かを計算し、4.5を引いています
                y = float(i) / 10.0 - 4.5
                # 中心(4.5, 4.5)からの距離を求め、最大値を１に規格化しています
                r = math.sqrt(x*x + y*y) / r_max
                r_int = int(r  * 40.0 + color) % 60

                #それぞれのＬＥＤの色を計算し、値を書き込んでいます
                (r, g, b) = cvt_col.hsv_to_rgb(r_int * 6, s, v)
                ar_color(i, r, g, b)
            # 色を表示しています
            sm.put(ar,8)
            utime.sleep_us(100)

    # ctl-C が押されたときの処理です
    except KeyboardInterrupt:
        #### clear ws2812b
        clear_all()
