# Isolation Considerations
---
## Electrical Spacing
### IEC60664-1: Insulation coordination for equipment within low-voltage supply systems
`Referenced Design: Technical White Paper Circuit Board Insulation Design According to IEC60664 for Motor Drive Applications Texas Instruments`
#### Clearance vs Creepages
- ***Clearance***: Shortest distance between two conductive materials measured through air
  - Air breakdown influenced by pollution degree, temperature, and relative humidity
  - Breakdown caused by impulses of massive voltage, therefor clearance is considered by a systems maximum peak voltage to determine it's overvoltage category (OVC Level).
- ***Creepage***: Shortest distance between two conductive materials measured along surface of isolator
  - Distance influenced by pollution degree, material characteristics, and isolator comparative tracking index (CTI)
  - Distance is more dependent on time and RMS of a voltage applied
  - Measured in days, weeks, or months instead of impulses

Comparative tracking Index Materials Table
|Material Group| CTI Range |
|---|---|
|I| 600 V < CTI|
|II| 400 V < CTI < 600 V|
|IIIa| 175 V < CTI < 400 V|
|IIIb| 100 V < CTI < 175 V|

<img src="/PCB_Design/PCB_Images/CreepageVsClearance.png" height=300 width=800>

#### Insulation Type
- ***Functional insulation:*** Insulation designed purely for the functionality of the system. Does not protect against electric shock
- ***Basic insulation:*** Insulation applied to live parts to prevent electric shock to any persons
- ***Double insulation:*** Supplementary insulation between basic insulation and user in cases of basic insulation failure and shock
- ***Reinforced insulation:*** Single insulation system designed to be equivalent to double insulation from shock

#### Decisive Voltage Class and Extra-Low Voltage
- ***Decisive Voltage Class(DVC):*** classification of voltage range used to determine the protective measures against electric shock

<img src="/PCB_Design/PCB_Images/DVC.png" height=200 width=800>

- ***Extra Low Voltage (ELV):*** any voltage not exceed 50V ac-rms and 120V dc

#### Protection Class
- ***Class 1:*** Equipment non-reliant on basic insulation by including connection of conductive parts to protective conductor (Earth)
- ***Class 2:*** Equipment non-reliant on basic insulation by including double/reinforced insulation without protective conductor or reliance on installation conditions

<img src="/PCB_Design/PCB_Images/ProtectiveClassesIsolation.png" height=300 width=600>

### Pollution Degree
- ***Pollution:*** Foreign matter affecting electrical strength or surface resistivity of insulation
- ***Micro-Environment:*** Immediate environment of insulation, affecting dimensions of creepage distance
- ***Pollution Degree:*** Numerical characterization of environment. Used in creepage and clearance distances

| Pollution Degree | Micro-Environment | Example |
|--|--|--|
| 1 | No pollution or only dry, non-conductive pollution occurs. The pollution has no influence. | Inside air-conditioned labs, under protective coatings, or within internal PWB layers. |
| 2 | Normally, only non-conductive pollution occurs. Occasionally, temporary conductivity caused by condensation is expected when equipment is out of operation. | Inside standard electrical enclosures, control cabinets, or household appliances. |
| 3 | Conductive pollution occurs, or dry non-conductive pollution becomes conductive due to expected condensation. | Electrical equipment in industrial environments or machine tools. |
| 4 | Continuous or persistent conductivity is generated, caused by conductive dust, rain, snow, or continuous high humidity. | Outdoor electrical equipment or heavy industrial installations exposed to weather. |

