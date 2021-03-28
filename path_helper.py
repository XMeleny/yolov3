import os


def split_url(url):
    if os.path.isdir(url):
        _dir = url
        filename = ""
        ext = ""
    else:
        (_dir, file) = os.path.split(url)
        temp = file.split('.')
        filename = temp[0]
        ext = temp[1]

    return {'dir': _dir, 'filename': filename, 'ext': ext}


def get_des_file_path(src_url, prefix='', suffix='', ext=''):
    split_result = split_url(src_url)

    # 添加前后缀
    filename = split_result['filename']
    if len(prefix) > 0:
        filename = prefix + "_" + filename
    if len(suffix) > 0:
        filename = filename + "_" + suffix

    # 添加文件格式
    if len(ext) == 0:
        filename = filename + "." + split_result['ext']
    else:
        filename = filename + "." + ext

    des_url = os.path.join(split_result['dir'], filename)
    # print(f'des_url = {des_url}')
    return des_url


if __name__ == '__main__':
    print(
        split_url(r"C:\Users\Meleny\Desktop\m'file\compulsory courses\GraduationProject\dataset\video\res_test\images"))

    print(split_url(
        r"C:\Users\Meleny\Desktop\m'file\compulsory courses\GraduationProject\dataset\video\res_test\images\res_test_127.jpg"))
