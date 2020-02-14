import os
from tempfile import mkdtemp
from urllib.request import urlopen, urlretrieve


def pytest_addoption(parser):
    parser.addoption('--webdl', action='store_true', default=False,
                     help='Whether or not to download files '
                          'required for testing from the web')


def fetch_flag_files(webdl):
    if not webdl:
        dirname = os.path.join(os.path.dirname(__file__), '../../flagser/test')
        try:
            fnames = os.listdir(dirname)
            flag_files = [os.path.join(dirname, fname) for fname in fnames
                          if fname.endswith(".flag")]
        except FileNotFoundError:
            print(f'.flag files looked for in {dirname}, but directory does '
                  'not exist. Pass the optional argument --webdl to '
                  'automatically download these files into a temporary '
                  'folder and run tests.')
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


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    webdl = metafunc.config.option.webdl
    if 'flag_file' in metafunc.fixturenames:
        flag_files = fetch_flag_files(webdl)
        metafunc.parametrize('flag_file', flag_files)
