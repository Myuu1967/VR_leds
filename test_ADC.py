#必用なライブラリをインポートします
import utime, machine
from machine import Pin, ADC


machine.freq(250_000_000)

#AD変換のポートより、vr0の値を読み込む
vr0 = ADC(26)
vr1 = ADC(27)
vr2 = ADC(28)

adc_factor = 3.3 / (65535)

#ここから処理がスタートします
if __name__ == '__main__':
    # Process arguments
    print('Press Ctrl-C to quit.')
    
    try:
        # 無限ループです
        while True:
            adc_val0 = vr0.read_u16() * adc_factor
            adc_val1 = vr1.read_u16() * adc_factor
            adc_val2 = vr2.read_u16() * adc_factor

            print('adc_val:', adc_val0, adc_val1, adc_val2, sep = ',')
            utime.sleep(1)

    # ctl-C が押されたときの処理です
    except KeyboardInterrupt:
        nop()
