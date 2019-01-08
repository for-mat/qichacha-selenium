# coding:utf-8
import urllib, urllib2, base64, sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def get_location(image,click_word):
    access_token = '24.7677cc6b1ab53f2b6e952552745688a7.2592000.1546054509.282335-14973263'
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token

    img = image

    '''
    #通过打开本地图片获取图片的base64编码
    # 二进制方式打开图文件
    f = open(r'a.jpg', 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    '''

    #params = {"image": img}
    #params = urllib.urlencode(params)
    body={"image": img, "recognize_granularity":"small"}    #recognize_granularity设置为small是识别单个字的位置
    data = urllib.urlencode(body)
    request = urllib2.Request(url, data)
    #request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read()               #这里是字符串类型的
    content = json.loads(content)           #通过json.loads()将string转为dict
    words_result = content['words_result']


    '''处理得到字符的位置信息'''
    lines_num = len(words_result)
    words_list = []
    for i in range(lines_num):
        a = words_result[i]['chars']
        for n in range(len(a)):
            words_list.append(a[n])

    words_dict = {i:v for i,v in enumerate(words_list)}
    #print words_dict

    word_num = len(words_dict)

    '''判断需要点击的文字是否存在，返回位置信息'''
    for i in range(word_num):
        if click_word in str(words_dict[i]):
             location = words_dict[i]['location']
             #print location
             return location

    try:
        location
    except NameError:
        location = words_dict[0]['location']
        return location


#get_location(click_word='\u9ad8',image='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')


