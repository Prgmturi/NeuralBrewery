---
id: pt100-itherm-tm411
product: Endress+Hauser iTHERM TM411
component: Sonda di temperatura PT100 igienica
tags: TT1, TT2, TT3, TT5a, TT5b
---

<!-- page 1 -->

TI01038T/09/EN/10.25-00
71721393
2025-10-10

Products

Solutions

Services

Technical Information
iTHERM ModuLine TM411
Metric RTD thermometer with or without
thermowell for hygienic applications

Easy-to-use metric version with outstanding
sensor
technology
Applications
• Specially designed for use in hygienic and aseptic applications in the Food &
Beverages and Life Sciences industries
• Measuring range: –200 to +600 °C (–328 to +1 112 °F)
• Pressure range up to 50 bar (725 psi)
• Protection class: up to IP69K
Head transmitters
All Endress+Hauser iTEMP transmitters are available with enhanced measurement
accuracy and reliability compared to directly wired sensors. Outputs and
communication protocol:
• Analog output 4 to 20 mA, HART, HART SIL, optional
• PROFIBUS PA, FOUNDATION Fieldbus
• PROFINET over Ethernet-APL
• IO-Link
Your benefits
• Optimum process control: fast response times with iTHERM QuickSens technology
(t90s: 1.5 s)
• Recalibrations up to 75% faster and more reliable with iTHERM QuickNeck. Quick
fastener for fast, tool-free removal of the insert
• High sensor availability under harsh conditions:
Vibration-resistant RTD technology iTHERM StrongSens (> 60g)
• Easy product selection, configuration and maintenance
• Increase productivity and product safety in hygienic applications with highly
accurate and reliable measurement
• Thermowells, hygienic process connections and housing, professionally produced,
made of high-quality materials with low surface roughness

<!-- page 2 -->

iTHERM ModuLine TM411

Table of contents
Function and system design . . . . . . . . . . . . . . . . . . . 3

Notes on selecting the right device . . . . . . . . . . . . . . . . . .
Measuring principle . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Measuring system . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Equipment architecture . . . . . . . . . . . . . . . . . . . . . . . . .

3
4
5
6

Input . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7

Measured variable . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
Measuring range . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7

Output . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

7

Power supply . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

8

Output signal . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
Family of temperature transmitters . . . . . . . . . . . . . . . . . 7

Wiring diagram for RTD . . . . . . . . . . . . . . . . . . . . . . . . . 8
Overvoltage protection . . . . . . . . . . . . . . . . . . . . . . . . . 15

Performance characteristics . . . . . . . . . . . . . . . . . . 15

Reference operating conditions . . . . . . . . . . . . . . . . . . .
Maximum measurement error . . . . . . . . . . . . . . . . . . . .
Influence of ambient temperature . . . . . . . . . . . . . . . . .
Self-heating . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Response time . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Calibration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Insulation resistance . . . . . . . . . . . . . . . . . . . . . . . . . .

15
16
16
17
17
18
19

Certificates and approvals . . . . . . . . . . . . . . . . . . .

Materials in contact with food/product (FCM) . . . . . . . . .
CRN approval . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Surface purity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Material resistance . . . . . . . . . . . . . . . . . . . . . . . . . . .

52

52
53
53
53

Ordering information . . . . . . . . . . . . . . . . . . . . . . . 53
Accessories . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53

Device-specific accessories . . . . . . . . . . . . . . . . . . . . . .
Service-specific accessories . . . . . . . . . . . . . . . . . . . . . .
Communication-specific accessories . . . . . . . . . . . . . . . .
Online tools . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
System components . . . . . . . . . . . . . . . . . . . . . . . . . . .

54
56
57
57
57

Documentation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 58

Brief Operating Instructions (KA) . . . . . . . . . . . . . . . . . .
Operating Instructions (BA) . . . . . . . . . . . . . . . . . . . . .
Safety Instructions (XA) . . . . . . . . . . . . . . . . . . . . . . . .
Functional Safety Manual (FY) . . . . . . . . . . . . . . . . . . . .

58
58
58
58

Installation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

Orientation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Installation instructions . . . . . . . . . . . . . . . . . . . . . . . .

19
19

Environment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

Ambient temperature range . . . . . . . . . . . . . . . . . . . . .
Storage temperature . . . . . . . . . . . . . . . . . . . . . . . . . .
Relative humidity . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Climate class . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Degree of protection . . . . . . . . . . . . . . . . . . . . . . . . . .
Shock and vibration resistance . . . . . . . . . . . . . . . . . . . .
Electromagnetic compatibility (EMC) . . . . . . . . . . . . . . .

23
23
23
23
23
23
23

Process . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

Process temperature range . . . . . . . . . . . . . . . . . . . . . .
Thermal shock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Process pressure range . . . . . . . . . . . . . . . . . . . . . . . . .
State of aggregation of the medium . . . . . . . . . . . . . . . .

23
23
23
24

Mechanical construction . . . . . . . . . . . . . . . . . . . .

24

Design, dimensions . . . . . . . . . . . . . . . . . . . . . . . . . . .
Insert . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Weight . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Materials . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Surface roughness . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Terminal heads . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Extension neck . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
Thermowell . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2

24
36
36
36
37
37
40
42

Endress+Hauser

<!-- page 3 -->

iTHERM ModuLine TM411

Function and system design
Notes on selecting the right
device

iTHERM ModuLine, hygienic
This device is part of the product line of modular thermometers for hygienic and aseptic applications.
Differentiating factors when selecting a suitable thermometer
iTHERM ModuLine TM4x1

iTHERM ModuLine TM4x2

Metric version

Imperial version

↓

↓

TM41x characterizes the device that uses cutting-edge technology, with features such as a replaceable insert,
quick-fastening extension neck (iTHERM QuickNeck), vibration-resistant and fast-response sensor technology
iTHERM StrongSens and QuickSens) and approval for use in hazardous areas
iTHERM ModuLine TM411

iTHERM ModuLine TM412

mm

inch
A0018691

A0018239

↓

↓

TM40x characterizes the device that uses basic technology, with features such as a fixed, non-replaceable
insert, application in non-hazardous areas, standard extension neck, low-cost unit
iTHERM ModuLine TM401

iTHERM ModuLine TM402

inch

mm
A0018692

Endress+Hauser

A0018693

3

<!-- page 4 -->

iTHERM ModuLine TM411

Measuring principle

Resistance thermometers (RTD)
These resistance thermometers use a Pt100 element as the temperature sensor according to
IEC 60751. The temperature sensor is a temperature-sensitive platinum resistor with a resistance of
100 Ω at 0 °C (32 °F) and a temperature coefficient α = 0.003851 °C-1.
There are two different versions of platinum resistance thermometers:
• Wire-wound (WW):WW In these thermometers, a double coil of fine, high-purity platinum wire
is accommodated in a ceramic support. This carrier is then sealed top and bottom with a ceramic
protective layer. These resistance thermometers not only facilitate very reproducible
measurements but also offer good long-term stability of the resistance/temperature characteristic
within temperature ranges up to 600 °C (1 112 °F). This type of sensor is relatively large in size and
is comparatively sensitive to vibrations.
• Thin-film platinum resistance thermometers(TF): A very thin, ultrapure platinum layer, approx.
1 μm thick, is vaporized in a vacuum on a ceramic substrate and then structured
photolithographically. The platinum conductor paths formed in this way create the measuring
resistance. Additional covering and passivation layers are applied and reliably protect the thin
platinum layer from contamination and oxidation, even at high temperatures.
The primary advantages of thin-film temperature sensors over wire-wound versions are their smaller
sizes and better vibration resistance. It should be noted that, due to the operating principle of TF
sensors, they frequently exhibit a relatively slight deviation in their resistance/temperature
characteristic from the standard characteristic defined in IEC 60751 at higher temperatures. As a
result, the tight limit values of tolerance class A as per IEC 60751 can only be observed with TF
sensors at temperatures up to approx. 300 °C (572 °F).
Thermocouples (TC)
Thermocouples are comparatively simple, robust temperature sensors which use the Seebeck effect
for temperature measurement: if two electrical conductors made of different materials are connected
at a point, a weak electrical voltage can be measured between the two open conductor ends if the
conductors are subjected to a thermal gradient. This voltage is called thermoelectric voltage or
electromotive force (emf). Its magnitude depends on the type of conducting materials and the
temperature difference between the "measuring point" (the junction of the two conductors) and the
"cold junction" (the open conductor ends). Accordingly, thermocouples primarily only measure
differences in temperature. The absolute temperature at the measuring point can be determined
from these if the associated temperature at the cold junction is known or is measured separately and
compensated for. The material combinations and associated thermoelectric voltage/temperature
characteristics of the most common types of thermocouple are standardized in the IEC 60584 and
ASTM E230/ANSI MC96.1 standards.

4

Endress+Hauser

<!-- page 5 -->

iTHERM ModuLine TM411

Measuring system

Endress+Hauser offers a complete portfolio of optimized components for the temperature measuring
point – everything you need for the seamless integration of the measuring point into the overall
facility. This includes:
• Power supply unit/barrier
• Display units
• Overvoltage protection
For more information, see the brochure "System Components - Solutions for a Complete
Measuring Point" (FA00016K)

1

2

3

4

5
A0047137

1
1
2

3

4
5

Endress+Hauser

Example of application, measuring point layout with additional Endress+Hauser components
Installed iTHERM compact thermometer with HART communication protocol
Process indicator from the RIA product range: The process indicator is looped into the current loop and
displays the measuring signal or the HART process variables in digital form. The process indicator does not
require an external power supply. It is powered directly from the current loop.
RN series active barrier - The active barrier (17.5 VDC, 20 mA) has a galvanically isolated output for supplying
voltage to 2-wire transmitters. The universal power supply works with an input supply voltage of 24 to 230 V
AC/DC, 0/50/60 Hz, which means that it can be used in all international power grids.
Communication examples: HART Communicator (handheld device), FieldXpert, Commubox FXA195 for
intrinsically safe HART communication with FieldCare via a USB port.
FieldCare is an FDT-based plant asset management tool from Endress+Hauser; for more details, see
'Accessories' section.

5

<!-- page 6 -->

iTHERM ModuLine TM411

Equipment architecture
Design

Options
1: Terminal
head →  37

• 316L, low head, optionally with display window
• Aluminum, high or low head, with or without display window
• Polypropylene, low head
• Polyamide, high head, without display window
benefits:
 Your
• Optimum terminal access thanks to low housing edge of bottom
section:
• Easier to use
• Lower installation and maintenance costs
• Optional display: local process display for added reliability
• IP69K protection: optimum protection even with high-pressure
cleaning

1
2

2: Wiring,
electrical
connection,
output signal
→ 7

• Ceramic terminal block
• Flying leads
• Head transmitter (4 to 20 mA, HART, PROFIBUS PA, FOUNDATION
Fieldbus, IO-Link), single-channel or two-channel, PROFINET over
Ethernet-APL
• Attachable display (optional)

3: Plug or cable
gland

• Polyamide or brass cable glands
• M12 plug, 4-pin/8-pin: PROFIBUS PA, Ethernet-APL, IO-Link
• 7/8" plug: PROFIBUS PA, FOUNDATION™ Fieldbus

4: Extension
neck →  40

Welded-in-place or removable either with the quick fastener (iTHERM
QuickNeck) or thread adapter nut G3/8"

3
4

benefits at a glance:
 Your
• iTHERM QuickNeck: tool-free removal of the insert:
• Saves time/costs on frequently calibrated measuring points
• Wiring mistakes avoided
• IP69K protection: safety under extreme process conditions

5
7

5: Process
connection
→  42

U

6

7a

7b

A0017758

6

More than 50 different versions.

6: Thermowell
→  42

• Versions with and without thermowell (insert in direct contact with
process).
• Various diameters
• Various tip shapes (straight or reduced)

7: Insert
→  36 with:
7a: iTHERM
QuickSens
7b: iTHERM
StrongSens

Sensor models: wire wound (WW) or thin-film sensor (TF).
benefits at a glance:
 Your
• iTHERM QuickSens - insert with the world's fastest response
time:
• Insert: ⌀3 mm (¹⁄₈ in) or ⌀6 mm (¹⁄₄ in)
• Fast, highly accurate measurements, delivering maximum
process safety and control
• Quality and cost optimization
• Minimization of necessary immersion length: better product
protection thanks to improved process flow
• iTHERM StrongSens - insert with unbeatable durability:
• Vibration resistance > 60g: lower life cycle costs thanks to
longer operating life and high plant availability
• Automated, traceable production: top quality and maximum
process safety
• High long-term stability: reliable measured values and high
level of system safety

Endress+Hauser

<!-- page 7 -->

iTHERM ModuLine TM411

Input
Measured variable

Temperature (temperature-linear transmission behavior)

Measuring range

Depends on the type of sensor used
Sensor type

Measuring range

Pt100 thin-film

–50 to +400 °C (–58 to +752 °F)

Pt100 thin-film, iTHERM
StrongSens, vibrationresistant > 60g

–50 to +500 °C (–58 to +932 °F)

Pt100 thin-film, iTHERM
QuickSens, fast-response

–50 to +200 °C (–58 to +392 °F)

Pt100 wire wound, extended
measuring range

–200 to +600 °C (–328 to +1 112 °F)

Output
Output signal

Generally, the measured value can be transmitted in one of two ways:
• Directly-wired sensors - sensor measured values forwarded without transmitter.
• Via all common protocols by selecting an appropriate Endress+Hauser iTEMP temperature
transmitter. All the transmitters listed below are mounted directly in the terminal head and wired
with the sensory mechanism.

Family of temperature
transmitters

Thermometers fitted with iTEMP transmitters are an installation-ready complete solution to
improve temperature measurement by significantly increasing measurement accuracy and reliability,
when compared to direct wired sensors, as well as reducing both wiring and maintenance costs.
4-20 mA head transmitter
They offer a high degree of flexibility, thereby supporting universal application with low inventory
storage. The iTEMP transmitters can be configured quickly and easily at a PC. Endress+Hauser offers
free configuration software which can be downloaded from the Endress+Hauser website.
HART head transmitter
The iTEMP transmitter is a 2-wire device with one or two measuring inputs and one analog output.
The device not only transfers converted signals from resistance thermometers and thermocouples, it
also transfers resistance and voltage signals using HART communication. Swift and easy operation,
visualization and maintenance using universal configuration software like FieldCare, DeviceCare or
FieldCommunicator 375/475. Integrated Bluetooth® interface for the wireless display of measured
values and configuration via Endress +Hauser SmartBlue app, optional.
PROFIBUS PA head transmitter
Universally programmable iTEMP head transmitter with PROFIBUS PA communication. Conversion
of various input signals into digital output signals. High measurement accuracy over the complete
operating temperature range. PROFIBUS PA functions and device-specific parameters are configured
via fieldbus communication.
FOUNDATION Fieldbus™ head transmitters
Universally programmable iTEMP head transmitter with FOUNDATION Fieldbus™ communication.
Conversion of various input signals into digital output signals. High measurement accuracy over the
complete operating temperature range. All iTEMP transmitters are approved for use in all the main
process control systems. The integration tests are performed in Endress+Hauser's 'System World'.
Head transmitter with PROFINET and Ethernet-APL™
The iTEMP transmitter is a 2-wire device with two measuring inputs. The device not only transfers
converted signals from resistance thermometers and thermocouples, it also transfers resistance and
voltage signals using the PROFINET protocol. Power is supplied via the 2-wire Ethernet connection
according to IEEE 802.3cg 10Base-T1. The iTEMP transmitter can be installed as an intrinsically safe
electrical apparatus in Zone 1 hazardous areas. The device can be used for instrumentation purposes
in the terminal head form B (flat face) according to DIN EN 50446.