### Overvoltage Category
Describes the short term overvoltage that occurs within a system, Usually occurs in milliseconds even in oscillatory waveforms, which should be heavily damped
|Category|Characteristics|Examples|
|--|--|--|
|Category I (OVC I)| applies to equipment connected to a circuit where measures have been taken to reduce transient overvoltage to a low level.| Inside the electrical circuit.|
|Category II (OVC II)| applies between the circuits not directly supplied by mains or the environment.|Appliances, portable tools and other plug-connected equipment.|
|Category III (OVC III)| applies to the circuits directly supplied by mains or the environment. |Downstream of and including the main distribution board like switchgear and other equipment in an industrial installation.|
|Category IV (OVC IV)| applies to equipment permanently connected at the origin of an installation.| Upstream of the main distribution board like electricity meters, primary overcurrent protection equipment and other equipment connected directly to outdoor open lines.|

<img src="/PCB_Design/PCB_Images/OvervoltageVFDExample.png" height=400 width=700>


### Power Systems and Non-Linear Loads

AC power systems (whether Delta or Wye configurations) dictate voltage relationships and grounding, but no real-world system perfectly maintains a pure sine wave, just as DC systems always have some underlying ripple.

#### Non-Linear Responses and Rectification:
When real circuitry is connected to a non-linear load (like a power supply with a diode bridge and smoothing capacitor), it does not draw current continuously. Instead, current is drawn in sharp, high-amplitude pulses. This occurs only at the peaks of the AC voltage sine wave, specifically when the incoming line voltage momentarily exceeds the voltage of the DC smoothing capacitor.

Voltage Distortion and Parasitic Ringing:
These massive current pulses cause an immediate voltage drop across the line's inherent impedance, causing the AC voltage wave to "flat-top." Additionally, the rapid change in current ($\frac{dI}{dt}$) excites high-frequency ringing across the system's parasitic inductances ($L_p$) and capacitances ($C_p$).

-   The voltage spike of this ringing is approximated by: $\Delta V_{ring} \approx I_{pulse} \times \sqrt{\frac{L_p}{C_p}}$
-   The amplitude envelope of this parasitic tank decays over time as: $A(t) = A_0 e^{-\frac{\omega_0 t}{2Q}}$
-   The tank's resonant frequency is: $f_0 = \frac{1}{2\pi \sqrt{L_p C_p}}$
-   The Quality factor ($Q$) is dictated by the total series resistance ($R$) in the loop: $Q = \frac{1}{R} \sqrt{\frac{L_p}{C_p}}$

#### Correction via Power Factor Correction (PFC):
To mitigate this distortion, PFC is applied to the circuit:
-   Passive PFC: Adding a series inductor slows the current's rate of change, spreading the sharp spikes into wider, smoother pulses.
-   Active PFC: A closed control loop dynamically forces the current to stay in phase with the AC voltage. Operating in Continuous Conduction Mode (CCM), the system utilizes high-frequency switching to bounce the current between a tight lower and upper bound, averaging out perfectly to match the shape of the input sine wave.

#### Real-World DC Outputs and Ripple:**
While theoretical DC is a perfectly flat line, practical DC power always contains variations. In switch-mode power supplies (such as buck, boost, or LLC converters), the continuous charging and discharging of the output filter network creates a periodic variation known as ripple voltage.
-   Parasitic Influence: The total output ripple isn't determined solely by the bulk capacitance ($C_{out}$). It is heavily dictated by the capacitor's Equivalent Series Resistance (ESR) and Equivalent Series Inductance (ESL).
-   The Ripple Equation: $\Delta V_{out} \approx \Delta I_L \times \left(ESR + \frac{1}{8 f_{sw} C_{out}}\right) + ESL \frac{di}{dt}$
-   Design Considerations: High RMS ripple current generates $I^2R$ heating inside the capacitor, which can degrade the component over time. Furthermore, for sensitive downstream loads (like microcontrollers relying on clean rails for precise ADC triggers), excessive ripple injects noise into signal measurements, often necessitating secondary LC filters or Low Dropout (LDO) regulators.

