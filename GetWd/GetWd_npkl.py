import os
import sys
import csv
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import logging
import notyscord as ntyd
import pickle
from pathlib import Path

urls = [
#["AmazonprimeVideo作品URL","Discordメンション用ロールID"],
["https://www.amazon.co.jp/gp/video/detail/B0C9QXPFTQ/ref=atv_hm_hom_c_TEdR0r_2_3", "hoge"],# 呪術
["https://www.amazon.co.jp/gp/video/detail/B0CJQ2TL1B/ref=atv_hm_hom_c_TEdR0r_2_1", "hoge"],# スパイ
["https://www.amazon.co.jp/gp/video/detail/B0CHLDW6FJ/ref=atv_hm_hom_c_TEdR0r_2_3", "hoge"],# MF
["https://www.amazon.co.jp/gp/video/detail/B0B5NS1ZNZ/ref=atv_hm_hom_c_5m1aZK_brws_3_1?jic=8%7CEgRzdm9k", "hoge"],# Drstone
["https://www.amazon.co.jp/gp/video/detail/B0CJRFZ6JD/ref=atv_hm_hom_c_TEdR0r_2_2", "hoge"] #フリーレン
]

os.chdir('./scriptdir')

# ログの記録するフォーマットを決める
log_format = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(filename='./testlog/log.log', level=logging.INFO, format=log_format)
logging.info('START')

pklfile = './pklfile/episnum.pkl'

try:
    # 作品一覧とエピソード数のpklを読み込む
    with open(pklfile, "rb") as tf:
        dict = pickle.load(tf)
        # reader = csv.DictReader(f)
        logging.info('Opened csv file"')

except:
    # 何かしら失敗した場合はDiscordに通知、ログ
    # ntyd.sendm('ファイルの取得に失敗しました')
    logging.error('Failed to get csv file')

    dict = {}   # 辞書を新たに作成
    dict["none"] = 0

for url in urls: # urlsに登録済みのページを順にチェック
    surl = url[0]
    tlt = url[1]
    logging.info(surl)
    try:
        # HTMLを取得する
        html = urllib.request.urlopen(surl)
        # HTMLのステータスコード（正常に取得できたかどうか）を記録する
        logging.info('HTTP STATUS CODE: ' + str(html.getcode()))
    except:
        # 取得に失敗した場合もLINEに通知してログを取る
        print('URLの取得に失敗しました')
        # print('URLの取得に失敗しました')
        # 念の為強制終了
        sys.exit(1)
    soup = BeautifulSoup(html, "html.parser")
    # タイトルを取得
    title = soup.find("h1")
    for titl in title:
        print(titl)
    if titl not in dict:
        dict[str(titl)] = 0
    # HTMLの中から各エピソードに共通で含まれるclass(c5qQpO)を抽出
    tags = soup.find_all(class_="c5qQpO")
    links = list()
    for tag in tags:
        # c5qQpOからエピソード序数を取り出す
        links.append(tag.get('id'))
    # print(links)
    epinum = len(links)
    epiold = dict[titl] # CSVに記録されている前回エピソード数

    if epinum != epiold:
        ntyd.sendm('<@&'+tlt+'> "'+titl+'" '+"のエピソードが更新されました")
        # epinumn = epinum
        dict[titl] = epinum # 記録用CSVのエピソード数も更新

with open(pklfile, "wb") as tf:
    pickle.dump(dict, tf)