Endress+Hauser

7

<!-- page 8 -->

iTHERM ModuLine TM411

Head transmitter with IO-Link
The iTEMP transmitter is an IO-Link device with a measurement input and an IO-Link interface. It
offers a configurable, simple and cost-effective solution thanks to digital communication via IO-Link.
The device is mounted in a terminal head form B (flat face) as per DIN EN 5044.
Advantages of the iTEMP transmitters:
• Dual or single sensor input (optionally for certain transmitters)
• Attachable display (optionally for certain transmitters)
• Unsurpassed reliability, accuracy and long-term stability in critical processes
• Mathematical functions
• Monitoring of the thermometer drift, sensor backup functionality, sensor diagnostic functions
• Sensor-transmitter-matching based on the Callendar van Dusen coefficients (CvD).

Power supply
• According to the 3-A Sanitary Standard and EHEDG, electrical connecting cables must be
smooth, corrosion-resistant and easy to clean.
• Grounding or shield connections are possible via special ground terminals on the terminal
head. →  37
Wiring diagram for RTD

Type of sensor connection

2

1
6

RD

+

5

RD

1+

+

-2-

4

WH

3

WH

3
A0045464

2
1
2
3

Head-mounted iTEMP TMT7x transmitter or TMT31 (single sensor input)
Sensor input, RTD and Ω: 4-, 3- and 2-wire
Power supply or fieldbus connection
Display connection/CDI interface

2

1

3

BK
RD

7

BK

RD
1

+

-2

WH
YE

WH
4
A0045466

3
1
2
3
4

8

Head-mounted iTEMP TMT8x transmitter (dual sensor input)
Sensor input 1, RTD: 4- and 3-wire
Sensor input 2, RTD: 3-wire
Power supply or fieldbus connection
Display connection

Endress+Hauser

<!-- page 9 -->

iTHERM ModuLine TM411

1
R1

RD

R3

RD

R3

R1

3

2
R2
R1

BK

RD

B6

BK

G4
B5

WH

W5

R2

RD

B5

W3

B6

W5

R1

W3

WH

G4

R3

RD

R1

R3

R1

RD

W6

W4 W4

WH

W6

WH

YE

4
A0045453

4
1
2
3
4

Terminal block mounted
3-wire single
2 x 3-wire single
4-wire single
Outside screw

C/Q

1
RD

6

L+

RD

5

WH

4

WH

L3

2
A0052495

5

Head-mounted iTEMP TMT36 transmitter (single sensor input)

1
RTD sensor input: 4-, 3- and 2-wire
2
Display connection
L+ 18 to 30 VDC power supply
L- 0 VDC power supply
C/Q IO-Link or switch output

Terminals
iTEMP head transmitters fitted with push-in terminals unless screw terminals are explicitly selected
or a double sensor is installed.
Cable entries
The cable entries must be selected during configuration of the device. Different terminal heads offer
different options in terms of the thread and number of available cable entries.
Device plugs
The manufacturer offers a wide variety of device plugs for the simple and fast integration of the
thermometer into a process control system. The following tables show the PIN assignments of the
various plug connector combinations.
The manufacturer advises against connecting thermocouples directly to connectors. The direct
connection to the pins of the plug might generate a new "thermocouple" which influences the
accuracy of the measurement. The thermocouples are connected in combination with a iTEMP
transmitter.
Abbreviations

Endress+Hauser

#1

Order: first transmitter/insert

#2

Order: second
transmitter/insert

i

Insulated. Wires marked 'i' are not connected and are
insulated with heat shrink tubes.

YE

Yellow

9

<!-- page 10 -->

iTHERM ModuLine TM411

GND

Grounded. Wires marked 'GND' are connected to the
internal grounding screw in the terminal head.

RD

Red

BN

Brown

WH

White

GNYE

Green-yellow

PK

Pink

BU

Blue

GN

Green

GY

Gray

BK

Black

Terminal head with a cable entry 1)
Plug

1x PROFIBUS PA

Plug thread
PIN number

M12
1

2

1x FOUNDATION™ Fieldbus
(FF)

1x PROFINET and EthernetAPL™

7/8"

M12

7/8"
3

4

1

2

3

4

1

2

3

4

1

2

3

4

Electrical connection (terminal head)
Flying leads and TC
3-wire terminal block
(1x Pt100)
4-wire terminal block
(1x Pt100)
6-wire terminal block
(2x Pt100)
1x TMT 4 to 20 mA
or HART®
2x TMT 4 to 20 mA
or HART® in the
terminal head with a
high cover
1x TMT PROFIBUS®
PA
2x TMT PROFIBUS®
PA

Not connected (not insulated)
WH
RD

RD
(#1) 2

RD

WH

)