#### Pulsating Voltages and the Sawtooth Profile:
When a working voltage is actively pulsed—such as the raw switching node of a converter or an unfiltered rectifier—the smoothed profile across the load often resembles a sawtooth or triangle wave.
-   The Charge/Discharge Cycle: This shape is born from the fundamental behavior of reactive elements. When a switch closes, energy floods the inductor or capacitor, causing a rapid voltage ramp. When the switch opens, the stored energy discharges more slowly and linearly into the load.
-   Sawtooth Formation: The rapid charge from an incoming current pulse, followed by the steady $RC$ drain into the load, inherently creates this sawtooth waveform.
-   Control Loop Implications: Depending on the load and topology, this sawtooth ripple rides on top of the DC offset. In analog or digital control schemes, this voltage ramp is often fed directly into comparators to generate the necessary Pulse-Width Modulation (PWM) signals, meaning the sawtooth itself is functional, not just a parasitic byproduct.


<img src="/PCB_Design/PCB_Images/TrueWorkingVoltage.png" Height=500 Width=400>

### Designing for Isolation
Before beginning a full designing, the conditions of the circuitry system must be defined. This involves defining the following:
- Functional blocks on circuit board
- System Voltage
- Environment conditions (pollution degree) for circuit board
- Mechanical constrains around circuit board. For example, limited height, closed to the conductive parts
connected to earth

and done using the following steps:
Step 1: Requirement & specification collection
Step 2: Voltage block definition
Step 3: Determination of types of insulation and OVC level
Step 4: Determination of working voltage
Step 5: Clearance Definition
Step 6: Creepage Definition


#### TI Example
Step 1: Requirement collection. An industrial motor drive system is listed with the following specifications:
- Class I device (In a metallic cabinet with chassis connect to earth)
- 3-phase power source with nominal 220 Vac and 380 Vac (wye power source), OVC III
- Industrial pollution degree 2 micro-environment
- Isolation required by end-user (Human Machine Interface - HMI)
- Hot side MCU control
- Operating altitude < 2000 m
<img src="/PCB_Design/PCB_Images/TIIsolationStep1.png" Height=500 Width=800>

Step 2: Voltage Block definition. This step specifies the voltage blocks in the electrical schematic. The electrical
circuit without internal galvanic isolation in which the voltage between two conductors cannot be above 50 Vac
and 120 Vdc for clearance.
<img src="/PCB_Design/PCB_Images/TIIsolationStep2.png" Height=500 Width=800>

Step 3: determine the insulation type and OVC level. The insulation type includes basic, functional and reinforced insulation. The OVC level includes I, II, III and IV. Table 2-1 shows the insulation type and OVC level between each voltage blocks.

Step 4: determine the working voltage (WV). The rated working voltage for clearance (CL) is the peak value and is referred to table B of IEC60664-1 while the working voltage for creepage (CR) is the RMS value. The table B of IEC60664-1 consists of 50 V, 100 V, 150 V, 300 V, 600 V, and 1000 V these 6 levels working voltages. Table 2-2 shows the working voltage for both clearance and creepage between each voltage blocks. The working voltage value is done by simulation and calculation.

<img src="/PCB_Design/PCB_Images/TIIsolationStep4.png" Height=500 Width=800>

Step 5: Clearance distance: Table F.1 of IEC60664-1 defines the rated impulse voltage according to each working voltage and OVC level while table F.2 defines the clearances to withstand transient over-voltages. Clearances shall be dimensioned to withstand the required impulse withstand voltage according table F.1 and F.2. With respect to impulse voltages, clearances of reinforced insulation shall be dimensioned as specified in Table F.2 corresponding to the rated impulse voltage but one step higher in the preferred series of values than that specified for basic insulation. For 220-V or 380-V systems, the impulse voltage is 1500 V for OVC1 with functional isolation, 4000 V for OVCIII with basic isolation and 6000 V for reinforced insulation. Then the corresponding clearance of pollution degree 2 is 0.5 mm for 1500 V with functional isolation, 3 mm for 4000 V with basic isolation and 5.5 mm for 6000 V with reinforced isolation.

