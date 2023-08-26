import requests
from concurrent.futures import ThreadPoolExecutor
import os
import sys

class Download:
    def __init__(self, file_name, dir):
        self.file_name = file_name
        self.dir = dir
        self.__main(self.file_name)
        self.__download_concurrently()
        
    def __download(self, url):
        response = requests.get(url)
        path = os.path.join(self.dir, os.path.basename(url))
        with open(path, 'wb') as file:
            file.write(response.content)

    
    def __download_concurrently(self, num_threads=100):
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for url in self.links:
                executor.submit(self.__download, url)
                

    def __main(self, file_name):
        self.links = []
        with open(file_name, 'r') as f:
            while True:
                url = f.readline().split('\n')[0]
                if url == '':
                    break
                self.links.append(url)
                


if __name__ == '__main__':
    file_name = sys.argv[1]
    dir = sys.argv[2]
    
    Download(file_name, dir)
