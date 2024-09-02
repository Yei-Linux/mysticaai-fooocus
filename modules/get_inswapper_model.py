def get_inswapper_model():
    print('function entered')
    import gdown
    print('gdown imported')
    import os
    model_url = 'https://drive.google.com/uc?id=1HvZ4MAtzlY74Dk4ASGIS9L6Rg5oZdqvu'
    model_output_path = 'models/checkpoints/inswapper.onnx'
    if not os.path.exists(model_output_path):
        print('reached if condition')
        gdown.download(model_url, model_output_path, quiet=False)



if __name__ == "__main__":
    get_inswapper_model()

    