Step 6: Creepage distance: Table F.4 of IEC60664-1 defines the creepage distances for functional, basic insulation to avoid failure according to different pollution degrees and material group of printed circuit board. Creepage distance for reinforced insulation shall be twice the creepage distance for basic insulation from table F.4. IEC61800-5-1 also defines that when the creepage distance is less than clearance determined by impulse voltage, then it shall be increased to that clearance.
  Creepage for 400-V working voltage = 2 mm (functional, basic), 4 mm (reinforced) (1)
  Creepage for 440-V working voltage = 40 V × (2.5 mm – 2 mm) / (500 V – 400 V) + 2 mm = 2.2 mm (2)
  Creepage for 565-V working voltage = 65 V × (3.2 mm – 2.5 mm) / (630 V – 500 V) + 2.5 mm = 2.8 mm (3)
Table 2-3 shows clearance and creepage distance between each voltage blocks

<img src="/PCB_Design/PCB_Images/TIIsolationStep6_1.png" Height=500 Width=800>


Finally, select the maximum value between clearance and creepage as the insulation distance, then put the values into PCB design tool as the constrain rules as Table 2-4 shows

<img src="/PCB_Design/PCB_Images/TIIsolationStep6_2.png" Height=500 Width=800>

Since the requirement is defined, the operating altitude is below 2000 meters. When the product or circuit board requires higher altitude than 2000 m, be sure to consider altitude correction factors. Table A.2 of IEC60664-1 defines the multiplication factor for air clearance. For example, 4000-m altitude correction factor is 1.29. Clearance distance for 2000 m is 3 mm, then clearance for 4000 m is 3 mm × 1.29 = 3.87 mm.

### IEC Table Requirements Examples

Below shows the example IEC creepage and clearance distances under the conditions described

<img src="/PCB_Design/PCB_Images/IEC_Example_Isolation1.png" Height=500 Width=1400>

Below shows the example TI chips and their needed distances for operation under the conditions described.

<img src="/PCB_Design/PCB_Images/IEC_TI_ICchips_ex.png" Height=500 Width=1400>

### IEC Tables

##### Table F.1 - Rated impulse withstand voltage for equipment energized directly from the mains supply
| Nominal voltage of the mains supply - Three-phase (V) | Nominal voltage of the mains supply - Single phase (V) | Voltage line to neutral derived from nominal voltages AC or DC (V) | Rated impulse withstand voltage - Overvoltage category I (V) | Rated impulse withstand voltage - Overvoltage category II (V) | Rated impulse withstand voltage - Overvoltage category III (V) | Rated impulse withstand voltage - Overvoltage category IV (V) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | 50 | 50 | 330 | 500 | 800 | 1 500 |
| | 100 | 100 | 500 | 800 | 1 500 | 2 500 |
| | 120 to 240 | 150 | 800 | 1 500 | 2 500 | 4 000 |
| 230/400, 277/480 | | 300 | 1 500 | 2 500 | 4 000 | 6 000 |
| 400/690 | | 600 | 2 500 | 4 000 | 6 000 | 8 000 |
| 1 000 | | 1 000 | 4 000 | 6 000 | 8 000 | 12 000 |
| >1 000 ≤ 1 250 f | | 1 250 | 4 000 | 6 000 | 8 000 | 12 000 |
| >1 250 ≤ 1 500 f | | 1 500 | 6 000 | 8 000 | 10 000 | 15 000 |


