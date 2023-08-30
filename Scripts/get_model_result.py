import requests
import os
import base64
import json
import cv2
import sys
import ast
import numpy as np
from natsort import natsorted
from tqdm import tqdm


class get_result_from_model():
    def __init__(self, endpoint, classes, Input, Output, **kwargs):
        self.endpoint = endpoint
        self.classes = list(classes)
        self.input = Input
        self.kwargs = kwargs
        self.output = Output
        
        self.__optional = list(kwargs.keys())
        self.__keys = ['single_img', 'url', 'model_name', 'response', 'generative']
        self.__set_kwargs()
        
        if self.kwargs['single_img']:
            self.Response = kwargs['response']
            print(self.__process_image(self.input))

        else:
            if self.kwargs['url']:
                self.__process_file()
            else:
                self.__process_folder()
    

    def __set_kwargs(self):
        for idx, k in enumerate(self.__keys):
            try:
                self.kwargs[self.__optional[idx]] = True
            except:
                pass
            if k not in self.__optional:
                self.kwargs[k] = False 
            


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
        if self.kwargs['url']:
            json_data = {
            "instances": [
                {
                    'image_url': image,
                    }   
                ]
            }

        else:
            image = cv2.imread(image)
            json_data = {
            "instances": [
                {
                    'image': self.__encode_image(image),
                    }
                ]
            }

        if self.kwargs['model_name']:
            headers = {
                'Content-Type': 'application/json',
                'model_name': self.kwargs['model_name']
            }
            
        else:
            headers = {
                'Content-Type': 'application/json',
            }

        link = self.endpoint

        response = requests.post(link, headers=headers, json=json_data)
        image_string = response.content
        
        if self.kwargs['generative']:
            det = json.loads(image_string)
            img_cv2 = self.__decode_base64_image(det['result'])
            cv2.imwrite('image4.jpg', img_cv2)
            print('Images has been written successfully')
            
        else:
            
            try:
                det = json.loads(image_string)            
                response = det['result']['classes']   # need to manually check the response
                if self.kwargs['response']:
                    RESPONSE = ''
                    for Class in self.classes:
                        if Class in response:
                            RESPONSE += f'{Class},'
                        else:
                            RESPONSE += ''
                    return RESPONSE
                
                else:
                    RESPONSE = ''
                    for Class in self.classes:
                        if Class in response:
                            RESPONSE += '1,'
                        else:
                            RESPONSE += '0,'
                    return RESPONSE

            except Exception as e:
                print('Exception Raised:', f'{image}', e)
                return '-1,' * len(self.classes)


    def __process_folder(self):
        images = natsorted(os.listdir(self.input))
        
        with open(f"{self.output}.csv", 'a') as f1:
            for image_filename in tqdm(images):
                image_path = os.path.join(self.input, image_filename)
                
                try:
                    RESPONSE = self.__process_image(image_path)  # Pass the correct arguments

                except Exception as e:
                    print(f'Error Raised on Image:{image_path}', e)
                    f1.write(f'{image_filename},{e}\n')
                    continue

                f1.write(f'{image_filename},{RESPONSE}\b\n')


    def __process_file(self):
        LINKS = []
        
        with open(self.input, 'r') as f:
            while True:
                lnk = f.readline().split('\n')[0]
                
                if lnk == '':
                    break
                LINKS.append(lnk)
        LINKS = natsorted(LINKS)
        
        with open(f"{self.output}/predicted.csv", 'a') as f1:
            for link in tqdm(LINKS):
                RESPONSE = self.__process_image(link)
                f1.write(f'{link},{RESPONSE}\n')

if __name__ == '__main__':
    endpoint = sys.argv[1]
    class_name = sys.argv[2]
    class_name = ast.literal_eval(class_name)
    Input = sys.argv[3]
    Output = sys.argv[4]
    optional_args = sys.argv[5:]
    
    optional_args_dict = {}
    for arg in optional_args:
        key, value = arg.split('=')
        optional_args_dict[key] = value
    
    get_result = get_result_from_model(endpoint, class_name, Input, Output, **optional_args_dict)

