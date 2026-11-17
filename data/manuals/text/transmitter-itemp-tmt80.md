---
id: transmitter-itemp-tmt80
product: Endress+Hauser iTEMP TMT80
component: Trasmettitore in testa 4-20 mA per PT100
tags: TT1, TT2, TT3, TT5a, TT5b
---

<!-- page 1 -->

TI00153R/09/EN/06.21-00
71551073
2021-10-20

Products

Solutions

Services

Technical Information
iTEMP TMT80
Universal temperature head transmitter for
resistance thermometers and thermocouples
PC-programmable

Application
• PC programmable (PCP) temperature head transmitter for the conversion of
different input signals into an analog, scalable 4 to 20 mA output signal
• For resistance thermometers (RTD) and thermocouples (TC)
• Device configuration via PC with configuration kit and PC software
Your benefits
• 2-wire power supply, analog output4 to 20 mA
• Fault signal in the event of sensor break or sensor short circuit, adjustable as per
NAMUR NE43
• Meets EMC requirements as per NAMUR NE21
• Galvanic isolation 500 V (input/output)
• Adjustment of the application-specific measuring range

<!-- page 2 -->

iTEMP TMT80

Function and system design
Measuring principle

Electronic recording and conversion of various input signals in industrial temperature measurement.

Measuring system

The iTEMP TMT80 temperature head transmitter is a two-wire transmitter with an analog output
and a measuring input for resistance thermometers with a 2-, 3-, or 4-wire connection and
thermocouples. The device is configured using a configuration kit and the free ReadWin 2000
operating software.

Input
Measured variable

Temperature (temperature-linear transmission behavior)

Measuring range

The device provides different measuring ranges depending on the sensor connection and input
signals:

Resistance thermometer (RTD)
as per standard
IEC 60751 (α = 0.00385)

Designation
Pt100
Pt1000

Measuring range limits
–200 to +850 °C (–328 to +1 562 °F)
–200 to +250 °C (–328 to +482 °F)

Min. span
10 K (18 °F)

• Connection type: 2-, 3- or 4-wire connection
• With 2-wire circuit, compensation of wire resistance possible (0 to 20 Ω)
• Cable resistance: sensor wire resistance up to max. 11 Ω per wire
• Sensor current: ≤ 0.6 mA

Thermocouples as per standard

IEC 60584, Part 1

Designation
Type B (PtRh30-PtRh6) (31)
Type K (NiCr-Ni) (36)
Type N (NiCrSi-NiSi) (37)
Type R (PtRh13-Pt) (38)
Type S (PtRh10-Pt) (39)

Measuring range limits
+40 to +1 820 °C (+104 to +3 308 °F)
–200 to +1 372 °C (–328 to +2 501 °F)
–270 to +1 300 °C (–454 to +2 372 °F)
–50 to +1 768 °C (–58 to +3 214 °F)
–50 to +1 768 °C (–58 to +3 214 °F)

Min. span
500 K
50 K
50 K
500 K
500 K

• Internal reference junction (Pt100)
• Reference junction accuracy: ± 1 K

Output
Output signal

Analog, 4 to 20 mA

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Signal on alarm

| Condition | Output current |
|---|---|
| Underranging | Linear drop to 3.8 mA |
| Overranging | Linear rise to 20.5 mA |
| Sensor breakage; sensor short-circuit (not for thermocouples) | ≤ 3.6 mA or ≥ 21.0 mA (if setting is ≥ 21.0 mA an output current ≥ 21.5 mA is guaranteed) |

Load

Max. (Vpower supply - 8 V) / 0.025 A (Current output)

Transmission behavior

Temperature linear

Galvanic isolation

U = 500 VAC (input/output)

1)

2

Not for thermocouples

Endress+Hauser

<!-- page 3 -->

iTEMP TMT80

Input current required

≤ 3.5 mA

Current limit

≤ 25 mA

Switch-on delay

4s

Power supply
Terminal assignment

3
1

2
6

RD
RD
4

5

WH

1

4

WH

3

2

A0047182

1
1
2
3
4

