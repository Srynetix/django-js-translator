"""Translate front-end code using a custom directive."""

from __future__ import print_function

import re
import os
import sys
import argparse

from collections import defaultdict

from django_js_translator.config_loader import config_load


def list_files_to_translate(path, extensions):
    """
    List files to translate from path.

    :param path         Path (str)
    :param extensions   Extensions to lookup (iterable)
    :return List of files (iterable)
    """
    result = []
    for root, _, files in os.walk(path):
        for filename in files:
            if filename.endswith(".js") or filename.endswith(".jsx") or filename.endswith(".html"):
                result.append(os.path.join(root, filename))

    return result


def generate_translation_output(output_map, output_path, file_body):
    """
    Generate translation output.

    :param output_map   Output translation map (dict)
    :param output_path  Output destination path (str)
    :param file_body    Output file body (str)
    """
    output = ""

    for k in sorted(output_map.keys()):
        output += "  \"{0}\": \"{{% trans \"{0}\" %}}\", // Count: {1}\n".format(k, len(output_map[k]))

    with open(output_path, mode="wt") as handle:
        handle.write(file_body.format(output))

    print("Translation written to `{0}`".format(output_path))


def prepare_translation(args):
    """
    Prepare translation.

    :param args     Arguments
    """
    translation_config = config_load(args.config_path)
    paths_to_analyze = translation_config['configuration']['paths']
    extensions = translation_config['configuration']['extensions']
    directive = translation_config['configuration']['directive']
    output_path = translation_config['configuration']['output']['path']
    output_body = translation_config['configuration']['output']['body']

    files = sum((list_files_to_translate(path, extensions) for path in paths_to_analyze), [])
    output_map = defaultdict(list)

    rgx = re.compile(ur'{0}\((?:\'(.*?)\'|\"(.*?)\")\)'.format(directive), flags=re.MULTILINE)
    for filename in files:
        with open(filename, mode="rt") as handle:
            content = handle.read()
            results = re.findall(rgx, content)

            for i in xrange(len(results)):
                res = [x for x in results[i] if x][0]
                output_map[res].append(filename)

    generate_translation_output(output_map, output_path, output_body)


def shell():
    """Main entry-point function."""
    parser = argparse.ArgumentParser(description="Prepare translation files for JS")
    parser.add_argument("config_path", help="Configuration file path")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    prepare_translation(args)
