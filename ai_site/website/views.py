import pickle
import re
import nltk
import json
from nltk.corpus import stopwords
from datetime import datetime   
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import pandas as pd

# Create your views here.


def index(response):
    dataset = pd.read_csv("../COVID19BE_CASES_AGESEX.csv")
    total=dataset["CASES"].sum()
    dataset=dataset.groupby(dataset['PROVINCE'])['CASES'].sum()
    dict = {"westvlaanderen":dataset["WestVlaanderen"],"oostvlaanderen":dataset["OostVlaanderen"],"antwerpen":dataset["Antwerpen"],
    "limburg":dataset["Limburg"],"vlaamsbrabant":dataset["VlaamsBrabant"],"brussel":dataset["Brussels"]
    ,"hennegouwen":dataset["Hainaut"],"waalsbrabant":dataset["BrabantWallon"],
    "liege":dataset["Liège"],"namen":dataset["Namur"],"luxemburg":dataset["Luxembourg"],"total":total}
    return render(response,"main/index.html",dict)

def predictor(response):
    return render(response,"main/predictor.html")



