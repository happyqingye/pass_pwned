import time
import sys
import hashlib
import requests
from utils import Color, progress_bar, extract_passwd, write_pass_to_file


__author__ = 'sehlat57'


class PassEncrypt(object):

    def __init__(self, passwd):
        self.passwd = passwd

    def encrypt(self):
        """
        Encrypt password with SHA1 algorithm
        :return: ecrypted password
        """
        encryption = hashlib.sha1()
        encryption.update(self.passwd.encode())
        return encryption.hexdigest()


class HIBPApi(object):

    color = Color()
    uri = 'https://api.pwnedpasswords.com/range/'
    headers = {'user_agent': 'pass_pwned'}

    def __init__(self, passwd, file_passwd):
            self.passwd = passwd
            self.path = file_passwd

    def passwd_check(self, attempts=3):
        """
        Check single password in HIBP database using web-API
        (sleeping between request to prevent HTTP 429 (Rate limit exceeded),
        please refer to https://haveibeenpwned.com/API/v2)
        :param attempts: number of attempts to check
        :return: result of the check as string
        """
        try:
            print('[{}] Checking password in DB:'.format(
                self.color.brush('working', 'cyan')))
            encrypted_pass = PassEncrypt(self.passwd).encrypt()
            for attempt in range(attempts):
                hibp_request = requests.get('{}{}'.format(self.uri,
                                                          encrypted_pass[:5]),
                                            headers=self.headers)
                if hibp_request.status_code == 200:
                    raw_data = hibp_request.text.split('\n')
                    suffixes = {hash_suff.split(':')[0]:int(hash_suff.split(':')[1].replace('\r', '')) for hash_suff in raw_data}
                    breaches = suffixes.get(encrypted_pass[5:].upper())
                    if breaches is not None:
                        return self.color.brush(
                            'Your password is PWNeD (appears {} times in DB) :('.format(breaches), 'red')
                    return self.color.brush(
                        'Your password is not found in HIBP DB', 'green')
                time.sleep(1.5)
            print('{}'.format(self.color.brush(
                'Unexpected response code. Shutting down', 'purple')))
            sys.exit()
        except Exception as e:
            print('[{}] oops, something went wrong: {}'.format(
                self.color.brush('fail', 'red'), e))
            print('{}'.format(self.color.brush(
                'Exception raised. Shutting down', 'purple')))
            sys.exit()

    def file_check(self, attempts=3):
        """
        Check set of passwords provided from the file in HIBP
        database using web-API (sleeping between request to prevent
        HTTP 429 (Rate limit exceeded), please refer to
        https://haveibeenpwned.com/API/v2)
        :param attempts: number of attempts to check
        :return: dictionary with password as key and result of the check as
        value
        """
        file_passwd = extract_passwd(self.path)
        pass_dict = {}
        completion = 0
        start_time = time.time()
        num_of_passwd = len(file_passwd)
        print('[{}] Checking passwords in HIBP DB:'.format(
                self.color.brush('working', 'cyan')))
        try:
            for passwd in file_passwd:
                progress_bar(completion, num_of_passwd, start_time)
                encrypted_pass = PassEncrypt(passwd).encrypt()
                for attempt in range(attempts):
                    hibp_request = requests.get('{}{}'.format(self.uri,
                                                          encrypted_pass[:5]),
                                            headers=self.headers)
                    if hibp_request.status_code == 200:
                        raw_data = hibp_request.text.split('\n')
                        suffixes = {hash_suff.split(':')[0]: int(
                            hash_suff.split(':')[1].replace('\r', '')) for
                                    hash_suff in raw_data}
                        breaches = suffixes.get(encrypted_pass[5:].upper())
                        if breaches is not None:
                            pass_dict[passwd] = 'PWNeD (appears {} times in DB) :('.format(breaches)
                            break
                        pass_dict[passwd] = 'Not found in HIBP DB'
                        break
                    time.sleep(1.5)
                pass_dict.setdefault(passwd, 'Not able to check')
                time.sleep(1.5)
                completion += 1
            progress_bar(completion, num_of_passwd, start_time)
            return pass_dict
        except Exception as e:
            print('[{}] oops, something went wrong: {}'.format(
                self.color.brush('fail', 'red'), e))
            print('{}'.format(self.color.brush(
                'Exception raised. Shutting down', 'purple')))
            sys.exit()

    def make_request_to_hibp(self):
        """
        Make single request to HIBP or several requests,
        depends CLI arguments provided (single password or file with passwords)
        """
        if self.passwd is not None:
            checked_passwd = self.passwd_check()
            print(checked_passwd)
            print(
                '[{}] for more information visit: {}'.format(
                    self.color.brush('done', 'green'),
                    self.color.brush('haveibeenpwned.com',
                                     'purple')))
        else:
            write_pass_to_file(self.file_check())
            print('For more information visit: {}'.format(self.color.brush(
                'haveibeenpwned.com', 'red')))