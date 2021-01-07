import base64
import io
import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from fbprophet import Prophet

df = pd.read_csv("../COVID19BE_CASES_AGESEX.csv")


def get_time_series_province(province):
    pd.options.mode.chained_assignment = None
    df_updated = df.dropna(axis=0)
    df_province = df_updated[(df_updated['PROVINCE'] == province)]
    df_province["DATE"] = pd.to_datetime(df_province["DATE"], format='%Y-%m-%d')
    df_province.drop(["REGION", "AGEGROUP", "SEX", "PROVINCE"], axis=1, inplace=True)
    return df_province.groupby("DATE", as_index=False).sum()


def get_time_series_total():
    pd.options.mode.chained_assignment = None
    df_updated = df.dropna(axis=0)
    df_updated["DATE"] = pd.to_datetime(df_updated["DATE"], format='%Y-%m-%d')
    df_updated.drop(["REGION", "AGEGROUP", "SEX"], axis=1, inplace=True)
    return df_updated.groupby('DATE', as_index=False).sum()


def make_prediction(date1, date2):
    my_dates = pd.date_range(date1, date2).tolist()
    future = pd.DataFrame({'ds': my_dates})
    return future


def fig_to_b64(fig):
    pic_IObytes = io.BytesIO()
    fig.savefig(pic_IObytes, format='png')
    pic_IObytes.seek(0)
    return base64.b64encode(pic_IObytes.read()).decode('ascii')


def get_provinces(response):
    arr = df.PROVINCE.unique()
    arr = np.append(["All"], arr)
    js = pd.Series(arr).to_json(orient='values')
    return HttpResponse(js)


def index(response):
    total = df["CASES"].sum()
    dataset = df.groupby(df['PROVINCE'])['CASES'].sum()
    dict = {
        "westvlaanderen": dataset["WestVlaanderen"],
        "oostvlaanderen": dataset["OostVlaanderen"],
        "antwerpen": dataset["Antwerpen"],
        "limburg": dataset["Limburg"],
        "vlaamsbrabant": dataset["VlaamsBrabant"],
        "brussel": dataset["Brussels"],
        "hennegouwen": dataset["Hainaut"],
        "waalsbrabant": dataset["BrabantWallon"],
        "liege": dataset["Liège"],
        "namen": dataset["Namur"],
        "luxemburg": dataset["Luxembourg"],
        "total": total
    }
    return render(response, "main/index.html", dict)


def predictor(response):
    if response.method != "POST":
        return render(response, "main/predictor.html")

    province = response.POST.get("province", "All")
    start = response.POST.get("start", '2020-10-01')
    end = response.POST.get("end", '2021-03-31')

    if province == "All":
        train = get_time_series_total()
    else:
        train = get_time_series_province(province)

    train.columns = ["ds", "y"]
    m = Prophet(yearly_seasonality=True, daily_seasonality=True)
    m.fit(train)

    forecast = m.predict(make_prediction(start, end))
    fig = m.plot(forecast)
    return render(response, "main/predictor.html", {"url": "data:image/png;base64," + fig_to_b64(fig)})
