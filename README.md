# TKINTER IZHIKEVICH NEURON MODEL WITH PYTHON

## Hodgkin-Huxley model

It is a mathematical model for the generation and transmission of action potentials in neurons. The origin of this model is based on circuit theory. It describes the electrical properties of cells that respond to stimuli, such as neurons and heart muscles. It is a constantly dynamic system.

![eg](https://user-images.githubusercontent.com/73841520/135606000-9d9ce66b-fc74-44f1-b261-fa42e3832fee.png)

It is the electrical equivalent circuit inside an axon. Part A: equivalent circuit for a very small portion of the dice. The resistance of the intercellular fluid is neglected. Part B: It is the electrical equivalent circuit that is formed by the sequential repetition of the circuit in the A part and corresponds to the whole membrane. Membrane potential in an active electrical equivalent circuit:

![Ekran görüntüsü 2021-09-30 134542](https://user-images.githubusercontent.com/73841520/135606994-9b4e99ad-b867-45ba-a6fd-04c417bddd55.png)

Hodgkin-Huxley action potential equation;
It is controlled by the Na gate, which enables activation by opening the depolarization result, the three m gate with fast motion, and an h gate with slow motion, which closes as a result of depolarization.

The K channel controls four slow-motion n-gate m-gates. If the highest conductivities corresponding to open Na and K channels are expressed as g(Na ) and gK, respectively;

![trj](https://user-images.githubusercontent.com/73841520/135607738-5e2b3839-a9e1-4b98-a4cc-b381c008f317.png)

This connection is called the action potential equation propagated by Hodgkin-Huxley.

![yj](https://user-images.githubusercontent.com/73841520/135607746-ce6892d6-abc9-4901-907a-68dfb5985ce2.png)

Here, action potential and the number of sodium and potassium channels opened at that moment represent the spatial distribution of events at a given time, while the right-to-left spread of stimuli, the graph shows how events change over time at a given time. Since the action potential is an undamped wave motion, the position of the axon also determines it.

## Izhikevich Neuron Model

Eugene M. Izhikevich stated in 2003 that two conditions are necessary for the development of brain models. These are computational simplicity and the ability to produce rich firing patterns. According to Izhikeivich, the Hodgkin-Huxley model is the most biophysically accurate but difficult to simulate neuron model. On the other hand, the integrated flesh-and-fire neuron model is computationally feasible, but not suitable for spikes of cortical neurons. The Izhikevich neuron model is a neuron model where the plausible aspects of these two neuron models meet: It is computationally efficient and realistic enough to simulate the spikes of cortical neurons.

![Ekran görüntüsü 2021-09-28 145151](https://user-images.githubusercontent.com/73841520/135607018-2b9719cf-4564-40ab-a5dd-e082dce809db.png)  # 2.1-2.2

In the equation, the equations of the Hodgkin-Huxley model are reduced to a two-dimensional system by bifurcation methodologies. The post-jump reset equation is shown below.

![Ekran görüntüsü 2021-09-28 145312](https://user-images.githubusercontent.com/73841520/135607033-5c678a7b-13a4-437f-bbe9-af739b1f1461.png)

v and u are dimensionless variables; a, b, c, d dimensionless parameters; t time. The variable v represents the membrane potential of the neuron; The variable u was used to represent activation of K+ ionic currents and deactivation of Na+ ionic currents, i.e. membrane recovery variable. If the jump reaches +30mV, the membrane voltage and recovery variable are reset (Equation (2.3)). It is the 0.04v 2 + 5v + 140 part in Eq.(2.1) that allows the variable v representing the membrane potential to have the ms scale of the mV and the time representing the t value.

According to the equations, the listening potential varies between 70-60 mV. Membrane potential before jumping can be at least -55 mV and at most -40 mV. The value that defines the time scale of u is a. The smaller the values, the slower it heals. The parameter that defines the sensitivity of u and v variables to sub-threshold fluctuations is parameter b. A large value for this parameter results in stronger binding of the variables v and u. Fast high threshold K+ conductivities cause a jump in the v variable, and slow high threshold K+ and N a+ conductivities cause a jump in u variable.

After the sudden jump of these values, reset parameters are c and d parameters, respectively. The different selection of these parameters allows various dynamics to occur, as shown in the figure.

![Ekran görüntüsü 2021-09-28 144432](https://user-images.githubusercontent.com/73841520/135607003-338488ca-19b9-428d-8343-ea4e2650915b.png)

Neocortical neurons are classified according to the types of jumps. Excitatory cortical cells are divided into three classes:

* RS: When RS neurons, the most specific neurons in the cortex, are stimulated by a constant stimulus, it starts with a few sudden jumps at first. It then continues to jump with a lower frequency. Increasing the power of the stimulus decreases the frequencies. In RS neuron type, c parameter is -65mV, d parameter is 8.

* IB: In the face of a constant stimulus, this neuron model first begins with an irregular and almost continuous jump. At this time, the variable u is created. Then repetitive jumps occur. The c and d parameters are -55mV and 4, respectively.

* CH: These neurons jump one after the other in response to a fixed value stimulus and line up in a heap. The frequency between hops can be as high as 40Hz. In this neuron type, the c parameter is -50mV and the d parameter is 2.

Inhibitory cortical cells are divided into two classes:

* FS: Performs high frequency jumps without adapting to a fixed value stimulus. Parameter a corresponds to a value of 0.1.

* LTS: It starts with high frequency adaptation. It continues with a decreasing but still higher frequency. The reason for the low ignition threshold is that parameter b is 0.25.
In addition, the stimulus response of thalamo-cortical neurons that provide the main input to the cortex is simulated with this model:

* TC: These neurons jump in two different ways. In the first state, it is the resting state and then the depolarized state. At rest, the variable v is around -60mV. The next state is the hyperpolarization state, in which a negative stimulus is given. The v variable is around -90Mv.

The model can model other types of neurons:

* RZ: Such neurons have damped and sustained oscillations. Parameter a is 0.1 and parameter b is 0.26.

The Izhikevich neuron model enabled the modeling of many different types of neurons in the brain. The compatibility of the equations we have explained above with the behavior of other neurons is also explained. It also helps to simulate large-scale neuronal networks.

![egr](https://user-images.githubusercontent.com/73841520/135608976-bbb9203d-5642-473b-b94f-f5b7485b0374.png)

![r3rf](https://user-images.githubusercontent.com/73841520/135608970-7ae4ccd2-7d11-4dd7-803c-697687768685.png)


