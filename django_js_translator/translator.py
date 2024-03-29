"""Translate front-end code using a custom directive."""

from __future__ import print_function, unicode_literals

from collections import defaultdict
import os
import re

from django_js_translator.config_loader import config_load


def list_files_to_translate(path, extensions, ignore_files):
    """
    List files to translate from path.

    :param path:            Path (str)
    :param extensions:      Extensions to lookup (iterable)
    :param ignore_files:    Ignore files (iterable)
    :return List of files (iterable)
    """
    result = []
    for root, _, files in os.walk(path):
        for filename in files:
            for extension in extensions:
                if filename.endswith(extension):
                    full_path = os.path.normpath(os.path.join(root, filename))
                    if full_path not in ignore_files:
                        result.append(full_path)

    return result


def generate_translation_output(output_map, show_files, show_lines):
    """
    Generate translation output.

    :param output_map   Output translation map (dict)
    :param show_files:  Show file names (bool)
    :param show_lines:  Show lines (bool)
    :return Translation output (str)
    """
    output = ""

    keys = output_map.keys()
    keys_len = len(keys)

    for i, k in enumerate(sorted(keys)):
        origins = output_map[k]
        if show_files:
            known_filenames = set()
            for origin in origins:
                filename, position = origin

                # Handle file repetitions
                if not show_lines and filename in known_filenames:
                    continue
                known_filenames.add(filename)

                output += "  // {0}".format(filename)
                if show_lines:
                    output += ":{0}".format(position)
                output += "\n"

        output += '  "{0}": "{{% trans "{0}" %}}"'.format(k)

        if i != keys_len - 1:
            output += ",\n"
            if show_files:
                output += "\n"

    return output


def write_translation_to_file(output_str, output_path, file_body):
    """
    Write translation output to file.

    :param output_str   Output content (str)
    :param output_path  Output destination path (str)
    :param file_body    Output file body (str)
    """
    with open(output_path, mode="wt") as handle:
        handle.write(file_body.format(output_str))

    print("Translation written to `{0}`".format(output_path))


def prepare_translation(args):
    """
    Prepare translation.

    :param args     Arguments
    """
    translation_config = config_load(args.config_path)
    dry_run = args.dry_run

    paths_to_analyze = translation_config["configuration"]["paths"]
    directive = translation_config["configuration"]["directive"]
    output_path = translation_config["configuration"]["output"]["path"]
    output_body = translation_config["configuration"]["output"]["body"]
    extensions = translation_config["configuration"].get("extensions", [".js, .jsx"])
    ignore_files = translation_config["configuration"].get("ignore", [])
    show_files = translation_config["configuration"].get("show_files", True)
    show_lines = translation_config["configuration"].get("show_lines", False)

    ignore_files = [os.path.normpath(p) for p in ignore_files]
    files = sum((list_files_to_translate(path, extensions, ignore_files) for path in paths_to_analyze), [])
    output_map = defaultdict(list)

    rgx_val = r"{0}\((?:\'(.*?)\'|\"(.*?)\")".format(directive)
    rgx = re.compile(rgx_val, flags=re.MULTILINE)
    for filename in files:
        with open(filename, mode="rt") as handle:
            content = handle.read()
            for match in re.finditer(rgx, content):
                target = match.groups()[0]
                if target is None:
                    target = match.groups()[1]
                if target is None:
                    continue
                position = match.span()
                output_map[target].append((filename, position))

    output = generate_translation_output(output_map, show_files, show_lines)
    if dry_run:
        print(output)
    else:
        write_translation_to_file(output, output_path, output_body)
