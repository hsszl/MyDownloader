import requests
import multitasking
import time
import tqdm


def get_file_size(url):
    response = requests.head(url)
    file_size = response.headers.get('Content-Length')
    if file_size is None:
        return '该文件不支持多线程分段下载！'
    return int(file_size)


while True:
    f_a = {}

    @multitasking.task
    def download(start, end, no):
        global f_a
        headers = {"Range": f"bytes={start}-{end}"}
        res = requests.get(url, headers=headers)
        f_a[str(no)] = res.content
        if len(f_a) != block_n:
            print("\r", end="")
        else:
            print("It's OK!")
        print("Download progress NO.{0}, {1}/{2} ok: {3}%: |".format(no, len(f_a), block_n, int(no / block_n * 100)),
              "▋" * (int(no / block_n * 35)), end="|")

    print("")
    url = input("Please copy the url to here: ")
    block_n = input("How many blocks you want?: ")
    if block_n == "":
        block_n = 4
    else:
        block_n = int(block_n)
    f_s = get_file_size(url)
    if f_s == '该文件不支持多线程分段下载！':
        print('该文件不支持多线程分段下载！')
        f_s = input("the size: ")
        if f_s == "":
            print(f_s)
    size_one = int(f_s / block_n)
    print(f"The size is: {get_file_size(url)}, An block size is: {size_one}")
    filename = input("please input to file name: ")

    for i in tqdm.trange(block_n, desc="Create thread"):
        if i != block_n - 1:
            download(size_one * i, size_one * (i + 1) - 1, i + 1)
        else:
            download(size_one * i, get_file_size(url), i + 1)

    open(filename, 'w').close()
    with open(filename, 'ab+') as f:
        while True:
            time.sleep(0.1)
            if len(f_a) == block_n:
                for x in tqdm.trange(len(f_a), desc="making file"):
                    f.write(f_a[str(x + 1)])
                break
            else:
                continue
