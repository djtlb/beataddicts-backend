import torch
from audiocraft.models import MusicGen
model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=10)
def generate_song(prompt_text):
    wav = model.generate([prompt_text])
    return wav[0].cpu().numpy()