Transmitter mounted in the terminal head
Sensor input, TC
Sensor input, RTD and Ω: 4-, 3- and 2-wire
Display connection/CDI interface
Power supply

Supply voltage

Ub = 8 to 35 V, reverse polarity protection

Residual ripple

Permitted residual ripple Uss ≤ 3 V at Ub ≥ 15 V, f max. = 1 kHz

Performance characteristics
Response time

1s

Reference operating
conditions

• Calibration temperature: +25 °C (+77 °F) ± 5 K (9 °F)
• Supply voltage: 24 VDC
• 4-wire circuit for resistance adjustment

Maximum measured error

The data relating to the measured error are typical values and correspond to a standard deviation of
± 3σ (normal distribution), i.e. 99.8% of all measured values achieve the specified values or better
values. Percentage values refer to the set span. The larger value applies.

Influence of the supply
voltage

2)

Designation

Accuracy

Resistance thermometer RTD

Pt100, Pt1000

0.5 K or 0.15%

Thermocouples TC

K, N
S, B, R

typ. 1.0 K or 0.15 %
typ. 2.0 K or 0.15 %

≤ ±0.01%/V deviation from 24 V 2)

All data is related to a full scale value

Endress+Hauser

3

<!-- page 4 -->

iTEMP TMT80

Long-term drift

≤ 0.1 K/Year 3) or ≤ 0.05%/Year 4)

Influence of ambient
temperature

• Resistance thermometer (RTD):
Td = ± [(15 ppm/K * (Upper range value - Lower range value)) + (50 ppm/K * Set measuring
range)] * Δ T
Example of Pt100 resistance thermometer:
Td = ± [(15 ppm/K * (850 °C + 200 °C)) + (50 ppm/K * 100 °C)] * 10 K = ±0.21 K
Upper range value: 850 °C, Lower range value: –200 °C, Measuring range (4 to 20 mA) configured
= 0 to +100 °C, Temperature deviation Δ T= 10 K
• Thermocouple (TC):
Td = ± [(50 ppm/K * (Upper range value - Lower range value)) + (50 ppm/K * Set measuring
range)] * Δ T
Δ T = Deviation in ambient temperature from reference operating condition (+25 °C (+77 °F) ±
5 K (9 °F)).

Influence of load

≤ ±0.02%/100 Ω 5)

Comparison point

Pt100, as per DIN IEC 60751 Class B (internal cold junction for thermocouples TC)

Installation
Mounting location

A

B

C

A0008035

A
B
C

Orientation

Terminal head in accordance with DIN EN 43 729 flat face, direct installation on insert with cable entry
(center hole 7 mm (0.28 in))
Separate from process in field housing
With clip on DIN rail as per IEC 60715 (TH35)

No restrictions

Environment
Ambient temperature range

3)
4)
5)

4

–40 to +85 °C (–40 to +185 °F)

Under reference operating conditions
% is related to the set span. The larger value is valid.
Under reference operating conditions

Endress+Hauser

<!-- page 5 -->

iTEMP TMT80

Storage temperature

–40 to +100 °C (–40 to +212 °F)

Humidity

• Condensation as per IEC 60 068-2-33:
• Max. rel. humidity: 95% as per IEC 60068-2-30

Climate class

As per IEC 60 654-1, Class C

Degree of protection

IP 00. Depends on the terminal head or field housing when installed.

Shock and vibration
resistance

4 g / 2 to 150 Hz as per IEC 60 068-2-6

Electromagnetic
compatibility (EMC)

CE compliance
Electromagnetic compatibility in accordance with all the relevant requirements of the IEC/EN 61326
series and NAMUR Recommendation EMC (NE21). For details, refer to the Declaration of
Conformity.
Maximum measured error <1% of measuring range.
Interference immunity as per IEC/EN 61326 series, industrial requirements
Interference emission as per IEC/EN 61326 series, Class B equipment

Mechanical construction
Design, dimensions

22.8 (0.9)

Æ44 (1.73)

33 (1.3)

Æ7

(0.28)

Æ5 (0.2)

A0013537

2

Dimensions of the head transmitter in mm (in)

Weight

Approx. 40 g (1.41 oz)

Materials

