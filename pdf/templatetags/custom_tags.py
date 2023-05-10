import os
from django import template
from django.utils.html import format_html
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

PALABRAS_MATEMATICA = [
    'teorema', 'Matemático/a', 'Hilbert', 'Turing', 'análisis',
    'Euler', 'Fermat', 'Pitágoras', 'autómata', 'Boole', 'Cantor', 'Perelman'
]

PALABRAS_FISICA = [
    'Experimentación', 'Físico/a', 'Astronomía', 'Mecánica', 'Newton',
    'Einstein', 'Galileo', 'Modelo', 'Tesla', 'Dinámica', 'Partículas'
]

IMAGES_PATH = 'static/images/'

def load_image(name):
    image_path = os.path.join(IMAGES_PATH, f"{name}.jpg")
    return static(image_path)

def is_valid_numeric_component(component):
    if component.startswith('+') or component.startswith('-'):
        component = component[1:]  # Ignorar el signo en la verificación
    return component.replace('.', '').isnumeric()

def tokenize_text(text):
    if text is None:
        return []

    tokens = text.split()  # Tokenizar por espacios en blanco

    processed_tokens = []
    for token in tokens:
        # Verificar el tipo de cada token y agregarlo a la lista procesada
        if token in PALABRAS_MATEMATICA:
            processed_tokens.append(('matematica', token))

        elif token in PALABRAS_FISICA:
            processed_tokens.append(('fisica', token))

        elif token.isdigit():
            processed_tokens.append(('integer', token))
        elif '.' in token and is_valid_numeric_component(token):
            processed_tokens.append(('real', token))
        elif 'e' in token.lower():
            parts = token.lower().split('e')
            if len(parts) == 2 and is_valid_numeric_component(parts[0]) and is_valid_numeric_component(parts[1]):
                processed_tokens.append(('scientific', token))
            else:
                processed_tokens.append(('error', token))
        elif token.endswith('i') and any(char in token[:-1] for char in ('+', '-')):
            real_part, imag_part = token[:-1].split('+') if '+' in token[:-1] else token[:-1].split('-')
            if is_valid_numeric_component(real_part) and is_valid_numeric_component(imag_part):
                processed_tokens.append(('complex', token))
            else:
                processed_tokens.append(('error', token))
        elif token.count('/') == 2:
            date_parts = token.split('/')
            if len(date_parts) == 3 and all(part.isdigit() for part in date_parts):
                day, month, year = date_parts
                if len(day) == 2 and len(month) == 2 and len(year) <= 4:
                    processed_tokens.append(('date', token))
                else:
                    processed_tokens.append(('error', token))
            else:
                processed_tokens.append(('error', token))
        elif token.count('-') == 2:
            date_parts = token.split('-')
            if len(date_parts) == 3 and all(part.isdigit() for part in date_parts):
                day, month, year = date_parts
                if len(day) == 2 and len(month) == 2 and len(year) <= 4:
                    processed_tokens.append(('date', token))
                else:
                    processed_tokens.append(('error', token))
            else:
                processed_tokens.append(('error', token))
                
        else:
            processed_tokens.append(('error', token))

    return processed_tokens

def resaltar_tokens(tokens):
    resaltado = ''
    for i, (tipo, valor) in enumerate(tokens):
        if i > 0 and tipo == tokens[i-1][0] and valor != tokens[i-1][1]:
            resaltado += ' '
        elif i > 0 and tipo != tokens[i-1][0]:
            resaltado += ' '
        if tipo == 'integer':
            resaltado += format_html('<span style="color: blue;">{}</span>', valor.replace(' ', '&nbsp;'))
        elif tipo == 'real':
            resaltado += format_html('<span style="color: green;">{}</span>', valor.replace(' ', '&nbsp;'))
        elif tipo == 'scientific':
            resaltado += format_html('<span style="color: purple;">{}</span>', valor.replace(' ', '&nbsp;'))
        elif tipo == 'complex':
            resaltado += format_html('<span style="color: red;">{}</span>', valor.replace(' ', '&nbsp;'))
        elif tipo == 'date':
            resaltado += format_html('<span style="color: orange;">{}</span>', valor.replace(' ', '&nbsp;'))
        elif tipo == 'matematica':
            resaltado += format_html('<span style="color: grey;">{}</span>', valor.replace(' ', '&nbsp;'))
        elif tipo == 'fisica':
            resaltado += format_html('<span style="color: grey;">{}</span>', valor.replace(' ', '&nbsp;'))
        else:
            resaltado += ' ' + valor + ' '
    return resaltado

@register.filter
def resaltar_texto(texto):
    tokens = tokenize_text(texto)
    texto_resaltado = resaltar_tokens(tokens)
    return mark_safe(texto_resaltado)