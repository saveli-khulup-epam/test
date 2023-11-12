from argparse import ArgumentParser


"""
Get manifest:
curl 'http://192.168.56.105:5000/v2/random_number/manifests/latest' -H 'accept: application/vnd.docker.distribution.manifest.v2+json' > manifest.json

Create tag `prod`
curl -XPUT 'http://192.168.56.105:5000/v2/random_number/manifests/a' -H 'content-type: application/vnd.docker.distribution.manifest.v2+json' -d '@manifest.json'

Delete tag
curl -X DELETE 'http://192.168.56.105:5000/v2/small/manifests/sha256:1af298531249b75dfd8d0acae611499be03cc35f29167c6558cf12a9e1e74cbc' -H 'content-type: application/vnd.docker.distribution.manifest.v2+json'
"""

parser = ArgumentParser()

parser.add_argument('cmd', choices=['tag', 'untag'], help='tag - tag, untag - untag')
parser.add_argument('image')
parser.add_argument('commit')
parser.add_argument('new_tag')


parser.add_argument('--registry', default='192.168.56.105:5000')

args = parser.parse_args()


if args.cmd == 'tag':
    ...
elif args.cmd == 'untag':
    ...
else:
    raise Exception("WA TA FUCK")