##### Table F.2 - Clearances to withstand transient overvoltages
| Required impulse withstand voltage (kV) | Case A (Inhomogeneous field) - Pollution degree 1 (mm) | Case A - Pollution degree 2 (mm) | Case A - Pollution degree 3 (mm) | Case B (Homogeneous field) - Pollution degree 1 (mm) | Case B - Pollution degree 2 (mm) | Case B - Pollution degree 3 (mm) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0,33 b | 0,01 | | | 0,01 | | |
| 0,40 | 0,02 | | | 0,02 | | |
| 0,50 b | 0,04 | | | 0,04 | | |
| 0,60 | 0,06 | 0,2 c, d | 0,8 d | 0,06 | 0,2 c, d | |
| 0,80 b | 0,10 | 0,2 c, d | 0,8 d | 0,10 | 0,2 c, d | |
| 1,0 | 0,15 | 0,25 | | 0,15 | | 0,8 d |
| 1,2 | 0,25 | 0,25 | | 0,2 | | 0,8 d |
| 1,5 b | 0,5 | 0,5 | | 0,3 | 0,3 | |
| 2,0 | 1,0 | 1,0 | 1,0 | 0,45 | 0,45 | |
| 2,5 b | 1,5 | 1,5 | 1,5 | 0,60 | 0,60 | |
| 3,0 | 2,0 | 2,0 | 2,0 | 0,80 | 0,80 | |
| 4,0 b | 3,0 | 3,0 | 3,0 | 1,2 | 1,2 | 1,2 |
| 5,0 | 4,0 | 4,0 | 4,0 | 1,5 | 1,5 | 1,5 |
| 6,0 b | 5,5 | 5,5 | 5,5 | 2,0 | 2,0 | 2,0 |
| 8,0 b | 8,0 | 8,0 | 8,0 | 3,0 | 3,0 | 3,0 |
| 10 | 11 | 11 | 11 | 3,5 | 3,5 | 3,5 |
| 12 b | 14 | 14 | 14 | 4,5 | 4,5 | 4,5 |
| 15 | 18 | 18 | 18 | 5,5 | 5,5 | 5,5 |
| 20 | 25 | 25 | 25 | 8,0 | 8,0 | 8,0 |
| 25 | 33 | 33 | 33 | 10 | 10 | 10 |
| 30 | 40 | 40 | 40 | 12,5 | 12,5 | 12,5 |
| 40 | 60 | 60 | 60 | 17 | 17 | 17 |
| 50 | 75 | 75 | 75 | 22 | 22 | 22 |
| 60 | 90 | 90 | 90 | 27 | 27 | 27 |
| 80 | 130 | 130 | 130 | 35 | 35 | 35 |
| 100 | 170 | 170 | 170 | 45 | 45 | 45 |

##### Table F.3 - Single-phase three-wire or two-wire AC or DC systems
| Nominal voltage of the mains supply (V) | Voltages rationalized for Table F.5: For insulation line-to-line All systems (V) | Voltages rationalized for Table F.5: For insulation line-to-earth Three-wire systems mid-point earthed (V) |
| :--- | :--- | :--- |
| 12.5 | 12.5 | |
| 24, 25 | 25 | |
| 30 | 32 | |
| 42 | | |
| 48 | 50 | |
| 50 c | | |
| 60 | 63 | |
| 30 to 60 | 63 | 32 |
| 100 c | 100 | |
| 110, 120 | 125 | |
| 150 c | 160 | |
| 200 | 200 | |
| 100 to 200 | 200 | 100 |
| 220 | 250 | |
| 110 to 220, 120 to 240 | 250 | 125 |
| 300 | 320 | |
| 220 to 440 | 500 | 250 |
| 600 c | 630 | |
| 480 to 960 | 1 000 | 500 |
| 1 000 | 1 000 | |
| 1 500 c, d | 1 500 | |

##### Table F.4 - Three-phase four-wire or three-wire AC systems
| Nominal voltage of the mains supply (V) | For insulation line-to-line All systems (V) | For insulation line-to-earth Three-phase four-wire systems neutral-earthed (V) | For insulation line-to-earth Three-phase three-wire systems unearthed or corner-earthed (V) |
| :--- | :--- | :--- | :--- |
| 60 | 63 | 32 | 63 |
| 110, 120, 127 | 125 | 80 | 125 |
| 150 d | 160 | | 160 |
| 200 | 200 | | 200 |
| 208 | 200 | 125 | 200 |
| 220, 230, 240 | 250 | 160 | 250 |
| 300 d | 320 | | 320 |
| 380, 400 | 400 | 250 | 400 |
| 415, 440 | 500 | 250 | 500 |
| 480, 500 | 500 | 320 | 500 |
| 575 | 630 | 400 | 630 |
| 600 d | 630 | | 630 |
| 660, 690 | 630 | 400 | 630 |
| 720, 830 | 800 | 500 | 800 |
| 960 | 1 000 | 630 | 1 000 |
| 1 000 d | 1 000 | | 1 000 |

