'''
Created on Aug 22, 2014

@author: sumanravuri
'''

import sys
import numpy as np
import scipy.io as sp
import copy
import argparse
from Vector_Math import Vector_Math

class Bidirectional_RNNLM_Weight(object):
    def __init__(self, init_hiddens = None, weights=None, bias=None, weight_type=None):
        """num_layers
        weights - actual Recurrent Neural Network weights, a dictionary with keys corresponding to layer, ie. weights['visible_hidden'], weights['hidden_hidden'], and weights['hidden_output'] each numpy array
        bias - NN biases, again a dictionary stored as bias['visible'], bias['hidden'], bias['output'], etc.
        weight_type - optional command indexed by same keys weights, possible optionals are 'rbm_gaussian_bernoullli', 'rbm_bernoulli_bernoulli'"""
        self.valid_layer_types = dict()
        self.valid_layer_types['visible_hidden'] = ['rbm_gaussian_bernoulli', 'rbm_bernoulli_bernoulli']
        self.valid_layer_types['hidden_hidden'] = ['rbm_bernoulli_bernoulli']
        self.valid_layer_types['hidden_output'] = ['logistic']
        self.bias_keys = ['visible', 'hidden_forward', 'hidden_backward', 'output']
        self.weights_keys = ['visible_hidden', 'hidden_hidden_forward', 'hidden_hidden_backward', 'hidden_output_forward', 'hidden_output_backward']
        self.init_hiddens_keys = ['forward', 'backward']
        
        if init_hiddens is None:
            self.init_hiddens = dict()
        else:
            self.init_hiddens = copy.deepcopy(init_hiddens)
        if weights is None:
            self.weights = dict()
        else:
            self.weights = copy.deepcopy(weights)
        if bias is None:
            self.bias = dict()
        else:
            self.bias = copy.deepcopy(bias)
        if weight_type is None:
            self.weight_type = dict()
        else:
            self.weight_type = copy.deepcopy(weight_type)
            
    def clear(self):
        self.num_layers = 0
        self.weights.clear()
        self.bias.clear()
        self.weight_type.clear()
        self.init_hiddens.clear()
        
    def dot(self, nn_weight2, excluded_keys = {'bias': [], 'weights': [], 'init_hiddens': []}):
        if type(nn_weight2) is not Bidirectional_RNNLM_Weight:
            print "argument must be of type Bidirectional_RNNLM_Weight... instead of type", type(nn_weight2), "Exiting now..."
            sys.exit()
        return_val = 0
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            return_val += np.sum(self.bias[key] * nn_weight2.bias[key])
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue
            return_val += np.sum(self.weights[key] * nn_weight2.weights[key])
        for key in self.init_hiddens_keys:
            if key in excluded_keys['init_hiddens']:
                continue
            return_val += np.sum(self.init_hiddens[key] * nn_weight2.init_hiddens[key])
        return return_val
    
    def __str__(self):
        string = ""
        for key in self.bias_keys:
            string = string + "bias key " + key + "\n"
            string = string + str(self.bias[key]) + "\n"
        for key in self.weights_keys:
            string = string + "weight key " + key + "\n"
            string = string + str(self.weights[key]) + "\n"
        for key in self.init_hiddens_keys:
            string = string + "init hiddens key " + key + "\n"
            string = string + str(self.init_hiddens[key]) + "\n"
        return string
    
    def print_statistics(self):
        for key in self.bias_keys:
            print "min of bias[" + key + "] is", np.min(self.bias[key]) 
            print "max of bias[" + key + "] is", np.max(self.bias[key])
            print "mean of bias[" + key + "] is", np.mean(self.bias[key])
            print "var of bias[" + key + "] is", np.var(self.bias[key]), "\n"
        for key in self.weights_keys:
            print "min of weights[" + key + "] is", np.min(self.weights[key]) 
            print "max of weights[" + key + "] is", np.max(self.weights[key])
            print "mean of weights[" + key + "] is", np.mean(self.weights[key])
            print "var of weights[" + key + "] is", np.var(self.weights[key]), "\n"
        for key in self.init_hiddens_keys:
            print "min of init_hiddens is", np.min(self.init_hiddens[key]) 
            print "max of init_hiddens is", np.max(self.init_hiddens[key])
            print "mean of init_hiddens is", np.mean(self.init_hiddens[key])
            print "var of init_hiddens is", np.var(self.init_hiddens[key]), "\n"
        
    def norm(self, excluded_keys = {'bias': [], 'weights': [], 'init_hiddens': []}, calc_init_hiddens=False):
        squared_sum = 0
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            squared_sum += np.sum(self.bias[key] ** 2)
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            squared_sum += np.sum(self.weights[key] ** 2)
        if calc_init_hiddens:
            for key in self.init_hiddens_keys:
                if key in excluded_keys['init_hiddens']:
                    continue
                squared_sum += np.sum(self.init_hiddens[key] ** 2)
        return np.sqrt(squared_sum)
    
    def max(self, excluded_keys = {'bias': [], 'weights': [], 'init_hiddens': []}, calc_init_hiddens=False):
        max_val = -float('Inf')
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            max_val = max(np.max(self.bias[key]), max_val)
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            max_val = max(np.max(self.weights[key]), max_val)
        if calc_init_hiddens:
            for key in self.init_hiddens_keys:
                if key in excluded_keys['init_hiddens']:
                    continue
                max_val = max(np.max(self.init_hiddens[key]), max_val)
        return max_val
    
    def min(self, excluded_keys = {'bias': [], 'weights': [], 'init_hiddens': []}, calc_init_hiddens=False):
        min_val = float('Inf')
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            min_val = min(np.min(self.bias[key]), min_val)
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            min_val = min(np.min(self.weights[key]), min_val)
        if calc_init_hiddens:
            for key in self.init_hiddens_keys:
                if key in excluded_keys['init_hiddens']:
                    continue
                min_val = min(np.min(self.init_hiddens[key]), min_val)
        return min_val
    
    def clip(self, clip_min, clip_max, excluded_keys = {'bias': [], 'weights': [], 'init_hiddens': []}, calc_init_hiddens=False):
        nn_output = copy.deepcopy(self)
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            np.clip(self.bias[key], clip_min, clip_max, out=nn_output.bias[key])
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            np.clip(self.weights[key], clip_min, clip_max, out=nn_output.weights[key])
        if calc_init_hiddens:
            for key in self.init_hiddens_keys:
                if key in excluded_keys['init_hiddens']:
                    continue  
                np.clip(self.init_hiddens[key], clip_min, clip_max, out=nn_output.init_hiddens[key])
        return nn_output
    
    def get_architecture(self):
        return [self.bias['visible'].size, self.bias['hidden_forward'].size, self.bias['output'].size]
    
    def size(self, excluded_keys = {'bias': [], 'weights': [], 'init_hiddens': []}, include_init_hiddens=True):
        numel = 0
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            numel += self.bias[key].size
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            numel += self.weights[key].size
        if include_init_hiddens:
            for key in self.init_hiddens_keys:
                numel += self.init_hiddens[key].size
        return numel
    
    def open_weights(self, weight_matrix_name): #completed
        """the weight file format is very specific, it contains the following variables:
        weights_visible_hidden, weights_hidden_hidden, weights_hidden_output,
        bias_visible, bias_hidden, bias_output,
        init_hiddens, 
        weights_visible_hidden_type, weights_hidden_hidden_type, weights_hidden_output_type, etc...
        everything else will be ignored"""
        try:
            weight_dict = sp.loadmat(weight_matrix_name)
        except IOError:
            print "Unable to open", weight_matrix_name, "exiting now"
            sys.exit()
        try:
            self.bias['visible'] = weight_dict['bias_visible']
        except KeyError:
            print "bias_visible not found. bias_visible must exist for", weight_matrix_name, "to be a valid weight file... Exiting now"
            sys.exit()
        
        try:
            self.bias['hidden_forward'] = weight_dict['bias_hidden_forward']
        except KeyError:
            print "bias_hidden_forward not found. bias_hidden_forward must exist for", weight_matrix_name, "to be a valid weight file... Exiting now"
            sys.exit()
        
        try:
            self.bias['hidden_backward'] = weight_dict['bias_hidden_backward']
        except KeyError:
            print "bias_hidden_backward not found. bias_hidden_backward must exist for", weight_matrix_name, "to be a valid weight file... Exiting now"
            sys.exit()
        
        try:
            self.bias['output'] = weight_dict['bias_output']
        except KeyError:
            print "bias_output not found. bias_output must exist for", weight_matrix_name, "to be a valid weight file... Exiting now"
            sys.exit()
        
        #TODO: dump these inside of try
        self.init_hiddens['forward'] = weight_dict['init_hiddens_forward']
        self.init_hiddens['backward'] = weight_dict['init_hiddens_backward']
        self.weights['visible_hidden'] = weight_dict['weights_visible_hidden']
        self.weights['hidden_hidden_forward'] = weight_dict['weights_hidden_hidden_forward']
        self.weights['hidden_hidden_backward'] = weight_dict['weights_hidden_hidden_backward']
        self.weights['hidden_output_forward'] = weight_dict['weights_hidden_output_forward']
        self.weights['hidden_output_backward'] = weight_dict['weights_hidden_output_backward']
        
        self.weight_type['visible_hidden'] = 'rbm_bernoulli_bernoulli' #weight_dict['weights_visible_hidden_type'].encode('ascii', 'ignore')
        self.weight_type['hidden_hidden'] = 'rbm_bernoulli_bernoulli' #weight_dict['weights_hidden_hidden_type'].encode('ascii', 'ignore')
        self.weight_type['hidden_output'] = 'logistic' #weight_dict['weights_hidden_output_type'].encode('ascii', 'ignore')
        
        del weight_dict
        self.check_weights()
        
    def init_random_weights(self, architecture, initial_bias_max, initial_bias_min, initial_weight_max, initial_weight_min, seed=0): #completed, expensive, should be compiled
        np.random.seed(seed)
        
