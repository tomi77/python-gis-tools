def decodeGMapPolylineEncoding(ascii_encoded_string):
    str_len = len(ascii_encoded_string)

    index = 0
    lat = 0
    lng = 0
    coord_pair = []

    while index < str_len:
        # GET THE LATITUDE
        shift = 0
        result = 0

        stay_in_loop = True
        while stay_in_loop:
            b = ord(ascii_encoded_string[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1

            if not b >= 0x20:
                stay_in_loop = False

        # Python ternary instruction..
        dlat = ~(result >> 1) if (result & 1) else result >> 1
        lat += dlat

        lat_num = lat * 1e-5

        # GET THE LONGITUDE
        shift = 0
        result = 0

        stay_in_loop = True
        while stay_in_loop:
            b = ord(ascii_encoded_string[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1

            if not b >= 0x20:
                stay_in_loop = False

        # Python ternary instruction..
        dlng = ~(result >> 1) if (result & 1) else result >> 1
        lng += dlng

        lng_num = lng * 1e-5

        coord_pair.append(str(lng_num) + " " + str(lat_num))

    # The data I was converting was rather dirty..
    # At first I expected 100% polygons, but sometimes the encodings returned
    # only one point. Clearly one point cannot represent a polygon. Nor can two
    # points represent a polygon. This was an issue because I wanted to return
    # proper WKT for every encoding, so I chose to handle the matter by
    # screening for 1, 2, and >=3 points, and returning WKT for Points, Lines,
    # and Polygons, respectively, and returning proper WKT.
    #
    # It's arguable that any encodings resulting in only one or two points
    # should be rejected.
    if len(coord_pair) == 1:
        wkt = 'POINT(%s)' % ','.join(coord_pair)
    elif len(coord_pair) == 2:
        wkt = 'POLYLINE(%s)' % ','.join(coord_pair)
    elif len(coord_pair) >= 3:
        wkt = 'POLYGON((%s,%s))' % (','.join(coord_pair), coord_pair[0])
    else:
        wkt = ''

    return wkt