##### Table F.5 - Creepage distances to avoid failure due to tracking (Combined 1 & 2)
| Voltage RMS (V) | Pollution degree 1: Printed wiring material (mm) | Pollution degree 1: All material groups (mm) | Pollution degree 2: Printed wiring material (mm) | Pollution degree 2: All material groups except IIIb (mm) | Pollution degree 2: Material group II (mm) | Pollution degree 2: Material group I (mm) | Pollution degree 3: Material group III (mm) | Pollution degree 3: Material group II (mm) | Pollution degree 3: Material group I (mm) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | 0,025 | 0,080 | 0,040 | 0,400 | 0,400 | 0,400 | 1,000 | 1,000 | 1,000 |
| 12,5 | 0,025 | 0,090 | 0,040 | 0,420 | 0,420 | 0,420 | 1,050 | 1,050 | 1,050 |
| 16 | 0,025 | 0,100 | 0,040 | 0,450 | 0,450 | 0,450 | 1,100 | 1,100 | 1,100 |
| 20 | 0,025 | 0,110 | 0,040 | 0,480 | 0,480 | 0,480 | 1,200 | 1,200 | 1,200 |
| 25 | 0,025 | 0,125 | 0,040 | 0,500 | 0,500 | 0,500 | 1,250 | 1,250 | 1,250 |
| 32 | 0,025 | 0,14 | 0,040 | 0,53 | 0,53 | 0,53 | 1,30 | 1,30 | 1,30 |
| 40 | 0,025 | 0,16 | 0,040 | 0,80 | 0,56 | 1,10 | 1,40 | 1,60 | 1,80 |
| 50 | 0,025 | 0,18 | 0,040 | 0,60 | 0,85 | 1,20 | 1,50 | 1,70 | 1,90 |
| 63 | 0,040 | 0,063 | 0,20 | 0,90 | 0,63 | 1,25 | 1,60 | 1,80 | 2,00 |
| 80 | 0,063 | 0,22 | 0,100 | 0,67 | 0,95 | 1,30 | 1,70 | 1,90 | 2,10 |
| 100 | 0,100 | 0,25 | 0,160 | 1,00 | 0,71 | 1,40 | 1,80 | 2,00 | 2,20 |
| 125 | 0,160 | 0,250 | 0,28 | 0,75 | 1,05 | 1,50 | 1,90 | 2,10 | 2,40 |
| 160 | 0,250 | 0,400 | 0,32 | 1,10 | 0,80 | 1,60 | 2,00 | 2,20 | 2,50 |
| 200 | 0,400 | 0,630 | 0,42 | 1,40 | 1,00 | 2,00 | 2,50 | 2,80 | 3,20 |
| 250 | 0,560 | 1,000 | 0,56 | 1,80 | 1,25 | 2,50 | 3,20 | 3,60 | 4,00 |
| 320 | 0,75 | 1,60 | 0,75 | 2,20 | 1,60 | 3,20 | 4,00 | 4,50 | 5,00 |
| 400 | 1,0 | 2,0 | 1,0 | 2,8 | 2,0 | 4,0 | 5,0 | 5,6 | 6,3 |
| 500 | 1,3 | 2,5 | 1,3 | 3,6 | 2,5 | 5,0 | 6,3 | 7,1 | 8,0 (7,9) d |
| 630 | 1,8 | 3,2 | 1,8 | 4,5 | 3,2 | 6,3 | 8,0 (7,9) d | 9,0 (8,4) d | 10,0 (9,0) c |
| 800 | 2,4 | 4,0 | 2,4 | 5,6 | 4,0 | 8,0 | 10,0 (9,0) d | 11,0 (9,6) d | 12,5 (10,2) d |
| 1 000 | 3,2 | 5,0 | 3,2 | 7,1 | 5,0 | 10,0 | 12,5 (10,2) d | 14,0 (11,2) d | 16,0 (12,8) d |
| 1 250 | | 4,2 | | 9,0 | 6,3 | 12,5 | 16,0 (12,8) | 18,0 (14,4) d | 20,0 (16,0) d |
| 1 600 | | 5,6 | | 11,0 | 8,0 | 16,0 | 20,0 (16,0) d | 22,0 (17,6) d | 25,0 (20,0) d |
| 2 000 | | 7,5 | | 14,0 | 10,0 | 20,0 | 25,0 (20,0) c | 28,0 (22,4) d | 32,0 (25,6) d |
| 2 500 | | 10,0 | | 18,0 | 12,5 | 25,0 | 32,0 (25,6) d | 36,0 (28,8) d | 40,0 (32,0) d |
| 3 200 | | 12,5 | | 22,0 | 16,0 | 32,0 | 40,0 (32,0) | 45,0 (36,0) d | 50,0 (40,0) d |
| 4 000 | | 16,0 | | 28,0 | 20,0 | 40,0 | 50,0 (40,0) d | 56,0 (44,8) d | 63,0 (50,4) d |
| 5 000 | | 20,0 | | 36,0 | 25,0 | 50,0 | 63,0 (50,4) d | 71,0 (56,8) d | 80,0 (64,0) d |
| 6 300 | | 25,0 | | 45,0 | 32,0 | 63,0 | 80,0 (64,0) d | 90,0 (72,0) d | 100,0 (80,0) d |
| 8 000 | | 32,0 | | 56,0 | 40,0 | 80,0 | 100,0 | 110,0 (88,0) | 125,0 (100,0) d |
| 10 000 | | 40,0 | | 71,0 | 50,0 | 100,0 | 125,0 | 140,0 (112,0) c | 160,0 (128,0) d |
| 12 500 | | 50,0 c | | 90,0 c | 63,0 c | 125,0 c | 160,0 c | 180,0 c | 200,0 |
| 16 000 | | 63,0 c | | 110,0 c | 80,0 c | 160,0 c | 200,0 | 220,0 c | 250,0 |
| 20 000 | | 80,0 | | 140,0 c | 100,0 c | 200,0 c | 250,0 | 280,0 c | 320,0 |
| 25 000 | | 100,0 c | | 180,0 c | 125,0 c | 250,0 | 320,0 | 360,0 c | 400,0 |
| 32 000 | | 125,0 | | 220,0 c | 160,0 c | 320,0 | 400,0 | 450,0 c | 500,0 |
| 40 000 | | 160,0 c | | 280,0 c | 200,0 c | 400,0 | 500,0 | 600,0 c | 630,0 |
| 50 000 | | 200,0 c | | 360,0 c | 250,0 c | 500,0 | 630,0 | | |
| 63 000 | | 250,0 c | | 450,0 c | 320,0 c | 630,0 | | | |

