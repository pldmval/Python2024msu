import argparse
from cowsay import cowsay, list_cows

parser = argparse.ArgumentParser()

parser.add_argument("-n", action="store_true")
parser.add_argument("-W", type=int, default=40)
parser.add_argument("-e", type=str)
parser.add_argument("-T", type=str)
parser.add_argument("-f", type=str)
parser.add_argument("-l", action="store_true")
parser.add_argument('-b', action='store_true')
parser.add_argument('-d', action='store_true')
parser.add_argument('-g', action='store_true')
parser.add_argument('-p', action='store_true')
parser.add_argument('-s', action='store_true')
parser.add_argument('-t', action='store_true')
parser.add_argument('-w', action='store_true')
parser.add_argument('-y', action='store_true')
parser.add_argument("message")

args = parser.parse_args()

preset = None
for p in "bdgpstwy":
    if getattr(args, p):
        preset = p
        break

if args.l:
    print(list_cows())
else:
    print(
        cowsay(
            message=args.message,
            cow=args.f,
            preset=preset,
            eyes=args.e,
            tongue=args.T,
            width=args.W,
            wrap_text=args.n,
        )
    )
