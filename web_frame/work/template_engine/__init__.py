import os
import re
from work.log import LOG_FUNC_NAME, LOG_OUT

pattern = r'{{(.*?)}}'


@LOG_FUNC_NAME()
def parse_args(obj):
    comp = re.compile(pattern)
    ret = comp.findall(obj)
    LOG_OUT('info', '  parse args: {}'.format(ret))
    return ret if ret else ()


@LOG_FUNC_NAME()
def replace_template(app, path, **options):
    LOG_OUT('info', '  path befor: {}'.format(path))
    content = '<h1>Not Fount Template</h1>'
    path = os.path.join(app.template_folder, path)
    LOG_OUT('info', '  path after: {}'.format(path))

    if os.path.exists(path):
        with open(path, 'rb') as f:
            content = f.read().decode()

        args = parse_args(content)
        if options:
            for arg in args:
                key = arg.strip()
                content = content.replace(
                        "{{%s}}" % arg, str(options.get(key, '')))
    return content