##### Table F.6 - Test voltages for verifying clearances only at different altitudes
| Rated impulse withstand voltage (kV) | Impulse test voltage at sea level (kV) | Impulse test voltage at 200 m altitude (kV) | Impulse test voltage at 500 m altitude (kV) |
| :--- | :--- | :--- | :--- |
| 0,33 | 0,355 | 0,357 | 0,350 |
| 0,5 | 0,537 | 0,541 | 0,531 |
| 0,8 | 0,934 | 0,920 | 0,899 |
| 1,5 | 1,751 | 1,725 | 1,685 |
| 2,5 | 2,920 | 2,874 | 2,808 |
| 4,0 | 4,824 | 4,923 | 4,675 |
| 6,0 | 7,236 | 7,385 | 7,013 |
| 8,0 | 9,847 | 9,648 | 9,350 |
| 10,0 | 12,060 | 12,309 | 11,688 |
| 12,0 | 14,770 | 14,471 | 14,025 |
| 15,0 | 18,464 | 18,091 | 17,533 |

##### Table F.7 - Severities for conditioning of solid insulation
| Test | Temperature (°C) | Relative humidity (%) | Time (h) | Number of cycles |
| :--- | :--- | :--- | :--- | :--- |
| a) Dry heat | +55 | | 48 | 1 |
| b) Change of temperature with specified rate of change | -10 to +55 | | Cycle duration 24 | 3 |
| c) Thermal shock (rapid change of temperature) | -10 to +55 | | b | |
| d) Damp heat, steady state | 30/40 a | 93 | 96 | 1 |

