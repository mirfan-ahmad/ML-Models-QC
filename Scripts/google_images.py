from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler
import sys

class MyImageDownloader(ImageDownloader):
    def process_meta(self, task):
        super(MyImageDownloader, self).process_meta(task)
        
        with open(self.txt_path, 'a') as f:
            f.write(task['file_url'] + '\n')


class MyGoogleImageCrawler(GoogleImageCrawler):
    def __init__(self, downloader_cls=MyImageDownloader, *args, **kwargs):
        super(MyGoogleImageCrawler, self).__init__(downloader_cls=downloader_cls, *args, **kwargs)


if __name__ == "__main__":
    search_query = sys.argv[1]
    number_of_images = int(sys.argv[2])
    output_path = sys.argv[3]
    
    crawler = MyGoogleImageCrawler(storage={'root_dir': output_path})
    crawler.downloader.txt_path = '/'.join(output_path.split('/')[:-2]) + '/links.txt'
    search_results = crawler.crawl(keyword=search_query, max_num=number_of_images)
    