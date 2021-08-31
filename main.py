from api_logic import *

fecha_ayer_str = ApiAndDate.date_string(1)
fecha_antier_str = ApiAndDate.date_string(2)


#============Constantes para Stock API===================================================
#stock trading apikey = KARVXIENLRA00XVG
COMPANY_NAME = "Tesla Inc"
STOCK = "TSLA"
STOCK_APIKEY= "YOUR STOCK APIKEY"
STOCK_URL = 'https://www.alphavantage.co/query'
#===============================Constantes PARA PUSHOVER===========================================================
PUSHOVER_USER_KEY = "YOUR PUSHOVER USER KEY"
PUSHOVER_APP_TOKEN = "YOUR PUSHOVER APP TOKEN"

#=============Constantes para News API=====================================================
NEWS_APIKEY = "YOUR API KEY"
NEWS_URL_TOP_HEADLINES = "https://newsapi.org/v2/top-headlines"
NEWS_URL_EVERYTHING = "https://newsapi.org/v2/everything"
#===========================================================================================

stock_params_daily = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_APIKEY,
}

stock_params_intraday = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": STOCK_APIKEY,
}

news_params_top_headlines = {
    "q" : "Tesla",
    "apiKey": NEWS_APIKEY,
}

news_params_everything = {
    "q" : "Tesla",
    "apiKey": NEWS_APIKEY,
    "from": fecha_ayer_str,
    "to": fecha_ayer_str,
}

#  Use https://www.alphavantage.co
#https://www.alphavantage.co/support/#api-key
#Obten los datos de la acciones desde la api

stock_data = ApiAndDate.stock_response(STOCK_URL, stock_params_daily).json()['Time Series (Daily)']

#Se hace una lista con todos los datos dentro del time series y se ingresa a los dos ultimos valores de cierre
data_list = [value for (key, value) in stock_data.items()]
cifra_cierre_ayer = data_list[0]["4. close"]
cifra_cierre_antier = data_list[1]["4. close"]

#Se obtiene la diferencia en porcentaje de las cifras de cierre
diferencia = float(cifra_cierre_ayer)/ float(cifra_cierre_antier) * 100


#Use https://newsapi.org
#Si la diferencia es menor que 95%(Se pierde) se manda un mensaje con las noticias
if 95 > diferencia:
    the_new_news = ApiAndDate.news_to_send(NEWS_URL_EVERYTHING, news_params_everything)
    news_message = f"La acción de tesla perdió un: {100 - diferencia}%.\n" \
                        f"Valor antier ({fecha_antier_str}): {cifra_cierre_antier}USD\n" \
                        f"Valor ayer ({fecha_ayer_str}): {cifra_cierre_ayer}USD\n"
    for i in the_new_news:
        news_message += i + "\n"
        news_message += the_new_news[i] + "\n"
    ApiAndDate.send_by_pushover(news_message, PUSHOVER_APP_TOKEN, PUSHOVER_USER_KEY)
#Si la diferencia es mayor que un 105% (Se gana) se manda un mensaje con las noticias
elif diferencia > 105:
    the_new_news = ApiAndDate.news_to_send(NEWS_URL_EVERYTHING, news_params_everything)
    news_message = f"La acción de tesla ganó un: {diferencia-100}%\n" \
                   f"Valor antier ({fecha_antier_str}): {cifra_cierre_antier}USD\n" \
                   f"Valor ayer ({fecha_ayer_str}): {cifra_cierre_ayer}USD\n"
    for i in the_new_news:
        news_message += i + "\n"
        news_message += the_new_news[i] + "\n"
    ApiAndDate.send_by_pushover(news_message, PUSHOVER_APP_TOKEN, PUSHOVER_USER_KEY)