##### Table F.8 - Dimensioning of clearances to withstand steady-state peak voltages, temporary overvoltages or recurring peak voltages
| Voltage a (peak value) b (kV) | Minimum clearances in air up to 2 000 m above sea level - Case A Inhomogeneous field conditions (mm) | Minimum clearances in air up to 2 000 m above sea level - Case B Homogeneous field conditions (mm) |
| :--- | :--- | :--- |
| 0,04 | 0,001 c | 0,001 c |
| 0,06 | 0,002 c | 0,002 c |
| 0,1 | 0,003 | 0,003 |
| 0,12 | 0,004 | 0,004 |
| 0,15 | 0,005 | 0,005 |
| 0,20 | 0,006 | 0,006 |
| 0,25 | 0,008 | 0,008 |
| 0,33 | 0,01 | 0,01 |
| 0,4 | 0,02 | 0,02 |
| 0,5 | 0,04 | 0,04 |
| 0,6 | 0,06 | 0,06 |
| 0,8 | 0,13 | 0,1 |
| 1,0 | 0,26 | 0,15 |
| 1,2 | 0,42 | 0,2 |
| 1,5 | 0,76 | 0,3 |
| 2,0 | 1,27 | 0,45 |
| 2,5 | 1,8 | 0,6 |
| 3,0 | 2,4 | 0,8 |
| 4,0 | 3,8 | 1,2 |
| 5,0 | 5,7 | 1,5 |
| 6,0 | 7,9 | 2 |
| 8,0 | 11,0 | 3 |
| 10 | 15,2 | 3,5 |
| 12 | 19 | 4,5 |
| 15 | 25 | 5,5 |
| 20 | 34 | 8 |
| 25 | 44 | 10 |
| 30 | 55 | 12,5 |
| 40 | 77 | 17 |
| 50 | 100 | 22 |
| 60 | | 27 |
| 80 | | 35 |
| 100 | | 45 |

##### Table F.9 - Additional information concerning the dimensioning of clearances to avoid partial discharge
| Voltage a (peak value) b (kV) | Minimum clearances in air up to 2 000 m above sea level - Case A Inhomogeneous field conditions (mm) |
| :--- | :--- |
| 0,2 / 0,25 | As specified for case A in Table F.8 |
| 0,33 | |
| 0,4 | |
| 0,5 | |
| 0,6 | |
| 0,8 | |
| 1,0 | |
| 1,2 | |
| 1,5 | |
| 2,0 | |
| 2,5 | 2,0 |
| 3,0 | 3,2 |
| 4,0 | 11 |
| 5,0 | 24 |
| 6,0 | 64 |
| 8,0 | 184 |
| 10 | 290 |
| 12 | 320 |

##### Table F.10 - Altitude correction factors for clearance correction
| Altitude (m) | Factor kd for distance correction |
| :--- | :--- |
| 0 | 0,784 |
| 200 | 0,803 |
| 500 | 0,833 |
| 1 000 | 0,884 |
| 2 000 | 1,000 |
