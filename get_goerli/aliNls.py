# # AccessKey ID
# # LTAI5tHfCmYkTf5qmxdD6TiM
# #
# # AccessKey Secret
# # ALQd9wbmPbZefUmfMVritaSAANXRDj
# # 用户登录名称 111@1807398199205363.onaliyun.com
# # AccessKey ID LTAI5tRzn8D8GNuE9r6pGtEU
# # AccessKey Secret Gri4J4dnyY4ev5VdFBtWVw553iLxM1

from environs import Env
import http.client
import pydub
import json
from pydub import AudioSegment
import base64
import hashlib
import hmac
import requests
import time
import uuid
from urllib import parse

env = Env()
env.read_env()


class AliNLS:
    def __init__(self):
        self.alinpl_appKey = env.str("alinpl_appKey")
        self.alinpl_url = env.str("alinpl_url")
        self.alinpl_access_key_id = env.str("alinpl_access_key_id")
        self.alinpl_access_key_secret = env.str("alinpl_access_key_secret")
        self.alinpl_token, self.expire_time = self.create_token(self.alinpl_access_key_id,
                                                                self.alinpl_access_key_secret)

    @staticmethod
    def _encode_text(text):
        encoded_text = parse.quote_plus(text)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')

    @staticmethod
    def _encode_dict(dic):
        keys = dic.keys()
        dic_sorted = [(key, dic[key]) for key in sorted(keys)]
        encoded_text = parse.urlencode(dic_sorted)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')

    @staticmethod
    def create_token(access_key_id, access_key_secret):
        parameters = {'AccessKeyId': access_key_id,
                      'Action': 'CreateToken',
                      'Format': 'JSON',
                      'RegionId': 'cn-shanghai',
                      'SignatureMethod': 'HMAC-SHA1',
                      'SignatureNonce': str(uuid.uuid1()),
                      'SignatureVersion': '1.0',
                      'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      'Version': '2019-02-28'}
        # 构造规范化的请求字符串
        query_string = AliNLS._encode_dict(parameters)
        # 构造待签名字符串
        string_to_sign = 'GET' + '&' + AliNLS._encode_text('/') + '&' + AliNLS._encode_text(query_string)
        # 计算签名
        secreted_string = hmac.new(bytes(access_key_secret + '&', encoding='utf-8'),
                                   bytes(string_to_sign, encoding='utf-8'),
                                   hashlib.sha1).digest()
        signature = base64.b64encode(secreted_string)
        # 进行URL编码
        signature = AliNLS._encode_text(signature)
        # 调用服务
        full_url = 'http://nls-meta.cn-shanghai.aliyuncs.com/?Signature=%s&%s' % (signature, query_string)
        # 提交HTTP GET请求

        response = requests.get(full_url)
        if response.ok:
            root_obj = response.json()
            key = 'Token'
            if key in root_obj:
                token = root_obj[key]['Id']
                expire_time = root_obj[key]['ExpireTime']
                return token, expire_time
        print(response.text)
        return None, None

    def get_str_from_voice(self, audio_file):
        """

        :rtype: object
        
        """
        # 组装请求

        # 服务请求地址
        format = 'OPUS'
        sampleRate = 16000
        enablePunctuationPrediction = False
        enableInverseTextNormalization = False
        enableVoiceDetection = False
        # 设置RESTful请求参数
        request = self.alinpl_url + '?appkey=' + self.alinpl_appKey
        request = request + '&format=' + format
        request = request + '&sample_rate=' + str(sampleRate)

        if enablePunctuationPrediction:
            request = request + '&enable_punctuation_prediction=' + 'true'

        if enableInverseTextNormalization:
            request = request + '&enable_inverse_text_normalization=' + 'true'

        if enableVoiceDetection:
            request = request + '&enable_voice_detection=' + 'true'

        token = self.alinpl_token
        opus_file = self.mp3_2_opus(audio_file)
        # 读取音频文件
        with open(opus_file, mode='rb') as f:
            audioContent = f.read()
        host = 'nls-gateway-cn-shanghai.aliyuncs.com'
        # 设置HTTPS请求头部
        httpHeaders = {
            'X-NLS-Token': token,
            'Content-type': 'application/octet-stream',
            'Content-Length': len(audioContent)
        }

        # Python 2.x使用httplib
        # conn = httplib.HTTPConnection(host)

        # Python 3.x使用http.client
        conn = http.client.HTTPConnection(host)

        conn.request(method='POST', url=request, body=audioContent, headers=httpHeaders)

        response = conn.getresponse()
        print('Response status and response reason:')
        print(response.status, response.reason)

        body = response.read()
        try:
            body = json.loads(body)
            status = body['status']
            if status == 20000000:
                result = body['result']
                return result
            else:
                print('Recognizer failed!')
                return None

        except ValueError:
            print('The response is not json format string')

        conn.close()
        return None

    def mp3_2_opus(self, input_file="1.mp3", output_file="1.opus"):
        """

        :rtype: str
        """
        audio_file = AudioSegment.from_mp3(input_file)
        pcm_data = audio_file.export(output_file, format="opus").name;
        return pcm_data


# appKey = 'jjZxLBLl40Xk2eI0'
# token = 'd3de817ccb39458ba10cb2c87ae78e2d'
#
# # 服务请求地址
# url = 'https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/asr'
#
# # 音频文件
# audioFile = 'file.opus'
# format = 'OPUS'
# sampleRate = 16000
# enablePunctuationPrediction = False
# enableInverseTextNormalization = False
# enableVoiceDetection = False
#
# # 设置RESTful请求参数
# request = url + '?appkey=' + appKey
# request = request + '&format=' + format
# request = request + '&sample_rate=' + str(sampleRate)
#
# if enablePunctuationPrediction:
#     request = request + '&enable_punctuation_prediction=' + 'true'
#
# if enableInverseTextNormalization:
#     request = request + '&enable_inverse_text_normalization=' + 'true'
#
# if enableVoiceDetection:
#     request = request + '&enable_voice_detection=' + 'true'
#
# print('Request: ' + request)
#
# AliNLS.get_str_from_voice(request, token, audioFile)
# audioFile = AliNLS().mp3_2_opus().name


# 音频文件
# audioFile = '1.mp3'
#
# # print('Request: ' + request)
# str = AliNLS().get_str_from_voice(audioFile)
# print("finally str:" + str)
#
#
