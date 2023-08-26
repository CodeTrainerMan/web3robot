# -*- coding: utf-8 -*-
"""
@Time ： 2023.02.26
@Auth ： william liu
@IDE ：PyCharm
"""
import requests, re, json, random, time

authorization_list = ["MTA2OTg2MTQ5MzI0MTI4MjYxMA.GKt9YE.nV2fWPwpxOTDD2Ao5GOKifMllncDbhJ4qvkr5w"]
dict_chanel_list = {"MTA2OTg2MTQ5MzI0MTI4MjYxMA.GKt9YE.nV2fWPwpxOTDD2Ao5GOKifMllncDbhJ4qvkr5w":["932761413372493854"]}


def basic_context():
    context_list = [
        "great!", "hello bro", "let's go !", "to the moon!", "gm", "couldn't sleep", "have a good day", "gm bro",
        "!!!!", "hello all", "welcome everyone", "thanks"
    ]
    text = random.choice(context_list)
    return text


def get_context(auth, chanel_id):

    if(chanel_id=="aaa"):
        context_list = [
            "great!", "hello bro", "let's go !", "to the moon!", "gm", "couldn't sleep", "have a good day", "gm bro",
            "!!!!", "hello all", "welcome everyone", "thanks"
        ]
        text = random.choice(context_list)
        return text

    print(auth, chanel_id)
    headr = {
        "Authorization": auth,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }
    # chanel_id = random.choice(chanel_list)
    url = "https://discord.com/api/v9/channels/{}/messages?limit=100".format(chanel_id)

    res = requests.get(url=url, headers=headr)


    result = json.loads(res.content)
    result_list = []
    for context in result:
        if ('<') not in context['content']:
            if ('@') not in context['content']:
                if ('http') not in context['content']:
                    if ('?') not in context['content']:
                        if len(str(context['content'])):
                            result_list.append(context['content'])

    return random.choice(result_list)


def chat():
    for key in range(len(authorization_list)):
        authorization = authorization_list[key]
        header = {
            "Authorization": authorization,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
        }
        for chanel_key in range(len(dict_chanel_list[authorization])):
            chanel_id = dict_chanel_list[authorization][chanel_key]
            print("用户:" + authorization, "id" + chanel_id, chanel_key)
            time.sleep(10)
            msg = {
                "content": basic_context(),  # 如果解决了cloudflare 可以换成 get_context()
                "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
                "tts": False
            }
            print(msg)
            url = 'https://discord.com/api/v9/channels/{}/messages'.format(chanel_id)
            try:
                res = requests.post(url=url, headers=header, data=json.dumps(msg))
                print(res)

            except:
                pass
            continue
        time.sleep(random.randrange(30, 50))


if __name__ == '__main__':
    while True:
        try:
            chat()
            sleeptime = random.randrange(120, 180)
            time.sleep(sleeptime)
        except:
            pass
        continue