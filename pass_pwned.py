import sys
from models import HIBPApi
from utils import parse_args, Color, draw_picture


__author__ = 'sehlat57'


def main():
    color = Color()
    draw_picture()
    cli_args = parse_args()  # parse CLI for arguments
    try:
        i_pwned = HIBPApi(passwd=cli_args.password,
                      file_passwd=cli_args.file_passwd)
        i_pwned.make_request_to_hibp()

    except KeyboardInterrupt:
        print(color.brush('\ninterrupted by user. Shutting down', 'purple'))
        sys.exit()

if __name__ == "__main__":
    main()
