import logging, time, subprocess, requests, random, os, threading
from six.moves.urllib import request as urequest
import os.path as osp

sleep_seconds = 5
total_max_retries = 3
wget = 'wget'
wget_options = ["--read-timeout=1"]
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
    logging.info('download_url - {0} as {1}'.format(url, local_path))
    logging.debug('download_url - if download fails, will try {0} times and wait {1} seconds each time'.format(max_retries, sleep_seconds))
    sec = random.random() * download_sleep_seconds
    logging.info('download_url - sleeping {} seconds'.format(sec))
    time.sleep(sec)

    try:
        r = urequest.urlopen(url)
        content_size = int(r.headers.get('content-length',0))
        if content_size == 0:
            raise DownloadError('download_url - content size is equal to 0')
    except Exception as e:
        if max_retries > 0:
            logging.info('download_url - trying again with {} available retries, first sleeping {} seconds'.format(max_retries,sleep_seconds))
            time.sleep(sleep_seconds)
            sema.release()
            run_download(url, local_path, max_retries = max_retries - 1)
        return

    remove(local_path)
    command=[wget,'-O',ensure_dir(local_path),url]
    for opt in wget_options:
        command.insert(1,opt)
    logging.info(' '.join(command))
    subprocess.call(' '.join(command),shell=True)

    file_size = osp.getsize(local_path)

    logging.info('download_url - local file size {0} remote content size {1}'.format(file_size, content_size))

    if int(file_size) != int(content_size):
        logging.warning('download_url - wrong file size, trying again, retries available {}'.format(max_retries))
        if max_retries > 0:
            logging.info('download_url - sleeping {} seconds'.format(sleep_seconds))
            time.sleep(sleep_seconds)
            sema.release()
            run_download(url, local_path, content_size, max_retries = max_retries-1)
            return
        else:
            sema.release()
            os.remove(local_path)
            raise DownloadError('download_url - failed to download file {}'.format(url))

    info_path = local_path + '.size'
    open(ensure_dir(info_path), 'w').write(str(content_size))

def run_download(threads, url, local_path, max_retries=total_max_retries):
    thread = threading.Thread(target=download_url, args=(url,local_path,max_retries))
    threads.append(thread)
    thread.start()

def download_scenes(downloads, downloadMeta):
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
    for thread in threads:
        thread.join()

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
