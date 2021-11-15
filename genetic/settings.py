'concentrates the configuration values'
import os

import dotenv

dotenv.load_dotenv()

# Settings for bits per each field
N_BITS_EPSILON = int(os.environ['N_BITS_EPSILON'])
N_BITS_MIN_SAMPLES = int(os.environ['N_BITS_MIN_SAMPLES'])
RANGE_EPSILON = list(map(int, os.environ['RANGE_EPSILON'].split(',')))


RATE_MUTATION = float(os.environ['RATE_MUTATION'])
INCREMENT_RATE_MUTATION = float(os.environ['INCREMENT_RATE_MUTATION'])
SIZE_ELITE = int(os.environ['SIZE_ELITE'])
MAX_EPOCHS = int(os.environ['MAX_EPOCHS'])
POPULATION_SIZE = int(os.environ['POPULATION_SIZE'])

OUTDIR = os.environ['OUTDIR']