• Housing: Polycarbonate (PC), complies with UL94 HB flammability standard (HB: Horizontal
Burning Test). Terminals: nickel-plated brass and gold-plated or tin-plated contacts.
• Potting: WEVO PU 403 FP/FL, approved in accordance with UL94 V0 flammability standard (V0:
Vertical Burning Test)

Terminals

Screw terminals, wires up to max. 1.75 mm2 (15 AWG) (secure screws) or 1.5 mm2 (16 AWG) with
wire end ferrules

Endress+Hauser

5

<!-- page 6 -->

iTEMP TMT80

Operability
Remote operation

Configuration using PC operating program ReadWin 2000
Menu

Configurable parameters

Standard settings

• Options for sensor type
• Connection type (2-, 3- or 4-wire connection)
• Options for measuring unit: °C, °F
• Measuring range limits (dependent on sensor type selected)
• Compensation of wire resistance (0 to 20 Ω for RTD 2-wire circuit)
• Failsafe mode: ≤ 3.6 mA or ≥21.0 mA;
(if setting ≥ 21.0 mA, an output current of ≥21.5 mA is guaranteed)
• Zero point, offset: –9.9 to +9.9 K

Certificates and approvals
Current certificates and approvals for the product are available via the Product Configurator at
www.endress.com.
1.

Select the product using the filters and search field.

2.

Open the product page.

The Configuration button opens the Product Configurator.

Accessories
Device-specific accessories

• Mounting kit for head transmitter (4 screws, 6 springs, 10 fuses)
Order code: 51001112
• Adapter for DIN rail mounting, DIN rail clip according to IEC 60715
Order code.: 71528231
• Field housing TAF10 for Endress+Hauser head transmitter, aluminum, IP 66
Order code: TAF10

Communication-specific
accessories

• FXA291 Commubox: PC interface cable, USB, with 4-pin plug;
Order code: 51516983
• TXU10-AA: ReadWin 2000 setup program and PC interface cable, USB, with 4-pin plug;
Order code: TXU10-...
ReadWin 2000 can also be downloaded directly from the Internet for free at the following address:
www.endress.com/readwin

Service-specific accessories
Accessories

Description

Applicator

Software for selecting and sizing Endress+Hauser measuring devices:
• Calculation of all the necessary data for identifying the optimum measuring
device: e.g. pressure loss, accuracy or process connections.
• Graphic illustration of the calculation results
Administration, documentation and access to all project-related data and
parameters over the entire life cycle of a project.
Applicator is available:
• Via the Internet: https://portal.endress.com/webapp/applicator
• On CD-ROM for local PC installation.

6

Endress+Hauser

<!-- page 7 -->

iTEMP TMT80

Configurator

Product Configurator - the tool for individual product configuration
• Up-to-the-minute configuration data
• Depending on the device: Direct input of measuring point-specific information
such as measuring range or operating language
• Automatic verification of exclusion criteria
• Automatic creation of the order code and its breakdown in PDF or Excel output
format
• Ability to order directly in the Endress+Hauser Online Shop
The Configurator is available on the Endress+Hauser website: www.endress.com ->
Click "Corporate" -> Select country -> Click "Products" -> Select the product using the
filters and search field -> Open product page -> The "Configure" button to the right
of the product image opens the Product Configurator.

W@M

Life cycle management for your plant
W@M supports with a wide range of software applications over the entire process:
from planning and procurement, to the installation, commissioning and operation
of the measuring devices. All the relevant device information, such as the device
status, spare parts and device-specific documentation, is available for every device
over the entire life cycle.
The application already contains the data of your Endress+Hauser device. Endress
+Hauser also takes care of maintaining and updating the data records.
W@M is available:
• Via the Internet: www.endress.com/lifecyclemanagement
• On CD-ROM for local PC installation.

Supplementary documentation
Operating Instructions iTEMP TMT80 (BA00292R)

Endress+Hauser

7

<!-- page 8 -->

*71551073*
71551073

www.addresses.endress.com

<!-- page 9 -->

Mouser Electronics
Authorized Distributor

Click to View Pricing, Inventory, Delivery & Lifecycle Information:

Endress+Hauser:
TMT80-AA
