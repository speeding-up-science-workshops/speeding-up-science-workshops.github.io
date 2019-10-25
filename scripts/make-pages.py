#! /usr/bin/env python3
import sys
import yaml
import argparse
import os
import shutil
import pprint
import urllib.request


template = """
# {title}

GitHub repository: [speeding-up-science-workshops/{github}/](https://github.com/speeding-up-science-workshops/{github})

DOI: [{doi}](https://doi.org/{doi})

[![Binder](https://mybinder.org/badge_logo.svg)]({binderurl})

{readme}

![](https://raw.githubusercontent.com/speeding-up-science-workshops/{github}/master/{image_filename})
"""

raw_readme_url = "https://raw.githubusercontent.com/speeding-up-science-workshops/{github}/master/README.md"


def grab_README_text(d):
    readme_url = raw_readme_url.format(**d)
    print(readme_url)
    with urllib.request.urlopen(readme_url) as fp:
        text = fp.read()
        text = text.decode('utf-8')
        text = text.splitlines()

        start = None
        for lineno in range(0, len(text)):
            if text[lineno].strip().startswith('## Summary'):
                start = lineno

        end = len(text)
        if start is not None:
            for lineno in range(start + 1, len(text)):
                if text[lineno].strip().startswith('## '):
                    end = lineno
            return "\n".join(text[start:end])
        return """(no summary text provide)"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('site_config_directory')
    p.add_argument('output_dir')
    p.add_argument('--verbose', action='store_true')

    args = p.parse_args()

    try:
        shutil.rmtree(args.output_dir)
    except FileNotFoundError:
        pass

    os.mkdir(args.output_dir)

    for dirname, subdirlist, filelist in os.walk(args.site_config_directory):
        for filename in filelist:
            fullpath = os.path.join(dirname, filename)
            if fullpath.endswith('~') or filename.startswith('.'):
                # ignore silently
                continue
            if not fullpath.endswith('.yml'):
                print('ignoring unknown file type {}', fullpath)
                continue

            basepath = os.path.basename(filename[:-4])

            d = yaml.load(open(fullpath, 'rt'))
            print('file:', fullpath)
            pprint.pprint(d)

            binderurl = 'https://mybinder.org/v2/zenodo/{doi}/'.format(**d)

            if d['binder-type'] == 'rstudio':
                binderurl += '?urlpath=rstudio'

            d['binderurl'] = binderurl

            d['readme'] = grab_README_text(d)

            outpath = os.path.join(args.output_dir, basepath + '.md')
            with open(outpath, 'wt') as fp:
                print('creating {}'.format(outpath), file=sys.stderr)

                fp.write(template.format(**d))


if __name__ == '__main__':
    sys.exit(main())
