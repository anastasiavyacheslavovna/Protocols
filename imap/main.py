from argparse import ArgumentParser

from imap_client import ImapClient


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-u', '--user', type=str, dest='login', required=True)
    parser.add_argument('-s', '--server', type=str, required=True)
    parser.add_argument('-n', '--messages', type=int, nargs='+', default=[1])
    parser.add_argument('--ssl', action='store_true')
    parser.add_argument('-d', '--mailbox', type=str, default='Inbox')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    server = args.server.split(":")
    if len(server) == 1:
        port = 143
    else:
        port = int(server[1])
    server = server[0]

    if len(args.messages) == 1:
        from_letter = to_letter = args.messages[0]
    else:
        from_letter = args.messages[0]
        to_letter = args.messages[1]

    try:
        client = ImapClient(args.login, server, port, args.ssl)\
            .connect()\
            .read(from_letter, to_letter, args.mailbox)\
            .close()
    except Exception as e:
        print(f'Exception: {e}')
