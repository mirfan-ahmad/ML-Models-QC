import os
import sys
from natsort import natsorted
from tqdm import tqdm

class Create_Labels:
    def __init__(self, mix_downloaded, *args):
        self.mix_downloaded = mix_downloaded
        self.true_annotated = list(args)
        self.storage_path = os.mkdir(os.path.jouin(os.getcwd(), 'Labels'))
        self.__create_from_folders()


    def __create_from_folders(self):
        images = natsorted(os.listdir(self.mix_downloaded))
        images_annotated = []
        for true in self.true_annotated:
            images_annotated.append(natsorted(os.listdir(os.path.join(os.getcwd(), true))))

        with open(f'{self.storage_path}/labels.csv', 'w') as file:
            index = 0
            for i in tqdm(range(images_annotated)):
                Response = f"{images_annotated[index][i]},"
                for j in range(images_annotated[i]):
                    if images_annotated[index][i] in images:
                        Response += '1,'
                    else:
                        Response += '0,'
                file.write(Response + '\b\n')
                index += 1
            print(f'Labeled file has been successfuly created on folders at {self.storage_path}')


if __name__ == '__main__':
    mix_downloaded = sys.argv[1]
    true_annotated = sys.argv[2:]

    Create_Labels(mix_downloaded, *true_annotated)
