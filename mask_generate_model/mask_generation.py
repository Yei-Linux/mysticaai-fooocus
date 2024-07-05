from PIL import Image
import torch.nn.functional as F
import torch
import numpy as np

import os
from mask_generate_model.normalizer_image import apply_transform
from mask_generate_model.options import opt

def generate_mask(numpy_image, net, palette, device = 'cpu'):
    if numpy_image is None:
        return

    if 'image' in numpy_image:
        numpy_image = numpy_image['image']

    #img = Image.open(input_image).convert('RGB')
    input_image = Image.fromarray(np.uint8(numpy_image))
    img = input_image
    
    img_size = img.size
    img = img.resize((768, 768), Image.BICUBIC)
    image_tensor = apply_transform(img)
    image_tensor = torch.unsqueeze(image_tensor, 0)

    alpha_out_dir = os.path.join(opt.output,'alpha')
    os.makedirs(alpha_out_dir, exist_ok=True)

    with torch.no_grad():
        output_tensor = net(image_tensor.to(device))
        output_tensor = F.log_softmax(output_tensor[0], dim=1)
        output_tensor = torch.max(output_tensor, dim=1, keepdim=True)[1]
        output_tensor = torch.squeeze(output_tensor, dim=0)
        output_arr = output_tensor.cpu().numpy()

    # Save final cloth segmentations
    cloth_seg = Image.fromarray(output_arr[0].astype(np.uint8), mode='P')
    cloth_seg.putpalette(palette)
    
    #cloth_seg = cloth_seg.resize((img[1], img[0]), Image.ANTIALIAS)
    img_shape = numpy_image.shape[:2]
    
    cloth_seg = cloth_seg.convert('RGB')
    cloth_seg = cloth_seg.resize((img_shape[1], img_shape[0]), Image.ANTIALIAS)

    cloth_seg_array = np.array(cloth_seg)

    print(numpy_image.shape)
    print(cloth_seg_array.shape)

    return cloth_seg_array
