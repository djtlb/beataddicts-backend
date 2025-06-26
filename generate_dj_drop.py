import os
def generate_dj_drop(text, filename='dj_drop.wav'):
    os.system(f'espeak-ng "{text}" -w static/outputs/{filename}')
    return f'static/outputs/{filename}'
