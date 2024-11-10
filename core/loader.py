from core.label_decoder import LabelDecoder
from core.config import HARDWARE_TYPE_CLASSIFIER_PATH, REQUEST_TYPE_CLASSIFIER_PATH
from core.classifier import Classifier


label_decoder = LabelDecoder()
hardware_type_classifier = Classifier(HARDWARE_TYPE_CLASSIFIER_PATH)
request_type_classifier = Classifier(REQUEST_TYPE_CLASSIFIER_PATH)
