from JobPool import *
from ComicDownloader import *

_logger = get_logger(__name__)


def _nop(data):
    _logger.info(f'_nop: data = {data}')
    if data == 5:
        return [JobItem(_nop, j) for j in range(40, 50)]
    return []


if __name__ == '__main__':
    url = r'http://www.nettruyen.com/truyen-tranh/vuong-gia-khong-nen-a-14653'
    pool = WorkerPool(10, JobItem(comic_parser, url))
    pool.start()
    pool.join()
    _logger.info("Done")
