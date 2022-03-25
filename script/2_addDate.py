import os
import pandas as pd
from tqdm import tqdm


def temp(csv_path):
    date = os.path.basename(csv_path).split('.')[0][-10:]
    hour = date[-2:]
    date = date[:4]+'-'+date[4:6]+'-'+date[6:8]
    df = pd.read_excel(csv_path)
    del df['lat']
    del df['lon']
    df['date'] = date
    df['hour'] = hour
    return df


def main():
    root = './data/prepro/hour'
    save = './data/newpro'
    os.makedirs(save, exist_ok=True)
    for i in os.listdir(root):
        xlsx_list = [os.path.join(root, i, j) for j in os.listdir(os.path.join(root, i))]
        df = temp(xlsx_list[0])
        for each in tqdm(xlsx_list[1:]):
            df = pd.concat([df, temp(each)])
        df.to_excel(os.path.join(save, f'{i}.xlsx'), encoding='utf-8-sig', index=0)


if __name__ == '__main__':
    main()
