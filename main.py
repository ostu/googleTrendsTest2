import pandas as pd
from pytrends.request import TrendReq
pytrend = TrendReq()

kw_list_rivals = ["яндекс", "yandex", "гугл", "google", "спутник"]
geo = pd.read_csv('iso3166-2_ru.csv')

def scrape_google(kwl, geocode):
    pytrend.build_payload(kwl, cat=47, timeframe='2001-01-01 2022-02-18', geo=geocode, gprop='')
    trends = pytrend.interest_over_time()
    try:
        trends = trends.drop(columns=['isPartial'])
    except:
        pass
    return trends

df = pd.DataFrame()
for i in range(len(geo)):
    df1 = scrape_google(kw_list_rivals, geo["geocode"][i])
    df1 = df1.unstack().reset_index(name='value')
    df1.rename(columns={'level_0': 'brand'}, inplace=True)
    df1 = df1.pivot(index='date', columns=['brand'], values='value')
    df1["yandex"] = df1["яндекс"] + df1["yandex"]
    df1["google"] = df1["гугл"] + df1["google"]
    df1["спутник"] = df1["спутник"]
    df1.pop("yandex")
    df1.pop("google")
    df1.pop("спутник")
    df1 = round(df1 * (100/df1.max().max())).astype(int)
    df1["geocode"] = geo["geocode"][i]
    df1["geoname"] = geo["geoname"][i]
    df = df.append(df1)

#print(df)
df.to_csv('google_trends_rivals.csv')

