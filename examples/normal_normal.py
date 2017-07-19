from pdb import set_trace as bb
import numpy as np
import torch
from torch.autograd import Variable
import torch.optim as optim

import pyro
from pyro.distributions import DiagNormal

from pyro.infer.abstract_infer import LikelihoodWeighting, lw_expectation
from pyro.infer.importance import Importance
from pyro.infer.kl_qp import KL_QP


def model():
    latent = pyro.sample("latent",
                         DiagNormal(Variable(torch.zeros(1, 1)),
                                    5 * Variable(torch.ones(1, 1))))
    x_dist = DiagNormal(latent, Variable(torch.ones(1, 1)))
    x = pyro.observe("obs", x_dist, Variable(torch.ones(1, 1)))
    return latent
#
# now let's try inference
infer = LikelihoodWeighting(model)
#
exp = lw_expectation(infer, lambda x: x, 101)
print(exp)

# and try importance!

def guide():
    latent = pyro.sample("latent",
                         DiagNormal(Variable(torch.zeros(1, 1)),
                                    5 * Variable(torch.ones(1, 1))))
    x_dist = DiagNormal(latent, Variable(torch.ones(1, 1)))

infer = Importance(model, guide)

exp = lw_expectation(infer, lambda x: x, 100)
print(exp)

def guide():
    mf_m = pyro.param("mf_m", Variable(torch.zeros(1, 1)))
    mf_v = pyro.param("mf_v", Variable(torch.ones(1, 1)))
    latent = pyro.sample("latent",
                         DiagNormal(mf_m, mf_v))

adam_params = {"lr": .0001}

infer = KL_QP(model, guide, pyro.optim(optim.Adam, adam_params))

exp = lw_expectation(infer, lambda x: x, 100)
print(exp)
