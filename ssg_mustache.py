import pystache
import ssg

# v 0.0.1

templates = {}

templates = ssg.get_templates('.mustache')
pystache_renderer = pystache.Renderer()
site_config = ssg.add_urls_to_site_config(ssg.get_config(), templates)



for template_key, template in templates.items():
    env = {'global': site_config, 'local': template['config']}

    # print('\n||||  ' + template_key + '   ||||\n')
    # print(env)

    ssg.create_html_file(template['html_path'], pystache_renderer.render_path(template['template_path'], env))
