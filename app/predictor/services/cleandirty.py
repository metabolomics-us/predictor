import os

from flask import abort, Blueprint
from flask import request
from pyspec.loader import Spectra
from pyspec.machine.factory import MachineFactory
from pyspec.machine.model.cnn import CNNClassificationModel
from pyspec.machine.spectra import Encoder

from predictor.util.responses import JsonResponse

# any prediction should only be done on the CPU to be system agnostic
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

factory = MachineFactory()

clean_dirty = Blueprint("clean_dirty", __name__, url_prefix='/rest')

# get model and encoder as configured
model: CNNClassificationModel = factory.load_model()
encoder: Encoder = factory.load_encoder()
dataset = "dataset/clean_dirty"


@clean_dirty.route('/predict/dirty', methods=['POST'])
def evaluate_spectra():
    """
    evaluates the incoming spectra object to be clean or dirty
    :return:
    """
    if not request.json or 'spectra' not in request.json:
        abort(500)
    else:
        data = request.json

        spectra = data['spectra']

        result = model.predict_from_spectra(input=dataset, spectra=Spectra(spectra=spectra),
                                            encoder=encoder)

        return JsonResponse(json_dict={'result': int(result)})

