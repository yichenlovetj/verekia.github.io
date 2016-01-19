import re
import os

# v1.1.0


def main():
    templates_base = '_templates' + os.sep
    all_templates = []
    all_pages = []

    print('===== Looking for templates and pages =====\n')

    for root, directories, filenames in os.walk('.'):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if file_path.startswith('.' + os.sep + templates_base) and file_path.endswith('.html'):
                all_templates.append(file_path[13:][:-5]) # Replace by math
            if file_path.endswith('.htmlo'):
                all_pages.append(file_path[:-6])

    print('Templates:')
    print(all_templates)
    print('\nPages:')
    print(all_pages)

    print('\n===== Building output files =====\n')

    for page in all_pages:
        page_path_input = page + '.htmlo'
        page_path_output = page + '.html'

        print('Building ' + page)

        with open(page_path_input, 'r') as input_file:
            output_file = open(page_path_output, 'w')

            for input_line in input_file:

                match = re.search('<!-- htmlo: (.+?) -->', input_line)
                if match:
                    # We replace the / by a \ in case we run on Windows
                    found_template_path = match.group(1).replace('/', os.sep)

                    if found_template_path in all_templates:
                        with open(templates_base + found_template_path + '.html', 'r') as template_file:
                            for template_line in template_file:
                                output_file.write(template_line)
                    else:
                        print('This template doesnt exist')
                else:
                    output_file.write(input_line)

            output_file.close()
        input_file.close()

main()
main()
main()
main()
main()