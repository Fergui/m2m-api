import logging, time, subprocess, requests, random, os, threading
from six.moves.urllib import request as urequest
import os.path as osp

ACQ_PATH = './ingest'

sleep_seconds = 5
total_max_retries = 3
wget = 'wget'
wget_options = ["--quiet", "--read-timeout=1", "--random-wait", "--progress=dot:giga", "--limit-rate=10m"]
download_sleep_seconds = 3

max_threads = 10
sema = threading.Semaphore(value=max_threads)
threads = []

class DownloadError(Exception):
    """
    Raised when the downloader is unable to retrieve a URL.
    """
    pass

def download_url(url, local_path, max_retries=total_max_retries, sleep_seconds=sleep_seconds):
    """
    Download a remote URL to the location local_path with retries.

    On download, the file size is first obtained and stored.  When the download completes,
    the file size is compared to the stored file.  This prevents broken downloads from
    contaminating the processing chain.

    :param url: the remote URL
    :param local_path: the path to the local file
    :param max_retries: how many times we may retry to download the file
    :param sleep_seconds: sleep seconds between retries
    """
    sema.acquire()
    bname = osp.basename(local_path)
    logging.info('download_url - {} - downloading {} as {}'.format(bname, url, local_path))
    sec = random.random() * download_sleep_seconds
    time.sleep(sec)

    try:
        r = requests.get(url, stream=True)
        content_size = int(r.headers.get('content-length',0))
        if content_size == 0:
            raise DownloadError('download_url - content size is equal to 0')
    except Exception as e:
        if max_retries > 0:
            logging.info('download_url - {} - trying again with {} available retries'.format(bname, max_retries))
            time.sleep(sleep_seconds)
            sema.release()
            download_url(url, local_path, max_retries = max_retries - 1, sleep_seconds=sleep_seconds)
        return

    remove(local_path)
    logging.info('download_url - {} - starting download...'.format(bname))
    command=[wget,'-O',ensure_dir(local_path),url]
    for opt in wget_options:
        command.insert(1,opt)
    logging.debug(' '.join(command))
    subprocess.call(' '.join(command),shell=True)

    file_size = osp.getsize(local_path)
    logging.info('download_url - {} - local file size {} remote content size {}'.format(bname, file_size, content_size))
    if int(file_size) != int(content_size):
        logging.warning('download_url - {} - wrong file size, trying again, retries available {}'.format(bname, max_retries))
        if max_retries > 0:
            time.sleep(sleep_seconds)
            sema.release()
            download_url(url, local_path, content_size, max_retries = max_retries-1, sleep_seconds=sleep_seconds)
            return
        else:
            sema.release()
            os.remove(local_path)
            raise DownloadError('download_url - {} - failed to download file {}'.format(bname, url))

    info_path = local_path + '.size'
    open(ensure_dir(info_path), 'w').write(str(content_size))
    logging.info('download_url - {} - success download'.format(bname))
    sema.release()

def run_download(threads, url, local_path, max_retries=total_max_retries):
    thread = threading.Thread(target=download_url, args=(url,local_path,max_retries))
    threads.append(thread)
    thread.start()

def download_scenes(downloads, downloadMeta):
    logging.info('download_scenes - downloading {} scenes'.format(len(downloads)))
    for download in downloads:
        idD = str(download['downloadId'])
        displayId = downloadMeta[idD]['displayId']
        url = download['url']
        local_path = osp.join(ACQ_PATH,displayId+'.tar')
        if available_locally(local_path):
            logging.info('downloadScenes - file {} is locally available'.format(local_path))
        else:
            run_download(threads, url, local_path)
        downloadMeta[idD].update({'url': url, 'local_path': local_path})
    finished = 0
    for thread in threads:
        thread.join()
        finished += 1
        logging.info('download_scenes - download finished by {}/{} scenes'.format(finished,len(threads)))
    logging.info('download_scenes - all download scenes finished')

def ensure_dir(path):
    """
    Ensure all directories in path if a file exist, for convenience return path itself.

    :param path: the path whose directories should exist
    :return: the path back for convenience
    """
    path_dir = osp.dirname(path)
    if not osp.exists(path_dir):
        os.makedirs(path_dir)
    return path

def remove(tgt):
    """
    os.remove wrapper
    """
    if osp.isfile(tgt):
        logging.info('remove - file {} exists, removing'.format(tgt))
        os.remove(tgt)

def available_locally(path):
    """
    Check if a file is available locally and if it's file size checks out.

    :param path: the file path
    """
    info_path = path + '.size'
    if osp.exists(path) and osp.exists(info_path):
        content_size = int(open(info_path).read())
        return osp.getsize(path) == content_size
    return False
