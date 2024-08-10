import argparse


def parameter_parser():
    parser = argparse.ArgumentParser(description='for Chat')
    parser.add_argument('--port', type=int,
                        default=9001, help='port')
    parser.add_argument('--batch_size', type=int,
                        default=8, help='batch_size')
    parser.add_argument('--max_passage_length', type=int,
                        default=512, help='max_passage_length')
    return parser.parse_args()
