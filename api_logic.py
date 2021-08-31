import datetime
import requests
class ApiAndDate:

    def news_to_send(news_url_everything:str, news_params_everything:dict) -> dict:
        "returns a dict of 3 items with the heading as key and url of article as value"
        news_response = requests.get(url=news_url_everything, params=news_params_everything)
        news_response.raise_for_status()

        news_dict = {}

        for i in range(3):
            news_dict[news_response.json()["articles"][i]["title"]] = news_response.json()["articles"][i]["url"]

        return news_dict

    def send_by_pushover(message: str, pushover_app_token:str, pushover_user_key:str):
        "Envia string por pushover el token es de un smartphone"
        pushover_response = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": pushover_app_token,
            "user": pushover_user_key,
            "message": message
        })
        print(pushover_response.text)

    def stock_response(stock_url: str, stock_params_daily:dict):
        stock_response = requests.get(stock_url, params=stock_params_daily)
        stock_response.raise_for_status()
        return stock_response

    def date_string(days_to_substract:int) -> str:
        """Restará el numero de días dado para dar un str con la fecha de ayer en el
        formato necesario 0000-00-00/Año-Mes-Día"""
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=days_to_substract)
        needed_date_str = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"
        return needed_date_str