import subprocess
import os
current_directory = os.path.dirname(__file__)
scrypy_dir = os.path.join(current_directory, 'myspider')

def run_scrapy_crawl():
    command1 = ['scrapy', 'crawl', 'parse_author', '-O', 'authors.json']
    command2 = ['scrapy', 'crawl', 'parse_quotes', '-O', 'quotes.json']
    subprocess.run(command1, cwd=scrypy_dir)
    subprocess.run(command2, cwd=scrypy_dir)


if __name__ == "__main__":
    run_scrapy_crawl()