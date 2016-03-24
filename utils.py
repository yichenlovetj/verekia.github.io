import errno
import io
import os

import pystache

import utils


def create_folders_to_path_if_needed(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def create_html_file(output_path, template_path, env):
    with io.open(output_path,'w', encoding='utf8') as output_file:
        output_file.write(pystache.Renderer(string_encoding='utf8').render_path(template_path, env))
        output_file.close()
