# import machine


def rgb_to_hsv( r, g, b ):
    ( h, s, v ) = ( 0, 0, 0 )
    
    _max = max( [r, g, b] )
    _min = min( [r, g, b] )

    if( _max == _min ):
        h = 0
    elif( r >= g and r >= b ):
        h = 60 * ((g - b) / (_max - _min))
        if h < 0:
            h += 360
    elif( g >= b and g >= r ):
        h = 60 * ((b - r) / (_max - _min)) + 120
    elif( b >= r and b >= g ):
        h = 60 * ((r - g) / (_max - _min)) + 240
        
    s = (_max - _min) / _max * 255
    v = _max
    
    h = int( max( min( h, 360 ), 0 ) )
    s = int( max( min( s, 255 ), 0 ) )
    v = int( max( min( v, 255 ), 0 ) )
    
    return (h, s, v)


def hsv_to_rgb( h, s, v ):
    ( r, g, b ) = ( 0, 0, 0 )
    
    h = max( min( h, 360 ), 0 )
    s = max( min( s, 255 ), 0 )
    v = max( min( v, 255 ), 0 )
    
    _max = v
    _min = _max - ( ( s / 255 ) * _max )
    
    if(     0 <= h <  60 ):
        r = int(_max)
        g = int((h/60)*(_max-_min)+_min)
        b = int(_min)
    elif(  60 <= h < 120 ):
        r = int(((120-h)/60)*(_max-_min)+_min)
        g = int(_max)
        b = int(_min)
    elif( 120 <= h < 180 ):
        r = int(_min)
        g = int(_max)
        b = int(((h-120)/60)*(_max-_min)+_min)
    elif( 180 <= h < 240 ):
        r = int(_min)
        g = int(((240-h)/60)*(_max-_min)+_min)
        b = int(_max)
    elif( 240 <= h < 300 ):
        r = int(((h-240)/60)*(_max-_min)+_min)
        g = int(_min)
        b = int(_max)
    elif( 300 <= h < 360 ):
        r = int(_max)
        g = int(_min)
        b = int(((360-h)/60)*(_max-_min)+_min)
    else:
        r = int(_max)
        g = int(_min)
        b = int(_min)
        
    r = int( max( min( r, 255 ), 0 ) )
    g = int( max( min( g, 255 ), 0 ) )
    b = int( max( min( b, 255 ), 0 ) )
    
    return (r, g, b)

