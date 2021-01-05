import numpy as np

###########################################################
# sample implementation of neural network backpropagation #
###########################################################


input_x = np.array([0.1, 0.3])
weights_input_hidden = np.array([0.4, -0.2])
weights_hidden_output = np.array([0.1])
target = 1
learning_rate = 0.8
epochs = 1000


def sigmoid(x) -> float:
    return 1/(1+np.exp(-x))


def forward_pass():
    output = np.dot(input_x, weights_input_hidden)
    hidden_unit_output = sigmoid(output)
    final_output = sigmoid(np.dot(hidden_unit_output, weights_hidden_output))
    return final_output, hidden_unit_output


def backward_pass(final_output, hidden_unit_output):
    ultimate_lyr_err = target - final_output
    ultimate_lyr_err_term = ultimate_lyr_err * final_output * (1-final_output)
    penultimate_err_term = weights_hidden_output*ultimate_lyr_err_term*hidden_unit_output*(1-hidden_unit_output)
    del_w_h_o = learning_rate*ultimate_lyr_err_term*hidden_unit_output
    del_w_i_h = learning_rate*penultimate_err_term*input_x
    return del_w_h_o, del_w_i_h, ultimate_lyr_err


for i in range(epochs):
    final_output, hidden_unit_output = forward_pass()
    del_w_h_o, del_w_i_h, err = backward_pass(final_output, hidden_unit_output)
    if i % 100 == 0:
        print(f"iteration {i}: error {err[0]}")
    weights_hidden_output = weights_hidden_output + del_w_h_o
    weights_hidden_input = weights_input_hidden + del_w_i_h
