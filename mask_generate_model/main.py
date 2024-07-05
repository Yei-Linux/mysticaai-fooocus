from mask_generate_model.process_model import load_seg_model
from mask_generate_model.mask_generation import generate_mask
from mask_generate_model.palette import get_palette

device = 'cpu'

def initialize_and_load_models():
    checkpoint_path = 'model/cloth_segm.pth'
    net = load_seg_model(checkpoint_path, device=device)    
    return net

net = initialize_and_load_models()
palette = get_palette(4)

def generate_mask_model(img):
    cloth_seg = generate_mask(img, net=net, palette=palette, device=device)
    return cloth_seg