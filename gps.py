import math
import os
import json

import folium
import pynmea2

for point in os.listdir('data/'):    
    print(point)
    file = open(f'data/{point}', encoding='utf-8')
    latitude = []
    longitude = []
    altitude = []

    SV = {}

    for line in file.readlines():
        try:
            if "GPGSV" in line:
                msg = pynmea2.parse(line)
                if msg.sv_prn_num_1.isdigit():
                    if msg.sv_prn_num_1 not in SV:
                        SV[msg.sv_prn_num_1] = []
                    SV[msg.sv_prn_num_1].append({
                        'deg': msg.elevation_deg_1 if msg.elevation_deg_1.isdigit() else 0,
                        'azimuth': msg.azimuth_1 if msg.azimuth_1.isdigit() else 0,
                        'snr': msg.snr_1 if msg.snr_1.isdigit() else 0
                    })
                
                if msg.sv_prn_num_2.isdigit():
                    if msg.sv_prn_num_2 not in SV:
                        SV[msg.sv_prn_num_2] = []
                    SV[msg.sv_prn_num_2].append({
                        'deg': msg.elevation_deg_2 if msg.elevation_deg_2.isdigit() else 0,
                        'azimuth': msg.azimuth_2 if msg.azimuth_2.isdigit() else 0,
                        'snr': msg.snr_2 if msg.snr_2.isdigit() else 0
                    })

                if msg.sv_prn_num_3.isdigit():
                    if msg.sv_prn_num_3 not in SV:
                        SV[msg.sv_prn_num_3] = []
                    SV[msg.sv_prn_num_3].append({
                        'deg': msg.elevation_deg_3 if msg.elevation_deg_3.isdigit() else 0,
                        'azimuth': msg.azimuth_3 if msg.azimuth_3.isdigit() else 0,
                        'snr': msg.snr_3 if msg.snr_3.isdigit() else 0
                    })

                if msg.sv_prn_num_4.isdigit():
                    if msg.sv_prn_num_4 not in SV:
                        SV[msg.sv_prn_num_4] = []
                    SV[msg.sv_prn_num_4].append({
                        'deg': msg.elevation_deg_4 if msg.elevation_deg_4.isdigit() else 0,
                        'azimuth': msg.azimuth_4 if msg.azimuth_4.isdigit() else 0,
                        'snr': msg.snr_4 if msg.snr_4.isdigit() else 0
                    })

            if "GPGGA" in line:
                msg = pynmea2.parse(line)     
                if msg.latitude and msg.longitude and msg.altitude:
                    latitude.append(msg.latitude)
                    longitude.append(msg.longitude)
                    altitude.append(msg.altitude)
                
        except Exception as e:
            print('Error: {}'.format(e))
            continue

    print(SV.keys())
    print(sum(latitude)/len(latitude), sum(longitude)/len(longitude))

    origin_point = [sum(latitude)/len(latitude), sum(longitude)/len(longitude)]
    
    fmap = folium.Map(location=origin_point, zoom_start=17, control_scale=True)
    fmap.add_child(folium.Marker(location=origin_point, popup=f"{point.split('.')[0]}"))
    # fmap.add_child(folium.Marker(location=origin_point, popup=f"{point.split('.')[0]} <br> altitude: {(sum(altitude)/len(altitude)):.2f}"))

    list_colors = [
        "#00FF00",
        "#12FF00",
        "#24FF00",
        "#35FF00",
        "#47FF00",
        "#58FF00",
        "#6AFF00",
        "#7CFF00",
        "#8DFF00",
        "#9FFF00",
        "#B0FF00",
        "#C2FF00",
        "#D4FF00",
        "#E5FF00",
        "#F7FF00",
        "#FFF600",
        "#FFE400",
        "#FFD300",
        "#FFC100",
        "#FFAF00",
        "#FF9E00",
        "#FF8C00",
        "#FF7B00",
        "#FF6900",
        "#FF5700",
        "#FF4600",
        "#FF3400",
        "#FF2300",
        "#FF1100",
        "#FF0000",
    ]
    list_colors.reverse()
    color_dict = {i: list_colors[i] for i in range(len(list_colors))}

    detail = {}

    length = .1
    for i in SV.keys():
        azimuths = list(map(lambda x: int(x['azimuth']), SV[i]))
        snrs = list(map(lambda x: int(x['snr']), SV[i]))
        degs = list(map(lambda x: int(x['deg']), SV[i]))
        azimuth = sum(azimuths)/len(azimuths)
        snr = sum(snrs)/len(snrs)
        deg = sum(degs)/len(degs)
        print(i, azimuth, snr, deg)
        end_lat = origin_point[0] + length * math.sin(math.radians(azimuth))
        end_lon = origin_point[1] + length * math.cos(math.radians(azimuth))
        fmap.add_child(folium.PolyLine(locations=[origin_point, [end_lat, end_lon]], color=color_dict[round(snr/(50/len(color_dict)))], popup=f"PRN:{i}"))
        detail[i] = {
            'azimuth': azimuth,
            'deg': deg,
            'snr': snr
        }
        # fmap.add_child(folium.Circle(location=[end_lat, end_lon], color="blue", fill_color="blue", fill=True, popup=f"prn: {i} <br> deg: {deg:.2f} <br> azimuth: {azimuth:.2f} <br> snr: {snr:.2f}"))
    json.dump(detail, open(f"json/{point.split('.')[0]}.json", 'w'), ensure_ascii=False)
    fmap.save(f"templates/maps/{point.split('.')[0]}.html")

json.dump(list(map(lambda x: x.split('.')[0], os.listdir('data/'))), open("json/place.json", 'w'), ensure_ascii=False)