#        initial_bias_range = initial_bias_max - initial_bias_min
#        initial_weight_range = initial_weight_max - initial_weight_min
#        self.bias['visible'] = initial_bias_min + initial_bias_range * np.random.random_sample((1,architecture[0]))
#        self.bias['hidden'] = initial_bias_min + initial_bias_range * np.random.random_sample((1,architecture[1]))
#        self.bias['output'] = initial_bias_min + initial_bias_range * np.random.random_sample((1,architecture[2]))
        
        self.bias['visible'] = 0.2 * np.random.randn(1,architecture[0])
        self.bias['hidden_forward'] = 0.2 * np.random.randn(1,architecture[1])
        self.bias['hidden_backward'] = 0.2 * np.random.randn(1,architecture[1])
        self.bias['output'] = 0.2 * np.random.randn(1,architecture[2])
        
#        self.init_hiddens = np.random.random_sample((1,architecture[1])) #because of sigmoid non-linearity
        self.init_hiddens['forward'] =  0.2 * np.random.randn(1,architecture[1])
        self.init_hiddens['backward'] =  0.2 * np.random.randn(1,architecture[1])
#        self.weights['visible_hidden']=(initial_weight_min + initial_weight_range * 
#                                        np.random.random_sample( (architecture[0],architecture[1]) ))
#        self.weights['hidden_hidden']=(initial_weight_min + initial_weight_range * 
#                                       np.random.random_sample( (architecture[1],architecture[1]) ))
#        self.weights['hidden_output']=(initial_weight_min + initial_weight_range * 
#                                       np.random.random_sample( (architecture[1],architecture[2]) ))
        
        self.weights['visible_hidden'] = 0.2 * np.random.randn( architecture[0],architecture[1]) 
        self.weights['hidden_hidden_forward'] = 0.2 * np.random.randn( architecture[1],architecture[1])
        self.weights['hidden_hidden_backward'] = 0.2 * np.random.randn( architecture[1],architecture[1])
        self.weights['hidden_output_forward'] = 0.2 * np.random.randn( architecture[1],architecture[2]) 
        self.weights['hidden_output_backward'] = 0.2 * np.random.randn( architecture[1],architecture[2])
        
        self.weight_type['visible_hidden'] = 'rbm_gaussian_bernoulli'
        self.weight_type['hidden_hidden'] = 'rbm_bernoulli_bernoulli'
