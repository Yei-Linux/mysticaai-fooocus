from PIL import Image, ImageOps
import numpy as np
import torch
from rembg import remove, new_session
from extras.GroundingDINO.util.inference import default_groundingdino

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def run_grounded_sam(input_image, text_prompt, box_threshold, text_threshold):
    # run grounding dino model
    boxes, _ = default_groundingdino(
        image=np.array(input_image),
        caption=text_prompt,
        box_threshold=box_threshold,
        text_threshold=text_threshold
    )

    return boxes.xyxy

def resize_mask(mask, target_shape):
    """
    Resized invert mask
    """
    mask_resized = mask.resize((target_shape[1], target_shape[0]), Image.ANTIALIAS)
    mask_resized_array = np.array(mask_resized)
    return mask_resized_array


def generate_mask_from_image(image, mask_model, extras):
    if image is None:
        return

    if 'image' in image:
        image = image['image']

    if mask_model == 'sam':
        boxes = run_grounded_sam(Image.fromarray(image), extras['sam_prompt_text'], box_threshold=extras['box_threshold'], text_threshold=extras['text_threshold'])
        boxes = np.array([[0, 0, image.shape[1], image.shape[0]]]) if len(boxes) == 0 else boxes
        extras['sam_prompt'] = []
        for idx, box in enumerate(boxes):
            extras['sam_prompt'] += [{"type": "rectangle", "data": box.tolist()}]

    mask_array= remove(
        image,
        session=new_session(mask_model, **extras),
        only_mask=True,
        **extras
    )


    mask_image = Image.fromarray(mask_array)
    mask_image_inverted = ImageOps.invert(mask_image)
    mask_image_inverted_array = resize_mask(mask_image_inverted, mask_array.shape[:2])

    print(mask_array.shape)
    print(mask_image_inverted_array.shape)

    return mask_image_inverted_array
