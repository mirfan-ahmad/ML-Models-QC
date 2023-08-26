import requests
import os
import base64
import json
import cv2
from natsort import natsorted
from tqdm import tqdm
import numpy as np

class get_result_from_model():
    def __init__(self, Input, Output, endpoint, classes, **kwargs):
        self.endpoint = endpoint
        self.classes = list(classes)
        self.input = Input
        self.output = Output
        self.url = kwargs['url']
        self.model_name = kwargs['model_name']
        self.Response = kwargs['response']
        self.single_img = kwargs['single_img']
        
        if self.single_img == 'y':
            print(self.process_image(self.input))
        else:
            if self.url:
                self.process_file()
            else:
                self.process_folder()

    def __encode_image(self, image):
        _, img_byts = cv2.imencode('.jpg', image)
        img_byts = base64.b64encode(img_byts).decode('utf-8')
        return img_byts


    def __decode_base64_image(self, image_string):
        image_bytes = base64.b64decode(image_string)
        image_arr = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
        return image


    def __process_image(self, image):
        if not self.url:
            image = cv2.imread(image)
            json_data = {
            "instances": [
                {
                    'image': self.__encode_image(image),
                    }
                ]
            }

        else:
            json_data = {
            "instances": [
                {
                    'image_url': image,
                    }
                ]
            }

        if not self.model_name:
            headers = {
                'Content-Type': 'application/json',
            }
        else:
            headers = {
                'Content-Type': 'application/json',
                'model_name': self.model_name
            }

        link = self.endpoint

        response = requests.post(link, headers=headers, json=json_data)
        image_string = response.content
        
        # if mask:
        #     det = json.loads(image_string)
        #     img_cv2 = self.decode_base64_image(det['result'])
        #     cv2.imwrite('image4.jpg', img_cv2)
        #     print('Images has been written successfully')
        
        try:
            # keys_lst = ['classes']
            det = json.loads(image_string)
            # for key, item in det.items():
            #     keys_lst.append(key)
            
            # response = det['result']['classes']   # need to manually check the response
            if not self.Response:
                RESPONSE = ''
                for Class in self.classes:
                    if Class in response:
                        RESPONSE += '1,'
                    else:
                        RESPONSE += '0,'
                return RESPONSE
            
            else:
                RESPONSE = ''
                for Class in self.classes:
                    if Class in response:
                        RESPONSE += f'{Class},'
                    else:
                        RESPONSE += ''
                return RESPONSE

        except Exception as e:
            print('Exception Raised:', e)
            return '-1,' * len(self.classes)


    def __process_folder(self):
        images = natsorted(os.listdir(self.input))
        with open(f"{self.output}.csv", 'a') as f1:
            for image_filename in tqdm(images):
                image_path = os.path.join(self.input, image_filename)
                RESPONSE = self.process_image(image_path)  # Pass the correct arguments
                f1.write(f'{image_filename},{RESPONSE}\b\n')


    def __process_file(self):
        with open(self.input, 'r') as f:
            with open(f"{self.output}.csv", 'w') as f:
                while True:
                    link = f.readline().split('\n')[0]
                    if link != '':
                        RESPONSE = self.process_image(link, url=True)
                        f.write(f'{link},{RESPONSE}\n')
                    else:
                        break

# if __name__ == '__main__':
#     endpoint=''
#     class_name='bedroom'
#     Input='input.jpg'
#     Output = ''
#     get_result = get_result_from_model(Input, Output, endpoint, url=True, *class_name)