RD
(#1)

+

i

+(#1) +(#2)

+

WH
WH

RD

WH

WH (#1)

RD
(#1)

RD
(#1)

-

i

+

i

-(#1)

(#2)

i

GND

+(#1) +(#2)

+

-(#1)

WH

RD

RD

WH

WH (#1)

RD
(#1)

RD
(#1)

-

i

+

i

-(#1)

(#2)

i

3)

+(#1)

RD

WH

GND

WH (#1)

-

i

-(#1)

-(#2)

Cannot be combined

-

1x TMT FF

-

+

2x TMT FF

-(#1)

+(#1)

GND

i

Cannot be combined
Cannot be combined

2x TMT PROFINET®

PIN position and color
code

4

3

1

2

1 BN
2 GNYE
3 BU
4 GY
A0018929

1)
2)
3)

10

1

3

2

4

1 BN
2 GNYE
3 BU
4 GY
A0018930

Cannot be combined
Ether Ether
netnetAPL
APL
signal signal
+

1x TMT PROFINET®
Cannot be combined

Cannot be
combined

Cannot be
combined

Cannot be combined
+(#1) +(#2)

3)

+

Cannot be
combined

WH

1

3

2

4

GND

Ether
Ether
netnetAPL
APL
signal
signal
+
- (#1)
(#1)

1 BU
2 BN
3 GY
4 GNYE
A0018931

4

3

1

2

-

1 RD
2 GN

A0052119

Options depend on product and configuration
Second Pt100 is not connected
If a head is used without grounding screw, e.g. plastic housing TA30S or TA30P, insulated 'i' instead of grounded GND

Endress+Hauser

<!-- page 11 -->

iTHERM ModuLine TM411

Terminal head with a cable entry 1)
Plug

4-pin/8-pin

Plug thread

M12

PIN number

1

2

3

4

5

6

7

8

Electrical connection (terminal head)
Flying leads and TC

Not connected (not insulated)

3-wire terminal block (1x Pt100)
4-wire terminal block (1x Pt100)

WH
RD

WH

RD

6-wire terminal block (2x Pt100)

i

WH
WH

BK

BK

YE

1x TMT 4 to 20 mA or HART®
2x TMT 4 to 20 mA or HART® in the
terminal head with a high cover

i
+(#1)

i

-(#1)

1x TMT PROFIBUS® PA

i

+(#2)

i

-(#2)

i

Cannot be combined

2x TMT PROFIBUS® PA
1x TMT FF

Cannot be combined

2x TMT FF
1x TMT PROFINET®

Cannot be combined

2x TMT PROFINET®

Cannot be combined
4

3

PIN position and color code
1

2

2 BN

3 GN

1 BN
2 GNYE
3 BU
4 GY

1 WH
8 RD
7 BU

4 YE
5 GY
6 PK

A0018929

A0018927

1)

Options depend on product and configuration

Terminal head with one cable entry
Plug

1x IO-Link, 4-pin

Plug thread

M12

PIN number

1

2

3

4

Electrical connection (terminal head)
Flying leads
3-wire terminal block (1x Pt100)

Not connected (not insulated)
RD

i

4-wire terminal block (1x Pt100)

RD

WH

Cannot be combined

6-wire terminal block (2x Pt100)
1x TMT 4 to 20 mA or HART
Cannot be combined

2x TMT 4 to 20 mA or HART in the terminal head with a high
cover
1x TMT PROFIBUS PA

Cannot be combined

2x TMT PROFIBUS PA
1x TMT FF

Cannot be combined

2x TMT FF
1x TMT PROFINET

Cannot be combined

2x TMT PROFINET
1x TMT IO-Link

Endress+Hauser

L+

-

L-

C/Q

11

<!-- page 12 -->

iTHERM ModuLine TM411

Plug

1x IO-Link, 4-pin

2x TMT IO-Link

L+ (#1)

-

L- (#1)
4

3

1

2

C/Q

1 BN
3 BU
4 BK

PIN position and color code

A0055383

Terminal head with two cable entries 1)
Plug

2x PROFIBUS PA

2x FOUNDATION™
Fieldbus (FF)

2x PROFINET and
Ethernet-APL™

7/8"(#1)/7/8"(#2)

M12 (#1)/M12 (#2)

Plug thread
M12(#1) / M12(#2)

#1

7/8"(#1)/7/8"(#2)

#2
A0021706

PIN number

1

2

3

4

1

2

3

4

1

2

3

4

1

2

3

4

Electrical connection (terminal head)
Flying leads and TC
3-wire terminal block (1x
Pt100)
4-wire terminal block (1x
Pt100)

Not connected (not insulated)
WH/i
RD/i

RD/i

WH/i
RD/i

RD/i

WH/i WH/i

WH/i
RD/i

RD/i

WH/i WH/i

WH/i WH/i

6-wire terminal block (2x
Pt100)

RD/B RD/B
K
K

WH/YE

RD/B RD/B
K
K

WH/YE

RD/B RD/B
K
K

WH/YE

1x TMT 4 to 20 mA or
HART®

+/i

-/i

+/i

-/i

+/i

-/i

+
2x TMT 4 to 20 mA or
(#1)/
HART® in the terminal head
+
with a high cover
(#2)

(#1)/
-(#2)

+
(#1)/
+
(#2)

(#1)/
-(#2)

i/i

i/i

1x TMT PROFIBUS® PA

+/i

-/i

2x TMT PROFIBUS® PA

+
(#1)/
+
(#2)

+
GND/
(#1)/
GND
(#1)/
+
-(#2)
(#2)

+/i

i/i

1x TMT PROFINET®

12

+
(#1)/
+
(#2)

Cannot be combined

i/i

(#1)/
-(#2)

GND/
(#1)/ GND
-(#2)

-/i
i/i

+
(#1)/
+(#2)

(#1)/
-(#2)

i/i

Cannot be combined

-/i
Cannot be combined

i/i

+/i

WH/i

-/i

1x TMT FF

2x TMT FF

i/i

Cannot be
combined

Cannot be combined

Cannot be combined

+/i

+
(#1)/
(#1)/
+
-(#2)
(#2)

i/i

GND/
GND

Cannot be combined

Cannot be combined

Ether Ether
netnetAPL
APL
signal signa
l+

GND

i

Endress+Hauser

<!-- page 13 -->

iTHERM ModuLine TM411

Plug

2x FOUNDATION™
Fieldbus (FF)

2x PROFIBUS PA

2x TMT PROFINET®

Cannot be combined

4

3

1

2

PIN position and color code

Cannot be combined

1 BN
2 GNYE
3 BU
4 GY

1

3

2

4

1)

Ether
Ether
netnetAPL
APL
signa
signal
l+
- (#1)
(#1)
and
and
(#2)
(#2)

Cannot be combined

1 BN
2 GNYE
3 BU
4 GY

A0018929

2x PROFINET and
Ethernet-APL™

1

3

2

4

A0018930

1 BU
2 BN
3 GY
4 GNYE

4

3

1

2

1 RD
2 GN

A0018931

A0052119

Options depend on product and configuration

Terminal head with two cable entries 1)
Plug

4-pin/8-pin

Plug thread
M12 (#1)/M12 (#2)

#1

#2
A0021706

PIN number

1

2

3

4

5

6

7

8

Electrical connection (terminal head)
Flying leads and TC
3-wire terminal block (1x
Pt100)
4-wire terminal block (1x
Pt100)

Not connected (not insulated)
WH/i
RD/i

RD/i
WH/i

6-wire terminal block (2x
Pt100)

RD/BK

1x TMT 4 to 20 mA or
HART®

+/i

2x TMT 4 to 20 mA or
HART® in the terminal head
with a high cover

+(#1)/ +(#2)

RD/BK

WH/i
WH/YE

i/i

-/i
i/i

i/i
-(#1)/-(#2)

1x TMT PROFIBUS® PA

Cannot be combined

2x TMT PROFIBUS® PA
1x TMT FF

Cannot be combined

2x TMT FF
1x TMT PROFINET®

Cannot be combined

2x TMT PROFINET®

Cannot be combined
4

3

PIN position and color code
1

2

3 GN

1 BN
2 GNYE
3 BU
4 GY

2 BN
1 WH
8 RD
7 BU

4 YE
5 GY
A0018929

6 PK
A0018927

1)

Options depend on product and configuration

Endress+Hauser

13

<!-- page 14 -->

iTHERM ModuLine TM411

Terminal head with two cable entries
Plug

2x IO-Link, 4-pin

Plug thread

M12(#1)/M12 (#2)

PIN number

1

2

3

4

Electrical connection (terminal head)
Flying leads

Not connected (not insulated)

3-wire terminal block (1x Pt100)

RD

i

4-wire terminal block (1x Pt100)
6-wire terminal block (2x Pt100)

RD

WH

Cannot be combined
RD/BK

i

RD/BK

WH/YE

1x TMT 4 to 20 mA or HART
Cannot be combined

2x TMT 4 to 20 mA or HART in the terminal head with a
high cover
1x TMT PROFIBUS PA

Cannot be combined

2x TMT PROFIBUS PA
1x TMT FF

Cannot be combined

2x TMT FF
1x TMT PROFINET

Cannot be combined

2x TMT PROFINET
1x TMT IO-Link

L+

-

L-

C/Q

2x TMT IO-Link

L+ (#1) and (#2)

-

L- (#1) and (#2)

C/Q

4

3

1

2

PIN position and color code

1 BN
3 BU
4 BK
A0055383

Connection combination: insert - transmitter 1)
Transmitter connection 2)
Insert

iTEMP TMT31/iTEMP TMT7x

iTEMP TMT8x

1x 1-channel

2x 1-channel

1x 2-channel

2x 2-channel

1x sensor (Pt100 or TC), flying
leads

Sensor (#1) : transmitter
(#1)

Sensor (#1) : transmitter
(#1)
(Transmitter (#2) not
connected)

Sensor (#1) : transmitter
(#1)

Sensor (#1) : transmitter (#1)
Transmitter (#2) not
connected

2x sensor (2x Pt100 or 2x TC),
flying leads

Sensor (#1) : transmitter
(#1)
Sensor (#2) insulated

Sensor (#1) : transmitter
(#1)
Sensor (#2): transmitter
(#2)

Sensor (#1) : transmitter
(#1)
Sensor (#2): transmitter
(#1)

Sensor (#1) : transmitter (#1)
Sensor (#2): transmitter (#1)
(Transmitter (#2) not
connected)

1x sensor (Pt100 or TC),with
terminal block 3)

Sensor (#1) : transmitter
in cover

Cannot be combined

Sensor (#1) : transmitter
in cover

Cannot be combined

14

Endress+Hauser

<!-- page 15 -->

iTHERM ModuLine TM411

Transmitter connection 2)
Insert

iTEMP TMT31/iTEMP TMT7x
1x 1-channel

2x sensor (2x Pt100 or 2x TC)
with terminal block

2x sensors (2x Pt100 or 2x TC)
in conjunction with feature
600, option MG 4)
1)
2)

3)
4)

2x 1-channel

Sensor (#1) : transmitter
in cover
Sensor (#2) not
connected

Cannot be combined

iTEMP TMT8x
1x 2-channel

2x 2-channel

Sensor (#1) : transmitter
in cover
Sensor (#2): transmitter
in cover
Sensor (#1) : transmitter
(#1)
Sensor (#2): transmitter
(#2)

Cannot be combined

Sensor (#1): transmitter (#1) channel 1
Sensor (#2): transmitter (#2) channel 1

Options depend on product and configuration
If 2 transmitters are selected in a terminal head, transmitter (#1) is installed directly on the insert. Transmitter (#2) is installed in the high cover.
A TAG cannot be ordered for the second transmitter as standard. The bus address is set to the default value and, if necessary, must be changed
manually before commissioning.
Only in the terminal head with a high cover, only 1 transmitter possible. A ceramic terminal block is automatically fitted on the insert.
Individual sensors each connected to channel 1 of a transmitter

Overvoltage protection

To protect against overvoltage in the power supply and signal/communication cables for the
thermometer electronics, Endress+Hauser offers the HAW562 surge arrester for DIN rail mounting
and the HAW569 for field housing installation.
For more information, see the Technical Information 'HAW562 Surge arrester' TI01012K and
'HAW569 Surge arrester' TI01013K.

Performance characteristics
Reference operating
conditions

Endress+Hauser

This data is relevant for determining the measurement accuracy of the iTEMP transmitters used. See
technical documentation of the specific iTEMP transmitter.

15

<!-- page 16 -->

iTHERM ModuLine TM411

Maximum measurement
error
Class

RTD resistance thermometer according to IEC 60751

Max. tolerances (°C)

Characteristics

RTD maximum sensor error
Cl. A

± (0.15 + 0.002 · |t| 1))

Cl. AA,
previously
1/3 Cl. B

± (0.1 + 0.0017 · |t|) 1)

Cl. B

± (0.3 + 0.005 · |t| 1))

Max. deviation (°C)

3.0

2.5

2.0

B
1.5

1.0

A
AA

0.5

-200

-100

0

100

200

300

400

500

600°C

AA
- 0.5

A

- 1.0

B

- 1.5
- 2.0

- 2.5

- 3.0 Max. deviation (°C)
A0045598

1)

|t| = Temperature absolute value in °C

To obtain the maximum tolerances in °F, multiply the results in °C by a factor of 1.8.
Temperature ranges
Sensor type 1)

Operating
temperature range

Class B

Class A

Class AA

Pt100 (WW)

–200 to +600 °C
(–328 to +1 112 °F)

–200 to +600 °C
(–328 to +1 112 °F)

–100 to +450 °C
(–148 to +842 °F)

–50 to +250 °C
(–58 to +482 °F)

Pt100 (TF)
Basic

–50 to +200 °C
(–58 to +392 °F)

–50 to +200 °C
(–58 to +392 °F)

–30 to +200 °C
(–22 to +392 °F)

-

Pt100 (TF)
Standard

–50 to +400 °C
(–58 to +752 °F)

–50 to +400 °C
(–58 to +752 °F)

–30 to +250 °C
(–22 to +482 °F)

0 to +150 °C
(+32 to +302 °F)

Pt100 (TF)
iTHERM
QuickSens

–50 to +200 °C
(–58 to +392 °F)

–50 to +200 °C
(–58 to +392 °F)

–30 to +200 °C
(–22 to +392 °F)

0 to +150 °C
(+32 to +302 °F)

Pt100 (TF)
iTHERM
StrongSens

–50 to +500 °C
(–58 to +932 °F)

–50 to +500 °C
(–58 to +932 °F)

–30 to +300 °C
(–22 to +572 °F)

0 to +150 °C
(+32 to +302 °F)

1)

Influence of ambient
temperature

16

Options depend on product and configuration

Depends on the head transmitter used. For details, see the Technical Information.

Endress+Hauser

<!-- page 17 -->

iTHERM ModuLine TM411

Self-heating

RTD elements are passive resistors that are measured using an external current. This measurement
current causes a self-heating effect in the RTD element itself which in turn creates an additional
measurement error. In addition to the measurement current, the size of the measurement error is
also affected by the temperature conductivity and flow velocity of the process. This self-heating error
is negligible if an Endress+Hauser iTEMP temperature transmitter (very small measurement current)
is connected.

Response time

Tests have been performed in water at 0.4 m/s (according to IEC 60751) and with a 10 K
temperature change.

Response time with heat transfer paste 1)

Thermowell

⌀6 mm (¹⁄₄ in)

⌀9 mm (0.35 in)

⌀12.7 mm (¹⁄₂ in)

1)

Shape of tip

Insert

1x Pt100
iTHERM
QuickSens,
TF

1x Pt100
iTHERM
StrongSens,
TF

1x Pt100
wire wound
WW

2x Pt100
wire wound
WW

1x Pt100
standard
thin-film TF

t50

t90

t50

t50

t90

t50

t90

t50

t90

8.5 s

26 s

5.5 s

18 s

8s

23 s

15 s

45 s

15 s

45 s

9.5 s

27 s

t90

Reduced 4.3 mm (0.17 in) x
20 mm (0.79 in)

⌀3 mm (¹⁄₈ in)

1s

2.5 s

Straight

⌀6 mm (¹⁄₄ in)

2s

9s

Reduced 5.3 mm (0.21 in) x
20 mm (0.79 in)

⌀3 mm (¹⁄₈ in)

1.25 s

4s

-

7s

20 s

7s

20 s

7s

23 s

Tapered 6.6 mm (0.26 in) x
60 mm (2.36 in)

⌀3 mm (¹⁄₈ in)

2.5 s

12 s

-

14 s

49 s

12 s

40 s

15 s

51 s

Straight

⌀6 mm (¹⁄₄ in)

4s

26 s

23 s

81 s

23 s

81 s

31 s

100 s

Reduced 5.3 mm (0.21 in) x
20 mm (0.79 in)

⌀3 mm (¹⁄₈ in)

1.5 s

5.5 s

9s

27 s

9s

27 s

6.5 s

21 s

Reduced 8 mm (0.31 in) x
32 mm (1.26 in)

⌀6 mm (¹⁄₄ in)

6s

36 s

22 s

69 s

22 s

69 s

26 s

90 s

8s

27 s

12 s

54 s
-

11 s

44 s

If using a thermowell.

Response time without heat transfer paste 1)

Thermowell

Shape of tip

Insert

⌀3 mm (¹⁄₈ in)

1x Pt100
iTHERM
QuickSens,
TF

1x Pt100
iTHERM
StrongSens,
TF

1x Pt100
wire wound
WW

2x Pt100
wire wound
WW

1x Pt100
standard
thin-film TF

t50

t50

t50

t90

t50

t90

t50

t90

1.75 s

5s

2s

6s

2.5 s

5.5 s

4s

10.5 s 4.5 s

12 s

4.75 s

13 s

9s

27 s

7.5 s

24 s

8.5 s

28 s

19 s

62 s

19 s

62 s

13.5 s

42 s

t90
0.75 s

t90
-

Without
thermowell

-

⌀6 mm (¹⁄₄ in)

Reduced 4.3 mm (0.17 in) x
20 mm (0.79 in)

⌀3 mm (¹⁄₈ in)

1s

3s

Straight

⌀6 mm (¹⁄₄ in)

2s

9s

Reduced 5.3 mm (0.21 in) x
20 mm (0.79 in)

⌀3 mm (¹⁄₈ in)

1.5 s

5s

-

7s

21 s

7s

21 s

8s

22 s

Tapered 6.6 mm (0.26 in) x
60 mm (2.36 in)

⌀3 mm (¹⁄₈ in)

5s

23 s

-

13 s

45 s

13 s

45 s

15.5 s

60 s

Straight

⌀6 mm (¹⁄₄ in)

5.5 s

41 s

23 s

82 s

23 s

82 s

32 s

105 s

⌀9 mm (0.35 in)

⌀12.7 mm (¹⁄₂ in)

Endress+Hauser

⌀6 mm (¹⁄₄ in)

0.5 s

1.5 s

2.5 s

16 s
-

8s

12 s

29 s

54 s

17

<!-- page 18 -->

iTHERM ModuLine TM411

Thermowell

1)

Shape of tip

Insert

1x Pt100
iTHERM
QuickSens,
TF

1x Pt100
iTHERM
StrongSens,
TF

1x Pt100
wire wound
WW

2x Pt100
wire wound
WW

1x Pt100
standard
thin-film TF

t50

t90

t50

t50

t90

t50

t90

t50

t90

10 s

30 s

10 s

30 s

8s

30 s

26 s

85 s

26 s

85 s

32 s

108 s

Reduced 5.3 mm (0.21 in) x
20 mm (0.79 in)

⌀3 mm (¹⁄₈ in)

2s

6s

Reduced 8 mm (0.31 in) x
32 mm (1.26 in)

⌀6 mm (¹⁄₄ in)

14.5 s

65 s

t90
-

16 s

53 s

If using a thermowell.

Response time for directly wired insert without transmitter.

Calibration

Calibration of thermometers
Calibration refers to the comparison between the display of a piece of measuring equipment and the
true value of a variable provided by the calibration standard under defined conditions. The aim is to
determine the deviation or measurement errors of the UUT from the true value of the measured
variable. For thermometers, calibration is usually only performed on the inserts. This checks only the
deviation of the sensor element caused by the insert design. However, in most applications, the
deviations caused by the design of the measuring point, integration into the process, the influence of
ambient conditions, and other factors are significantly greater than the deviations related to the
insert. Calibration of inserts is generally carried out using two methods:
• Calibration at fixed points, e.g. at the freezing point of water at 0 °C,
• Calibration compared against a precise reference thermometer.
The thermometer to be calibrated must display either the fixed point temperature or the
temperature of the reference thermometer as accurately as possible. Temperature-controlled
calibration baths with very homogeneous thermal values, or special calibration furnaces are typically
used for thermometer calibrations. The measurement uncertainty may increase due to heat
conduction errors and short immersion lengths. The existing measurement uncertainty is recorded
on the individual calibration certificate. For accredited calibrations in accordance with ISO 17025, a
measurement uncertainty that is twice as high as the accredited measurement uncertainty is not
permitted. If this limit is exceeded, only a factory calibration is possible.
Sensor-transmitter-matching
The resistance/temperature curve of platinum resistance thermometers is standardized but in
practice it is rarely possible to keep to the values precisely over the entire operating temperature
range. For this reason, platinum resistance sensors are divided into tolerance classes, such as Class
A, AA or B as per IEC 60751. These tolerance classes describe the maximum permissible deviation of
the specific sensor characteristic curve from the standard curve, i.e. the maximum temperaturedependent characteristic error that is permitted. The conversion of measured sensor resistance
values to temperatures in temperature transmitters or other meter electronics is often susceptible to
considerable errors as the conversion is generally based on the standard characteristic curve.
When Endress+Hauser iTEMP temperature transmitters are used, this conversion error can be
reduced significantly by sensor-transmitter-matching:
• Calibration at three temperatures at least and determination of the actual temperature sensor
characteristic curve,
• Adjustment of the sensor-specific polynomial function using Calendar-van Dusen (CvD)
coefficients
• Configuration of the temperature transmitter with the sensor-specific CvD coefficients for
resistance/temperature conversion, and
• another calibration of the reconfigured temperature transmitter with connected resistance
thermometer.
Endress+Hauser offers its customers this kind of sensor-transmitter matching as a separate service.
Furthermore, the sensor-specific polynomial coefficients of platinum resistance thermometers are
always provided on every Endress+Hauser calibration certificate where possible, e.g. at least three
calibration points, so that users themselves can also appropriately configure suitable temperature
transmitters.
For the device, Endress+Hauser offers standard calibrations at a reference temperature of
–80 to +600 °C (–112 to +1 112 °F) based on the ITS90 (International Temperature Scale).
Calibrations in other temperature ranges are available from an Endress+Hauser sales center on

18

Endress+Hauser

<!-- page 19 -->

iTHERM ModuLine TM411

request. Calibrations are traceable to national and international standards. The calibration certificate
is referenced to the serial number of the device. Only the insert is calibrated.
Minimum immersion length (IL) for inserts required to perform a correct calibration
Due to the limitations of furnace geometries, the minimum immersion lengths must be
observed at high temperatures to enable a calibration to be performed with an acceptable
degree of measurement uncertainty. The same applies when using a head transmitter. Due to
heat conduction, minimum lengths must be observed in order to guarantee the functionality of
the transmitter –40 to +85 °C (–40 to +185 °F).
Calibration temperature

Minimum immersion length IL in mm without head transmitter

–196 °C (–320.8 °F)

120 mm (4.72 in) 1)

–80 to +250 °C (–112 to +482 °F)

No minimum immersion length required 2)

+251 to +550 °C (+483.8 to +1 022 °F)

300 mm (11.81 in)

+551 to +600 °C (+1 023.8 to +1 112 °F)

400 mm (15.75 in)

1)
2)

Insulation resistance

With iTEMP head transmitter min. 150 mm (5.91 in) is required
at a temperature of +80 to +250 °C (+176 to +482 °F), the iTEMP head transmitter requires min.
50 mm (1.97 in)

Insulation resistance ≥ 100 MΩ at ambient temperature, measured between the terminals and the
outer jacket with a minimum voltage of 100 VDC.

Installation
Orientation

No restrictions once self-draining is guaranteed in the process. If there is an opening to detect leaks
at the process connection, this opening must be at the lowest possible point.

Installation instructions

The immersion length of the thermometer can influence the measurement accuracy. If the
immersion length is too small, then measurement errors are caused by heat conduction via the
process connection and the container wall. For installation in a pipe, an immersion length is
therefore recommended that ideally corresponds to half the pipe diameter.
• Installation options: Pipes, tanks or other plant components
• To minimize the heat conduction error, a minimum immersion length is recommended depending
on the type of sensor used and the design of the insert. This immersion length corresponds to the
minimum insertion length for the calibration.
• ATEX certification: Observe the installation instructions in the Ex documentation.

Endress+Hauser

19

<!-- page 20 -->

iTHERM ModuLine TM411

U

4

3

1
≥ 3°

Dt

dt
2

Lt
≥ 3°

A0008946

6

Installation examples

1, 2 Perpendicular to the flow direction, installed at a min. angle of 3° to ensure self-draining
3
On elbows
4
Inclined installation in pipes with a small nominal diameter
U
Immersion length

In the case of pipes with a small nominal diameter, it is advisable for the tip of the thermometer
to project well into the process so that it extends past the pipe axis (2 and 3).
Installation at an angle (4) could be another solution. When determining the immersion length
or installation depth, all the parameters of the thermometer and of the medium to be measured
must be taken into account (e.g. flow velocity, process pressure).
The requirements of the EHEDG and the 3-A Sanitary Standard must be adhered to.
Installation instructions EHEDG/cleanability: Lt ≤ (Dt-dt)
Installation instructions 3-A/cleanability: Lt ≤ 2(Dt-dt)
Pay attention to the exact position of the sensor element in the thermometer tip.
Available options depend on product and configuration.
20 mm
(0.79 in)
10 mm
(0.4 in)

0

1

2

3

4

5
A0041814

1
2
3
4
5

iTHERM StrongSens or iTHERM TrustSens for 5 to 7 mm (0.2 to 0.28 in)
iTHERM QuickSens for 0.5 to 1.5 mm (0.02 to 0.06 in)
Thermocouple (not grounded) for 3 to 5 mm (0.12 to 0.2 in)
Wire-wound sensor for 5 to 20 mm (0.2 to 0.79 in)
Standard thin-film sensor for 5 to 10 mm (0.2 to 0.39 in)

To minimize the heat dissipation, 20 to 25 mm of the sensor should extend into the medium beyond
the sensor element.

20

Endress+Hauser

<!-- page 21 -->

iTHERM ModuLine TM411

This results in the following recommended minimum immersion lengths:
• iTHERM TrustSens or iTHERM StrongSens 30 mm (1.18 in)
• iTHERM QuickSens 25 mm (0.98 in)
• Wire wound sensor 45 mm (1.77 in)
• Standard thin-film sensor 35 mm (1.38 in)
Special consideration should be given to tee thermowells, as the immersion length is very short on
account of their design, and the measurement error is higher as a result. It is therefore
recommended to use elbow thermowells with iTHERM QuickSens sensors.
1

2

A0041794

7
1
2

Endress+Hauser

Process connections for thermometer installation in pipes with small nominal diameters
Varivent process connection type N for DN40
Tee or elbow thermowell (illustrated) for weld-in as per DIN 11865/ASME BPE

21

<!-- page 22 -->

iTHERM ModuLine TM411

A

B

C

D

1
8
2

13
9
3

10

11
12

14
16

7
4

5

15

6
A0040345

8
A
1
2
3
4
5
6
7
B
8
9
10
C
11
12
D
13
14
15
16

Versions for hygiene-compliant installation (depends on the version ordered)
Dairy fitting according to DIN 11851, only in connection with EHEDG-certified and self-centering sealing ring
Sensor with dairy fitting
Groove slip-on nut
Counterpart connection
Centering ring
R0.4
R0.4
Sealing ring
Varivent process connection for VARINLINE housing
Sensor with Varivent connection
Counterpart connection
O-ring
Clamp according to DIN 32676
Molded seal
Counterpart connection
Liquiphant M G1" process connection, horizontal installation
Weld-in adapter
Vessel wall
O-ring
Thrust collar

NOTICE
The following action must be taken if a sealing ring or O-ring fails:
‣ Remove the thermometer.
‣ Clean the thread and the O-ring joint or sealing surface.
‣ Replace the O-ring or sealing ring.
‣ Perform CIP after installation.
The counterpieces for the process connections and the seals or sealing rings are not supplied
with the thermometer. Liquiphant M weld-in adapters with associated seal kits are available as
accessories. →  53.
In the case of weld-in connections, exercise care when performing the welding work on the process
side:
1.

Use suitable welding material.

2.

Flush-weld or weld with welding radius ≥ 3.2 mm (0.13 in).

3.

Avoid crevices, folds or gaps.

4.

Ensure the surface is honed and polished, Ra ≤ 0.76 µm (30 µin).
As a general rule, the thermometers should be installed in such a way that does not impact
their ability to be cleaned (the requirements of the 3-A Sanitary Standard must be observed).
The Varivent connections, Liquiphant M weld-in adapters and Ingold connections with weld-in
adapters enable flush-mounted installation.
For the requirements for installation according to the EHEDG and 3-A Sanitary Standard, see
the Operating Instructions for the modular hygienic thermometers (BA02023T).

22

Endress+Hauser

<!-- page 23 -->

iTHERM ModuLine TM411

Environment
Ambient temperature range

Terminal head

Temperature in °C (°F)

Without mounted head transmitter

Depends on the terminal head used and the cable gland or fieldbus
connector; see "Terminal heads" section. →  37

With mounted iTEMP head transmitter

–40 to +85 °C (–40 to +185 °F)

With mounted iTEMP head transmitter
and display

–30 to +85 °C (–22 to 185 °F)

Extension neck

Temperature in °C (°F)

Quick-fastening iTHERM QuickNeck

–50 to +140 °C (–58 to +284 °F)

Storage temperature

For information, see the ambient temperature.

Relative humidity

Depends on the transmitter used. If Endress+Hauser iTEMP head transmitters are used:
• Condensation permitted as per IEC 60 068-2-33
• Max. rel. humidity: 95% as per IEC 60068-2-30

Climate class

As per EN 60654-1, Class C

Degree of protection

Max. IP69K, depending on the design (terminal head, connector, etc.)

Shock and vibration
resistance

The Endress+Hauser inserts meet the requirements of IEC 60751 which specify shock and vibration
resistance of 3g in the range from 10 to 500 Hz. The vibration resistance at the measuring point
depends on the sensor type and design, see the following table:
Version

Vibration resistance for the sensor tip

Pt100 (WW or TF)

30 m/s² (3g) 1)

iTHERM StrongSens Pt100 (TF)
iTHERM QuickSens Pt100 (TF), version: ⌀6 mm (0.24 in)

> 600 m/s² (60g)

1)

Electromagnetic
compatibility (EMC)

Vibration resistance also applies to quick-fastening iTHERM QuickNeck.

Depends on the head transmitter used. For details, see the Technical Information.

Process
Process temperature range

Depends on the type of sensor used, maximum –200 to +600 °C (–328 to +1 112 °F)

Thermal shock

Thermal shock resistance in CIP/SIP processes with a temperature increase and decrease from
+5 to +130 °C (+41 to +266 °F) within 2 seconds.

Process pressure range

The maximum possible process pressure depends on various influencing factors, such as the design,
process connection and process temperature. For information on the maximum possible process
pressures for the individual process connections, see the 'Process connection' section. →  42
It is possible to verify the mechanical loading capacity depending on the installation and
process conditions using the online TW Sizing Module for thermowells in the Endress+Hauser
Applicator software. This is valid for DIN thermowell calculations. See 'Accessories' section.

Endress+Hauser

23

<!-- page 24 -->

iTHERM ModuLine TM411

Example of the permitted flow velocity depending on the immersion length and process
medium
The maximum allowable flow velocity to which the thermometer can be exposed decreases as the
immersion depth of the insert in the flowing medium increases. In addition, it is dependent on the
diameter of the thermometer tip, the medium type, the process temperature and the process
pressure. The following figures exemplify the maximum permitted flow velocities in water and
superheated steam at a process pressure of 40 bar (580 PSI).
v (ft/s) v (m/s)
290 90
260 80
230 70
200 60
160 50
130 40
100 30
B
65 20
30 10

A

0
300

200

100

0

400

500

600

L (mm)
0

2

4

6

8

10

12

14
L (in)

16

18

20

22

24

A0032462

9
A
B
L
v

State of aggregation of the
medium

Permitted flow velocity, thermowell diameter 9 mm (0.35 in)
Medium water at T = 50 °C (122 °F)
Medium superheated steam at T = 160 °C (320 °F)
Immersion length exposed to flow
Flow velocity

Gaseous or liquid (also with high viscosity, e.g. yogurt).

Mechanical construction
Design, dimensions

All dimensions in mm (in). The design of the thermometer depends on the thermowell version used:
• Thermometer without a thermowell
• Diameter 6 mm (¹⁄₄ in)
• Diameter 9 mm (0.35 in)
• Diameter 12.7 mm (¹⁄₂ in)
• Thermowell version as tee thermowell and elbow thermowell as per DIN 11865/ASME BPE for
welding in
Various dimensions, such as the immersion length U for example, are variable values and are
therefore indicated as items in the following dimensional drawings.

24

Endress+Hauser

<!-- page 25 -->

iTHERM ModuLine TM411

Variable dimensions:
Item

Description

E

Extension neck length, variable depending on configuration or optionally predefined for version
with iTHERM QuickNeck

IL

Insertion length of insert

L

Thermowell length (U+T)

B

Thermowell base thickness: predefined, depends on thermowell version (see also the individual
table data)

T

Length of thermowell lagging: variable or predefined, depends on thermowell version (see also the
individual table data)

U

Immersion length: variable, depending on the configuration

X

Variable for calculating the insertion length of the insert, depends on different screw-in lengths in
the terminal head thread M24x1.5 or NPT ½", see insert length calculation (IL) →  36

2

1

NPT ½“

X

8 (0.32)

15 (0.6)

M24x1.5

X

E
E
A0020889

 10
1
2
ØID

Endress+Hauser

Different screw-in lengths in terminal head thread for M24x1.5 and ½" NPT

Thread M24x1.5: X = 11 mm (0.43 in), mat.: 1.4305 (coupling)
Thread NPT ½": X = 26 mm (1.02 in) or with terminal head TA30S = 31 mm (1.22 in), mat.:
1.4305 (coupling)

Insert diameter 6 mm (¹⁄₄ in) or 3 mm (¹⁄₈ in)

25

<!-- page 26 -->

iTHERM ModuLine TM411

Without thermowell
For installation in an existing thermowell

1.1

1.2

2

3

4

M24x1.5

NPT ½“

M24x1.5

M24x1.5

M24x1.5

X

X

X

5

X

X
E

U

E

!9
(0.35)

!9
(0.35)
G¼“

E

12
(0.47)

E

U

IL

U
U

U

U

A0018315

1.1 Thermometer without extension neck, insert surface not specified, product structure: feature 80, option A0; X = 11 mm (0.43 in) for connection
thread M24x1.5
1.2 Thermometer without extension neck, insert surface not specified, product structure: feature 80, option A0; X = 26 mm (1.02 in) for connection
thread NPT ½"; X = 31 mm (1.22 in) for connection thread NPT ½" and terminal head TA30S
2
Thermometer with quick-fastening iTHERM QuickNeck, top and bottom part, G3/8" internal thread for thermowell connection
3
Thermometer with quick-fastening iTHERM QuickNeck, top part
4
Thermometer with replaceable extension neck TE411, G3/8" union nut for thermowell connection
5
Thermometer with replaceable extension neck TE411, external thread G¼" for compression fitting TK40
Can be selected for all versions: thread M24x1.5 or ½" NPT to terminal head

Pay attention to the following equations when calculating the immersion length U for immersion into
an existing thermowell TT411:
Version 1

U = L 1) + E 2) + 4 mm (0.16 in) - B

Version 2 and 4

U = L 1) + 4 mm (0.16 in) - B

Version 3, thermowell diameter
9 mm (0.35 in)

U = L 1) + 4 mm (0.16 in)(for spring travel) - B

Version 3, thermowell diameter
6 mm (¹⁄₄ in)/ 12.7 mm (¹⁄₂ in)

U = L 1) + 36 mm (1.42 in)+ 4 mm (0.16 in)(for spring travel) - B

Version 5

U = U(incl. TK40)

1)
2)

Item (see drawing
above)

L = total length of the thermowell available onsite = Uthermowell + Tthermowell
E = length of the extension neck provided onsite (if available)

Version

Length

Version 1:
Without extension neck

E=0

Version 2:
iTHERM QuickNeck with thread M24x1.5 to terminal head
Extension neck
length E

• A0: E not required
• X1: E= variable length
iTHERM QuickNeck with thread NPT ½" to terminal head
• A0: E not required
• X1: E= variable length

26

• 62 mm (2.44 in)
• Variable, depending on the
configuration
• 54 mm (2.13 in)
• Variable, depending on the
configuration

Endress+Hauser

<!-- page 27 -->

iTHERM ModuLine TM411

Item (see drawing
above)

Version

Length

Version 3:
iTHERM QuickNeck top part with thread M24x1.5 to terminal head

• 30 mm (1.18 in)
• Variable, depending on the
configuration

• A0: E not required
• X1: E= variable length
iTHERM QuickNeck top part with thread NPT ½" to terminal head

• 22 mm (0.87 in)
• Variable, depending on the
configuration

• A0: E not required
• X1: E= variable length
Version 4: With replaceable extension neck, G3/8" union nut for thermowell
connection

Variable, depending on the configuration

Version 5: With replaceable extension neck and external thread G¼" for
compression fitting TK40, with thread M24x1.5 or ½" NPT to terminal head

70 mm (2.76 in)

Immersion length U

Independent of the version

Variable, depending on the configuration

Variable length X

• Connection thread M24x1.5
• Connection thread ½" NPT
• Connection thread ½" NPT and terminal head
TA30S

11 mm (0.43 in)
28 mm (1.1 in)
31 mm (1.22 in)

IL = U+E+X

With compression fitting TK40 as process connection, insert in direct contact with the process

1

2

3

4

U

!9
(0.35)

G¼“

U
!6
(¼)

X

E = 70 (2.56)

E = 70 (2.56)

X

!44 (1.73)
!33 (1.3)

8 (0.32)

X

X

5

NPT ½“

M24x1.5

M4x1
!9
(0.35)

IL
G¼“

!6
(¼)

U

!6
(¼)

U

!6
(¼)

!6
(¼)

A0017700

1
2
3
4
5

Movable compression fitting TK40 - variably fixable immersion length U, only connection thread M24x1.5
Without compression fitting for use if compression fitting is available at point of installation, insert with polished surface - product structure: feature
80, option A1 or A3 - only connection thread M24x1.5
Compression fitting TK40 fixed by extension neck - fixed immersion length U, connection thread M24x1.5
Compression fitting TK40 fixed by extension neck - fixed immersion length U, connection thread ½" NPT
Insert, for example with mounted head transmitter

Item

Version

Length

Extension neck length
Extension neck ⌀9 mm (0.35 in)
E
Immersion length U

Independent of the version

Variable length X

• Versions 1 and 2: Without extension neck, connection thread M24x1.5
• Version 3: With extension neck, connection thread M24x1.5
• Version 4: With extension neck, connection thread ½" NPT
• With extension neck and TA30S terminal head

Endress+Hauser

70 mm (2.76 in)
Variable, depending
on the
configuration
IL = U+X
IL = U+E+X
IL = U+E+X
IL = U+E+X

39 mm (1.54 in)
11 mm (0.43 in)
26 mm (1.02 in)
31 mm (1.22 in)

27

<!-- page 28 -->

iTHERM ModuLine TM411

With thermowell diameter 6 mm (¹⁄₄ in)

NPT ½“

M24x1.5

X
36 (1.42)

X
E
E

!9
(0.35)

G3/8“
T

T
!6 (0.24)

L

L
U

U

B

1

2

3

4

5

6

7

8

10

9

A0017790

1
2
3
4
5
6
7
8
9
10

Thermometer with replaceable extension neck TE411 and process connection as clamp version
Without process connection
Process connection version as spherical compression fitting TK40
Process connection version as metal sealing system M12x1.5
Process connection version as metal sealing system G½"
Process connection version as cylindrical weld-in adapter ⌀12 x 40 mm
Process connection version as cylindrical weld-in adapter ⌀30 x 40 mm
Process connection version as spherical-cylindrical weld-in adapter ⌀30 x 40 mm
Process connection version as spherical weld-in adapter ⌀25 mm
Thermometer with quick-fastening iTHERM QuickNeck and process connection as sanitary connection
according to DIN 11851

• Replaceable extension neck or quick-fastening iTHERM QuickNeck
• Thread M24x1.5 or ½" NPT to terminal head
• G3/8" thread for thermowell connection
Item

Version

Length

Replaceable extension neck ⌀9 mm (0.35 in)

Variable, depending on the
configuration

iTHERM QuickNeck with thread M24x1.5 to
terminal head, with option:
Extension neck length E

• A0: E not required
• X1: E= variable length
iTHERM QuickNeck with thread NPT ½" to
terminal head, with option:

Length of thermowell
lagging T 1)

28

• 62 mm (2.44 in)
• Variable, depending on the
configuration

• A0: E not required
• X1: E= variable length

• 54 mm (2.13 in)
• Variable, depending on the
configuration

Metal sealing system M12x1.5

46 mm (1.81 in)

Metal sealing system G½"

60 mm (2.36 in)

Tri-clamp (0.5"-0.75")

24 mm (0.94 in)

Microclamp (DN8)

23 mm (0.91 in)

Clamp DN12 according to DIN 32676

24 mm (0.94 in)

Clamp DN25/DN40 according to DIN 32676

21 mm (0.83 in)

Endress+Hauser

<!-- page 29 -->

iTHERM ModuLine TM411

Item

Version

Length

Dairy fitting DN25/DN32/DN40 according to
DIN 11851

29 mm (1.14 in)

Spherical-cylindrical weld-in adapter

58 mm (2.28 in)

Cylindrical weld-in adapter ⌀12 mm (0.47 in)

55 mm (2.17 in)

Without process connection (only G3/8"
thread), where necessary with compression
fitting TK40

11 mm (0.43 in)

Cylindrical weld-in adapter

55 mm (2.17 in)

Spherical weld-in adapter

47 mm (1.85 in)

Immersion length U

Independent of the version

Variable, depending on the
configuration

Variable length X

• With connection thread M24x1.5
• With connection thread ½" NPT
• With terminal head TA30S

15 mm (0.6 in)
30 mm (1.18 in)
35 mm (1.38 in)

Calculation of IL for the insert:
IL = U+T+E-B+X
Base thickness B
1)

Endress+Hauser

Reduced tip ⌀4.3 mm (0.17 in)

3 mm (0.12 in)

Depends on the process connection

29

<!-- page 30 -->

iTHERM ModuLine TM411

With thermowell diameter 9 mm (0.35 in)
Extension neck not replaceable, but can be separated with the option of the quick-fastening iTHERM QuickNeck.
M24x1.5

X

T

!15 (0.6)

L
!9 (0.35)

U

B

1

2

3

4

5

6

7

8

NPT ½“

X
E
T

U
L
!9
(0.35)

B

9

10

11

12

13

14
A0017761

1
2
3
4
5
6
7
8
9
10
11
12
13
14

Thermometer without replaceable extension neck, connection thread M24x1.5, process connection as clamp version
Process connection version as cylindrical weld-in adapter ⌀30 x 40 mm
Process connection version as spherical-cylindrical weld-in adapter ⌀30 x 40 mm
Process connection version as spherical weld-in adapter ⌀25 mm
Process connection version as dairy fitting according to DIN 11851
Process connection version as aseptic pipe union according to DIN 11864-1 Form A
Process connection version as metal sealing system G½"
Process connection thread as per ISO 228 for Liquiphant weld-in adapter
Process connection version APV Inline
Process connection version Varivent
Process connection version Ingold connection
Process connection SMS 1147
Process connection version Neumo Biocontrol
Thermometer with quick-fastening iTHERM QuickNeck and process connection, as clamp version for example

Item

Extension neck length
E

30

Version

Length

Without iTHERM QuickNeck

0

With iTHERM QuickNeck
With thread M24x1.5 to terminal head
• A0: E not required
• X1: E= variable length

• 30 mm (1.18 in)
• Variable, depending on the
configuration

Endress+Hauser

<!-- page 31 -->

iTHERM ModuLine TM411

Item

Version

Length

With thread ½" NPT to terminal head
• A0: E not required
• X1: E= variable length

• 22 mm (0.9 in)
• Variable, depending on the
configuration

Without iTHERM QuickNeck

Variable, depending on the
configuration

With iTHERM QuickNeck, depending on the process connection:

Length of thermowell
lagging T

SMS 1147, DN25

40 mm (1.57 in)

SMS 1147, DN38

41 mm (1.61 in)

SMS 1147, DN51

42 mm (1.65 in)

Varivent, type F, D = 50 mm (1.97 in)
Varivent, type N, D = 68 mm (2.67 in)

52 mm (2.05 in)

Varivent, type B, D = 31 mm (1.22 in)

56 mm (2.2 in)

G1" thread according to ISO 228 for Liquiphant weld-in adapter

77 mm (3.03 in)

Spherical-cylindrical weld-in adapter

70 mm (2.76 in)

Cylindrical weld-in adapter

67 mm (2.64 in)

Aseptic pipe union according to DIN11864-A, DN25

42 mm (1.65 in)

Aseptic pipe union according to DIN11864-A, DN40

43 mm (1.69 in)

Dairy fitting according to DIN 11851, DN32

47 mm (1.85 in)

Dairy fitting according to DIN 11851, DN40
Dairy fitting according to DIN 11851, DN50

48 mm (1.89 in)

Clamp according to DIN 32676, DN12
Clamp according to DIN 32676, DN25

37 mm (1.46 in)

Clamp according to DIN 32676, DN40
Clamp according to DIN 32676, DN63.5

39 mm (1.54 in)

Clamp according to DIN 32676, DN70
Microclamp (DN18)

47 mm (1.85 in)

Tri-clamp (0.75")

46 mm (1.81 in)

Ingold connection ⌀25 mm (0.98 in) x 30 mm (1.18 in)

78 mm (3.07 in)

Ingold connection ⌀25 mm (0.98 in) x 46 mm (1.81 in)

94 mm (3.7 in)

Metal sealing system G½"

74 mm (2.91 in)

APV Inline, DN50

51 mm (2.01 in)

Immersion length U

Independent of the version

Variable, depending on the
configuration

Variable length X

• Without iTHERM QuickNeck, connection thread
M24x1.5
• With iTHERM QuickNeck, connection thread M24x1.5
• With iTHERM QuickNeck, connection thread NPT ½"
• With iTHERM QuickNeck, terminal head TA30S

IL = U+T-B+X
IL = U+E+T-B+X
IL = U+E+T-B+X
IL = U+E+T-B+X

15 mm (0.6 in)
15 mm (0.6 in)
30 mm (1.18 in)
35 mm (1.38 in)

Reduced tip ⌀3 mm (0.12 in) x 20 mm (0.79 in)
Base thickness B

Tapered tip ⌀ 6.6 mm (0.26 in) x 60 mm (2.36 in)

3 mm (0.12 in)

Straight tip

Endress+Hauser

31

<!-- page 32 -->

iTHERM ModuLine TM411

!9
(0.35)

M24x1.5

NPT ½“

X

X

E

E

T

T

36 (1.42)

With thermowell diameter 12.7 mm (¹⁄₂ in)

L

L
!12.7
(0.5)

U

U

B

B
1

2

3

4

5

6

7
A0018313

1
2
3
4
5
6
7

Thermometer with replaceable extension neck TE411 and process connection as clamp version
Process connection version as cylindrical weld-in adapter ⌀12.7 mm (0.5 in)
Process connection version as spherical weld-in adapter ⌀25 mm
Process connection version as dairy fitting according to DIN 11851
Thread according to ISO 228 for Liquiphant weld-in adapter
Process connection version Varivent
Thermometer with quick-fastening iTHERM QuickNeck and process connection, as clamp version for example

• Replaceable extension neck or quick-fastening iTHERM QuickNeck
• G3/8" thread for thermowell connection
• Thermowell welded at the tip
Item

Version

Length

Replaceable extension neck,
⌀9 mm (0.35 in)

Variable, depending on the
configuration

iTHERM QuickNeck with thread M24x1.5
to terminal head, with option:
Extension neck length E

• A0: E not required
• X1: E= variable length

• 62 mm (2.44 in)
• Variable, depending on the
configuration

iTHERM QuickNeck with thread NPT ½" to
terminal head, with option:
A0: E not required

54 mm (2.13 in)

Weld-in adapter, cylindrical,
⌀12.7 mm (0.5 in) 1)

12 mm (0.47 in)

All other process connections

65 mm (2.56 in)

Immersion length U

Independent of the process connection

Variable, depending on the
configuration

Variable length X

• With connection thread M24x1.5
• With connection thread ½" NPT
• With terminal head TA30S

15 mm (0.6 in)
30 mm (1.18 in)
35 mm (1.38 in)

Length of thermowell lagging
T

Calculation of IL for the insert:
IL = U+T+E-B+X
Base thickness B

32

Reduced tip ⌀5.3 mm (0.21 in) x
20 mm (0.79 in)

3 mm (0.12 in)

Endress+Hauser

<!-- page 33 -->

iTHERM ModuLine TM411

Item

1)

Version

Length

Reduced tip ⌀8 mm (0.31 in) x
32 mm (1.26 in)

4 mm (0.16 in)

Straight tip

6 mm (0.24 in)

See Fig. Version 2

Thermowell version as tee thermowell or elbow thermowell, optimized

34 (1.34)

11 (0.43)

No welds, no dead legs

G3/8"

0.7 (0.03)

U

!4.5 (0.18)
1

2

3

4
A0036509

 11
1
2
3
4
U

Thermowell as per DIN 11865 or ASME BPE

Tee thermowell with threaded QuickNeck bottom part, torque 5 Nm (3.69 lbf ft) and glued with threadlocking
adhesive
Tee thermowell with extension neck connection G3/8"
Elbow thermowell with extension neck connection G3/8"
Elbow thermowell threaded QuickNeck bottom part, torque 5 Nm (3.69 lbf ft) and glued with threadlocking
adhesive
Immersion length

• Pipe sizes as per DIN 11865 series A (DIN), B (ISO) and C (ASME BPE)
• 3-A marked for nominal diameters ≥ DN25
• EHEDG certified for nominal diameters ≥ DN25
• ASME BPE compliance for nominal diameters ≥ DN25
• IP69K protection class
• 1.4435+316L material, delta ferrite content < 0.5%
• Temperature range: –60 to +200 °C (–76 to +392 °F)
• Pressure range: PN25 as per DIN11865

Endress+Hauser

33

<!-- page 34 -->

iTHERM ModuLine TM411

Due to the short immersion length U in the case of small pipe diameters, the use of iTHERM
QuickSens inserts is recommended.
As a general rule, the longer the immersion length U, the better the measurement accuracy. For
small pipe diameters, it is therefore advisable to use elbow thermowells to enable a maximum
immersion length U.
Suitable immersion lengths for the following thermometers with G3/8" extension neck
connection:
• iTHERM CompactLine TMR35: 83 mm (3.27 in)
• iTHERM TM411: 85 mm (3.35 in)
• iTHERM TM311: 85 mm (3.35 in)
• iTHERM TrustSens TM371: 85 mm (3.35 in)
Suitable immersion lengths for the following thermometers with QuickNeck connection:
• iTHERM TM411: 119 mm (4.7 in)
• iTHERM TrustSens TM371: 119 mm (4.7 in)

34

Endress+Hauser

<!-- page 35 -->

iTHERM ModuLine TM411

Possible combinations of the thermowell versions with the available process connections and
quick-fastening iTHERM QuickNeck
Process connection and size

Thermowell diameter
6 mm (¹⁄₄ in) 9 mm (0.35 in) 12.7 mm (¹⁄₂ in)

Without process connection (for installation with
compression fitting)

iTHERM QuickNeck for ⌀9 mm
(0.35 in) 1)



-

-

-

-

-



-



-



-

-

-

Weld-in adapter
Cylindrical ⌀12.7 mm (0.5 in)
Cylindrical ⌀30 x 40 mm
Cylindrical ⌀12 x 40 mm



Spherical-cylindrical ⌀30 x 40 mm





-



Spherical ⌀25 mm (0.98 in)







-













-







Clamp according to DIN 32676
DN10 - 20

DN25 - 40 (1 - 1.5 in)
DN50 (2 in)
DN63.5 (2.5 in)
DN70 - 76.5 (3 in)





Dairy fitting according to DIN 11851
DN25
DN32, DN40
DN50









-

-



Aseptic pipe union according to DIN 11864-1 Form A
DN25, DN40

-



Metal sealing system
M12x1.5
G½"





-



Thread according to ISO 228 for Liquiphant weld-in adapter
G¾" for FTL20, FTL31, FTL33
G¾" for FTL50

-





G1" for FTL50



APV Inline
DN50

-



-



Type B, ⌀31 mm; Type F, ⌀50 mm ; Type N, ⌀68 mm

-







25 x 30 mm or 25 x 46 mm

-



-



DN25, DN38, DN51

-



-



D25 PN16, D50 PN16, D65 PN16

-



-

-

Varivent

Ingold connection

SMS 1147

Neumo Biocontrol

1)

In the case of 6 mm (¼ in) and 12.7 mm (½ in) diameters, the iTHERM QuickNeck is available for all process connection versions.

Endress+Hauser

35

<!-- page 36 -->

iTHERM ModuLine TM411

Depending on the application, iTHERM TS111 inserts with different RTD sensors are available for
the thermometer:

Insert

Sensor

Standard thin-film

iTHERM StrongSens

iTHERM QuickSens 1)

Wire wound

1x Pt100, 3- or 4-wire
1x Pt100, 3- or 4wire, mineral
insulated

Sensor design;
connection method

1x Pt100, 3- or 4-wire,
mineral insulated

1x Pt100, 3- or 4-wire,
mineral insulated

• ⌀6 mm (¹⁄₄ in),
mineral insulated
• ⌀3 mm (¹⁄₈ in), Teflon
insulated

Vibration
resistance of the
insert tip

Up to 3g

Enhanced vibration
resistance > 60g

• ⌀3 mm (¹⁄₈ in) up to 3g
• ⌀6 mm (¹⁄₄ in) > 60g

Up to 3g

Measuring range;
accuracy class

–50 to +400 °C
(–58 to +752 °F), Class A
or AA

–50 to +500 °C
(–58 to +932 °F), Class A
or AA

–50 to +200 °C
(–58 to +392 °F), Class A
or AA

–200 to +600 °C (–328 to +1 112 °F), Class
A or AA

Diameter

3 mm (¹⁄₈ in),
6 mm (¹⁄₄ in)

6 mm (¹⁄₄ in)

1)

2x Pt100, 3-wire,
mineral insulated

3 mm (¹⁄₈ in), 6 mm (¹⁄₄ in)

Recommended for immersion lengths U < 70 mm (2.76 in)

The iTHERM TS111 insert is available as a spare part. The insertion length (IL) depends on the
immersion length of the thermowell (U), the length of the extension neck (E), the thickness of the
base (B), the length of the thermowell lagging (L) and the variable length (X). The insertion length
(IL) must be taken into consideration when replacing the unit. Formulas for calculating IL →  24.
For more information on the deployed iTHERM TS111 insert with enhanced vibration
resistance and fast-response sensor, see the Technical Information (TI01014T/09/).
Spare parts currently available for your product can be found online at:
https://www.endress.com/en/instrumentation-services, product root: TM411. Always quote
the serial number of the device when ordering spare parts! The insertion length IL is
automatically calculated using the serial number.
Weight

0.5 to 2.5 kg (1 to 5.5 lbs) for standard versions.

Materials

Extension neck and thermowell, insert, process connection.
The temperatures for continuous operation specified in the following table are only intended as
reference values for use of the various materials in air and without any significant compressive load.

36

Endress+Hauser

<!-- page 37 -->

iTHERM ModuLine TM411

The maximum operating temperatures can be reduced considerably in cases where abnormal
conditions such as high mechanical load occur or in aggressive media.

Name

Short formula

AISI 316L
(corresponds to
1.4404
or 1.4435)

X2CrNiMo17-13-2,
X2CrNiMo18-14-3

650 °C (1 202 °F) 1)

1.4435+316L, delta
ferrite < 1% or <
0.5%

1)

Surface roughness

Recommended
max. temperature
for continuous use
in air

• Austenitic stainless steel
• High corrosion resistance in general
• Particularly high corrosion resistance in
chlorine-based and acidic, non-oxidizing
atmospheres through the addition of
molybdenum (e.g. phosphoric and
sulfuric acids, acetic and tartaric acids
with a low concentration)
• Increased resistance to intergranular
corrosion and pitting
• The wetted part is a thermowell made of
316L or 1.4435+316L passivated with
3% sulfuric acid.

With regard to analytical limits, the specifications of both materials (1.4435 and 316L)
are met simultaneously. In addition, the delta ferrite content of the parts in contact with
the process is limited to <1% or <0.5%.
≤3% for weld seams (in accordance with Basel Standard II)

Can be used to a limited extent up to 800 °C (1472 °F) for low compressive loads and in non-corrosive
media. Contact your Endress+Hauser sales team for further information.

Values for process/product contact surfaces:
Standard surface, mechanically polished 1)
1)

Mechanically polished , buffed

Ra ≤ 0.76 µm (30 µin)

2)

Ra ≤ 0.38 µm (15 µin)

Mechanically polished 1), buffed and electropolished
1)
2)

Terminal heads

Properties

Ra ≤ 0.38 µm (15 µin)+ electropolished

Or any other finishing method that meets the Ra max
Not compliant with ASME BPE

All terminal heads have an internal shape and size in accordance with DIN EN 50446, flat face, and
a thermometer connection with a M24x1.5 or ½" NPT thread. All dimensions in mm (in). The
sample cable glands in the diagrams correspond to M20x1.5 connections with non-Ex polyamide
cable glands. Specifications without head transmitter installed. For ambient temperatures with head
transmitter installed, see the 'Environment' section. →  23
As a special feature, Endress+Hauser offers terminal heads with optimized terminal accessibility for
easy installation and maintenance.

TA30A

Specification

15.5 (0.6)

68.5 (2.7)

107.5 (4.23)

28
(1.1)

78 (3.1)
A0009820

Endress+Hauser

• Protection degree:
• IP66/68 (NEMA Type 4x encl.)
• For ATEX: IP66/67
• Temperature: –50 to +150 °C (–58 to +302 °F) without cable
gland
• Material: aluminum, polyester powder coated
Seals: silicone
• Threaded cable entry: G ½", NPT ½" and M20x1.5;
• Head color: blue, RAL 5012
• Cap color: gray, RAL 7035
• Weight: 330 g (11.64 oz)
• Ground terminal, internal and external
• Available with sensors with 3-A® symbol

37

<!-- page 38 -->

iTHERM ModuLine TM411

TA30A with display window in cover

Specification

15.5 (0.6)

91.6 (3.61)

107.5 (4.23)

28
(1.1)78 (3.1)
A0009821

TA30D

Specification

15.5 (0.6)

110 (4.3)

107.5 (4.23)

28
(1.1) 78 (3.1)
A0009822

TA30P

• Protection degree:
• IP66/68 (NEMA Type 4x encl.)
• For ATEX: IP66/67
• Temperature: –50 to +150 °C (–58 to +302 °F) without cable
gland
• Material: aluminum, polyester powder coated
Seals: silicone
• Threaded cable entry: G ½", NPT ½" and M20x1.5
• Two head transmitters can be mounted. In the standard
configuration one transmitter is mounted in the terminal
head cover and an additional terminal block is installed
directly on the insert.
• Head color: blue, RAL 5012
• Cap color: gray, RAL 7035
• Weight: 390 g (13.75 oz)
• Ground terminal, internal and external
• Available with sensors with 3-A® symbol

Specification

(3.3
)

114 (4.5)
41.5 (1.63)

!83

28
(1.1)
85 (3.4)
A0023477

38

• Protection degree:
• IP66/68 (NEMA Type 4x encl.)
• For ATEX: IP66/67
• Temperature: –50 to +150 °C (–58 to +302 °F) without cable
gland
• Material: aluminum, polyester powder coated
Seals: silicone
• Threaded cable entry: G ½", NPT ½" and M20x1.5
• Head color: blue, RAL 5012
Cap color: gray, RAL 7035
• Weight: 420 g (14.81 oz)
• Display window: single-pane safety glass according to DIN
8902
• Display window in cover for head transmitter with TID10
display
• Ground terminal, internal and external
• Available with sensors with 3-A® symbol

• Degree of protection: IP65
• Max. temperature: –40 to +120 °C (–40 to +248 °F)
• Material: polyamide (PA12), antistatic
Seals: silicone
• Threaded cable entry: M20x1.5
• Two head transmitters can be mounted. In the standard
version, one transmitter is mounted in the terminal head
cover and an additional terminal block is installed directly on
the insert.
• Head and cap color: black
• Weight: 135 g (4.8 oz)
• Type of protection: intrinsic safety (G Ex ia)
• Ground terminal: only internal via auxiliary clamp
• Available with sensors with 3-A® symbol

Endress+Hauser

<!-- page 39 -->

iTHERM ModuLine TM411

TA30R (optionally with display window in
cover)

96 (3.8)

71 (2.8)
96 (3.8)*

64 (2.52)

25 (1)

64 (2.52)

Specification
• Degree of protection - standard version: IP69K (NEMA Type
4x encl.)
Degree of protection - version with display window: IP66/68
(NEMA Type 4x encl.)
• Temperature: –50 to +130 °C (–58 to +266 °F) without cable
gland
• Material: stainless steel 316L, abrasive-blasted or polished
Seals: silicone, optional EPDM for applications free from
paint-wetting impairment substances
Display window: polycarbonate (PC)
• Cable entry thread NPT ½" and M20x1.5
• Weight
• Standard version: 360 g (12.7 oz)
• Version with display window: 460 g (16.23 oz)
• Display window in cover optionally for head transmitter with
display TID10
• Ground terminal: internal as standard
• Available with sensors with 3-A® symbol
• Not allowed for Class II and III applications

A0017145

* Dimensions of version with display window
in cover

TA30R (high version for two transmitters)

Specification
• Degree of protection: IP69K (NEMA Type 4x encl.)
• Temperature: –50 to +130 °C (–58 to +266 °F) without cable
gland
• Material: stainless steel 316L, abrasive-blasted or polished
Seals: EPDM
• Cable entry thread NPT ½" and M20x1.5
• Weight: 460 g (16.23 oz)
• For two head transmitters
• Ground terminal: internal as standard
• Not allowed for Class II and III applications
• Available with 3-A marked sensors

96 (3.8)

116 (4.57)

64 (2.52)

25
(1)

64 (2.52)
A0034644

Endress+Hauser

39

<!-- page 40 -->

iTHERM ModuLine TM411

TA30S

Specification
81.

50 (1.97)

87 (3.43)

7 (3

• Degree of protection: IP65 (NEMA Type 4x encl.)
• Temperature: –40 to +85 °C (–40 to +185 °F) without cable
gland
• Material: polypropylene (PP), FDA-compliant, seals: O-ring
EPDM
• Cable entry thread: ¾" NPT (with adapter for ½" NPT),
M20x1.5
• Protective assembly connection: ½" NPT
• Color: white
• Weight: approx. 100 g (3.5 oz)
• Ground terminal: only internal via auxiliary terminal
• Not allowed for Class II and III applications
• Available with 3-A marked sensors

.22

)

28
(1.1)
78 (3.1)
122 (4.8)
A0017146

Cable glands and connectors 1)
Suitable for
cable entry

Degree of
protection

Temperature range

Suitable cable diameter

IP68

–30 to +95 °C
(–22 to +203 °F)

7 to 12 mm (0.27 to 0.47 in)

½" NPT, ¾" NPT,
M20x1.5
(optionally 2x
cable entry)

IP68

–40 to +100 °C
(–40 to +212 °F)

½" NPT,
M20x1.5
(optionally 2x
cable entry)

IP69K

–20 to +95 °C
(–4 to +203 °F)

Cable gland for dust ignition-proof area, ½" NPT,
polyamide
M20x1.5

IP68

–20 to +95 °C
(–4 to +203 °F)

Cable gland for dust ignition-proof area, M20x1.5
nickel-plated brass

IP68 (NEMA Type –20 to +130 °C
4x)
(–4 to +266 °F)

M12 plug, 4-pin, 316 (PROFIBUS® PA,
Ethernet-APL™, IO-Link®

IP67

–40 to +105 °C
(–40 to +221 °F)

-

IP67

–30 to +90 °C
(–22 to +194 °F)

-

IP67

–40 to +105 °C
(–40 to +221 °F)

-

Type
Cable gland, polyamide blue (indication
of Ex-i circuit)

Cable gland, polyamide

½" NPT,
M20x1.5
M20x1.5

M12 plug, 8-pin, 316
7/8" plug, 4-pin, 316 (FOUNDATION ™
Fieldbus, PROFIBUS® PA)
1)

½" NPT

½" NPT,
M20x1.5

5 to 9 mm (0.19 to 0.35 in)

Depending on product and configuration

Cable glands are not available for encapsulated, flameproof thermometers.

Extension neck

40

Extension neck in standard version or with optional quick-fastening iTHERM QuickNeck.
• Tool-free removal of the insert:
• Saves time/costs on frequently calibrated measuring points
• Wiring mistakes avoided
• IP69K protection class

Endress+Hauser

<!-- page 41 -->

8 (0.32)

NPT ½“

M24x1.5

E = 51 (2)

!9
(0.35)

3

E = 60 (2.36)

E
E

8
(0.32)

M24x1.5

15 (0.6)

4

G3/8"
G¼“

E = 28
(1.1)

15 (0.6)

M24x1.5

NPT ½“

8 (0.32)

G3/8"

E = 19.5
(0.77)

E

15 (0.6)

!9
(0.35)

NPT ½“

NPT ½“

E

M24x1.5

2

15 (0.6)

1

8 (0.32)

iTHERM ModuLine TM411

A0017953

 12
1
2
3
4

Endress+Hauser

Dimensions of extension neck type TE411, different versions, each with M24x1.5 or NPT ½" thread to the
terminal head

With G¼" external thread for compression fitting TK40, 3-A marked
With G3/8" union nut for thermowell version: ⌀6 mm (¼ in), ⌀12.7 mm (0.5 in) and tee thermowell and
elbow thermowell versions
Quick-fastening iTHERM QuickNeck for thermowell version: ⌀6 mm (¼ in), ⌀12.7 mm (0.5 in) and tee
thermowell or elbow thermowell versions
Quick-fastening iTHERM QuickNeck - top part, for installation in an existing thermowell with iTHERM
QuickNeck

41

<!-- page 42 -->

iTHERM ModuLine TM411

Thermowell

Process connections
All dimensions in mm (in).
Type

Version

Aseptic pipe union according to DIN
11864-1, Form A

!D

Dimensions
d

D

i

a

h

DN25

26 mm
(1.02 in)

42.9 mm
(1.7 in)

26 mm
(1.02 in)

29 mm
(1.14 in)

9 mm
(0.35 in)

DN40

38 mm
(1.5 in)

54.9 mm
(2.16 in)

38 mm
(1.5 in)

41 mm
(1.61 in)

10 mm
(0.39 in)

Technical properties
• Pmax. = 40 bar (580 psi)
• 3-A marked and EHEDG certified
• ASME BPE compliance

h
U
!i !a
!d
A0009562

Weld-in
Type of fitting 1)

Model
Weld-in adapter

d = 12.7 mm (¹⁄₂ in), U = immersion length
from lower edge of thread,
T = 12 mm (0.47 in)

2: Cylindrical 3)

d x h = 12 mm (0.47 in) x 40 mm (1.57 in),
T = 55 mm (2.17 in)

3: Cylindrical

d x h = 30 mm (1.18 in) x 40 mm (1.57 in)

4: Sphericalcylindrical

d x h = 30 mm (1.18 in) x 40 mm (1.57 in)

5: Spherical

d = 25 mm (0.98 in)
h = 24 mm (0.94 in)

1: Cylindrical

T
T
!d

h

!d

!d

h

U
U

U
1

2

Dimensions

2)

3

Technical properties

• Pmax. depends on the weld-in
process
• With 3-A symbol and
EHEDG certification
• ASME BPE compliance

T
!d
h

T

h

!d
U

U
4

5
A0009569

1)
2)
3)

42

Options depend on product and configuration
For thermowell 12.7 mm (½ in)
For thermowell 6 mm (¼ in)

Endress+Hauser

<!-- page 43 -->

iTHERM ModuLine TM411

Releasable process connection
Type

Technical properties

Sanitary connection according to DIN 11851

!D

B
A
U

• 3-A marked and EHEDG certified
(only with EHEDG-certified and selfcentering sealing ring).
• ASME BPE compliance

!i !a
!d

1
R0.4

2
R0.4
A0009561

1
2

Centering ring
Sealing ring
Version 1)

Pmax.

D

A

B

i

a

44 mm
(1.73 in)

30 mm
(1.18 in)

10 mm
(0.39 in)

26 mm
(1.02 in)

29 mm
(1.14 in)

40 bar (580 psi)

DN32

50 mm
(1.97 in)

36 mm
(1.42 in)

10 mm
(0.39 in)

32 mm
(1.26 in)

35 mm
(1.38 in)

40 bar (580 psi)

DN40

56 mm
(2.2 in)

42 mm
(1.65 in)

10 mm
(0.39 in)

38 mm
(1.5 in)

41 mm
(1.61 in)

40 bar (580 psi)

DN50

68 mm
(2.68 in)

54 mm
(2.13 in)

11 mm
(0.43 in)

50 mm
(1.97 in)

53 mm
(2.1 in)

25 bar (363 psi)

DN25

1)

Dimensions

Pipes in accordance with DIN 11850

Endress+Hauser

43

<!-- page 44 -->

iTHERM ModuLine TM411

Version 1)

Type

d

Clamp according to DIN 32676 3)

Microclamp 4) DN8
(0.5"), Form A

!D

!a

U

Tri-clamp DN8
(0.5"), Form B

!d
!D

R0.5

0.4

1.6

.2
R1

0.8 ± 0.1

U

Dimensions
D
25 mm
(0.98 in)

a
-

Clamp DN10-20,
Form B

34 mm
(1.34 in)

16 to 25.3 mm
(0.63 to 0.99 in)

Clamp DN25-40
(1"-1.5"), Form B

50.5 mm
(1.99 in)

29 to 42.4 mm
(1.14 to 1.67 in)

Clamp DN50 (2"),
Form B

64 mm
(2.52 in)

44.8 to 55.8 mm
(1.76 to 2.2 in)

Clamp DN63.5
(2.5"), Form B

77.5 mm
(3.05 in)

68.9 to 75.8 mm
(2.71 to 2.98 in)

Clamp DN70-76.5
(3"), Form B

91 mm
(3.58 in)

> 75.8 mm (2.98 in)

2.16 ± 0.1

R0.8

A

!d

2)

Technical properties

• Pmax. = 16 bar (232
psi), depends on
clamp ring and
suitable seal
• With 3-A symbol
• Pmax. = 16 bar (232
psi), depends on
clamp ring and
suitable seal
• 3-A marked and
EHEDG certified (in
connection with
Combifit seal)
• Can be used with
'Novaseptic Connect
(NA Connect)'
which enables
flush-mount
installation

Conformity
DIN 32676 5)
DIN 32676
ASME BPE Type B;
DIN 32676
ASME BPE Type B;
DIN 32676
ASME BPE Type B;
DIN 32676
ASME BPE Type B;
DIN 32676

Form A

.8

R0

Form B
A0009566

Form A: In compliance with ASME BPE
Type A
Form B: In compliance with ASME BPE
Type B and DIN 32676
1)
2)
3)
4)
5)

44

Options depend on product and configuration
Pipes in accordance with ISO 2037 and BS 4825 Part 1
replaces ISO 2852
Microclamp (not contained in DIN 32676); no standard pipes
Groove diameter = 20 mm

Endress+Hauser

<!-- page 45 -->

iTHERM ModuLine TM411

Version 1)

Type

Technical properties

Metal sealing system

!6
(¼)

14
(0.55)

8 (0.3)

!10
(0.4)

M12
x1.5

20°

U

22 (0.87)
T
A0009574

Pmax. = 16 bar (232 psi)

M12x1.5

!18
(0.71)

!6 (¼)

 13

14
(0.55)

Thermowell diameter 6 mm (¼ in)

8 (0.31)

 Maximum torque = 10 Nm (7.38 lbf ft)

G½”

22.5°

U

37 (1.46)
T
A0020856

G½"

"18 (0.71)
"9 (0.35)

 14

14
(0.55)

8 (0.31)
Pmax. = 16 bar (232 psi)

G½”

Thermowell diameter 9 mm (0.35 in)

45°

 Maximum torque = 10 Nm (7.38 lbf ft)

37 (1.46)
T

U

"18 (0.71)
"8 (0.31)

A0009571

20 (0.8)

14
(0.55)

8 (0.31)
Pmax. = 16 bar (232 psi)

G½”

45°

Thermowell diameter 8 mm (0.31 in)

 Maximum torque = 10 Nm (7.38 lbf ft)

3 (0.12)

37 (1.46)
U

T
A0022326

1)

Options depend on product and configuration

Endress+Hauser

45

<!-- page 46 -->

iTHERM ModuLine TM411

Type

Version

Technical properties

Process adapter

35 (1.38)

20 5 (0.20)
(0.79)

!50 (1.97)
!45 (1.77)

D45

U
A0034881

Unit of measurement mm (in)

Type
Thread according to ISO 228 (for
Liquiphant weld-in adapter)

L1

L1 thread length

A

1 (SW/AF)

G¾" for
FTL20/31/33
adapter

1

G

Dimensions

Version G

16 mm (0.63 in)

25.5 mm (1 in)

32

18.6 mm
(0.73 in)

29.5 mm
(1.16 in)

41

G¾" for FTL50
adapter

A

G1" for FTL50
adapter

U
A0009572

Type

Dimensions

Version

d

A

B

M

h

69 mm
(2.72 in)

99.5 mm
(3.92 in)

82 mm
(3.23 in)

2xM8

19 mm
(0.75 in)

Technical properties

• Pmax. = 25 bar (362 psi)
at max. 150 °C (302 °F)
• Pmax. = 40 bar (580 psi)
at max. 100 °C (212 °F)
• For more information
about hygienic
compliance in
conjunction with
FTL31/33/50 adapters,
see Technical
Information TI00426F.

Technical properties

APV Inline

!B

M
DN50

h

• Pmax. = 25 bar (362 psi)
• 3-A marked and EHEDG certified
• ASME BPE compliance

U

!d
!A

A0018435

Version 1)

Varivent®
!A
!B

h

Type

Dimensions

Technical properties

D

A

B

h

Type B

31 mm
(1.22 in)

105 mm
(4.13 in)

-

22 mm
(0.87 in)

Type F

50 mm
(1.97 in)

145 mm
(5.71 in)

135 mm
(5.31 in)

24 mm
(0.95 in)

Pmax.

10 bar
(145 psi)

• With 3-A symbol and EHEDG
certification
• ASME BPE compliance

U
!D
A0021307

46

Endress+Hauser

<!-- page 47 -->

iTHERM ModuLine TM411

Dimensions

Version 1)

Type

Type N

Technical properties

D

A

B

h

68 mm
(2.67 in)

165 mm
(6.5 in)

155 mm
(6.1 in)

24.5 mm
(0.96 in)

Pmax.

VARINLINE housing connection flange is suitable for welding into the conical or torispherical head in tanks or containers with a small
 The
diameter (≤ 1.6 m (5.25 ft)) and up to a wall thickness of 8 mm (0.31 in).
®

Varivent® Type F cannot be used for installations in pipes in combination with the VARINLINE® housing connection flange.

1)

Options depend on product and configuration

Type

Technical properties

Varivent® for VARINLINE® housing for installation in pipes

!i
!a

U

• With 3-A symbol and
EHEDG certification
• ASME BPE compliance

!D

A0009564

Version 1)

Type N, according to DIN
11866, series A

Type N, according to EN
ISO 1127, series B

Type N, according to DIN
11866, series C
Type N, according to DIN
11866, series C

Endress+Hauser

Dimensions
D

68 mm (2.67 in)

68 mm (2.67 in)

68 mm (2.67 in)

68 mm (2.67 in)

i

a

DN40: 38 mm (1.5 in)

DN40: 41 mm (1.61 in)

DN50: 50 mm (1.97 in)

DN50: 53 mm (2.1 in)

DN65: 66 mm (2.6 in)

DN65: 70 mm (2.76 in)

DN80: 81 mm (3.2 in)

DN80: 85 mm (3.35 in)

DN100: 100 mm (3.94 in)

DN100: 104 mm (4.1 in)

DN125: 125 mm (4.92 in)

DN125: 129 mm (5.08 in)

DN150: 150 mm (5.9 in)

DN150: 154 mm (6.06 in)

38.4 mm (1.51 in)

42.4 mm (1.67 in)

44.3 mm (1.75 in)

48.3 mm (1.9 in)

56.3 mm (2.22 in)

60.3 mm (2.37 in)

72.1 mm (2.84 in)

76.1 mm (3 in)

82.9 mm (3.26 in)

42.4 mm (3.5 in)

108.3 mm (4.26 in)

114.3 mm (4.5 in)

OD 1½": 34.9 mm (1.37 in)

OD 1½": 38.1 mm (1.5 in)

OD 2": 47.2 mm (1.86 in)

OD 2": 50.8 mm (2 in)

OD 2½": 60.2 mm (2.37 in)

OD 2½": 63.5 mm (2.5 in)

OD 3": 73 mm (2.87 in)

OD 3": 76.2 mm (3 in)

Pmax.

DN40 to DN65:
16 bar (232 psi)

DN80 to DN150:
10 bar (145 psi)

42.4 mm (1.67 in) to
60.3 mm (2.37 in):
16 bar (232 psi)
76.1 mm (3 in) to
114.3 mm (4.5 in):
10 bar (145 psi)

OD 1½" to OD 2½":
16 bar (232 psi)

OD 3" to OD 4": 10 bar (145 psi)

47

<!-- page 48 -->

iTHERM ModuLine TM411

Type

Technical properties

Type F, according to DIN
11866, series C
1)

50 mm (1.97 in)

OD 4": 97.6 mm (3.84 in)

OD 4": 101.6 mm (4 in)

OD 1": 22.2 mm (0.87 in)

OD 1": 25.4 mm (1 in)

16 bar (232 psi)

Options depend on product and configuration

Due to the small immersion length U, the use of iTHERM QuickSens inserts is recommended.
Tee thermowell, optimized (no welding, no dead legs)
Type of fitting 1)

Model
Tee thermowell for welding in as per DIN
11865 (series A, B and C)

Series
A

!18
!3.1
(0.12)

(0.71)

83 (3.26)

G3/8”

Series
B

!4.5

(0.18)
L

0.7 (0.03)

!D

s

1)
2)
3)

48

D

DN10 PN25

13 mm
(0.51 in)

DN15 PN25

19 mm
(0.75 in)

DN20 PN25

23 mm
(0.91 in)

DN25 PN25

29 mm
(1.14 in)

DN32 PN25

32 mm
(1.26 in)

DN13.5 PN25

13.5 mm
(0.53 in)

DN17.2 PN25

17.2 mm
(0.68 in)

s 2)

L

Technical properties

1.5 mm
(0.06 in)

1.6 mm
(0.063 in)
• Pmax. = 25 bar (362 psi)
• 3-A marked 3) and EHEDG
certified 3)
• ASME BPE compliance 3)

48 mm
(1.89 in)

DN21.3 PN25

21.3 mm
(0.84 in)

DN26.9 PN25

26.9 mm
(1.06 in)

DN33.7 PN25

33.7 mm
(1.33 in)

2 mm
(0.08 in)

DN12.7 PN25
(½")

12.7 mm
(0.5 in)

1.65 mm
(0.065 in)

DN19.05
PN25 (¾")

19.05 mm
(0.75 in)

DN25.4 PN25
(1")

25.4 mm
(1 in)

DN38.1 PN25
(1½")

38.1 mm
(1.5 in)

A0035898

Series
C

Dimensions in mm (in)

Options depend on product and configuration
Wall thickness
Applies to ≥ DN25. The radius ≥ 3.2 mm (¹⁄₈ in) cannot be maintained for smaller nominal diameters.

Endress+Hauser

<!-- page 49 -->

iTHERM ModuLine TM411

Elbow thermowell, optimized (no welding, no dead legs)
Dimensions

Version 1)

Type
Elbow thermowell for welding in as per
DIN 11865 (series A, B and C)

Series A

L2

D

83 (3.26)

0.7 (0.03)

s

L1

D!

Series B

!4.5
(0.18) !D
A0035899

Series C

1)
2)
3)

L2

s 2)

DN10 PN25

13 mm
(0.51 in)

22 mm 24 mm 1.5 mm
(0.87 in) (0.95 in) (0.06 in)

DN15 PN25

19 mm
(0.75 in)

25 mm (0.98 in)

DN20 PN25

23 mm
(0.91 in)

27 mm (1.06 in)

DN25 PN25

29 mm
(1.14 in)

30 mm (1.18 in)

DN32 PN25

35 mm
(1.38 in)

33 mm (1.3 in)

DN13.5
PN25

13.5 mm
(0.53 in)

22 mm 24 mm 1.6 mm
(0.87 in) (0.95 in) (0.063 in)

DN17.2
PN25

17.2 mm
(0.68 in)

24 mm (0.95 in)

DN21.3
PN25

21.3 mm
(0.84 in)

26 mm (1.02 in)

DN26.9
PN25

26.9 mm
(1.06 in)

29 mm (1.14 in)

DN33.7
PN25

33.7 mm
(1.33 in)

32 mm (1.26 in)

DN12.7
PN25 (½")

12.7 mm
(0.5 in)

DN19.05
PN25 (¾")

19.05 mm
(0.75 in)

22 mm 24 mm 1.65 mm
(0.87 in) (0.95 in)
(0.065 in)
25 mm (0.98 in)

DN25.4
PN25 (1")

25.4 mm
(1 in)

28 mm (1.1 in)

DN38.1
PN25 (1½")

38.1 mm
(1.5 in)

35 mm (1.38 in)

G3/8”

!3.1
(0.12)

L1

Technical properties

• Pmax. = 25 bar (362 psi)
• 3-A marked 3) and EHEDG
certified 3)
• ASME BPE compliance 3)

2.0 mm
(0.08 in)

Options depend on product and configuration
Wall thickness
Applies to ≥ DN25. The radius ≥ 3.2 mm (¹⁄₈ in) cannot be maintained for smaller nominal diameters.

Due to the short immersion length U, the use of iTHERM QuickSens inserts is generally
recommended for T-piece/elbow piece process connections according to DIN 11865.
Type

Version, dimensions D x h

Technical properties

Ingold connection

G1¼“

h
x

!D

4
(0.16)

25 mm (0.98 in) x 30 mm (1.18 in)
x = 1.5 mm (0.06 in)

25 mm (0.98 in) x 46 mm (1.81 in)
x = 6 mm (0.24 in)

Pmax. = 25 bar (362 psi)
A seal is included in the scope
of delivery. V75SR material:
Complies with FDA, 3-A
Sanitary Standard 18-03 Class
1 and USP Class VI

U
A0009573

Endress+Hauser

49

<!-- page 50 -->

iTHERM ModuLine TM411

Model

Type of fitting

SMS 1147

!A
!D
h
1
2
3

Dimensions

Technical properties

D

A

h

DN25

32 mm
(1.26 in)

35.5 mm
(1.4 in)

7 mm (0.28 in)

DN38

48 mm
(1.89 in)

55 mm
(2.17 in)

8 mm (0.31 in)

DN51

60 mm
(2.36 in)

65 mm
(2.56 in)

9 mm (0.35 in)
Pmax. = 6 bar (87 psi)

U
A0009568

1
2
3

Cap nut
Sealing ring
Counterpart connection

 The counterpart connection must fit the sealing ring and fix it in place.
Type

Version

Dimensions
A

B

D

d

h

D25
PN16

64 mm
(2.52 in)

50 mm
(1.97 in)

30.4 mm
(1.2 in)

7 mm
(0.28 in)

20 mm
(0.79 in)

D50
PN16

90 mm
(3.54 in)

70 mm
(2.76 in)

49.9 mm
(1.97 in)

9 mm
(0.35 in)

Technical properties

NEUMO BioControl

!B

M

h

• Pmax. = 16 bar (232 psi)
• With 3-A symbol
27 mm
(1.06 in)

U
D65
PN25

!D
!A

120 mm
(4.72 in)

95 mm
(3.74 in)

67.9 mm
(2.67 in)

11 mm
(0.43 in)

A0018497

The 316L compression fittings can only be used once due to deformation. This applies to all the
compression fitting components. A replacement compression fitting must be secured at another
point (grooves in thermowell).
PEEK compression fittings must never be used at a temperature that is lower than the
temperature present when the compression fitting is secured. This is because the fitting would
no longer be leak-tight as a result of heat contraction of the PEEK material.
SWAGELOK or similar fittings are strongly recommended for higher requirements.

50

Endress+Hauser

<!-- page 51 -->

iTHERM ModuLine TM411

Compression fitting
Type of fitting 1)

Model

Dimensions

Technical properties 2)

Spherical or cylindrical

di

D

h

Spherical
Sealing taper material
316L

6.3 mm
(0.25 in) 3)

25 mm
(0.98 in)

33 mm
(1.3 in)

• Pmax. = 50 bar (725 psi)
• Tmax. for 316L sealing taper
= +200 °C (+392 °F),
tightening torque = 40 Nm

33 mm
(1.3 in)

• Pmax. = 10 bar (145 psi)
• Tmax. for PEEK sealing taper
= +200 °C (+392 °F),
tightening torque = 10 Nm
• The TK40 PEEK sealing
taper is EHEDG tested and 3A marked

57 mm
(2.24 in)

• Pmax. = 10 bar (145 psi)
• Tmax. for ELASTOSIL®
sealing taper =
+200 °C (+392 °F),
tightening torque = 5 Nm
• The Elastosil® compression
fitting is EHEDG tested and
3-A marked

!d

h

!di

!D
A0058214

Compression fitting TK40 for weld-in

h

!di

Spherical
Sealing taper material
PEEK
Thread G¼"

!D
!d
!d
1

6.3 mm
(0.25 in) 3)

25 mm
(0.98 in)

2

A0018912

1 Movable
2
Fixed
6.2 mm
(0.24 in) 3)

!d

Cylindrical
Material of sealing taper
ELASTOSIL®
Thread G½"

h

!di

9.2 mm
(0.36 in)

30 mm
(1.18 in)

!D
A0058543

1)
2)
3)

Options depend on product and configuration
All the pressure specifications apply for cyclic temperature load
For insert or thermowell diameter Ød = 6 mm (0.236 in).

Endress+Hauser

51

<!-- page 52 -->

iTHERM ModuLine TM411

Shape of tip
The thermal response time, the reduction of the flow cross-section and the mechanical load that
occurs in the process are the criteria that matter when selecting the shape of the tip. Advantages of
using reduced or tapered thermometer tips:
• A smaller tip shape has less impact on the flow characteristics of the pipe carrying the medium.
• The flow characteristics are optimized, thereby increasing the stability of the thermowell.
• Endress+Hauser offers users a range of thermowell tips to meet every requirement:
• Reduced tip with ⌀4.3 mm (0.17 in) and ⌀5.3 mm (0.21 in): walls of lower thickness
significantly reduce the response times of the overall measuring point.
• Tapered tip with ⌀6.6 mm (0.26 in) and reduced tip with ⌀8 mm (0.31 in): walls of greater
thickness are particularly well suited to applications with a higher degree of mechanical load or
wear (e.g. pitting, abrasion etc.).
2

D2 = !5.3
(0.21)

!D1 =
!D2

!D1

!6.6

(0.26)
!6.4
(0.25)

!3.2
(0.13)

D2 = !6.6
(0.26)

!D1

32 (1.26)

(0.28)

!3.5
(0.14)

!3.2
(0.13)
D2 = !4.3
(0.17)

!D1

20 (0.8)

!7

20 (0.8)

20 (0.8)

!3.3
(0.13)

!D1 =
!D2

!D1

!D1

3

40 (1.6) 20
(0.8)

1

D2 = !8
(0.31)

D2 = !5.3
(0.21)

A0017174

 15

Thermowell tips available (reduced, straight or tapered)

Item no.

Thermowell (⌀D1)

Insert (⌀ID)

1

⌀6 mm (¹⁄₄ in)

Reduced tip

⌀3 mm (¹⁄₈ in)

2

⌀9 mm (0.35 in)

• Reduced tip with ⌀5.3 mm (0.21 in)
• Straight tip
• Tapered tip with ⌀6.6 mm (0.26 in)

• ⌀3 mm (¹⁄₈ in)
• ⌀6 mm (¹⁄₄ in)
• ⌀3 mm (¹⁄₈ in)

3

⌀12.7 mm (¹⁄₂ in)

• Reduced tip with ⌀5.3 mm (0.21 in)
• Straight tip
• Reduced tip with ⌀8 mm (0.31 in)

• ⌀3 mm (¹⁄₈ in)
• ⌀6 mm (¹⁄₄ in)
• ⌀6 mm (¹⁄₄ in)

It is possible to check the mechanical loading capacity as a function of the installation and
process conditions online using the Sizing Thermowell calculation tool in the Endress+Hauser
Applicator software. https://portal.endress.com/webapp/applicator

Certificates and approvals
Current certificates and approvals for the product are available at www.endress.com on the relevant
product page:

Materials in contact with
food/product (FCM)

52

1.

Select the product using the filters and search field.

2.

Open the product page.

3.

Select Downloads.

The materials of the thermometer in contact with food/product (FCM) comply with the following
European regulations:
• (EC) No. 1935/2004, Article 3, paragraph 1, Articles 5 and 17 on materials and articles intended
to come into contact with food.
• (EC) No. 2023/2006 on good manufacturing practice for materials and articles intended to come
into contact with food.
• (EU) No. 10/2011 on plastic materials and articles intended to come into contact with food.

Endress+Hauser

<!-- page 53 -->

iTHERM ModuLine TM411

• EHEDG certification, type EL CLASS I. EHEDG-certified/tested process connections. →  42
• 3-A authorization no. 1144, 3-A Sanitary Standard 74-07. Listed process connections. →  42
• ASME BPE (latest edition), certificate of conformity can be ordered for indicated options.
• FDA-compliant
• All surfaces in contact with the medium are free of animal derived ingredients (ADI/TSE) and do
not contain any materials derived from bovine or animal sources.
CRN approval

The CRN approval is only available for certain thermowell versions. These versions are identified and
displayed accordingly during the configuration of the device.
Detailed ordering information is available for your nearest sales organization
www.addresses.endress.com or in the Download Area under www.endress.com :
1.

Select the country

2.

Select Downloads

3.

In the search area: select Approvals/approval type

4.

Enter the product code or device

5.

Start the search

Surface purity

• Free from oil and grease for O2 applications, optional
• PWIS-free (PWIS = paint-wetting impairment substances as per DIL0301), optional

Material resistance

Material resistance - including resistance of housing - to the following Ecolab cleaning/disinfection
agents:
• P3-topax 66
• P3-topactive 200
• P3-topactive 500
• P3-topactive OKTO
• And demineralized water

Ordering information
Detailed ordering information is available from your nearest sales organization
www.addresses.endress.com or in the Product Configurator at www.endress.com:
1.

Select the product using the filters and search field.

2.

Open the product page.

3.

Select Configuration.
Product Configurator - the tool for individual product configuration
• Up-to-the-minute configuration data
• Depending on the device: direct input of information specific to the measuring point, such as
the measuring range or operating language
• Automatic verification of exclusion criteria
• Automatic creation of the order code and its breakdown in PDF or Excel output format
• Ability to order directly in the Endress+Hauser Online Shop

Accessories
The accessories currently available for the product can be selected at www.endress.com:

Endress+Hauser

1.

Select the product using the filters and search field.

2.

Open the product page.

3.

Select Spare parts & Accessories.

53

<!-- page 54 -->

iTHERM ModuLine TM411

Device-specific accessories

Accessory

Description

Welding boss with sealing taper
(metal - metal)

15 (0.6)

G½”

Order number:
• 71424800 (G½")
• 71405560 (M12x1.5)

34 (1.34)

16 (0.63)

!30 (1.18)

Welding boss for G½" and M12x1.5 thread
Metal-sealing; conical
Material of wetted parts: 316L/1.4435
Max. process pressure 16 bar (232 PSI)

A0006621

17 (0.67)

13 (0.51)

M12x1.5

!7.6 (0.3)
!20 (0.8)
A0018236

Dummy plug for G½” or M12x1.5 conical metal-sealing welding boss
Material: SS 316L/1.4435

8 (0.31)

Dummy plug

Order number:
• 71424800 (G½")
• 71535692 (M12x1.5)

1

37 (1.46)

G½”/
M12x1.5

!18
(0.71)

A0045726

1 Size across flats AF22

Weld-in adapter for Ingold process
connection
(OD25 mm (0.98 in)x50 mm
(1.97 in)

G 1¼”

Material of wetted parts: 316L/1.4435
Weight: 0.32 kg (0.7 lb)
Adapter for Ingold process connection with 3.1 material certificate, order
number: 71531585
Adapter for Ingold process connection, order number: 71531588

50 (1.97)

O-ring seal set
• Silicone O-ring in accordance with FDA CFR 21
• Maximum temperature: 230 °C (446 °F)
• Order number: 71220351

A0008956

54

Endress+Hauser

<!-- page 55 -->

iTHERM ModuLine TM411

Diameter ⌀D: 24 to 26 mm (0.94 to 1.02 in)
Material: Thermoplastic polyolefin - elastomer (TPE), free from
plasticizers
Maximum temperature: +150 °C (+302 °F)
Order number: 71275424

35 (1.38)

20 (0.79)

Flexible handle cap to cover the
QuickNeck bottom part

!D
A0027201

Weld-in adapter
For detailed information about the order code and hygienic compliance of the adapters and
spare parts, see the Technical Information (TI00426F).
Weld-in adapter

Material

Roughness µm (µin) process side

316L (1.4435)

≤1.5 (59.1)

316L (1.4435)

≤0.8 (31.5)

316L (1.4435)

≤0.8 (31.5)

316L (1.4435)

≤0.8 (31.5)

A0008246

G ¾, d=29 pipe-mounting

A0008251

G ¾, d=50 vessel-mounting

A0008256

G ¾", d=55, with flange

A0011924

G 1", d=53, without flange

Endress+Hauser

55

<!-- page 56 -->

iTHERM ModuLine TM411

316L (1.4435)

≤0.8 (31.5)

316L (1.4435)

≤0.8 (31.5)

A0008248

G 1", d=60, with flange

A0008253

G 1" adjustable

Maximum process pressure for the weld-in adapters:
• 25 bar (362 PSI) at maximum 150 °C (302 °F)
• 40 bar (580 PSI) at maximum 100 °C (212 °F)
Service-specific accessories

Modems/Edge devices
Commubox FXA195 USB/HART modem
Connects intrinsically safe 'smart transmitters' with a HART protocol to the USB interface of a
laptop/PC. This enables the remote operation of the transmitters with FieldCare.
Technical Information TI00404F
www.endress.com/fxa195
Software
DeviceCare SFE100
DeviceCare is an Endress+Hauser configuration tool for field devices using the following
communication protocols: HART, PROFIBUS DP/PA, FOUNDATION Fieldbus, IO/Link, Modbus, CDI
and Endress+Hauser Common Data Interfaces.
Technical Information TI01134S
www.endress.com/sfe100
FieldCare SFE500
FieldCare is a configuration tool for Endress+Hauser and third-party field devices based on DTM
technology.
The following communication protocols are supported: HART, WirelessHART, PROFIBUS,
FOUNDATION Fieldbus, Modbus, IO-Link, EtherNet/IP, PROFINET and PROFINET APL.
Technical Information TI00028S
www.endress.com/sfe500
Netilion
With the Netilion lloT ecosystem, Endress+Hauser enables the optimization of plant performance,
digitization of workflows, sharing of knowledge and improved collaboration. Drawing upon decades
of experience in process automation, Endress+Hauser offers the process industry an IIoT ecosystem
designed to effortlessly extract insights from data. These insights allow process optimization, leading
to increased plant availability, efficiency, reliability and ultimately a more profitable plant.
www.netilion.endress.com

56

Endress+Hauser

<!-- page 57 -->

iTHERM ModuLine TM411

Field Xpert SMT50
Universal, high-performance tablet PC for device configuration.
Technical Information TI01555S
www.endress.com/smt50
Field Xpert SMT77 via WLAN
Universal, high-performance tablet PC for device configuration in Ex Zone 1 areas.
Technical Information TI01418S
www.endress.com/smt77
SmartBlue app
SmartBlue from Endress+Hauser allows easy wireless field device configuration via Bluetooth® or
WLAN. By providing mobile access to diagnostic and process information, SmartBlue saves time,
even in hazardous and difficult-to-access environments.

A0033202

 16

Communication-specific
accessories

QR code for free Endress+Hauser SmartBlue app

Configuration kit TXU10
Configuration kit for PC-programmable transmitter - FDT/DTM-based plant asset management tool,
FieldCare/DeviceCare, and interface cable (4-pin connector) for PC with USB port.
For more information, please refer to: www.endress.com

Online tools

Product information about the entire life cycle of the device is available at:
www.endress.com/onlinetools

System components

Process indicators from the RIA product family
Easily readable process indicators with various functions: loop-powered indicators for displaying
4-20mA values, display of up to four HART variables, process indicators with control units, limit
value monitoring, sensor power supply, and galvanic isolation.
Universal application thanks to international hazardous area approvals, suitable for panel mounting
or field installation..
For more information, please refer to: www.endress.com
RN series active barrier
Single- or two-channel active barrier for safe separation of 0/4 to -20 mA standard signal circuits
with bidirectional HART transmission. In the signal duplicator option, the input signal is transmitted
to two galvanically isolated outputs. The device has one active and one passive current input; the
outputs can be operated actively or passively.
For more information, please refer to: www.endress.com
Data Manager of the RSG product family
Data Managers are flexible and powerful systems to organize process values. Up to 20 universal
inputs and up to 14 digital inputs for direct connection of sensors, optionally with HART, are
available as an option. The measured process values are clearly presented on the display and logged
safely, monitored for limit values and analyzed. The values can be forwarded via common
communication protocols to higher-level systems and connected to one another via individual plant
modules.
For more information, please refer to: www.endress.com

Endress+Hauser

57

<!-- page 58 -->

iTHERM ModuLine TM411

Documentation
The following document types are available in the Downloads area of the Endress+Hauser website
(www.endress.com/downloads):
For an overview of the scope of the associated Technical Documentation, refer to the following:
• Device Viewer (www.endress.com/deviceviewer): Enter the serial number from the
nameplate
• Endress+Hauser Operations app: Enter serial number from nameplate or scan matrix code on
nameplate.
Brief Operating Instructions
(KA)

Guide that takes you quickly to the 1st measured value
The Brief Operating Instructions contain all the essential information from incoming acceptance to
initial commissioning.

Operating Instructions (BA)

Reference document
These Operating Instructions contain all the information that is required in the various life cycle
phases of the device: from product identification, incoming acceptance and storage, to installation,
connection, operation and commissioning, through to troubleshooting, maintenance and disposal.

Safety Instructions (XA)

Depending on the approval, the following Safety Instructions (XA) are supplied with the device. They
are an integral part of the Operating Instructions.
The nameplate indicates the Safety Instructions (XA) that are relevant to the device.

Functional Safety Manual
(FY)

Depending on the SIL approval, the Functional Safety Manual (FY) is an integral part of the
Operating Instructions and applies in addition to the Operating Instructions, Technical Information
and ATEX Safety Instructions.
The different requirements that apply for the protective function are described in the
Functional Safety Manual (FY).

58

Endress+Hauser

<!-- page 59 -->



<!-- page 60 -->

*71721393*
71721393

www.addresses.endress.com