#        self.weight_type['hidden_hidden_backward'] = 'rbm_bernoulli_bernoulli'
        self.weight_type['hidden_output'] = 'logistic'
        
        print "Finished Initializing Weights"
        self.check_weights()
        
    def init_zero_weights(self, architecture, verbose=False):
        self.init_hiddens['forward'] = np.zeros((1,architecture[1]))
        self.init_hiddens['backward'] = np.zeros((1,architecture[1]))
        self.bias['visible'] = np.zeros((1,architecture[0]))
        self.bias['hidden_forward'] = np.zeros((1,architecture[1]))
        self.bias['hidden_backward'] = np.zeros((1,architecture[1]))
        self.bias['output'] = np.zeros((1,architecture[2]))
        
        self.init_hiddens['forward'] = np.zeros((1,architecture[1]))
        self.init_hiddens['backward'] = np.zeros((1,architecture[1]))
         
        self.weights['visible_hidden'] = np.zeros( (architecture[0],architecture[1]) )
        self.weights['hidden_hidden_forward'] = np.zeros( (architecture[1],architecture[1]) )
        self.weights['hidden_hidden_backward'] = np.zeros( (architecture[1],architecture[1]) )
        self.weights['hidden_output_forward'] = np.zeros( (architecture[1],architecture[2]) )
        self.weights['hidden_output_backward'] = np.zeros( (architecture[1],architecture[2]) )
        
        self.weight_type['visible_hidden'] = 'rbm_gaussian_bernoulli'
        self.weight_type['hidden_hidden'] = 'rbm_bernoulli_bernoulli'
        self.weight_type['hidden_output'] = 'logistic'
        if verbose:
            print "Finished Initializing Weights"
        self.check_weights(False)
        
    def check_weights(self, verbose=True): #need to check consistency of features with weights
        """checks weights to see if following conditions are true
        *feature dimension equal to number of rows of first layer (if weights are stored in n_rows x n_cols)
        *n_cols of (n-1)th layer == n_rows of nth layer
        if only one layer, that weight layer type is logistic, gaussian_bernoulli or bernoulli_bernoulli
        check is biases match weight values
        if multiple layers, 0 to (n-1)th layer is gaussian bernoulli RBM or bernoulli bernoulli RBM and last layer is logistic regression
        """
        if verbose:
            print "Checking weights...",
        
        #check weight types
        if self.weight_type['visible_hidden'] not in self.valid_layer_types['visible_hidden']:
            print self.weight_type['visible_hidden'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['visible_hidden'], "...Exiting now"
            sys.exit()
        if self.weight_type['hidden_hidden'] not in self.valid_layer_types['hidden_hidden']:
            print self.weight_type['hidden_hidden'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['hidden_hidden'], "...Exiting now"
            sys.exit()
#        if self.weight_type['hidden_hidden_forward'] not in self.valid_layer_types['hidden_hidden_forward']:
#            print self.weight_type['hidden_hidden_forward'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['hidden_hidden_forward'], "...Exiting now"
#            sys.exit()
#        if self.weight_type['hidden_hidden_backward'] not in self.valid_layer_types['hidden_hidden_backward']:
#            print self.weight_type['hidden_hidden_backward'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['hidden_hidden_backward'], "...Exiting now"
#            sys.exit()
        if self.weight_type['hidden_output'] not in self.valid_layer_types['hidden_output']:
            print self.weight_type['hidden_output'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['hidden_output'], "...Exiting now"
            sys.exit()
        
        #check biases
        if self.bias['visible'].shape[1] != self.weights['visible_hidden'].shape[0]:
            print "Number of visible bias dimensions: ", self.bias['visible'].shape[1],
            print " of layer visible does not equal visible weight dimensions ", self.weights['visible_hidden'].shape[0], "... Exiting now"
            sys.exit()
            
        if self.bias['output'].shape[1] != self.weights['hidden_output_forward'].shape[1]:
            print "Number of visible bias dimensions: ", self.bias['visible'].shape[1],
            print " of layer visible does not equal output weight dimensions ", self.weights['hidden_output_forward'].shape[1], "... Exiting now"
            sys.exit()
        if self.bias['output'].shape[1] != self.weights['hidden_output_backward'].shape[1]:
            print "Number of visible bias dimensions: ", self.bias['visible'].shape[1],
            print " of layer visible does not equal output weight dimensions ", self.weights['hidden_output_backward'].shape[1], "... Exiting now"
            sys.exit()
        
        if self.bias['hidden_forward'].shape[1] != self.weights['visible_hidden'].shape[1]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_forward'].shape[1],
            print " of layer 0 does not equal hidden weight dimensions ", self.weights['visible_hidden'].shape[1], " of visible_hidden layer ... Exiting now"
            sys.exit()
        if self.bias['hidden_forward'].shape[1] != self.weights['hidden_output_forward'].shape[0]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_forward'].shape[1],
            print " of layer 0 does not equal hidden weight dimensions ", self.weights['hidden_output_forward'].shape[0], "of hidden_output_forward layer... Exiting now"
            sys.exit()
        if self.bias['hidden_forward'].shape[1] != self.weights['hidden_hidden_forward'].shape[0]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_forward'].shape[1],
            print " of layer 0 does not equal input weight dimensions ", self.weights['hidden_hidden_forward'].shape[0], " of hidden_hidden_forward layer... Exiting now"
            sys.exit()
        if self.bias['hidden_forward'].shape[1] != self.weights['hidden_hidden_forward'].shape[1]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_forward'].shape[1],
            print " of layer 0 does not equal output weight dimensions ", self.weights['hidden_hidden_forward'].shape[1], " hidden_hidden_forward layer... Exiting now"
            sys.exit()
        if self.bias['hidden_forward'].shape[1] != self.init_hiddens['forward'].shape[1]:
            print "dimensionality of hidden bias", self.bias['hidden_forward'].shape[1], "and the forward initial hiddens", self.init_hiddens['forward'].shape[1], "do not match. Exiting now."
            sys.exit()
        
        if self.bias['hidden_backward'].shape[1] != self.weights['visible_hidden'].shape[1]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_backward'].shape[1],
            print " of layer 0 does not equal hidden weight dimensions ", self.weights['visible_hidden'].shape[1], " of visible_hidden layer ... Exiting now"
            sys.exit()
        if self.bias['hidden_backward'].shape[1] != self.weights['hidden_output_backward'].shape[0]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_backward'].shape[1],
            print " of layer 0 does not equal hidden weight dimensions ", self.weights['hidden_output_backward'].shape[0], "of hidden_output_backward layer... Exiting now"
            sys.exit()
        if self.bias['hidden_backward'].shape[1] != self.weights['hidden_hidden_backward'].shape[0]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_backward'].shape[1],
            print " of layer 0 does not equal input weight dimensions ", self.weights['hidden_hidden_backward'].shape[0], " of hidden_hidden_backward layer... Exiting now"
            sys.exit()
        if self.bias['hidden_backward'].shape[1] != self.weights['hidden_hidden_backward'].shape[1]:
            print "Number of hidden bias dimensions: ", self.bias['hidden_backward'].shape[1],
            print " of layer 0 does not equal output weight dimensions ", self.weights['hidden_hidden_backward'].shape[1], " hidden_hidden_backward layer... Exiting now"
            sys.exit()
        if self.bias['hidden_backward'].shape[1] != self.init_hiddens['backward'].shape[1]:
            print "dimensionality of hidden bias", self.bias['hidden_backward'].shape[1], "and the backward initial hiddens", self.init_hiddens['backward'].shape[1], "do not match. Exiting now."
            sys.exit()
            
        #check weights
        if self.weights['visible_hidden'].shape[1] != self.weights['hidden_hidden_forward'].shape[0]:
            print "Dimensionality of visible_hidden", self.weights['visible_hidden'].shape, "does not match dimensionality of hidden_hidden_forward", "\b:",self.weights['hidden_hidden_forward'].shape
            print "The second dimension of visible_hidden must equal the first dimension of hidden_hidden layer"
            sys.exit()
        if self.weights['visible_hidden'].shape[1] != self.weights['hidden_hidden_backward'].shape[0]:
            print "Dimensionality of visible_hidden", self.weights['visible_hidden'].shape, "does not match dimensionality of hidden_hidden_backward", "\b:",self.weights['hidden_hidden_backward'].shape
            print "The second dimension of visible_hidden must equal the first dimension of hidden_hidden layer"
            sys.exit()
        if self.weights['hidden_hidden_forward'].shape[1] != self.weights['hidden_hidden_forward'].shape[0]:
            print "Dimensionality of hidden_hidden_forward", self.weights['hidden_hidden_forward'].shape, "is not square, which it must be. Exiting now..."
            sys.exit()
        if self.weights['hidden_hidden_backward'].shape[1] != self.weights['hidden_hidden_backward'].shape[0]:
            print "Dimensionality of hidden_hidden_backward", self.weights['hidden_hidden_backward'].shape, "is not square, which it must be. Exiting now..."
            sys.exit()
        if self.weights['hidden_hidden_forward'].shape[1] != self.weights['hidden_output_forward'].shape[0]:
            print "Dimensionality of hidden_hidden_forward", self.weights['hidden_hidden_forward'].shape, "does not match dimensionality of hidden_output", "\b:",self.weights['hidden_output_forward'].shape
            print "The second dimension of hidden_hidden_forward must equal the first dimension of hidden_output layer"
            sys.exit()
        if self.weights['hidden_hidden_backward'].shape[1] != self.weights['hidden_output_forward'].shape[0]:
            print "Dimensionality of hidden_hidden_backward", self.weights['hidden_hidden_backward'].shape, "does not match dimensionality of hidden_output", "\b:",self.weights['hidden_output_backward'].shape
            print "The second dimension of hidden_hidden_backward must equal the first dimension of hidden_output layer"
            sys.exit()
        if self.weights['hidden_hidden_forward'].shape[1] != self.init_hiddens['forward'].shape[1]:
            print "dimensionality of hidden_hidden_forward weights", self.weights['hidden_hidden_forward'].shape[1], "and the initial hiddens forward", self.init_hiddens['forward'].shape[1], "do not match. Exiting now."
            sys.exit()
        if self.weights['hidden_hidden_backward'].shape[1] != self.init_hiddens['backward'].shape[1]:
            print "dimensionality of hidden_hidden_backward weights", self.weights['hidden_hidden_backward'].shape[1], "and the backward initial hiddens", self.init_hiddens['backward'].shape[1], "do not match. Exiting now."
            sys.exit() 
        
        if verbose:
            print "seems copacetic"
            
    def write_weights(self, output_name): #completed
        weight_dict = dict()
        weight_dict['bias_visible'] = self.bias['visible']
        weight_dict['bias_hidden_forward'] = self.bias['hidden_forward']
        weight_dict['bias_hidden_backward'] = self.bias['hidden_backward']
        weight_dict['bias_output'] = self.bias['output']
        
        weight_dict['weights_visible_hidden'] = self.weights['visible_hidden']
        weight_dict['weights_hidden_hidden_forward'] = self.weights['hidden_hidden_forward']
        weight_dict['weights_hidden_hidden_backward'] = self.weights['hidden_hidden_backward']
        weight_dict['weights_hidden_output_forward'] = self.weights['hidden_output_forward']
        weight_dict['weights_hidden_output_backward'] = self.weights['hidden_output_backward']
        weight_dict['init_hiddens_forward'] = self.init_hiddens['forward']
        weight_dict['init_hiddens_backward'] = self.init_hiddens['backward']
        try:
            sp.savemat(output_name, weight_dict, oned_as='column')
        except IOError:
            print "Unable to save ", self.output_name, "... Exiting now"
            sys.exit()
        else:
            print output_name, "successfully saved"
            del weight_dict

    def assign_weights(self,other):
        if self.get_architecture() != other.get_architecture():
            raise ValueError("Neural net models do not match... Exiting now")
        
        for key in self.bias_keys:
            self.bias[key][:] = other.bias[key][:]
        for key in self.weights_keys:
            self.weights[key][:] = other.weights[key][:]
        for key in self.init_hiddens_keys:
            self.init_hiddens[key][:] = other.init_hiddens[key][:]

    def __neg__(self):
        nn_output = copy.deepcopy(self)
        for key in self.bias_keys:
            nn_output.bias[key] = -self.bias[key]
        for key in self.weights_keys:
            nn_output.weights[key] = -self.weights[key]
        for key in self.init_hiddens_keys:    
            nn_output.init_hiddens[key] = -self.init_hiddens[key]
        return nn_output
    
    def __add__(self,addend):
        nn_output = copy.deepcopy(self)
        if type(addend) is Bidirectional_RNNLM_Weight:
            if self.get_architecture() != addend.get_architecture():
                print "Neural net models do not match... Exiting now"
                sys.exit()
            
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] + addend.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] + addend.weights[key]
            for key in self.init_hiddens_keys:
                nn_output.init_hiddens[key] = self.init_hiddens[key] + addend.init_hiddens[key]
            return nn_output
        #otherwise type is scalar
        addend = float(addend)
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] + addend
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] + addend
        for key in self.init_hiddens_keys:
            nn_output.init_hiddens[key] = self.init_hiddens[key] + addend
        return nn_output
        
    def __sub__(self,subtrahend):
        nn_output = copy.deepcopy(self)
        if type(subtrahend) is Bidirectional_RNNLM_Weight:
            if self.get_architecture() != subtrahend.get_architecture():
                print "Neural net models do not match... Exiting now"
                sys.exit()
            
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] - subtrahend.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] - subtrahend.weights[key]
            for key in self.init_hiddens_keys:
                nn_output.init_hiddens[key] = self.init_hiddens[key] - subtrahend.init_hiddens[key]
            return nn_output
        #otherwise type is scalar
        subtrahend = float(subtrahend)
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] - subtrahend
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] - subtrahend
        for key in self.init_hiddens_keys:
            nn_output.init_hiddens[key] = self.init_hiddens[key] - subtrahend
        return nn_output
    
    def __mul__(self, multiplier):
        #if type(scalar) is not float and type(scalar) is not int:
        #    print "__mul__ must be by a float or int. Instead it is type", type(scalar), "Exiting now"
        #    sys.exit()
        nn_output = copy.deepcopy(self)
        if type(multiplier) is Bidirectional_RNNLM_Weight:
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] * multiplier.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] * multiplier.weights[key]
            for key in self.init_hiddens_keys:
                nn_output.init_hiddens[key] = self.init_hiddens[key] * multiplier.init_hiddens[key]
            return nn_output
        #otherwise scalar type
        multiplier = float(multiplier)
        
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] * multiplier
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] * multiplier
        for key in self.init_hiddens_keys:
            nn_output.init_hiddens[key] = self.init_hiddens[key] * multiplier
        return nn_output
    
    def __div__(self, divisor):
        #if type(scalar) is not float and type(scalar) is not int:
        #    print "Divide must be by a float or int. Instead it is type", type(scalar), "Exiting now"
        #    sys.exit()
        nn_output = copy.deepcopy(self)
        if type(divisor) is Bidirectional_RNNLM_Weight:
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] / divisor.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] / divisor.weights[key]
            for key in self.init_hiddens_keys:
                nn_output.init_hiddens[key] = self.init_hiddens[key] / divisor.init_hiddens[key]
            return nn_output
        #otherwise scalar type
        divisor = float(divisor)
        
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] / divisor
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] / divisor
        for key in self.init_hiddens_keys:
            nn_output.init_hiddens[key] = self.init_hiddens[key] / divisor
        return nn_output
    
    def __pow__(self, scalar):
        if scalar == 2:
            return self * self
        scalar = float(scalar)
        nn_output = copy.deepcopy(self)
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] ** scalar
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] ** scalar
        for key in self.init_hiddens_keys:
            nn_output.init_hiddens[key] = nn_output.init_hiddens[key] ** scalar
        return nn_output

    def __iadd__(self, nn_weight2):
        if type(nn_weight2) is not Bidirectional_RNNLM_Weight:
            print "argument must be of type Bidirectional_RNNLM_Weight... instead of type", type(nn_weight2), "Exiting now..."
            sys.exit()
        if self.get_architecture() != nn_weight2.get_architecture():
            print "Neural net models do not match... Exiting now"
            sys.exit()

        for key in self.bias_keys:
            self.bias[key] += nn_weight2.bias[key]
        for key in self.weights_keys:
            self.weights[key] += nn_weight2.weights[key]
        for key in self.init_hiddens_keys:
            self.init_hiddens[key] += nn_weight2.init_hiddens[key]
        return self
    
    def __isub__(self, nn_weight2):
        if type(nn_weight2) is not Bidirectional_RNNLM_Weight:
            print "argument must be of type Bidirectional_RNNLM_Weight... instead of type", type(nn_weight2), "Exiting now..."
            sys.exit()
        if self.get_architecture() != nn_weight2.get_architecture():
            print "Neural net models do not match... Exiting now"
            sys.exit()

        for key in self.bias_keys:
            self.bias[key] -= nn_weight2.bias[key]
        for key in self.weights_keys:
            self.weights[key] -= nn_weight2.weights[key]
        for key in self.init_hiddens_keys:
            self.init_hiddens[key] -= nn_weight2.init_hiddens[key]
        return self
    
    def __imul__(self, scalar):
        #if type(scalar) is not float and type(scalar) is not int:
        #    print "__imul__ must be by a float or int. Instead it is type", type(scalar), "Exiting now"
        #    sys.exit()
        scalar = float(scalar)
        for key in self.bias_keys:
            self.bias[key] *= scalar
        for key in self.weights_keys:
            self.weights[key] *= scalar
        for key in self.init_hiddens_keys:
            self.init_hiddens[key] *= scalar
        return self
    
    def __idiv__(self, other):
        if type(other) is Bidirectional_RNNLM_Weight:
            for key in self.bias_keys:
                self.bias[key] /= other.bias[key]
            for key in self.weights_keys:
                self.weights[key] /= other.weights[key]
            for key in self.init_hiddens_keys:
                self.init_hiddens[key] /= other.init_hiddens[key]
            
        else:
            scalar = float(other)
            for key in self.bias_keys:
                self.bias[key] /= scalar
            for key in self.weights_keys:
                self.weights[key] /= scalar
            for key in self.init_hiddens_keys:
                self.init_hiddens[key] /= scalar
        return self
    
    def __ipow__(self, scalar):
        scalar = float(scalar)
        for key in self.bias_keys:
            self.bias[key] **= scalar
        for key in self.weights_keys:
            self.weights[key] **= scalar
        for key in self.init_hiddens_keys:
            self.init_hiddens[key] **= scalar
        return self
    
    def __copy__(self):
        return Bidirectional_RNNLM_Weight(self.init_hiddens, self.weights, self.bias, self.weight_type)
    
    def __deepcopy__(self, memo):
        return Bidirectional_RNNLM_Weight(copy.deepcopy(self.init_hiddens, memo), copy.deepcopy(self.weights,memo), 
                                          copy.deepcopy(self.bias,memo), copy.deepcopy(self.weight_type,memo))