# based on https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.6.0/modules/ui_gradio_extensions.py

import os
import gradio as gr
import args_manager

from modules.localization import localization_js


GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse

modules_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.dirname(modules_path)


def webpath(fn):
    if fn.startswith(script_path):
        web_path = os.path.relpath(fn, script_path).replace('\\', '/')
    else:
        web_path = os.path.abspath(fn)

    return f'file={web_path}?{os.path.getmtime(fn)}'

# def javascript_footer_html():
#     head= f'<script defer type="text/javascript" src="https://template-signin.s3.us-east-1.amazonaws.com/signin.js?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDrLsc81VaaeSq%2BpyB3PZPJqqFJXU2ed%2B8tnzOgl%2FO5MQIhAOIHHShAMJJ%2Fa4o3W95eW%2Bz0teUiVr5E4TUqdy1xYFczKuQCCEsQBBoMNTc4ODA5Njg0NTE4IgzV%2FoZAe9K34Oms%2BYoqwQKk6GnTuyBt3ZkTVn%2BQRjK19MJ6W%2B6ZUAgIygVQjfzfu7ELIqesBVc0BxJ9IiEaBGSyAuZ7uDzHWv7sX2Rg%2F4gl2nP2S3K3el887u%2F4GWJ5xkCJMf35S49riI2f37V08hhRxO1ZD2FS%2BgfIaxxNFScX7k9lQqMHiS%2BMiRaWJlULMI3I2npc2p1jqA8YVUZ%2BsDiXrc%2Fj4ZgkaQZIOooYkCL6QkCFR7O%2BD4JyynKVofagAUKzvfvPuFp25cxYZep6ZA7n2BPyHT8WkeOx8pHSWyCpni925noqXthuumL5zsJn93wQ6fUxGgmj6OjxIUE%2B1vY%2Bd5W2RswOUDahFR1ZagRpW%2BQ4Y1Xh0FjKlk4KxFhQZIbR5r8IRuuuc3XFcbBXs5RhqcGkYovbGtV195HeX8mhO7lvMfpxzszuQueu4T3g7FEw1ZDosgY6sgJp7%2BrD6mu9mqRndqRsuiqCDx%2Fej7AbP2y5FOvZ%2BLGIO15dpf98oYSsCH18VQdKnGc5QPBs0kFQyGKIutb%2BatWshL6kvqu2z%2FFdNbxt%2BWsvxzO0JSLuZfavJzdtzTmyoedomX%2F%2Fnb5z1I8j0SooZDGeCArKHDvt6XEUJhivbKPv2JDZgs6zMifsid2NYEgIGjQT4BL7gSao%2B6zHxNKJp%2Fx5Lg5aFAulvLVc9hhB5DLgLXA1MPf7rXJ3RsZjWvcdJLiWG9j96hvkinLwVAgV8E2QZ86Fz6m%2FQYo%2B7yjOAuYDKvqYYaMelMikPEpmZiplT1gh0dHvdFHYk8Vt7OEG8gxvWu4UdqBafZIlhown%2FrOqr5AZ%2B9Cb5kM4UtzrFyrneO6QRsbp9A%2BNm%2FDzDnMAzRRGGwk%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240601T034430Z&X-Amz-SignedHeaders=host&X-Amz-Expires=299&X-Amz-Credential=ASIAYNQ564ITHXPXF774%2F20240601%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b28814b8d6b85a00e6b664313b73a18db79cbde21284a7787691ca0d86ab746d"></script>'
#     return head

def javascript_html():
    script_js_path = webpath('javascript/script.js')
    context_menus_js_path = webpath('javascript/contextMenus.js')
    localization_js_path = webpath('javascript/localization.js')
    zoom_js_path = webpath('javascript/zoom.js')
    edit_attention_js_path = webpath('javascript/edit-attention.js')
    viewer_js_path = webpath('javascript/viewer.js')
    image_viewer_js_path = webpath('javascript/imageviewer.js')
    samples_path = webpath(os.path.abspath('./sdxl_styles/samples/fooocus_v2.jpg'))

    head = f'<script type="text/javascript">{localization_js(args_manager.args.language)}</script>\n'
    head += f'<script type="text/javascript" src="{script_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{context_menus_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{localization_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{zoom_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{edit_attention_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{viewer_js_path}"></script>\n'
    head += f'<script type="text/javascript" src="{image_viewer_js_path}"></script>\n'
    head += f'<meta name="samples-path" content="{samples_path}">\n'

    if args_manager.args.theme:
        head += f'<script type="text/javascript">set_theme(\"{args_manager.args.theme}\");</script>\n'

    return head


def css_html():
    style_css_path = webpath('css/style.css')
    head = f'<link rel="stylesheet" property="stylesheet" href="https://trova-images.s3.amazonaws.com/signin.css">'
    head += f'<link rel="stylesheet" property="stylesheet" href="{style_css_path}">'
    
    return head

# definir una funcion que retorne la funcion de dos numeros


def reload_javascript():
    js = javascript_html()
    css = css_html()
    # js_footer = javascript_footer_html()
    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</head>', f'{js}</head>'.encode("utf8"))

        res.body = res.body.replace(b'</body>', f'{css}</body><footer></footer>'.encode("utf8"))

        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response
