import requests
import base64
import json
API_KEY = ''
GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='

# TEXT_DETECTION:比較的短い文字
# DOCUMENT_TEXT_DETECTION:文章
DETECTION_TYPE = "DOCUMENT_TEXT_DETECTION"

def request_cloud_vison_api(image_base64, type="DOCUMENT_TEXT_DETECTION"):
    """ http のリクエストでVisionAPIにアクセス """
    api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_base64.decode('utf-8')
            },
            'features': [{
                'type': type,
                'maxResults': 10,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()


def img_to_base64(filepath):
    """ 画像データをエンコード """
    with open(filepath, 'rb') as img:
        img_byte = img.read()
    return base64.b64encode(img_byte)


def render_doc_text(file_path):

    result = request_cloud_vison_api(image_base64=img_to_base64(file_path),
                                     type=DETECTION_TYPE)

    data_list = []
    # データの取得 textAnnotationsに座標とテキスト fullTextAnnotationにテキスト
    result_list = result["responses"][0]["textAnnotations"]
    for d in result_list:
        data_list.append([d['boundingPoly']['vertices'], d['description']])

    # 1つ目除外
    data_list = data_list[1:len(data_list)]
    return data_list

