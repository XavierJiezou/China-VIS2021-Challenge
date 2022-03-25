import requests
import pandas as pd
from tqdm import tqdm


def query(location_list, key):
    url = 'https://restapi.amap.com/v3/geocode/regeo'
    params = {
        'key': key,
        'location': location_list,  # limit: 20
        'batch': 'true'
    }
    res = requests.get(url, params=params).json()
    address_list = []
    if res['status'] == '1':
        for i in range(len(res['regeocodes'])):
            temp = res['regeocodes'][i]['addressComponent']
            province = temp['province']
            city = temp['city']
            if not city:
                if province in ['北京市', '天津市', '上海市', '重庆市']:
                    city = province  # 更改直辖市的 `province`` 和 `city` 字段都是直辖市的名称
                else:
                    # 更改省直辖县的 `city` 字段为 `district` 字段的数值
                    city = temp['district']
            else:
                pass
            address_list.append({
                'province': province,
                'city': city
            })
        return address_list
    else:
        print({
            'info': res['info'],
            'location_list': location_list
        })


def reGeo(csv_path, key):
    df = pd.read_csv(csv_path, encoding='utf-8')
    df.columns = [item.strip() for item in df.columns.values]
    del df['']
    lon = df['lon'].astype(str)
    lat = df['lat'].astype(str)
    new = lon + ',' + lat
    location_total = []
    for i in range(0, len(new.values), 20):
        if i+20 > len(new.values):
            end = len(new.values)
        else:
            end = i+20
        location_total.append('|'.join(new.values[i:end]))
    address_total = []
    for item in tqdm(location_total):
        address_total += query(item, key)
    province = []
    city = []
    for item in address_total:
        province += [item['province']]
        city += [item['city']]
    df['province'] = province
    df['city'] = city
    df.to_csv('template.csv', encoding='utf-8', index=0)


if __name__ == '__main__':
    # 请务必将 'key' 替换为您自己申请的高德地图 API 的 key
    reGeo('./data/hour/2013/CN-Reanalysis2013010100.csv', 'key')
