from pathlib import Path
from google.cloud import vision

def render_doc_text(filein):

    client = vision.ImageAnnotatorClient()

    p = Path(__file__).parent / filein
    with p.open('rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    data_list = []
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    box = [{'x':v.x, 'y':v.y} for v in word.bounding_box.vertices]
                    text = [symbol.text for symbol in word.symbols]
                    data_list.append([box, ''.join(text)])
    return data_list
