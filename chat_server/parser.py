import argparse


def parameter_parser():
    parser = argparse.ArgumentParser(description="chat server")
    parser.add_argument('--port', type=int,
                        default=9010, help='port')
    parser.add_argument('--model_path', type=str,
                        default='model/qwen2-7b-instrust-awq-q4_K_M.gguf', help='model path')
    parser.add_argument('--n_ctx', type=int,
                        default=2048, help='n_ctx')

    return parser.parse_args()
