import os
from tempfile import mkdtemp
from urllib.request import urlopen, urlretrieve


def fetch_flag_files(webdl):
    if not webdl:
        dirname = os.path.join(os.path.dirname(__file__), "../../flagser/test")
        flag_files = [os.path.join(dirname, fname)
                      for fname in os.listdir(dirname)
                      if fname.endswith(".flag")]
    else:
        # Download from remote bucket
        temp_dir = mkdtemp()
        bucket_url = 'https://storage.googleapis.com/l2f-open-models/' \
                     'giotto-tda/flagser/test/'
        flag_files_list = bucket_url + 'flag_files_list.txt'
        with urlopen(flag_files_list) as f:
            flag_file_names = f.read().decode('utf8').splitlines()
            flag_files = []
            for fname in flag_file_names:
                url = bucket_url + fname
                fpath = os.path.join(temp_dir, fname)
                urlretrieve(url, fpath)
                flag_files.append(fpath)
    return flag_files