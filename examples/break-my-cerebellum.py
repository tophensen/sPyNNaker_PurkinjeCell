import pylab
import IPython
import spynnaker7.pyNN as sim
from python_models7.neuron.builds\
    .if_curr_exp_supervision import IFCurrExpSupervision
from python_models7.neuron.plasticity.stdp.timing_dependence\
    .timing_dependence_cerebellum import TimingDependenceCerebellum

# ------------------------------------------------------------------
# This example uses the sPyNNaker implementation of cerebellar
# STDP
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Common parameters
# ------------------------------------------------------------------
teaching_time = 400.
tau=60.
peak_time = 100.
#num_pre_cells = 100

# Population parameters
model = IFCurrExpSupervision
#model = sim.IF_curr_exp
cell_params = {'cm': 0.25,  # nF
               'i_offset': 0.0,
               'tau_m': 10.0,
               'tau_refrac': 2.0,
               'tau_syn_E': 2.5,
               'tau_syn_I': 2.5,
               'v_reset': -70.0,
               'v_rest': -65.0,
               'v_thresh': -55.4
               }

# SpiNNaker setup
ts=1.0	# does not work at 0.4, 0.6, 0.8, why??
sim.setup(timestep=ts, min_delay=ts, max_delay=15*ts)

sim_time = 4000.
pre_stim = []

spike_times = []

######## CRASH ME BY USING 1.0ms steps instead of 2.0ms
for t in pylab.arange(0,teaching_time,1.0):
    spike_times.append([t,sim_time-t])

pre_stim = sim.Population(len(spike_times),sim.SpikeSourceArray,{'spike_times': spike_times},label="Granules")
#dummy_stim = sim.Population(1,sim.SpikeSourceArray,{'spike_times': [sim_time]},label="dummy")

nn_pc = 10 # number of purkinje cells (and inferior olive cells)
teaching_stim = sim.Population(nn_pc, sim.SpikeSourceArray,
    {'spike_times': [[teaching_time+j*ts for j in range(i)] for i in range(nn_pc)]},label="Inferior Olives")

# Neuron populations
population = sim.Population(nn_pc, model, cell_params, label="Purkinjes")
population.record("spikes")
population2 = sim.Population(nn_pc, sim.IF_curr_exp, cell_params, label="fake purk")
population2.record("spikes")

# Plastic Connection between pre_pop and post_pop
stdp_model = sim.STDPMechanism(
    timing_dependence = TimingDependenceCerebellum(tau=tau, peak_time=peak_time),
    weight_dependence = sim.AdditiveWeightDependence(w_min=1.0, w_max=15.0, A_plus=0.5, A_minus=0.01)
)

#stdp_model = sim.STDPMechanism(
#    timing_dependence = sim.SpikePairRule(tau_plus=tau, tau_minus=tau),
#    weight_dependence = sim.AdditiveWeightDependence(w_min=1.0, w_max=15.0, A_plus=0.1, A_minus=0.1)
#)


# Connections between spike sources and neuron populations
    ####### SET HERE THE PARALLEL FIBER-PURKINJE CELL LEARNING RULE
ee_connector = sim.AllToAllConnector(weights=1.0)
projection_pf = sim.Projection(pre_stim, population, ee_connector,
                                         synapse_dynamics=sim.SynapseDynamics(slow=stdp_model),
                                         target='excitatory')

                                         
proj2 = sim.Projection(pre_stim, population2, ee_connector,target='excitatory')

# SET HERE THE TEACHING SIGNAL PROJECTION
ee_connector = sim.OneToOneConnector(weights=0.0)
proj_teaching = sim.Projection(teaching_stim, population, ee_connector, target='supervision')
#proj_dummy = sim.Projection(dummy_stim,population,sim.OneToOneConnector(weights=1000.1), target='inhibitory')

#IPython.embed()

print("Simulating for %us" % (sim_time / 1000))

# Run simulation
sim.run(sim_time)

# Get weight from each projection
end_w = projection_pf.getWeights() #[p.getWeights()[0] for p in projections_pf]
print end_w

# -------------------------------------------------------------------
# Plot curve
# -------------------------------------------------------------------
# Plot STDP curve
figure, axis = pylab.subplots()
axis.set_xlabel('Time Delta')
axis.set_ylabel('Weight')
#axis.set_ylim((0.0, 1.0))

for i in range(nn_pc):
    axis.plot([t[0] - teaching_time for t in spike_times], end_w[i::nn_pc],marker="o",ms=1.0,mec="k",label="%i IO spikes"%i)
#axis.axvline(teaching_time, linestyle="--")

pylab.legend(loc='lower left')
pylab.show()
#IPython.embed()
# End simulation on SpiNNaker
sim.end()
