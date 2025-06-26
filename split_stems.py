import os
def split_stems(input_path):
    out_dir = input_path.replace('.wav', '_stems')
    os.system(f'spleeter separate -p spleeter:2stems -o {out_dir} {input_path}')
    return out_dir
