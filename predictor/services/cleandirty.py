import os
from time import time

from flask import abort, Blueprint
from flask import request
from pyspec.loader import Spectra
from pyspec.machine.factory import MachineFactory
from pyspec.machine.share.s3 import S3Share

from predictor.util.timeit import timeit
from predictor.util.responses import JsonResponse
import tensorflow as tf

# any prediction should only be done on the CPU to be system agnostic
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def load_model():
    global clean_dirty_model
    global clean_dirty_encoder
    global graph

    share = S3Share(read_only=True)
    share.retrieve("clean_dirty", force=True)
    factory = MachineFactory()

    # get model and encoder as configured
    clean_dirty_model = factory.load_model()
    clean_dirty_encoder = factory.load_encoder()
    graph = tf.get_default_graph()


clean_dirty = Blueprint("clean_dirty", __name__, url_prefix='/rest')


@clean_dirty.route('/predict/dirty', methods=['POST'])
def evaluate_spectra():
    """
    evaluates the incoming spectra object to be clean or dirty
    :return:
    """
    from predictor.app import logger
    if not request.json or 'spectra' not in request.json:
        logger.info("request did not contain spectra!")
        abort(500)
    else:
        data = request.json

        spectra = data['spectra']

        logger.info("received spectra!")

        global graph
        with graph.as_default():
            begin = time()
            try:
                result = clean_dirty_model.predict_from_spectra(input="datasets/clean_dirty",
                                                                spectra=Spectra(spectra=spectra),
                                                                encoder=clean_dirty_encoder)

                logger.info("predicted result: {}".format(result))
                return JsonResponse(json_dict={'result': int(result)})
            finally:
                logger.info("prediction took {} s".format((time() - begin) / 1000))
