import io
import os

import yaml

import utils

# v 0.0.1

def get_base_uri_from_path(path, extension):

    # .\_pages\page-a\index.mustache => page-a
    # .\_pages\index.mustache => homepage

    base_uri = path.replace(os.sep, '/')

    # ./_pages/page-a/index.mustache
    # ./_pages/index.mustache

    base_uri = base_uri[9:]

    # page-a/index.mustache
    # index.mustache

    base_uri = base_uri[:-(len('index' + extension))]

    # page-a/
    # ''

    if base_uri == '':
        base_uri = 'homepage' 

    if base_uri[-1:] == '/':
        base_uri = base_uri[:-1]

    # page-a
    # homepage

    return base_uri


def get_templates(extension):
    # Index all index template files and their associated config file
    templates = {}
    for root, directories, filenames in os.walk('.' + os.sep + '_pages'):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if file_path.endswith('index' + extension):
                base_path = file_path[:-(len(extension))]
                config_path = base_path + '.yaml'
                if os.path.isfile(config_path):
                    template = {}
                    template['template_path'] = file_path

                    base_uri = get_base_uri_from_path(file_path, extension)
                    template['html_path'] = base_path.replace('_pages' + os.sep, '') + '.html'

                    if base_uri == 'homepage':
                        template['html_path'] = template['html_path'].replace('homepage' + os.sep, '')

                    template['config'] = get_config(config_path)

                    # Add the template object to templates dict at base_uri key
                    templates[base_uri] = template
                else:
                    break
    return templates


def get_config(config_filename=None):
    if not config_filename:
        config_filename = '_pages' + os.sep + 'config.yaml'
    stream = open(config_filename, 'r', encoding="utf-8")
    return yaml.load(stream)


def add_urls_to_site_config(site_config, templates):
    site_config_with_urls = site_config.copy()
    for template_key, template in templates.items():
        site_config_with_urls[template_key]['url'] = '/' + template_key + '/' if template_key != 'homepage' else '/'
    return site_config_with_urls


def create_html_file(path, content):
    utils.create_folders_to_path_if_needed(path.replace('index.html', ''))
    with io.open(path,'w', encoding='utf8') as output_file:
        output_file.write(content)
        output_file.close()
