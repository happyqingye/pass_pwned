import os
import sys
from time import time
from datetime import datetime
import argparse
import textwrap
import getpass

__author__ = 'sehlat57'


class Color(object):
    color_dict = {'green': '\x1b[1;32m',
                  'red': '\x1b[1;31m',
                  'blue': '\x1b[1;34m',
                  'purple': '\x1b[1;35m',
                  'cyan': '\x1b[1;36m'}

    def brush(self, text, color):
        """
        Coloring text in CLI
        :param text: text to modify
        :param color: color to apply
        :return: modified text
        """
        if color.lower() in self.color_dict:
            return '{}{}\x1b[0m'.format(self.color_dict[color.lower()], text)
        else:
            print('sorry, unknown color')


def extract_passwd(path):
    """
    Get passwords from txt file provided by user
    :return: set of passwords to check
    """
    color = Color()
    if os.path.exists(path):
        with open(path, 'r') as file_passwd:
            passwds = file_passwd.read()
            list_raw = passwds.split(',')
            extracted_passwd = {account.strip() for account in list_raw}
            if len(extracted_passwd) == 1 and extracted_passwd.pop() == '':
                print(
                    '[{}] No passwords found in file'.format(
                        color.brush('fail', 'red')))
                print('{}'.format(color.brush('Shutting down', 'purple')))
                sys.exit()
            print('[{}] Passwords extracted'.format(
                color.brush('ok', 'green')))
            return {account.strip() for account in list_raw}
    print('[{}] No file with passwords found, please check path'.format(
        color.brush('fail', 'red')))
    print('{}'.format(color.brush('Shutting down', 'purple')))
    sys.exit()


def progress_bar(completion, total, start_time, width=20):
    """
    Print progress bar in stdout
    :param completion: passwords checked
    :param total: total passwords to checl
    :param start_time: time stamp before first appear of progress bar in stdout
    :param width: width of progress bar
    :return:
    """
    progress = int(completion / total * 100)
    completion = completion
    total = total
    seconds_passed = time() - start_time
    time_stamp = '{:02.0f}:{:02.0f}:{:02.0f}'.format(
        seconds_passed // 3600, seconds_passed % 3600 // 60,
        seconds_passed % 60)
    bar = '\x1b[1;30;46m \x1b[0m' * int(
        width * completion / total) + ' ' * int(
        width - (width * completion / total))
    show = ('\r{}%|{}|{}/{}|time passed: {}'.format(
        progress if progress < 100 else 100, bar, completion, total,
        time_stamp))
    sys.stdout.write(show)
    sys.stdout.flush()
    if completion >= total:
        sys.stdout.write('\n')


def write_pass_to_file(result):
    """
    :param result: dict with key as password, value as result of the check in
    HIBP
    :return:
    """
    color = Color()
    width = max([len('{}{}'.format(
        passwd, rslt)) for passwd, rslt in result.items()]) + 10
    dir_name = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_name, 'checked_passwords.txt'), 'a') as checked:
        checked.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        checked.write('\n{}'.format('*' * width))
        for passwd, rslt in result.items():
            checked.write('\n*{}*'.format(
                '{} - {}'.format(passwd, rslt).center(width - 2)))
        checked.write('\n{}\n'.format('*' * width))
    print('[{}] Results are saved to file: {},\n       path: {}'.format(
        color.brush('done', 'green'),
        color.brush('checked_passwords.txt', 'cyan'),
        color.brush(dir_name, 'purple')))


class PassAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        """Hides password in CLI"""
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)


def parse_args():
    """
    Parse arguments:
    required:
    -password - password to check ib HIBP DB
    or
    -file with passwords - list of passwords

    :return: parsed arguments from command line
    """
    parser = argparse.ArgumentParser(
        prog='PassPwned',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        --------------------------------------------
        Script generates hash of password using SHA1
        algorithm and make post request to Troy Hunt
        https://haveibeenpwned.com/ where hash is 
        being compared to more than 300 million
        other hashes in DB.
        If your password hash is found the API will
        respond with HTTP 200.
        --------------------------------------------
        For more information about HIBP project
        please visit https://haveibeenpwned.com/,
        https://www.troyhunt.com/
        --------------------------------------------
        Example:
        python3 pass_pwned.py -p #Enter your Password
        or
        python3 pass_pwned.py -f PATH_TO_FILE
        ____________________________________________

        '''))
    parser.add_argument('-p', '--password',
                        action=PassAction,
                        nargs='?',
                        dest='password',
                        help='\npassword to check',
                        default=None
                        )
    parser.add_argument('-f', '--file',
                        default=None,
                        dest='file_passwd'
                        )
    args = parser.parse_args()
    if args.password is None and args.file_passwd is None:
        parser.error('No arguments provided')
    return args


def draw_picture():
    print("""
██╗  ██╗██╗██████╗ ██████╗ 
██║  ██║██║██╔══██╗██╔══██╗
███████║██║██████╔╝██████╔╝
██╔══██║██║██╔══██╗██╔═══╝ 
██║  ██║██║██████╔╝██║     
╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝     
""")
    print(Color().brush('haveibeenpwned.com by Troy Hunt', 'purple'))