import requests
import json

class YandexGPT:
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    API_TOKEN = ''
    CATALOG = ''

    def get_answer(self,text):
        payload = {
            "modelUri": f"gpt://{self.CATALOG}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.4,
                "maxTokens": 100,
                "reasoningOptions": {
                    "mode": "DISABLED"
                }
            },
            "messages": [
                {
                    "role": "user",
                    "text": text,
                },
                {
                    "role": "system",
                    "text": "Отвечай как Diogen и еще больше слов"
                }
            ]
        }
        headers = {'Authorization': f"Api-Key {self.API_TOKEN}"}
        res = requests.post(self.url, json=payload, headers=headers)
        res = res.json()
        text = res['result']['alternatives'][0]['message']['text']
        print(res)
        print(text)

while True:
    text = input('Твой вопрос ')
    jandex = YandexGPT()
    res = jandex.get_answer(text)
    print(res)


