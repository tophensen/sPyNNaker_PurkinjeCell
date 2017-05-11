import pylab

import spynnaker7.pyNN as p

from python_models7.neuron.builds.my_model_curr_exp import MyModelCurrExp
from python_models7.neuron.builds.my_model_curr_exp_my_additional_input \
    import MyModelCurrExpMyAdditionalInput
from python_models7.neuron.builds.my_model_curr_exp_my_threshold \
    import MyModelCurrExpMyThreshold
from python_models7.neuron.builds.my_model_curr_my_synapse_type \
    import MyModelCurrMySynapseType
from python_models7.neuron.plasticity.stdp.timing_dependence\
    .my_timing_dependence import MyTimingDependence
from python_models7.neuron.plasticity.stdp.weight_dependence\
    .my_weight_dependence import MyWeightDependence

# Set the run time of the execution
run_time = 1000

# Set the time step of the simulation in milliseconds
time_step = 1.0

# Set the number of neurons to simulate
n_neurons = 1

# Set the i_offset current
i_offset = 0.0

# Set the weight of input spikes
weight = 2.0

# Set the times at which to input a spike
spike_times = range(0, run_time, 100)


# A function to create a graph of voltage against time
def create_v_graph(population, title):
    v = population.get_v()
    if v is not None:
        ticks = len(v) / n_neurons
        pylab.figure()
        pylab.xlabel('Time (ms)')
        pylab.ylabel("Membrane Voltage")
        pylab.title(title)

        for pos in range(n_neurons):
            v_for_neuron = v[pos * ticks: (pos + 1) * ticks]
            pylab.plot([i[1] for i in v_for_neuron],
                       [i[2] for i in v_for_neuron])

p.setup(time_step)

input_pop = p.Population(
    1, p.SpikeSourceArray, {"spike_times": spike_times}, label="input")

my_model_pop = p.Population(
    1, MyModelCurrExp,
    {
        "my_parameter": -70.0,
        "i_offset": i_offset,
    },
    label="my_model_pop")
p.Projection(
    input_pop, my_model_pop,
    p.OneToOneConnector(weights=weight))

my_model_my_synapse_type_pop = p.Population(
    1, MyModelCurrMySynapseType,
    {
        "my_parameter": -70.0,
        "i_offset": i_offset,
        "my_ex_synapse_parameter": 0.5
    },
    label="my_model_my_synapse_type_pop")
p.Projection(
    input_pop, my_model_my_synapse_type_pop,
    p.OneToOneConnector(weights=weight))

my_model_my_additional_input_pop = p.Population(
    1, MyModelCurrExpMyAdditionalInput,
    {
        "my_parameter": -70.0,
        "i_offset": i_offset,
        "my_additional_input_parameter": 0.05
    },
    label="my_model_my_additional_input_pop")
p.Projection(
    input_pop, my_model_my_additional_input_pop,
    p.OneToOneConnector(weights=weight))

my_model_my_threshold_pop = p.Population(
    1, MyModelCurrExpMyThreshold,
    {
        "my_parameter": -70.0,
        "i_offset": i_offset,
        "threshold_value": -10.0,
        "my_threshold_parameter": 0.4
    },
    label="my_model_my_threshold_pop")
p.Projection(
    input_pop, my_model_my_threshold_pop,
    p.OneToOneConnector(weights=weight))

my_model_stdp_pop = p.Population(
    1, MyModelCurrExp,
    {
        "my_parameter": -70.0,
        "i_offset": i_offset,
    },
    label="my_model_pop")
stdp = p.STDPMechanism(
    timing_dependence=MyTimingDependence(
        my_potentiation_parameter=2.0,
        my_depression_parameter=0.1),
    weight_dependence=MyWeightDependence(
        w_min=0.0, w_max=10.0, my_parameter=0.5))
p.Projection(
    input_pop, my_model_stdp_pop,
    p.OneToOneConnector(weights=weight))
stdp_connection = p.Projection(
    input_pop, my_model_stdp_pop,
    p.OneToOneConnector(weights=0),
    synapse_dynamics=p.SynapseDynamics(slow=stdp))

my_model_pop.record_v()
my_model_my_synapse_type_pop.record_v()
my_model_my_additional_input_pop.record_v()
my_model_my_threshold_pop.record_v()

p.run(run_time)

print stdp_connection.getWeights()

create_v_graph(
    my_model_pop, "My Model")
create_v_graph(
    my_model_my_synapse_type_pop, "My Model with My Synapse Type")
create_v_graph(
    my_model_my_additional_input_pop, "My Model with My Additional Input")
create_v_graph(
    my_model_my_threshold_pop, "My Model with My Threshold")
pylab.show()

p.end()
