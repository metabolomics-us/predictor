import os

from flask import abort, Blueprint
from flask import request
from pyspec.loader import Spectra
from pyspec.machine.factory import MachineFactory

from predictor.util.responses import JsonResponse

# any prediction should only be done on the CPU to be system agnostic
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def load_model():
    global model
    global encoder

    factory = MachineFactory()

    # get model and encoder as configured
    model = factory.load_model()
    encoder = factory.load_encoder()


clean_dirty = Blueprint("clean_dirty", __name__, url_prefix='/rest')


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

        result = model.predict_from_spectra(input="dataset/clean_dirty", spectra=Spectra(spectra=spectra),
                                            encoder=encoder)

        return JsonResponse(json_dict={'result': int(result)})
