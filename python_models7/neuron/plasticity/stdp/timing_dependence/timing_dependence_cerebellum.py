from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence\
    import AbstractTimingDependence
from spynnaker.pyNN.models.neuron.plasticity.stdp.synapse_structure\
    import SynapseStructureWeightOnly
from spynnaker.pyNN.models.neuron.plasticity.stdp.common \
    import plasticity_helpers

import logging
import math

logger = logging.getLogger(__name__)

# Constants
LOOKUP_SIN_SIZE = 512
LOOKUP_SIN_SHIFT = 0

class TimingDependenceCerebellum(AbstractTimingDependence):

    # noinspection PyPep8Naming
    def __init__(
            self,
            tau=40.0,
            peak_time=100.0):
        AbstractTimingDependence.__init__(self)
        self._tau = tau
        self._peak_time = peak_time

        self._synapse_structure = SynapseStructureWeightOnly()


    @property
    def tau(self):
        return self._tau

    @tau.setter
    def tau(self, tau):
        self._tau = tau

    @property
    def peak_time(self):
        return self._peak_time

    @peak_time.setter
    def peak_time(self, peak_time):
        self._peak_time = peak_time

    def is_same_as(self, timing_dependence):

        if not isinstance(timing_dependence, TimingDependenceCerebellum):
            return False

        return (
            (self._tau ==
                timing_dependence._tau) and
            (self._peak_time ==
                timing_dependence._peak_time))

    @property
    def vertex_executable_suffix(self):

        # to indicate that it is compiled with this timing dependence
        # Note: The expected format of the binary name is:
        #    <neuron_model>_stdp[_mad|]_<timing_dependence>_<weight_dependence>
        return "cerebellum"

    @property
    def pre_trace_n_bytes(self):

        # the number of bytes in the pre_trace_t data
        # structure in the C code
        return 0

    def get_parameters_sdram_usage_in_bytes(self):

        return 4 + (2 * LOOKUP_SIN_SIZE)

    @property
    def n_weight_terms(self):
        return 1

    def write_parameters(self, spec, machine_time_step, weight_scales):
        # Write peak time in timesteps
        peak_time_data = int(self._peak_time * (1000.0 / machine_time_step) - LOOKUP_SIN_SIZE/2  + 0.5)
        print "peak time data:", peak_time_data, "peak_time:", self._peak_time
        spec.write_value(data=peak_time_data,
                         data_type=DataType.INT32)

        # Calculate time constant reciprocal
        time_constant_reciprocal = (1.0 / float(self._tau)) * (machine_time_step / 1000.0)

        # This offset is the quasi-symmetry point
        sinadd_pwr = 20
        zero_offset = math.atan(-1./sinadd_pwr)
        max_value = math.exp(-zero_offset)*math.cos(zero_offset)**sinadd_pwr

        # Generate LUT
        last_value = None
        for i in range(-LOOKUP_SIN_SIZE/2,-LOOKUP_SIN_SIZE/2 + LOOKUP_SIN_SIZE):
            # Apply shift to get time from index
            time = (i << LOOKUP_SIN_SHIFT)
            
            # Multiply by time constant and calculate negative exponential
            value = float(time) * time_constant_reciprocal + zero_offset
            # we want a single bump only, so we clip the arg at pi/2
            if abs(value) > math.pi/2.:
                exp_float = 0.0
            else:
                exp_float = math.exp(-value) * math.cos(value)**sinadd_pwr / max_value
            print i, exp_float, 

            # Convert to fixed-point and write to spec
            last_value = plasticity_helpers.float_to_fixed(1.0*exp_float, plasticity_helpers.STDP_FIXED_POINT_ONE)
            print last_value, plasticity_helpers.STDP_FIXED_POINT_ONE
            spec.write_value(data=last_value, data_type=DataType.UINT16)

        self._tau_last_entry = float(last_value) / float(plasticity_helpers.STDP_FIXED_POINT_ONE)


    @overrides(AbstractTimingDependence.get_parameter_names)
    def get_parameter_names(self):
        return ['tau', 'peak_time']

    @property
    def synaptic_structure(self):
        return self._synapse_structure
