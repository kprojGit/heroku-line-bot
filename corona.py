from email import message
import pandas as pd
import requests
import io
import datetime

def get_num_infect():

    # URL
    url = "https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv"
    r = requests.get(url).content
    df = pd.read_csv(io.BytesIO(r),sep=",")

    print(df)

    # 今
    now = datetime.datetime.now()
    # 一日前
    yesterday = now - datetime.timedelta(days=1)

#strftimeで%と文字の間にハイフンを追加すると、先行ゼロを削除できるが　windowsの場合は#を使用するので気を付けないとエラーになる

    df_yesterday = df[df['日付'] == yesterday.strftime('%Y/%-m/%-d')]
    day = yesterday.strftime('%Y/%-m/%-d')
    df_s = df_yesterday.sort_values('各地の感染者数_1日ごとの発表数',ascending=False)

    i=1
    message=''
    for prefecture in df_s['都道府県名']:
        df_a = df_yesterday[df_yesterday['都道府県名'] == prefecture]
        infected = int(df_a['各地の感染者数_1日ごとの発表数'])
        print(str(i)+"位 "+prefecture+" : "+str(infected)+"人\n")
        message = message + str(i)+"位　"+prefecture+" : "+str(infected)+"人\n"
        i=i+1
        if i > 5:
            break
    message= '\n'+str(day)+' 新規感染者数\n'+message
    return message



# 結果の確認
# get_num_infect()
    
