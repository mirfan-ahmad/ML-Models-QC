import sys
import shutil
import cv2
import os


class Annotate_Images:
    def __init__(self, img_dir, main_dir):
        self.meta = ''
        self.meta_dict = dict()
        self.img_dir = img_dir
        self.main_dir = main_dir
        self.__create_folders()
        print(f'\n{self.meta}')
        self.__annotate()
    
    def __create_folders(self):
        i = 1
        while True:
            folder_name = input('Enter folder name: ')
            self.meta += f'Press {i} to choose {folder_name}\n'
            self.meta_dict[str(i)] = folder_name
            os.makedirs(os.path.join(self.main_dir, folder_name), exist_ok=True)
            if input('Do you want to create a new folder (y/n)? ') == 'n':
                break
            i += 1
    
    def __paste(self, tag, image_name):
        path = os.path.join(self.img_dir, image_name)
        print(path)
        shutil.copy(path, os.path.join(self.main_dir, tag, image_name))
    
    def __annotate(self):
        images = os.listdir(self.img_dir)
        
        for idx, img_name in enumerate(images):
            try:
                image = cv2.imread(os.path.join(self.img_dir, img_name))
                print('checking:', idx)
                
                cv2.imshow(str(idx), image)
                key = chr(cv2.waitKey(0) & 0xFF)
                
                while True:
                    key = chr(cv2.waitKey(0) & 0xFF)
                    if key in self.meta_dict:
                        self.__paste(self.meta_dict[key], img_name)
                    if key == 'q':
                        break
                cv2.destroyAllWindows()

            except Exception as e:
                print(e)


if __name__ == '__main__':
    img_dir = sys.argv[1]
    main_dir = os.getcwd()
    
    Annotate_Images(img_dir, main_dir)

