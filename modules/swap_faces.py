import os
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image


def get_inswapper_model():
    import gdown
    model_url = 'https://drive.google.com/uc?id=1HvZ4MAtzlY74Dk4ASGIS9L6Rg5oZdqvu'
    model_output_path = 'inswapper.onnx'
    if not os.path.exists(model_output_path):
        gdown.download(model_url, model_output_path, quiet=False)


def detect_faces(image):
    """Detect faces in an image using the FaceAnalysis app."""
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(320, 320))
    faces = app.get(image)
    # Sort faces by their horizontal position
    faces = sorted(faces, key=lambda x: x.bbox[0])
    return faces


# def swap_faces(source_image, target_image):
#     """Swap the source face into the target face position in the target image."""
#     source_faces = detect_faces(source_image)
#     target_faces = detect_faces(target_image)

#     swapper = insightface.model_zoo.get_model('models/checkpoints/inswapper_128.onnx', download=False, download_zip=False)

#     result_image = target_image.copy()
#     swapped_image = swapper.get(result_image, target_faces[0], source_faces[0], paste_back=True)
#     # swapped_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
#     cv2.imwrite('swapped2.jpg', swapped_image)

#     # yield gr.update(visible=False), \
#     #       gr.update(visible=False), \
#     #       gr.update(visible=False), \
#     #       gr.update(visible=True, value=[swapped_image])
#     return swapped_image

def swap_faces(source_image, target_image):
    """Swap the source face into the target face position in the target image."""
    source_faces = detect_faces(source_image)
    target_faces = detect_faces(target_image)

    if not source_faces or not target_faces:
        print("No faces detected in either the source or target image.")
        return None

    swapper = insightface.model_zoo.get_model(
        'models/checkpoints/inswapper_128.onnx', download=False, download_zip=False)

    result_image = target_image.copy()
    swapped_image = swapper.get(
        result_image, target_faces[0], source_faces[0], paste_back=True)

    return swapped_image
