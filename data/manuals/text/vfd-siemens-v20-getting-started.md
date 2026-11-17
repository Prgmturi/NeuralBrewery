---
id: vfd-siemens-v20-getting-started
product: Siemens SINAMICS V20
component: Inverter dell'agitatore
tags: M1
---

<!-- page 1 -->

 SINAMICS V20 Inverter

___________________
Preface
1
___________________
Safety instructions

SINAMICS
SINAMICS V20 Inverter

2
___________________
Mechanical installation
3
___________________
Electrical installation
4
___________________
Commissioning
5
___________________
Parameter list

Getting Started

6
___________________
Fault and warning codes
7
___________________
Technical specifications
8
___________________
Ordering data

11/2012
A5E31623806

<!-- page 2 -->

Legal information
Warning notice system
This manual contains notices you have to observe in order to ensure your personal safety, as well as to prevent
damage to property. The notices referring to your personal safety are highlighted in the manual by a safety alert
symbol, notices referring only to property damage have no safety alert symbol. These notices shown below are
graded according to the degree of danger.
DANGER
indicates that death or severe personal injury will result if proper precautions are not taken.
WARNING
indicates that death or severe personal injury may result if proper precautions are not taken.
CAUTION
indicates that minor personal injury can result if proper precautions are not taken.
NOTICE
indicates that property damage can result if proper precautions are not taken.
If more than one degree of danger is present, the warning notice representing the highest degree of danger will
be used. A notice warning of injury to persons with a safety alert symbol may also include a warning relating to
property damage.

Qualified Personnel
The product/system described in this documentation may be operated only by personnel qualified for the specific
task in accordance with the relevant documentation, in particular its warning notices and safety instructions.
Qualified personnel are those who, based on their training and experience, are capable of identifying risks and
avoiding potential hazards when working with these products/systems.

Proper use of Siemens products
Note the following:
WARNING
Siemens products may only be used for the applications described in the catalog and in the relevant technical
documentation. If products and components from other manufacturers are used, these must be recommended
or approved by Siemens. Proper transport, storage, installation, assembly, commissioning, operation and
maintenance are required to ensure that the products operate safely and without any problems. The permissible
ambient conditions must be complied with. The information in the relevant documentation must be observed.

Trademarks
All names identified by ® are registered trademarks of Siemens AG. The remaining trademarks in this publication
may be trademarks whose use by third parties for their own purposes could violate the rights of the owner.

Disclaimer of Liability
We have reviewed the contents of this publication to ensure consistency with the hardware and software
described. Since variance cannot be precluded entirely, we cannot guarantee full consistency. However, the
information in this publication is reviewed regularly and any necessary corrections are included in subsequent
editions.

Siemens AG
Industry Sector
Postfach 48 48
90026 NÜRNBERG
GERMANY

A5E31623806
Ⓟ 11/2012 Technical data subject to change

Copyright © Siemens AG 2012.
All rights reserved

<!-- page 3 -->

Preface
Purpose of this manual
This manual provides you with information about the proper installation, basic
commissioning, and operation of SINAMICS V20 inverters.

SINAMICS V20 user documentation components
Document

Content

Available languages

Operating Instructions

Describes how you install, operate, and
commission the SINAMICS V20 inverter

English
Chinese
German
Italian
Korean
Portuguese
Spanish

Getting Started

(this manual)

English
Chinese
German
Italian
Korean
Portuguese
Spanish

Product Information

Describes how you install and operate the
following options or spare parts:


Parameter Loaders



Dynamic Braking Modules



External Basic Operator Panels (BOPs)



BOP Interface Modules



Shield Connection Kits



Replacement Fans

English
Chinese

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

3

<!-- page 4 -->

Preface

Technical support
Country

Hotline

China

+86 400 810 4288

Germany

+49 (0) 911 895 7222

Italy

+39 (02) 24362000

Brazil

+55 11 3833 4040

India

+91 22 2760 0150

Korea

+82 2 3450 7114

Turkey

+90 (216) 4440747

USA

+1 423 262 5710

Further service contact information: Support contacts
(http://support.automation.siemens.com/WW/view/en/16604999)

For ordering information, see Chapter "Ordering data (Page 61)".

SINAMICS V20 Inverter

4

Getting Started, 11/2012, A5E31623806

<!-- page 5 -->

Table of contents
Preface ...................................................................................................................................................... 3
1

Safety instructions ..................................................................................................................................... 7

2

Mechanical installation............................................................................................................................. 13

3

4

2.1

Mounting orientation and clearance.............................................................................................13

2.2

Mounting ......................................................................................................................................14

2.3

SINAMICS V20 Flat Plate variant ................................................................................................16

Electrical installation ................................................................................................................................ 19
3.1

Typical system connections .........................................................................................................19

3.2

Terminal description.....................................................................................................................21

Commissioning ........................................................................................................................................ 23
4.1

The built-in Basic Operator Panel (BOP).....................................................................................23

4.2

Editing parameters.......................................................................................................................25

4.3

Setting the 50 / 60 Hz selection menu .........................................................................................27

4.4
4.4.1
4.4.2
4.4.3
4.4.4
4.4.5

Quick commissioning ...................................................................................................................28
Structure of the setup menu.........................................................................................................28
Setting motor data........................................................................................................................29
Setting connection macros...........................................................................................................30
Setting application macros...........................................................................................................41
Setting common parameters........................................................................................................43

4.5

Restoring to defaults ....................................................................................................................44

5

Parameter list .......................................................................................................................................... 45

6

Fault and warning codes.......................................................................................................................... 55

7

Technical specifications........................................................................................................................... 57

8

Ordering data........................................................................................................................................... 61

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

5

<!-- page 6 -->

Table of contents

SINAMICS V20 Inverter

6

Getting Started, 11/2012, A5E31623806

<!-- page 7 -->

Safety instructions

1

Before installing and putting this equipment into operation, read the following safety
instructions and all the warning labels attached to the equipment carefully. Make sure that
the warning labels are kept in a legible condition and replace missing or damaged labels.

General
DANGER
Death from electric shock
Hazardous voltage remains present in the internal DC link capacitors when the power is
removed.
Touching terminals could lead to death from electric shock.
Do not touch any terminals within five minutes after the power supply for the inverter has
been switched off.
Protective earthing conductor current
The inverter can cause a DC current in the protective earthing conductor. Therefore, with
the earth leakage of the inverter having the potential to be greater than AC 3.5 mA, a fixed
earth connection is required and the minimum size of the protective earth conductor shall
comply with the local safety regulations for high leakage current equipment. The SINAMICS
V20 inverter has not been designed to work with a Residual Current Device (RCD) or
Residual Current Monitoring Device (RCM).
WARNING
Safe use of inverters
This equipment contains dangerous voltages and controls potentially dangerous rotating
mechanical parts. Loss of life, severe personal injury, or property damage could result if the
instructions contained in this manual are not followed.
Only suitable qualified personnel should work on this equipment, and only after becoming
familiar with all safety instructions, installation, commissioning, operation, and maintenance
procedures contained in this manual.
Any unauthorized modifications of the equipment are not allowed.
Protection in case of direct contact by means of voltages < 60 V (PELV = Protective Extra
Low Voltage according to EN 61800-5-1) is only permissible in areas with equipotential
bonding and in dry indoor rooms. If these conditions are not fulfilled, other protective
measures against electric shock must be applied, for example, protective insulation.
The inverter must always be grounded. If the inverter is not correctly grounded, this can
lead to extremely hazardous conditions which, under certain circumstances, can result in
death.
The device must be disconnected from the electrical power supply before any connections
with the device are established or in any way altered.

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

7

<!-- page 8 -->

Safety instructions

Install the inverter on a metal mounting plate in a control cabinet. The mounting plate has to
be unpainted and with a good electrical conductivity.
It is strictly prohibited for any mains disconnection to be performed on the motor-side of the
system, if the inverter is in operation and the output current is not zero.
Take particular notice of the general and regional installation and safety regulations
regarding work on dangerous voltage installations (for example, 61800-5-1) as well as the
relevant regulations regarding the correct use of tools and personal protective equipment
(PPE).
NOTICE
Static discharge
Static discharges on interfaces (for example, terminal or connector pins) can cause
malfunctions or defects. Therefore, when working with inverters or inverter components,
ESD protective measures should be observed.

Transport and storage
NOTICE
Excessive physical shocks or vibration
Protect the equipment from physical shocks or vibration during transport and storage. It is
important that the equipment is protected from water (rainfall) and excessive temperatures.

Installation
WARNING
Cable connection
Only permanently-wired input power connections are allowed. The equipment must be
earthed (IEC 536 Class 1, NEC and other applicable standards).
Faults with the control equipment
Wherever faults occurring in the control equipment can lead to substantial material damage
or even grievous bodily injury (that is, potentially dangerous faults), additional external
precautions must be taken to ensure or enforce safe operation, even when a fault occurs
(for example, independent limit switches, mechanical interlocks, etc.).
Requirements for United States / Canadian installations (UL/cUL)
Suitable for use on a circuit capable of delivering not more than 40000 rms Symmetrical
Amperes, 480 Vac maximum for 400 V variants of inverters or 240 Vac maximum for 230 V
variants of inverters, when protected by UL/cUL-certified Class J fuses only. For each
frame size A to D use class 1 75 °C copper wire only.
This equipment is capable of providing internal motor overload protection according to
UL508C. In order to comply with UL508C, parameter P0610 must not be changed from its
factory setting of 6.

SINAMICS V20 Inverter

8

Getting Started, 11/2012, A5E31623806

<!-- page 9 -->

Safety instructions

For Canadian (cUL) installations the inverter mains supply must be fitted with any external
recommended suppressor with the following features:
 Surge-protective devices; device shall be a Listed Surge-protective device (Category
code VZCA and VZCA7)
 Rated nominal voltage 480/277 VAC (for 400 V variants) or 240 VAC (for 230 V
variants), 50/60 Hz, 3-phase (for 400 V variants) or 1-phase (for 230V variants)
 Clamping voltage VPR = 2000 V (for 400 V variants) / 1000 V (for 230 V variants), IN =
3 kA min, MCOV = 508 VAC (for 400 V variants) / 264 VAC (for 230V variants), SCCR =
40 kA
 Suitable for Type 1 or Type 2 SPD application
 Clamping shall be provided between phases and also between phase and ground
WARNING
Branch-circuit protective device
The opening of the branch-circuit protective device may be an indication that a fault current
has been interrupted. To reduce the risk of fire or electric shock, current-carrying parts and
other components of the controller should be examined and the controller should be
replaced if damaged. If burnout of the current element of an overload relay occurs, the
complete overload relay must be replaced.
CAUTION
Cable connection
Separate the control cables from the power cables as much as possible.
Keep the connecting cables away from rotating mechanical parts.
NOTICE
Motor supply voltage
Make sure that the motor is configured for the correct supply voltage.
Inverter mounting
Mount the inverter vertically to a flat and non-combustible surface.

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

9

<!-- page 10 -->

Safety instructions

Commissioning
WARNING
High-voltage terminals
The following terminals can carry dangerous voltages even if the inverter is not operating:
- The mains input terminals L1, L2, L3, and PE terminal
- The motor terminals U, V, W, and output earth terminal
- The DC link terminals DC+ and DC- The braking resistor terminals R1 and R2 (Frame size D only)
This equipment must not be used as an "emergency stop" mechanism (see EN 60204,
9.2.5.4).
It is not allowed to open, connect or disconnect the equipment during its operation.

Operation
WARNING
Risks with incorrect parameterization
Certain parameter settings may cause the inverter to restart automatically after an input
power failure, for example, the automatic restart function.
Motor parameters must be accurately configured for motor overload protection to operate
correctly.
Use of braking resistor
If an unsuitable braking resistor is used, this could result in a fire and severe damage to
people, property and equipment. Use an appropriate braking resistor and install it correctly.
The temperature of a braking resistor increases significantly during operation. Avoid coming
into direct contact with braking resistors.
WARNING
Hot surface
During operation and for a short time after switching-off the inverter, the marked surfaces of
the inverter can reach a high temperature. Avoid coming into direct contact with these
surfaces.
CAUTION
Use of fuses
This equipment is suitable for use in a power system up to 40,000 symmetrical amperes
(rms), for the maximum rated voltage + 10 % when protected by an appropriate standard
fuse.

SINAMICS V20 Inverter

10

Getting Started, 11/2012, A5E31623806

<!-- page 11 -->

Safety instructions

NOTICE
Electromagnetic interference
Use of mobile radio devices (for example, telephones, walkie-talkies) in the immediate
vicinity of the devices (< 1.8 m) can interfere with the functioning of the equipment.

Repair
WARNING
Repair and replacement of equipment
Repairs on equipment may only be carried out by Siemens Service, by repair centers
authorized by Siemens or by authorized personnel who are thoroughly acquainted with all
the warnings and operating procedures contained in this manual.
Any defective parts or components must be replaced using parts contained in the relevant
spare parts lists.
Disconnect the power supply before opening the equipment for access.

Dismantling and disposal
NOTICE
Inverter disposal
The packaging of the inverter is re-usable. Retain the packaging for future use.
Easy-to-release screw and snap connectors allow you to break the unit down into its
component parts. You can recycle these component parts, dispose of them in accordance
with local requirements or return them to the manufacturer.

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

11

<!-- page 12 -->

Safety instructions

Residual risks
CAUTION
Residual risks associated with the control and drive components of a PDS
The control and drive components of a power drive system (PDS) are approved for
industrial and commercial use in industrial line supplies. Their use in public line supplies
requires a different configuration and/or additional measures.
These components may only be operated in closed housings or in higher-level control
cabinets with protective covers that are closed, and when all of the protective devices are
used.
These components may only be handled by qualified and trained technical personnel who
are knowledgeable and observe all of the safety information and instructions on the
components and in the associated technical user documentation.
When carrying out a risk assessment of a machine in accordance with the EU Machinery
Directive, the machine manufacturer must consider the following residual risks associated
with the control and drive components of a PDS.
1. Unintentional movements of driven machine components during commissioning,
operation, maintenance, and repairs caused by, for example:
– Hardware defects and / or software errors in the sensors, controllers, actuators, and
connection technology
– Response times of the controller and drive
– Operating and/or ambient conditions not within the scope of the specification
– Condensation / conductive contamination
– Parameterization, programming, cabling, and installation errors
– Use of radio devices / cellular phones in the immediate vicinity of the controller
– External influences / damage
2. Exceptional temperatures as well as emissions of noise, particles, or gas caused by, for
example:
– Component malfunctions
– Software errors
– Operating and/or ambient conditions not within the scope of the specification
– External influences / damage
3. Hazardous shock voltages caused by, for example:
– Component malfunctions
– Influence of electrostatic charging
– Induction of voltages in moving motors
– Operating and/or ambient conditions not within the scope of the specification
– Condensation / conductive contamination
– External influences / damage
4. Electrical, magnetic and electromagnetic fields generated in operation that can pose a
risk to people with a pacemaker, implants or metal replacement joints, etc. if they are
too close.
5. Release of environmental pollutants or emissions as a result of improper operation of
the system and/or failure to dispose of components safely and correctly.

SINAMICS V20 Inverter

12

Getting Started, 11/2012, A5E31623806

<!-- page 13 -->

2

Mechanical installation
2.1

Mounting orientation and clearance
The inverter must be mounted in an enclosed electrical operating area or a control cabinet.

Mounting orientation
Always mount the inverter in an upright position.

,QYHUWHU
,QYHUWHU

Mounting clearance
Top

≥ 100 mm

Bottom

≥100 mm (for frame sizes B to D, and frame size A without fan)
≥ 85 mm (for fan-cooled frame size A)
≥ 0 mm

6LGHRIFDELQHWHQFORVXUH

PP

DLU

PP

PP

PP

DLU

6LGHRIFDELQHWHQFORVXUH

Side

PP

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

13

<!-- page 14 -->

Mechanical installation
2.2 Mounting

2.2

Mounting

Mounting methods

Applicable frame sizes

Remarks

Cabinet panel mounting

Frame sizes A to D

The inverter is mounted directly on the surface of the cabinet
panel.

Push-through mounting

Frame sizes B to D

The inverter is mounted with the heatsink extended through
the back of the cabinet panel.

Outline dimensions and drill patterns (cabinet panel mounting)
Frame size C
184
182
169
108


















Frame size D
240
206.5
172.5
98









Drill
pattern

+

Frame size B
140
160
164.5
106



+

'
'

Frame size A
90
150
166
145.5 (114.5*)
-



:

(Unit: mm)
W
H
H1
D
D1

H1: height of frame size A with
fan

Fixings:

Fixings:

D1: depth inside the cabinet for
push-through mounting

4 x M4 screws

4 x M5 screws

4 x M4 nuts

4 x M5 nuts

4 x M4 washers

4 x M5 washers

Tightening torque: 1.8 Nm ± 10%

Tightening torque: 2.5 Nm ± 10%

* Depth of Flat Plate inverter (400 V 0.75 kW variant only)

Drill patterns and cut-outs (push-through mounting)
Frame size C








&XWRXWDUHD




&XWRXWDUHD




















&XWRXW
DUHD

Frame size D




Frame size B
Drill pattern and cutout (mm)

Fixings

4 x M4 screws

4 x M5 screws

4 x M5 screws

Tightening torque

1.8 Nm ± 10%

2.5 Nm ± 10%

2.5 Nm ± 10%

SINAMICS V20 Inverter

14

Getting Started, 11/2012, A5E31623806

<!-- page 15 -->

Mechanical installation
2.2 Mounting

Mounting steps (push-through mounting)










3XVKRQHVLGHRIWKHKHDWVLQNWKURXJKWKHEDFNRIWKHFDELQHW
SDQHO



0RYHWKHKHDWVLQNWRZDUGVWKHHGJHRIWKHFXWRXWDUHDXQWLOWKH
FRQFDYHGVORWRIWKHKHDWVLQNHQJDJHVZLWKWKHHGJHRIWKH
FXWRXWDUHD



3XVKWKHRWKHUVLGHRIWKHKHDWVLQNWKURXJKWKHEDFNRIWKH
FDELQHWSDQHO



0RYHWKHKHDWVLQNWRZDUGVWKHHGJHRIWKHFXWRXWDUHDXQWLO
VXIILFLHQWVSDFHIRUSXVKLQJWKHHQWLUHKHDWVLQNWKURXJKWKHEDFN
RIWKHFDELQHWSDQHOLVOHIW



3XVKWKHHQWLUHKHDWVLQNWKURXJKWKHEDFNRIWKHFDELQHWSDQHO



$OLJQWKHIRXUPRXQWLQJKROHVLQWKHLQYHUWHUZLWKWKHFRUUHVSRQGL
QJKROHVLQWKHFDELQHWSDQHO)L[WKHDOLJQHGKROHVZLWKIRXU
VFUHZV



Note
A gap is reserved at the bottom of the cut-out area to allow fan removal from outside the
cabinet without removing the inverter.

*DSUHVHUYHGIRU
IDQUHPRYDO

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

15

<!-- page 16 -->

Mechanical installation
2.3 SINAMICS V20 Flat Plate variant

2.3

SINAMICS V20 Flat Plate variant
The SINAMICS V20 Flat Plate variant is designed to allow greater flexibility in the installation
of the inverter. Adequate measures must be taken to ensure the correct heat dissipation,
which may require an additional external heatsink outside the electrical enclosure.

WARNING
Additional heat load
Operation with an input voltage greater than 400 V and 50 Hz or with a pulse frequency
greater than 4 kHz will cause an additional heat load on the inverter. These factors must be
taken into account when designing the installation conditions and must be verified by a
practical load test.
CAUTION
Cooling considerations
The minimum vertical clearance of 100 mm above and below the inverter must be
observed. Stacked mounting is not allowed for the SINAMICS V20 inverters.

Technical data
Average power output
370 W

550 W

750 W

Operating temperature range

0 °C to 40 °C

Max. heatsink loss

24 W

27 W

31 W

Max. control loss *

9.25 W

9.25 W

9.25 W

Recommended thermal resistance of
heatsink

1.8 K/W

1.5 K/W

1.2 K/W

Recommended output current

1.3 A

1.7 A

2.2 A

* With I/O fully loaded

SINAMICS V20 Inverter

16

Getting Started, 11/2012, A5E31623806

<!-- page 17 -->

Mechanical installation
2.3 SINAMICS V20 Flat Plate variant

Installing
1. Prepare the mounting surface for the inverter using the dimensions given in Section
“Mounting (Page 14)".
2. Ensure that any rough edges are removed from the drilled holes, the flat plate heatsink is
clean and free from dust and grease, and the mounting surface and if applicable the
external heatsink are smooth and made of unpainted metal (steel or aluminium).
3. Apply a non-silicone heat transfer compound with a minimum thermal transfer co-efficient
of 0.9 W/m.K evenly to the rear surface of the flat plate heatsink and the surface of the
rear plate.
4. Mount the inverter securely using four M4 screws with a tightening torque of 1.8 Nm
(tolerance: ± 10%).
5. If it is required to use an external heatsink, first apply the paste specified in Step 3 evenly
to the surface of the external heatsink and the surface of the rear plate, and then connect
the external heatsink on the other side of the rear plate.
6. When the installation is completed, run the inverter in the intended application while
monitoring r0037[0] (measured heatsink temperature) to verify the cooling effectiveness.
The heatsink temperature must not exceed 90 °C during normal operation, after
allowance has been made for the expected ambient temperature range for the
application.
Example:
If the measurements are made in 20 °C ambient, and the machine is specified up to 40
°C, then the heatsink temperature reading must be increased by [40-20] = 20 °C, and the
result must remain below 90 °C.
If the heatsink temperature exceeds the above limit, then further cooling must be
provided (for example, with an extra heatsink) until the conditions are met.
Note
The inverter will trip with fault condition F4 if the heatsink temperature rises above 100
°C. This protects the inverter from potential damage due to high temperatures.

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

17

<!-- page 18 -->

Mechanical installation
2.3 SINAMICS V20 Flat Plate variant

SINAMICS V20 Inverter

18

Getting Started, 11/2012, A5E31623806

<!-- page 19 -->

3

Electrical installation
3.1

Typical system connections

Typical system connections
$&9WR9
$&9WR9

%23,QWHUIDFH0RGXOH
RSWLRQ

([WHUQDO%23
RSWLRQ

)XVH
3(

&RQWDFWRU

3(

/LQHUHDFWRU
RSWLRQ

3(

)LOWHU RSWLRQ

OK

3DUDPHWHU/RDGHU
RSWLRQ
%UDNLQJUHVLVWRU
RSWLRQ

([SDQVLRQSRUW

//1 9
3(
RU
3URWHFWLYH
//1/ 9
HDUWK

V20

7KLVRSWLRQLVRQO\IRUIUDPH
VL]H$%&
5

5 3(
'\QDPLFEUDNLQJ
PRGXOH RSWLRQ

3(

8 9 :

3(

5 5
'& '&

3(
'&

'&

2XWSXWUHDFWRU
RSWLRQ
:
9
8

0RWRU

3(

3URWHFWLYHHDUWK

For ordering information of available options and spare parts, see Chapter "Ordering data (Page 61)".
SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

19

<!-- page 20 -->

Electrical installation
3.1 Typical system connections

Recommended fuse types
Frame size

400 V

Recommended fuse type

Frame size

CE-compliant (Siba
URZ)

UL-compliant

A

50 124 34 (16 A)

15 A 600 VAC, class J

Recommended fuse type
CE-compliant (Siba UL-compliant
URZ)

230 V

A

3NA3805 (16 A)

15 A 600 VAC, class J

B

50 124 34 (20 A)

20 A 600 VAC, class J

B

3NA3812 (32 A)

30 A 600 VAC, class J

C

50 140 34 (30 A)

30 A 600 VAC, class J

C

3NA3820 (50 A)

50 A 600 VAC, class J

D

50 140 34 (63 A)

60 A 600 VAC, class J

Wiring diagram
FSD

FSA to FSC

3(
/
/
/

400 V

'& '&

5

5
3(

Main circuit

8
9

/
/

230 V

M

:

Control circuit
Digital outputs

Digital inputs
'2
',

',

',

',

',

',

'2

Transistor output

',

313

131

'2&

',

',&

',&

9

9

9

9

'21&

Relay output

'212

Analog output

Analog inputs

$2
9

9

$,
9
RS-485
3
1
9

$,

Expansion port

SINAMICS V20 Inverter

20

Getting Started, 11/2012, A5E31623806

<!-- page 21 -->

Electrical installation
3.2 Terminal description

3.2

Terminal description
0DLQVWHUPLQDOV
//1/
3(WHUPLQDO
9YDULDQWV

)UDPHVL]H$

([SDQVLRQSRUW

)UDPHVL]HV%DQG&

8VHUWHUPLQDOV
2XWSXWHDUWK
WHUPLQDO

$OLJQDIODWELWVFUHZGULYHU ELW
VL]H[PP ZLWKWKH
WHUPLQDO3XVKLWGRZQZDUGVRQ
WKHUHOHDVHOHYHUZLWKD
PD[LPXPIRUFHRI1DQG
LQVHUWWKHFRQWUROZLUHIURP
EHORZ

)UDPHVL]H'

3(WHUPLQDO
'&WHUPLQDOV
'&'&
%UDNLQJUHVLVWRUWHUPLQDOV
55

0RWRUWHUPLQDOV
89:

User terminals:
7UDQVLVWRURXWSXW 5HOD\RXWSXW
9

$,

$,

$2

9

3

1

',

',

',

',

',&

9

9





























56

$QDORJLQSXWV

'2 '2 '2 '2 '2
1&
12
&



'LJLWDOLQSXWV

5HIHUHQFHSRWHQWLDOIRU
DQDORJ,2DQG56









'LJLWDORXWSXWV
5HIHUHQFHSRWHQWLDOIRU
GLJLWDOLQSXWV

$QDORJRXWSXW

Recommended cable cross-sections and screw tightening torques
Frame
size

Mains and PE terminals

Rated output
power

Cable crosssection
400 V
A
B

0.37 to 0.75 kW
1.1 to 2.2 kW
3.0 to 4.0 kW

1.0 mm2
1.5 mm2
2.5 mm2

Screw tightening torque
(tolerance: ± 10%)
1.0 Nm

Motor / DC / braking resistor / output earth
terminals
Cable crosssection
1.0 mm2

Screw tightening torque
(tolerance: ± 10%)
1.0 Nm

1.5 mm2
2.5 mm2

1.5 Nm

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

21

<!-- page 22 -->

Electrical installation
3.2 Terminal description
Frame
size

Rated output
power

Mains and PE terminals
Cable crosssection

C
D
230 V
A

B
C

5.5 kW
7.5 kW
11 to 15 kW

4.0 mm2
6.0 mm2
10 mm2

0.12 to 0.25 kW
0.37 to 0.55 kW
0.75 kW

1.5 mm2
2.5 mm2
4.0 mm2

1.1 to 1.5 kW
2.2 to 3.0 kW

6.0 mm2 *
10 mm2

Screw tightening torque
(tolerance: ± 10%)
2.4 Nm

Motor / DC / braking resistor / output earth
terminals
Cable crosssection
4.0 mm2
6.0 mm2
10 mm2

Screw tightening torque
(tolerance: ± 10%)
2.4 Nm

1.0 Nm

1.0 mm2

1.0 Nm

2.4 Nm

2.5 mm2
4.0 mm2

1.5 Nm
2.4 Nm

* With a UL-certified, suitable fork crimp

NOTICE
Damage to the mains terminals
During electrical installation of the inverter frame size A / B, use stranded cables / cables
with UL-certified, suitable fork crimps rather than solid cables / cables with pin crimps for
mains terminal connection.
&DEOHZLWK
8/FHUWLILHGIRUN
FULPS

&DEOHZLWK
SLQFULPS

6WUDQGHGFDEOH

6ROLGFDEOH

Maximum motor cable lengths
Maximum cable length

Inverter variant
Without output reactor
400 V
230 V

With output reactor

Unshielded cable

Shielded cable

Unshielded cable

Shielded cable

50 m
50 m

25 m (10 m*)
25 m (10 m*)

150 m
200 m

150 m
200 m

* For filtered variants of frame size A inverters only.

Permissible I/O terminal cable cross sections
Cable type

Permissible cable cross section

Solid or stranded cable
Ferrule without insulating sleeve
Ferrule with insulating sleeve

0.5 to 1.5 mm2
0.5 to 1.0 mm2
0.5 mm2

SINAMICS V20 Inverter

22

Getting Started, 11/2012, A5E31623806

<!-- page 23 -->

4

Commissioning
4.1

The built-in Basic Operator Panel (BOP)
$ODUP

5HYHUVH
5XQQLQJ

)DXOW

$872+$1'-2*PRGH

6WDWXV/('

/&'
GLVSOD\

83
V

A

Hz

1/min kW

%

'2:1
M

6723

OK

)81&7,21
2.

581

Menu structure
50 / 60 Hz Selection
Menu

First power-up or after factory reset
V 

M
OK



Subsequent power-up

V

M
M

Setup
Menu

!V

V

Display
Menu

Parameter
Menu

M

!V
2XWSXWIUHTXHQF\+]

0RWRUGDWD

M

OK

V

(GLWRUYLHZDOODYDLODEOH
SDUDPHWHUV

V

2XWSXWYROWDJH9
&RQQHFWLRQPDFUR
OK

M

V

V

0RWRUFXUUHQW$

$SSOLFDWLRQPDFUR
M

V

OK

V

OK

V

9GF9

&RPPRQSDUDPHWHUV

M

V

6HWSRLQW
OK

V

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

23

<!-- page 24 -->

Commissioning
4.1 The built-in Basic Operator Panel (BOP)

Button functions
Stops the inverter
Single press

OFF1 stop reaction: the inverter brings the motor to a standstill in the rampdown time set in parameter P1121.
Note:
If configured to be an OFF1 stop, this button is inactive in AUTO mode.

Double press (< 2 s) or
OFF2 stop reaction: the inverter allows the motor to coast to a standstill
long press ( > 3 s)
without using any ramp-down timings.
Starts the inverter
) displays.
If the inverter is started in HAND / JOG mode, the inverter running icon (
Note:
This button is inactive if the inverter is configured for control from terminals (P0700 = 2, P1000 = 2) and
is in AUTO mode.
Multi-function button
Short press ( < 2 s)

M





Enters the parameter setting menu or moves to the next screen
Restarts the digit by digit editing on the selected item
If pressed twice in digit by digit editing, returns to the previous screen
without changing the item being edited

Long press ( > 2 s)




Returns to the status screen
Enters the setup menu

Short press ( < 2 s)





Switches between status values
Enters edit value mode or change to the next digit
Clears faults

OK

M

+

OK

Long press ( > 2 s)
 Quick parameter number or value edit
Hand / Jog / Auto
Press to switch between different modes:
M

M

Auto mode

(No icon)





OK

OK

M

Hand mode
(With hand icon)



OK

Jog mode

(With flashing hand icon)

Note:
Jog mode is only available if the motor is stopped.





+

When navigating a menu, it moves the selection up through the screens available.
When editing a parameter value, it increases the displayed value.
When the inverter is in RUN mode, it increases the speed.
Long press (> 2 s) of the key quickly scrolls up through parameter numbers, indices, or values.

 When navigating a menu, it moves the selection down through the screens available.
 When editing a parameter value, it decreases the displayed value.
 When the inverter is in RUN mode, it decreases the speed.
 Long press (> 2 s) of the key quickly scrolls down through parameter numbers, indices, or values.
Reverses the direction of rotation of the motor. Pressing the two keys once activates reverse motor
rotation. Pressing the two keys once again deactivates reverse rotation of the motor. The reserve icon (
) on the display indicates that the output speed is opposite to the setpoint.

SINAMICS V20 Inverter

24

Getting Started, 11/2012, A5E31623806

<!-- page 25 -->

Commissioning
4.2 Editing parameters

Inverter status icons
Inverter has at least one pending fault.
Inverter has at least one pending alarm.
:

Inverter is running (motor frequency may be 0 rpm).

(flashing):

Inverter may be energized unexpectedly (for example, in frost protection
mode).

Motor rotates in the reversed direction.

4.2

:

Inverter is in HAND mode.

(flashing):

Inverter is in JOG mode.

Editing parameters

Normal editing of parameters
Note
Pressing
or
for longer than two seconds to quickly increase or decrease the
parameter numbers or indexes is only possible in the parameter menu.
This editing method is best suited when small changes are required to parameter numbers,
indexes, or values.
● To increase or decrease the parameter number, index, or value, press
than two seconds.

or

● To quickly increase or decrease the parameter number, index, or value, press
for longer than two seconds.

for less
or

● To confirm the setting, press OK .
● To cancel the setting, press M .

Digit-by-digit editing
Note
Digit-by-digit editing of parameter numbers or indexes is only possible in the parameter
menu.
Digit-by-digit editing can be performed on parameter numbers, parameter indexes, or
parameter values. This editing method is best suited when large changes are required to
parameter numbers, indexes, or values. For information about the inverter menu structure,
refer to Section "The built-in Basic Operator Panel (BOP) (Page 23)".

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

25

<!-- page 26 -->

Commissioning
4.2 Editing parameters

Example 1:

Example 2:

Example 3:

Editing parameter numbers

Editing parameter indices

Editing parameter values

If a parameter is an array, edit indices
as illustrated below. For example,
change r0947[0] to r0947[63]:

OK

V

!V

M

V

OK

V

M

V

OK

!V

M

OK

V

OK

V

OK

!V

OK

V

OK

V

M

OK

V

V
M



M

M

OK

V

V

M


OK

'RXEOHSUHVV

V

'RXEOHSUHVV

M

'RXEOHSUHVV

M

V

V


OK

OK

V

OK

V

V

3DUDPHWHUYDOXH
LQGH[

3DUDPHWHUYDOXH
HGLW

SINAMICS V20 Inverter

26

Getting Started, 11/2012, A5E31623806

<!-- page 27 -->

Commissioning
4.3 Setting the 50 / 60 Hz selection menu

4.3

Setting the 50 / 60 Hz selection menu
This menu is used to set the motor base frequency according to which region of the world
that the motor is used. The menu is visible only on first power-up or after a factory reset
(P0970).
The motor base frequency can also be selected by changing P0100 to the desired value.

)LUVWSRZHURQIDFWRU\
UHVHW

50 / 60 Hz selection menu
Hz

&RQILUPWKHVHOHFWLRQ
OK

Hz

Hz

"

V

Setup
Menu

KS"

"

([LWZLWKRXWPDNLQJD
VHOHFWLRQ
M

V 



Display
Menu

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

27

<!-- page 28 -->

Commissioning
4.4 Quick commissioning

4.4

Quick commissioning
Note
This section describes how to perform the quick commissioning through the setup menu. If
you are used to commissioning the inverter by setting parameters of your choice in the
parameter menu, refer to the SINAMICS V20 Inverter Operating Instructions for a detailed
description.

4.4.1

Structure of the setup menu
Parameter
Menu

M

M

!V

V
Display
Menu

M

M

!V

!V

Setup
Menu



0RWRUGDWD

M

V

&RQQHFWLRQPDFUR

M



V

$SSOLFDWLRQPDFUR

M



V

&RPPRQSDUDPHWHUV

M



V

SINAMICS V20 Inverter

28

Getting Started, 11/2012, A5E31623806

<!-- page 29 -->

Commissioning
4.4 Quick commissioning

4.4.2

Setting motor data

Text menu
If you set P8553 to 1, parameter numbers in this menu are replaced with short text.

Setting parameters
Parameter
P0100

Access
level

Function

1

50 / 60 Hz selection

Text menu
(if P8553 = 1)
(EU - US)

=0: Europe [kW], 50 Hz (factory default)
=1: North America [hp], 60 Hz
=2: North America [kW], 60 Hz
P0304[0] ●

1

Rated motor voltage [V]

(MOT V)

Note that the input of rating plate data must correspond with
the wiring of the motor (star / delta)
P0305[0] ●

1

Rated motor current [A]

(MOT A)

Note that the input of rating plate data must correspond with
the wiring of the motor (star / delta)
P0307[0] ●

1

Rated motor power [kW / hp]

P0100 = 0 or 2:

(MOT P)

P0100 =1:

(MOT HP)

If P0100 = 0 or 2, motor power unit = [kW]
If P0100 = 1, motor power unit = [hp]

P0308[0] ●

1

Rated motor power factor (cosφ)

(M COS)

Visible only when P0100 = 0 or 2
P0309[0] ●

1

Rated motor efficiency [%]

(M EFF)

Visible only when P0100 = 1
Setting 0 causes internal calculation of value.
P0310[0] ●

1

Rated motor frequency [Hz]

(M FREQ)

P0311[0] ●

1

Rated motor speed [RPM]

(M RPM)

P1900

2

Select motor data identification

(MOT ID)

= 0: Disabled
= 2: Identification of all parameters in standstill
Note: "●" indicates that the value of this parameter must be entered according to the rating plate of the motor.

See also
Parameter list (Page 45)
SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

29

<!-- page 30 -->

Commissioning
4.4 Quick commissioning

4.4.3

Setting connection macros
NOTICE
Connection macro settings
When commissioning the inverter, the connection macro setting is a one-off setting. Make
sure that you proceed as follows before you change the connection macro setting to a
value different from your last setting:
1. Do a factory reset (P0010 = 30, P0970 = 1)
2. Repeat the quick commissioning and change the connection macro
Failure to observe may cause the inverter to accept the parameter settings from both the
currently and the previously selected macros, which may lead to undefined and
unexplainable inverter operation.
However, communication parameters P2010, P2011, P2021 and P2023 for connection
macros Cn010 and Cn011 are not reset automatically after a factory reset. If necessary,
reset them manually.
After changing P2023 setting for Cn010 or Cn011, power-cycle the inverter. During the
power-cycle, wait until LED has gone off or the display has gone blank (may take a few
seconds) before re-applying power.

Functionality
This menu selects which macro is required for standard wiring arrangements. The default
one is "Cn000" for connection macro 0.
All connection macros only change the CDS0 (command data set 0) parameters. The CDS1
parameters are used for the BOP control. For more information about the CDS parameters,
see SINAMICS V20 Inverter Operating Instructions.
Connection
macro

Description

Cn000

Factory default setting. Makes no parameter changes.

Cn001

BOP as the only control source

Cn002

Control from terminals (PNP / NPN)

Cn003

Fixed speeds

Cn004

Fixed speed binary mode

Cn005

Analog input and fixed frequency

Cn006

External push button control

Cn007

External push button with analog setpoint

Cn008

PID control with analog input reference

Cn009

PID control with the fixed value reference

Cn010

USS control

Cn011

MODBUS RTU control

Display example

The minus sign indicates that this macro
is the currently selected macro.

SINAMICS V20 Inverter

30

Getting Started, 11/2012, A5E31623806

<!-- page 31 -->

Commissioning
4.4 Quick commissioning

Setting connection macros
0LQXVVLJQVLJQLILHVFXUUHQW
VHOHFWHGPDFUR
!V

0RWRUGDWD

!V
M

V
V

&RQQHFWLRQPDFUR


V

M

V
OK
M

V

V

$SSOLFDWLRQPDFUR

&Q[[[

&XUUHQWVHOHFWHGPDFUR

Connection macro Cn001 - BOP as the only control source






















10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1



N
6SHHG

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW

0~20mA=
0~50/60Hz

Connection macro settings:
Parameter

Description

P0700[0]
P1000[0]
P0731[0]
P0732[0]
P0771[0]
P0810[0]

Selection of command source
Selection of frequency
BI: Function of digital output 1
BI: Function of digital output 2
CI: Analog output
BI: CDS bit 0 (Hand/Auto)

Factory
default
1
1
52.3
52.7
21
0

Default for
Cn001
1
1
52.2
52.3
21
0

Remarks
BOP
BOP MOP
Inverter running
Inverter fault active
Actual frequency
Hand mode

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

31

<!-- page 32 -->

Commissioning
4.4 Quick commissioning

Connection macro Cn002 - Control from terminals (PNP / NPN)
External control - Potentiometer with setpoint
● Hand / Auto switch between the BOP and terminals by pressing M + OK
● Both NPN and PNP can be realized with the same parameters. You can change the
connection of the digital input common terminal to 24 V or 0 V to decide the mode.
0~10V=
0~50/60Hz

2Q2II
5HYHUVH
)DXOWDFNQRZOHGJHPHQW
-2*IRUZDUG























10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1



 




M

OK

P+ N







220V



N

6SHHG

5XQQLQJ

)DXOW

0~20mA=
0~50/60Hz

PNP

0~10V=
0~50/60Hz

2Q2II
5HYHUVH
)DXOWDFNQRZOHGJHPHQW



















-2*IRUZDUG




10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

 


5XQQLQJ



M

OK

P+ N



220V







)DXOW

0~20mA=
0~50/60Hz

NPN

Connection macro settings:
Parameter

Description

P0700[0]
P1000[0]
P0701[0]
P0702[0]
P0703[0]

Selection of command source
Selection of frequency
Function of digital input 1
Function of digital input 2
Function of digital input 3

Factory
default
1
1
0
0
9

Default for
Cn002
2
2
1
12
9

Remarks
Terminal as command source
Analog as speed setpoint
ON / OFF
Reverse
Fault acknowledgement

SINAMICS V20 Inverter

32

Getting Started, 11/2012, A5E31623806

<!-- page 33 -->

Commissioning
4.4 Quick commissioning
Parameter

Description

P0704[0]
P0771[0]
P0731[0]
P0732[0]

Function of digital input 4
CI: Analog output
BI: Function of digital output 1
BI: Function of digital output 2

Factory
default
15
21
52.3
52.7

Default for
Cn002
10
21
52.2
52.3

Remarks
JOG forward
Actual frequency
Inverter running
Inverter fault active

Connection macro Cn003 - Fixed speeds
Three fixed speeds with ON / OFF
● Hand / Auto switch between the BOP and terminal by pressing M + OK
● If several digital inputs are active at the same time, the selected frequencies are
summed, e.g. FF1 + FF2 + FF3
2Q2II
6SHHGORZ
6SHHGPLGGOH
6SHHGKLJK






















10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW

0~20mA=
0~50/60Hz

Connection macro settings:
Parameter

Description

P0700[0]
P1000[0]
P0701[0]
P0702[0]
P0703[0]
P0704[0]
P1016[0]
P1020[0]
P1021[0]
P1022[0]
P1001[0]
P1002[0]
P1003[0]
P0771[0]

Selection of command source
Selection of frequency
Function of digital input 1
Function of digital input 2
Function of digital input 3
Function of digital input 4
Fixed frequency mode
BI: Fixed frequency selection bit 0
BI: Fixed frequency selection bit 1
BI: Fixed frequency selection bit 2
Fixed frequency 1
Fixed frequency 2
Fixed frequency 3
CI: Analog output

Factory
default
1
1
0
0
9
15
1
722.3
722.4
722.5
10
15
25
21

Default for
Cn003
2
3
1
15
16
17
1
722.1
722.2
722.3
10
15
25
21

Remarks
Terminal as command source
Fixed frequency
ON / OFF
Fixed speed bit 0
Fixed speed bit 1
Fixed speed bit 2
Direct selection mode
DI2
DI3
DI4
Speed low
Speed middle
Speed high
Actual frequency

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

33

<!-- page 34 -->

Commissioning
4.4 Quick commissioning
Parameter

Description

P0731[0]
P0732[0]

BI: Function of digital output 1
BI: Function of digital output 2

Factory
default
52.3
52.7

Default for
Cn003
52.2
52.3

Remarks
Inverter running
Inverter fault active

Connection macro Cn004 - Fixed speeds in binary mode
Fixed speeds with ON command in binary mode
● Up to 16 different fixed frequency values (0 Hz, P1001 ... P1015) can be selected by the
fixed frequency selectors (P1020 ... P1023)
)L[HGVSHHGELW
)L[HGVSHHGELW
)L[HGVSHHGELW
)L[HGVSHHGELW






















10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW

0~20mA=
0~50/60Hz

Connection macro settings:
Parameter

Description
Selection of command source
Selection of frequency
Function of digital input 1
Function of digital input 2
Function of digital input 3
Function of digital input 4
Fixed frequency mode
BI: ON / OFF1

Factory
default
1
1
0
0
9
15
1
19.0

Default for
Cn004
2
3
15
16
17
18
2
1025.0

P0700[0]
P1000[0]
P0701[0]
P0702[0]
P0703[0]
P0704[0]
P1016[0]
P0840[0]
P1020[0]
P1021[0]
P1022[0]
P1023[0]
P0771[0]
P0731[0]
P0732[0]

BI: Fixed frequency selection bit 0
BI: Fixed frequency selection bit 1
BI: Fixed frequency selection bit 2
BI: Fixed frequency selection bit 3
CI: Analog output
BI: Function of digital output 1
BI: Function of digital output 2

722.3
722.4
722.5
722.6
21
52.3
52.7

722.0
722.1
722.2
722.3
21
52.2
52.3

Remarks
Terminals as command source
Fixed frequency
Fixed speed bit 0
Fixed speed bit 1
Fixed speed bit 2
Fixed speed bit 3
Binary mode
Inverter starts at the fixed speed
selected
DI1
DI2
DI3
DI4
Actual frequency
Inverter running
Inverter fault active

SINAMICS V20 Inverter

34

Getting Started, 11/2012, A5E31623806

<!-- page 35 -->

Commissioning
4.4 Quick commissioning

Connection macro Cn005 - Analog input and fixed frequency
The analog input works as an additional setpoint.
● If DI2 and DI3 are active together, the selected frequencies are summed, i.e. FF1 + FF2
0~10V=
0~50/60Hz

212))
)L[HGVSHHGELW
)L[HGVSHHGELW
)DXOWDFNQRZOHGJHJPHQW























10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

 




M





220V

5XQQLQJ

OK

P+ N





)DXOW

0~20mA=
0~50/60Hz

Function diagram
When the fixed speed is selected, the additional setpoint channel from the analog is
disabled. If there is no fixed speed setpoint, the setpoint channel connects to the analog
input.
$GGLWLRQDOVHWSRLQW
GLVDEOHG

+

FF 01

FF 02

)L[HGVSHHGV

$QDORJLQSXW

6HWSRLQW

r1025

Connection macro settings:
Parameter

Description

P0700[0]
P1000[0]
P0701[0]
P0702[0]
P0703[0]
P0704[0]
P1016[0]
P1020[0]
P1021[0]
P1001[0]
P1002[0]

Selection of command source
Selection of frequency
Function of digital input 1
Function of digital input 2
Function of digital input 3
Function of digital input 4
Fixed frequency mode
BI: Fixed frequency selection bit 0
BI: Fixed frequency selection bit 1
Fixed frequency 1
Fixed frequency 2

Factory
default
1
1
0
0
9
15
1
722.3
722.4
10
15

Default for
Cn005
2
23
1
15
16
9
1
722.1
722.2
10
15

Remarks
Terminals as command source
Fixed frequency + analog setpoint
ON / OFF
Fixed speed bit 0
Fixed speed bit 1
Fault acknowledgement
Direct selection mode
DI2
DI3
Fixed speed 1
Fixed speed 2

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

35

<!-- page 36 -->

Commissioning
4.4 Quick commissioning
Parameter

Description

P1074[0]
P0771[0]
P0731[0]
P0732[0]

BI: Disable additional setpoint
CI: Analog output
BI: Function of digital output 1
BI: Function of digital output 2

Factory
default
0
21
52.3
52.7

Default for
Cn005
1025.0
21
52.2
52.3

Remarks
FF disables the additional setpoint
Actual frequency
Inverter running
Inverter fault active

Connection macro Cn006 - External push button control
Note that the command sources are pulse signals.

2))KROG
21SXOVH
023XS
023GRZQ






















10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW

0~20mA=
0~50/60Hz

Connection macro settings:
Parameter

Description
Selection of command source
Selection of frequency
Function of digital input 1
Function of digital input 2
Function of digital input 3
Function of digital input 4
Selection of 2 / 3-wire method

Factory
default
1
1
0
0
9
15
0

Default for
Cn006
2
1
2
1
13
14
3

P0700[0]
P1000[0]
P0701[0]
P0702[0]
P0703[0]
P0704[0]
P0727[0]

P0771[0]
P0731[0]
P0732[0]
P1040[0]
P1047[0]

CI: Analog output
BI: Function of digital output 1
BI: Function of digital output 2
Setpoint of the MOP
MOP ramp-up time of the RFG

21
52.3
52.7
5
10

21
52.2
52.3
0
10

P1048[0]

MOP ramp-down time of the RFG

10

10

Remarks
Terminals as command source
BOP MOP
OFF1 / hold
ON pulse
MOP up pulse
MOP down pulse
3-wire
ON pulse + OFF1 / HOLD +
Reverse
Actual frequency
Inverter running
Inverter fault active
Initial frequency
Ramp-up time from zero to
maximum frequency
Ramp-down time from maximum
frequency to zero

SINAMICS V20 Inverter

36

Getting Started, 11/2012, A5E31623806

<!-- page 37 -->

Commissioning
4.4 Quick commissioning

Connection macro Cn007 - External push buttons with analog control
Note that the command sources are pulse signals.
0~10V=
0~50/60Hz

2))KROG
)RUZDUGSXOVH21
5HYHUVHSXOVH21
)DXOWDFNQRZOHGJHPHQWSXOVH























10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1



N
6SHHG

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW

0~20mA=
0~50/60Hz

2))
)RUZDUG
5HYHUVH

Connection macro settings:
Parameter

Description
Selection of command source
Selection of frequency
Function of digital input 1
Function of digital input 2
Function of digital input 3
Function of digital input 4
Selection of 2 / 3-wire method

Factory
default
1
1
0
0
9
15
0

Default for
Cn007
2
2
1
2
12
9
2

P0700[0]
P1000[0]
P0701[0]
P0702[0]
P0703[0]
P0704[0]
P0727[0]

P0771[0]
P0731[0]
P0732[0]

CI: Analog output
BI: Function of digital output 1
BI: Function of digital output 2

21
52.3
52.7

21
52.2
52.3

Remarks
Terminals as command source
Analog
OFF hold
Forward pulse + ON
Reverse pulse + ON
Fault acknowledgement
3-wire
STOP + Forward pulse + Reverse
pulse
Actual frequency
Inverter running
Inverter fault active

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

37

<!-- page 38 -->

Commissioning
4.4 Quick commissioning

Connection macro Cn008 - PID control with analog reference
aP$
$FWXDOYDOXH

212))

3,'
VHWSRLQW
)DXOWDFNQRZOHGJHPHQWSXOVH























10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW

PID controller

0~20mA=
0~50/60Hz

Note
If a negative setpoint for the PID control is desired, change the setpoint and feedback wiring
as needed.
When you switch to Hand mode from PID control mode, P2200 becomes 0 to disable the
PID control. When you switch it back to Auto mode, P2200 becomes 1 to enable the PID
control again.
Connection macro settings:
Parameter

Description

P0700[0]
P0701[0]
P0703[0]
P2200[0]
P2253[0]
P2264[0]
P0756[1]
P0771[0]
P0731[0]
P0732[0]

Selection of command source
Function of digital input 1
Function of digital input 3
Enable PID controller
CI: PID setpoint
CI: PID feedback
Type of AI
CI: Analog output
BI: Function of digital output 1
BI: Function of digital output 2

Factory
default
1
0
9
0
0
755.0
0
21
52.3
52.7

Default for
Cn008
2
1
9
1
755.0
755.1
2
21
52.2
52.3

Remarks
Terminals as command source
ON / OFF
Fault acknowledgement
Enable PID
PID Setpoint = Analog input 1
PID feedback = Analog input 2
Analog input 2, 0 to 20 mA
Actual frequency
Inverter running
Inverter fault active

SINAMICS V20 Inverter

38

Getting Started, 11/2012, A5E31623806

<!-- page 39 -->

Commissioning
4.4 Quick commissioning

Connection macro Cn009 - PID control with the fixed value reference
aP$
$FWXDOYDOXH

212))
)L[HG3,'VHWSRLQW
)L[HG3,'VHWSRLQW
)L[HG3,'VHWSRLQW























10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

 


6SHHG



M

OK

P+ N







220V

5XQQLQJ



)DXOW

PID controller

0~20mA=
0~50/60Hz

Connection macro settings:
Parameter

Description

P0700[0]
P0701[0]
P0702[0]
P0703[0]
P0704[0]
P2200[0]
P2216[0]
P2220[0]
P2221[0]
P2222[0]
P2253[0]
P2264[0]

Selection of command source
Function of digital input 1
Function of digital input 2
Function of digital input 3
Function of digital input 4
Enable PID controller
Fixed PID setpoint mode
BI: Fixed PID setpoint select bit 0
BI: Fixed PID setpoint select bit 1
BI: Fixed PID setpoint select bit 2
CI: PID setpoint
CI: PID feedback

Factory
default
1
0
0
9
15
0
1
722.3
722.4
722.5
0
755.0

Default for
Cn009
2
1
15
16
17
1
1
722.1
722.2
722.3
2224
755.1

Remarks
Terminals as command source
ON / OFF
DI2 = PID fixed value 1
DI3 = PID fixed value 2
DI4 = PID fixed value 3
Enable PID
Direct selection
BICO connection DI2
BICO connection DI3
BICO connection DI4
PID setpoint = fixed value
PID feedback = AI2

Connection macro Cn010 - USS control






















10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

0~20mA=
0~50/60Hz

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW
56866
212))VSHHG

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

39

<!-- page 40 -->

Commissioning
4.4 Quick commissioning
Connection macro settings:
Parameter

Description

P0700[0]
P1000[0]
P2023[0]
P2010[0]
P2011[0]
P2012[0]
P2013[0]
P2014[0]

Selection of command source
Selection of frequency
RS485 protocol selection
USS / MODBUS baudrate
USS address
USS PZD length
USS PKW length
USS / MODBUS telegram off time

Factory
default
1
1
1
8
0
2
127
2000

Default for
Cn010
5
5
1
8
1
2
127
500

Remarks
RS485 as the command source
RS485 as the speed setpoint
USS protocol
Baudrate 38400 bps
USS address for inverter
Number of PZD words
Variable PKW words
Time to receive data

Connection macro Cn011 - MODBUS RTU control






















10V AI1 AI2 0V DI1 DI2 DI3 DI4 DIC 24V 0V
DO2

0V
0V
AO+ AO- DO1+ DO1


N

6SHHG

 




5XQQLQJ

M

OK

P+ N



220V







)DXOW
5602'%86578
212))VSHHG

0~20mA=
0~50/60Hz

Connection macro settings:
Parameter

Description
Selection of command source
Selection of frequency
RS485 protocol selection
USS / MODBUS baudrate
MODBUS address
MODBUS reply timeout

Factory
default
1
1
1
8
1
1000

Default for
Cn011
5
5
2
6
1
1000

P0700[0]
P1000[0]
P2023[0]
P2010[0]
P2021[0]
P2022[0]
P2014[0]

USS / MODBUS telegram off time

2000

100

Remarks
RS485 as the command source
RS485 as the speed setpoint
MODBUS RTU protocol
Baudrate 9600 bps
MODBUS address for inverter
Maximum time to send reply back
to the master
Time to receive data

SINAMICS V20 Inverter

40

Getting Started, 11/2012, A5E31623806

<!-- page 41 -->

Commissioning
4.4 Quick commissioning

4.4.4

Setting application macros
NOTICE
Application macro settings
When commissioning the inverter, the application macro setting is a one-off setting. Make
sure that you proceed as follows before you change the application macro setting to a value
different from your last setting:
1. Do a factory reset (P0010 = 30, P0970 = 1)
2. Repeat the quick commissioning and change the application macro
Failure to observe may cause the inverter to accept the parameter settings from both the
currently and the previously selected macros, which may lead to undefined and
unexplainable inverter operation.

Functionality
This menu defines certain common applications. Each application macro provides a set of
parameter settings for a specific application. After you select an application macro, the
corresponding settings are applied to the inverter to simplify the commissioning process.
The default application macro is "AP000" for application macro 0. If none of the application
macros fits your application, select the one that is the closest to your application and make
further parameter changes as desired.
Application
macro

Description

Display example

AP000

Factory default setting. Makes no parameter changes.

AP010

Simple pump applications

AP020

Simple fan applications

AP021

Compressor applications

AP030

Conveyor applications

The minus sign indicates that this macro is
the currently selected macro.

Setting application macros
0LQXVVLJQVLJQLILHVFXUUHQW
VHOHFWHGPDFUR
!V

&RQQHFWLRQPDFUR

!V
M

V
V

$SSOLFDWLRQPDFUR


V

M

V
OK
M

&RPPRQSDUDPHWHUV

V

V
$3[[[

&XUUHQWVHOHFWHGPDFUR

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

41

<!-- page 42 -->

Commissioning
4.4 Quick commissioning

Application macro AP010 - Simple pump applications
Parameter

Description

Factory
default

Default for
AP010

Remarks

P1080[0]

Minimum frequency

0

15

P1300[0]
P1110[0]
P1210[0]

Control mode
BI: Inhibit negative frequency setpoint
Automatic restart

0
0
1

7
1
2

Inverter running at a lower speed
inhibited
Quadratic V/f
Reverse pump rotation inhibited
Fault acknowledgement at
power-on

P1120[0]

Ramp-up time

10

10

P1121[0]

Ramp-down time

10

10

Ramp-up time from zero to
maximum frequency
Ramp-down time from maximum
frequency to zero

Application macro AP020 - Simple fan applications
Parameter

Description

Factory
default

Default for
AP020

Remarks

P1110[0]
P1300[0]
P1200[0]

BI: Inhibit negative frequency setpoint
Control mode
Flying start

0
0
0

1
7
2

P1210[0]

Automatic restart

1

2

Reverse fan rotation inhibited
Quadratic V/f
Search for the speed of the
running motor with a heavy
inertia load so that the motor
runs up to the setpoint
Fault acknowledgement at
power-on

P1080[0]

Minimum frequency

0

20

P1120[0]

Ramp-up time

10

10

P1121[0]

Ramp-down time

10

20

Inverter running at a lower speed
inhibited
Ramp-up time from zero to
maximum frequency
Ramp-down time from maximum
frequency to zero

Application macro AP021 - Compressor applications
Parameter

Description

Factory
default

Default for
AP021

Remarks

P1300[0]
P1080[0]

Control mode
Minimum frequency

0
0

0
10

P1312[0]

Starting boost

0

30

P1311[0]

Acceleration boost

0

0

P1310[0]

Continuous boost

50

50

Linear V/f
Inverter running at a lower speed
inhibited
Boost only effective when
accelerating for the first time
(standstill)
Boost only effective when
accelerating or braking
Additional boost over the complete
frequency range

SINAMICS V20 Inverter

42

Getting Started, 11/2012, A5E31623806

<!-- page 43 -->

Commissioning
4.4 Quick commissioning
Parameter

Description

Factory
default

Default for
AP021

Remarks

P1120[0]

Ramp-up time

10

10

P1121[0]

Ramp-down time

10

10

Ramp-up time from zero to
maximum frequency
Ramp-down time from maximum
frequency to zero

Application macro AP030 - Conveyor applications
Parameter

Description

Factory
default

Default for
AP030

Remarks

P1300[0]
P1312[0]

Control mode
Starting boost

0
0

1
30

P1120[0]

Ramp-up time

10

5

V/f with FCC
Boost only effective when
accelerating for the first time
(standstill)
Ramp-up time from zero to
maximum frequency

P1121[0]

Ramp-down time

10

5

4.4.5

Setting common parameters

Ramp-down time from maximum
frequency to zero

Functionality
This menu provides some common parameters for inverter performance optimization.

Text menu
If you set P8553 to 1, parameter numbers in this menu are replaced with short text.

Setting parameters
Parameter
P1080[0]

Access
level

Function

1

Minimum motor frequency

Text menu
(if P8553 = 1)

(MIN F)
P1082[0]

1

Maximum motor frequency
(MAX F)

P1120[0]

1

Ramp-up time
(RMP UP)

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

43

<!-- page 44 -->

Commissioning
4.5 Restoring to defaults

Parameter
P1121[0]

Access
level

Function

1

Ramp-down time

Text menu
(if P8553 = 1)

(RMP DN)
P1058[0]

2

JOG frequency
(JOG P)

P1060[0]

2

JOG ramp-up time
(JOG UP)

P1001[0]

2

Fixed frequency setpoint 1
(FIX F1)

P1002[0]

2

Fixed frequency setpoint 2
(FIX F2)

P1003[0]

2

Fixed frequency setpoint 3
(FIX F3)

P2201[0]

2

Fixed PID frequency setpoint 1
(PID F1)

P2202[0]

2

Fixed PID frequency setpoint 2
(PID F2)

P2203[0]

2

Fixed PID frequency setpoint 3
(PID F3)

4.5
Parameter

Restoring to defaults
Function

Setting

P0003

User access level

= 1 (standard user access level)

P0010

Commissioning parameter

= 30 (factory setting)

P0970

Factory reset

= 1: parameter reset to user defaults if stored, else factory
defaults (restoring to user defaults)
= 21: parameter reset to factory defaults deleting user defaults if
stored (restoring to factory defaults)

After the setting for P0970, the inverter displays "8 8 8 8 8" and then the screen shows
"P0970". P0970 and P0010 are automatically reset to their original value 0.

SINAMICS V20 Inverter

44

Getting Started, 11/2012, A5E31623806

<!-- page 45 -->

5

Parameter list

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter access level

| Access level | Description | Remarks |
|---|---|---|
| 0 | User-defined parameter list | Defines a limited set of parameters to which the end user has access. See P0013 for details on use. |
| 1 | Standard | Allows access into most frequently used parameters. |
| 2 | Extended | Allows extended access to more parameters. |
| 3 | Expert | For expert use only. |
| 4 | Service | Only for use by authorized service personnel, password protected. |

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| r0002 | Inverter state | - | - | 2 |
| P0003 | User access level (0 = User defined parameter list; 1 = Standard; 2 = Extended; 3 = Expert; 4 = Service) | 0-4 | 1 | 1 |
| P0004 | Parameter filter (0 = All parameters; 12 = Inverter features; 2 = Inverter; 13 = Motor control; 3 = Motor; 19 = Motor identification; 5 = Technology application / units; 20 = Communication; 7 = Commands, binary I/O; 21 = Warnings / faults / monitoring; 8 = Analog input and analog output; 22 = Technology controller; 10 = Setpoint channel / RFG) | 0 - 22 | 0 | 1 |
| P0010 | Commissioning parameter (0 = Ready; 1 = Quick commissioning; 2 = Inverter; 29 = Download; 30 = Factory setting) | 0 - 30 | 0 | 1 |
| r0018 | Firmware version | - | - | 1 |
| r0021 | CO: Actual filtered frequency [Hz] | - | - | 2 |
| r0025 | CO: Actual output voltage [V] | - | - | 2 |
| r0026[0] | CO: Actual filtered DC-link voltage [V] | - | - | 2 |
| r0027 | CO: Actual output current [A] | - | - | 2 |
| r0031 | CO: Actual filtered torque [Nm] | - | - | 2 |
| r0032 | CO: Actual filtered power | - | - | 2 |

<!-- page 46 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| r0035[0...2] | CO: Actual motor temperature [°C] | - | - | 2 |
| r0039 | CO: Energy consumpt. meter [kWh] | - | - | 2 |
| P0040 | Reset energy consumpt. and energy saved meter (0 = No reset; 1 = Reset r0039 to 0) | 0-1 | 0 | 2 |
| P0042[0...1] | Energy saving scaling (Index [0]: Factor for kWh to currency conversion; Index [1]: Factor for kWh to CO2 conversion) | 0.000 - 100.00 | 0.000 | 2 |
| r0043[0...2] | Energy saved [kWh] | - | - | 2 |
| r0050 | CO / BO: Active command data set | - | - | 2 |
| r0051[0...1] | CO: Active inverter data set (DDS) | - | - | 2 |
| r0052.0...15 | CO / BO: Active status word 1 | - | - | 2 |
| r0053.0...15 | CO / BO: Active status word 2 | - | - | 2 |
| P0100 | Europe / North America (0 = Europe [kW], motor base frequency is 50 Hz; 1 = North America [hp], motor base frequency is 60 Hz; 2 = North America [kW], motor base frequency is 60 Hz) | 0-2 | 0 | 1 |
| r0206 | Rated inverter power [kW] / [hp] | - | - | 2 |
| r0207[0...2] | Rated inverter current [A] | - | - | 2 |
| r0208 | Rated inverter voltage [V] | - | - | 2 |
| r0209 | Maximum inverter current [A] | - | - | 2 |
| P0304[0...2] | Rated motor voltage [V] | 10 - 2000 | 400 | 1 |
| P0305[0...2] | Rated motor current [A] | 0.01 - 10000.00 | 1.86 | 1 |
| P0307[0...2] | Rated motor power | 0.01 - 2000.00 | 0.75 | 1 |
| P0308[0...2] | Rated motor cosφ | 0.000 - 1.000 | 0.000 | 1 |
| P0309[0...2] | Rated motor efficiency [%] | 0.0 - 99.9 | 0.0 | 1 |
| P0310[0...2] | Rated motor frequency [Hz] | 12.00 - 599.00 | 50.00 | 1 |
| P0311[0...2] | Rated motor speed [RPM] | 0 - 40000 | 1395 | 1 |
| P0335[0...2] | Motor cooling (0 = Self-cooled: Shaft mounted fan attached motor (IC410 or IC411); 1 = Force-cooled: Separately powered cooling fan (IC416); 2 = Self-cooled and internal fan; 3 = Force-cooled and internal fan) | 0-3 | 0 | 2 |
| P0340[0...2] | Calculation of motor parameters (0 = No calculation; 1 = Complete parameterization; 2 = Calculation of equivalent circuit data; 3 = Calculation of V/f control data; 4 = Calculation of controller settings only) | 0-4 | 0 | 2 |
| P0507 | Application macro | 0 - 255 | 0 | 1 |
| r0512 | CO: Scaled filtered frequency | - | - | 2 |
| P0604[0...2] | Threshold motor temperature [°C] | 0.0 - 200.0 | 130.0 | 2 |
| P0640[0...2] | Motor overload factor [%] | 10.0 - 400.0 | 150.0 | 2 |
| P0700[0...2] | Selection of command source (0 = Factory default setting; 1 = Operator panel (keypad); 2 = Terminal; 5 = USS / MBUS on RS485) | 0-5 | 1 | 1 |

<!-- page 47 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| P0701[0...2] | Function of digital input 1 (0 = Digital input disabled; 16 = Fixed frequency selector bit1; 1 = ON / OFF1; 17 = Fixed frequency selector bit2; 2 = ON reverse / OFF1; 18 = Fixed frequency selector bit3; 3 = OFF2 - coast to standstill; 22 = QuickStop Source 1; 4 = OFF3 - quick ramp-down; 23 = QuickStop Source 2; 9 = Fault acknowledge; 24 = QuickStop Override; 10 = JOG right; 25 = DC brake enable; 11 = JOG left; 27 = Enable PID; 12 = Reverse; 29 = External trip; 13 = MOP up (increase frequency); 33 = Disable additional freq setpoint; 14 = MOP down (decrease frequency); 99 = Enable BICO parameterization; 15 = Fixed frequency selector bit0) | 0 - 99 | 0 | 2 |
| P0702[0...2] | Function of digital input 2 | 0 - 99 | 0 | 2 |
| P0703[0...2] | Function of digital input 3 | 0 - 99 | 9 | 2 |
| P0704[0...2] | Function of digital input 4 | 0 - 99 | 15 | 2 |
| P0712[0...2] | Analog / digital input 1 | 0 - 99 | 0 | 2 |
| P0713[0...2] | Analog / digital input 2 | 0 - 99 | 0 | 2 |
| P0717 | Connection macro | 0 - 255 | 0 | 1 |
| r0722.0...12 | CO / BO: Digital input values | - | - | 2 |
| P0727[0...2] | Selection of 2 / 3-wire method (0 = Siemens (start / dir); 1 = 2-wire (fwd / rev); 2 = 3-wire (fwd / rev); 3 = 3-wire (start / dir)) | 0-3 | 0 | 2 |
| P0731[0...2] | BI: Function of digital output 1 | - | 52.3 | 2 |
| P0732[0...2] | BI: Function of digital output 2 | - | 52.7 | 2 |
| r0752[0...1] | Actual analog input [V] or [mA] | - | - | 2 |
| r0754[0...1] | Actual analog input value after scaling [%] | - | - | 2 |
| r0755[0...1] | CO: Actual analog input after scaling [4000h] | - | - | 2 |
| P0756[0...1] | Type of analog input (0 = Unipolar voltage input (0 to +10 V); 1 = Unipolar voltage input with monitoring (0 to 10 V); 2 = Unipolar current input (0 to 20 mA); 3 = Unipolar current input with monitoring (0 to 20 mA); 4 = Bipolar voltage input (-10 V to +10 V)) | 0-4 | 0 | 2 |
| P0757[0...1] | Value x1 of analog input scaling | -20 - 20 | 0 | 2 |
| P0758[0...1] | Value y1 of analog input scaling [%] | -99999 - 99999 | 0.0 | 2 |
| P0759[0...1] | Value x2 of analog input scaling | -20 - 20 | 10 | 2 |
| P0760[0...1] | Value y2 of analog input scaling [%] | -99999 - 99999 | 100.0 | 2 |
| P0761[0...1] | Width of analog input deadband | 0 - 20 | 0 | 2 |
| P0771[0] | CI: Analog output | - | 21[0] | 2 |

<!-- page 48 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| P0773[0] | Smooth time analog output [ms] | 0 - 1000 | 2 | 2 |
| r0774[0] | Actual analog output value [V] or [mA] | - | - | 2 |
| P0775[0] | Permit absolute value | 0 - 65535 | 0 | 2 |
| P0777[0] | Value x1 of analog output scaling [%] | -99999 - 99999 | 0.0 | 2 |
| P0778[0] | Value y1 of analog output scaling | 0 - 20 | 0 | 2 |
| P0779[0] | Value x2 of analog output scaling [%] | -99999 - 99999 | 100.0 | 2 |
| P0780[0] | Value y2 of analog output scaling | 0 - 20 | 20 | 2 |
| P0781[0] | Width of analog output deadband | 0 - 20 | 0 | 2 |
| r0785.0 | CO / BO: Status word of analog output | - | - | 2 |
| P0809[0...2] | Copy command data set (CDS) (Index [0]: Copy from CDS; Index [1]: Copy to CDS; Index [2]: Start copy) | 0-2 | [0] 0 [1] 1 [2] 0 | 2 |
| P0810 | BI: command data set bit 0 (Hand / Auto) | - | 0 | 2 |
| P0811 | BI: command data set bit 1 | - | 0 | 2 |
| P0819[0...2] | Copy inverter data set (DDS) (Index [0]: Copy from DDS; Index [1]: Copy to DDS; Index [2]: Start copy) | 0-2 | [0] 0 [1] 1 [2] 0 | 2 |
| P0927 | Parameter changeable via | - | 1111 bin | 2 |
| r0947[0...63] | CO: Last fault code | - | - | 2 |
| P0970 | Factory reset (0 = Disabled; 1 = Parameter reset; 21 = User Default Parameter Reset) | 0 - 21 | 0 | 1 |
| P1000[0...2] | Selection of frequency setpoint (0 = No main setpoint; 30 = No main setpoint + Fixed frequency; 1 = MOP setpoint; 31 = MOP setpoint + Fixed frequency; 2 = Analog setpoint; 32 = Analog setpoint + Fixed frequency; 3 = Fixed frequency; 33 = Fixed frequency + Fixed frequency; 5 = USS on RS485; 35 = USS on RS485 + Fixed frequency; 7 = Analog setpoint 2; 37 = Analog setpoint 2 + Fixed frequency; 10 = No main setpoint + MOP setpoint; 50 = No main setpoint + USS on RS485; 11 = MOP setpoint + MOP setpoint; 51 = MOP setpoint + USS on RS485; 12 = Analog setpoint + MOP setpoint; 52 = Analog setpoint + USS on RS485; 13 = Fixed frequency + MOP setpoint; 53 = Fixed frequency + USS on RS485; 15 = USS on RS485 + MOP setpoint; 55 = USS on RS485 + USS on RS485; 17 = Analog setpoint 2 + MOP setpoint; 57 = Analog setpoint 2 + USS on RS485; 20 = No main setpoint + Analog setpoint; 70 = No main setpoint + Analog setpoint 2; 21 = MOP setpoint + Analog setpoint; 71 = MOP setpoint + Analog setpoint 2; 22 = Analog setpoint + Analog setpoint; 72 = Analog setpoint + Analog setpoint 2; 23 = Fixed frequency + Analog setpoint; 73 = Fixed frequency + Analog setpoint 2; 25 = USS on RS485 + Analog setpoint; 75 = USS on RS485 + Analog setpoint 2; 27 = Analog setpoint 2 + Analog setpoint; 77 = Analog setpoint 2 + Analog setpoint 2) | 0 - 77 | 1 | 1 |
| P1001[0...2] | Fixed frequency 1 [Hz] | -599.00 - 599.00 | 10.00 | 2 |

<!-- page 49 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| P1002[0...2] | Fixed frequency 2 [Hz] | -599.00 - 599.00 | 15.00 | 2 |
| P1003[0...2] | Fixed frequency 3 [Hz] | -599.00 - 599.00 | 25.00 | 2 |
| P1004[0...2] | Fixed frequency 4 [Hz] | -599.00 - 599.00 | 50.00 | 2 |
| P1005[0...2] | Fixed frequency 5 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1006[0...2] | Fixed frequency 6 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1007[0...2] | Fixed frequency 7 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1008[0...2] | Fixed frequency 8 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1009[0...2] | Fixed frequency 9 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1010[0...2] | Fixed frequency 10 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1011[0...2] | Fixed frequency 11 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1012[0...2] | Fixed frequency 12 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1013[0...2] | Fixed frequency 13 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1014[0...2] | Fixed frequency 14 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1015[0...2] | Fixed frequency 15 [Hz] | -599.00 - 599.00 | 0.00 | 2 |
| P1016[0...2] | Fixed frequency mode (1 = Direct selection; 2 = Binary selection) | 1-2 | 1 | 2 |
| P1031[0...2] | MOP mode | - | 1 | 2 |
| P1032 | Inhibit reverse direction of MOP (0 = Reverse direction is allowed; 1 = Reverse direction inhibited) | 0-1 | 1 | 2 |
| P1040[0...2] | Setpoint of the MOP [Hz] | -599.00 - 599.00 | 5.00 | 2 |
| P1047[0...2] | MOP ramp-up time of the RFG [s] | 0.00 - 1000.00 | 10.00 | 2 |
| P1048[0...2] | MOP ramp-down time of the RFG [s] | 0.00 - 1000.0 | 10.00 | 2 |
| r1050 | CO: Actual output freq. of the MOP [Hz] | - | - | 2 |
| P1058[0...2] | JOG frequency [Hz] | 0.00 - 599.00 | 5.00 | 2 |
| P1059[0...2] | JOG frequency left [Hz] | 0.00 - 599.00 | 5.00 | 2 |
| P1060[0...2] | JOG ramp-up time [s] | 0.00 - 650.00 | 10.00 | 2 |
| P1061[0...2] | JOG ramp-down time [s] | 0.00 - 650.00 | 10.00 | 2 |
| P1080[0...2] | Minimum frequency [Hz] | 0.00 - 599.00 | 0.00 | 1 |
| P1082[0...2] | Maximum frequency [Hz] | 0.00 - 599.00 | 50.00 | 1 |
| P1120[0...2] | Ramp-up time [s] | 0.00 - 650.00 | 10.00 | 1 |
| P1121[0...2] | Ramp-down time [s] | 0.00 - 650.00 | 10.00 | 1 |
| P1130[0...2] | Ramp-up initial rounding time [s] | 0.00 - 40.00 | 0.00 | 2 |
| P1131[0...2] | Ramp-up final rounding time [s] | 0.00 - 40.00 | 0.00 | 2 |
| P1132[0...2] | Ramp-down initial rounding time [s] | 0.00 - 40.00 | 0.00 | 2 |
| P1133[0...2] | Ramp-down final rounding time [s] | 0.00 - 40.00 | 0.00 | 2 |
| P1134[0...2] | Rounding type (0 = Continuous smoothing; 1 = Discontinuous smoothing) | 0-1 | 0 | 2 |
| P1135[0...2] | OFF3 ramp-down time [s] | 0.00 - 650.00 | 5.00 | 2 |
| P1200 | Flying start (0 = Flying start disabled; 1 = Flying start always active; searches in both directions; 2 = Flying start active after power on, fault, OFF2; searches in both directions; 3 = Flying start active after fault, OFF2; searches in both directions; 4 = Flying start always active; searches in direction of setpoint only; 5 = Flying start active after power on, fault, OFF2; searches in direction of setpoint only; 6 = Flying start active after fault, OFF2; searches in direction of setpoint only) | 0-6 | 0 | 2 |

<!-- page 50 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| P1210 | Automatic restart (0 = Disabled; 1 = Trip reset after power on, P1211 disabled; 2 = Restart after mains blackout, P1211 disabled; 3 = Restart after mains brownout or fault, P1211 enabled; 4 = Restart after mains brownout, P1211 enabled; 5 = Restart after mains blackout and fault, P1211 disabled; 6 = Restart after mains brown- /blackout or fault, P1211 enabled; 7 = Restart after mains brown- /blackout or fault, trip when P1211 expires) | 0-7 | 1 | 2 |
| P1215 | Holding brake enable (0 = Motor holding brake disabled; 1 = Motor holding brake enabled) | 0-1 | 0 | 2 |
| P1216 | Holding brake release delay [s] | 0.0 - 20.0 | 1.0 | 2 |
| P1217 | Holding time after ramp down [s] | 0.0 - 20.0 | 1.0 | 2 |
| P1227[0...2] | Zero speed detection monitoring time [s] | 0.0 - 300.0 | 4.0 | 2 |
| P1232[0...2] | DC braking current [%] | 0 - 250 | 100 | 2 |
| P1233[0...2] | Duration of DC braking [s] | 0.00 - 250.00 | 0.00 | 2 |
| P1234[0...2] | DC braking start frequency [Hz] | 0.00 - 599.00 | 599.00 | 2 |
| P1236[0...2] | Compound braking current [%] | 0 - 250 | 0 | 2 |
| P1237 | Dynamic braking (0 = Disabled; 1 = 5 % duty cycle; 2 = 10 % duty cycle; 3 = 20 % duty cycle; 4 = 50 % duty cycle; 5 = 100 % duty cycle) | 0-5 | 0 | 2 |
| P1300[0...2] | Control mode (0 = V/f with linear characteristic; 5 = V/f for textile applications; 1 = V/f with FCC; 6 = V/f with FCC for textile applications; 2 = V/f with quadratic characteristic; 7 = V/f with quadratic eco; 3 = V/f with programmable characteristic; 19 = V/f control with independent voltage setpoint; 4 = V/f with linear eco) | 0 - 19 | 0 | 2 |
| P1310[0...2] | Continuous boost [%] | 0.0 - 250.0 | 50.0 | 2 |
| P1311[0...2] | Acceleration boost [%] | 0.0 - 250.0 | 0.0 | 2 |
| P1312[0...2] | Starting boost [%] | 0.0 - 250.0 | 0.0 | 2 |
| P1335[0...2] | Slip compensation [%] | 0.0 - 600.0 | 0.0 | 2 |
| P1336[0...2] | Slip limit [%] | 0 - 600 | 250 | 2 |
| r1348 | Economy mode factor [%] | - | - | 2 |
| P1800[0...2] | Pulse frequency [kHz] | 2 - 16 | 4 | 2 |
| P1820[0...2] | Reverse output phase sequence (0 = Forward; 1 = Reverse the Motor) | 0-1 | 0 | 2 |

<!-- page 51 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| P1900 | Select motor data identification (0 = Disabled; 2 = Identification of all parameters in standstill) | 0-2 | 0 | 2 |
| r1926 | Identified gating unit dead time [μs] | - | - | 2 |
| P2010[0...1] | USS / MODBUS baudrate (6 = 9600 bps; 10 = 76800 bps; 7 = 19200 bps; 11 = 93750 bps; 8 = 38400 bps; 12 = 115200 bps; 9 = 57600 bps; Index [0]: USS / MODBUS on RS485; Index [1]: USS on RS232 (reserved)) | 6 - 12 | 8 | 2 |
| P2011[0...1] | USS address | 0 - 31 | 0 | 2 |
| P2021 | Modbus address | 1 - 247 | 1 | 2 |
| P2023 | RS485 protocol selection (0 = None; 1 = USS; 2 = Modbus; Note: After changing P2023, a power-cycle of the inverter (which may take several seconds) is required.) | 0-2 | 1 | 1 |
| r2110[0...3] | CO: Warning number | - | - | 2 |
| P2157[0...2] | Threshold frequency f_2 [Hz] | 0.00 - 599.00 | 30.00 | 2 |
| P2158[0...2] | Delay time of threshold freq f_2 [ms] | 0 - 10000 | 10 | 2 |
| P2159[0...2] | Threshold frequency f_3 [Hz] | 0.00 - 599.00 | 30.00 | 2 |
| P2160[0...2] | Delay time of threshold freq f_3 [ms] | 0 - 10000 | 10 | 2 |
| P2200[0...2] | BI: Enable PID controller | - | 0 | 2 |
| P2201[0...2] | Fixed PID setpoint 1 [%] | -200.00 - 200.00 | 10.00 | 2 |
| P2202[0...2] | Fixed PID setpoint 2 [%] | -200.00 - 200.00 | 20.00 | 2 |
| P2203[0...2] | Fixed PID setpoint 3 [%] | -200.00 - 200.00 | 50.00 | 2 |
| P2204[0...2] | Fixed PID setpoint 4 [%] | -200.00 - 200.00 | 100.00 | 2 |
| P2205[0...2] | Fixed PID setpoint 5 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2206[0...2] | Fixed PID setpoint 6 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2207[0...2] | Fixed PID setpoint 7 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2208[0...2] | Fixed PID setpoint 8 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2209[0...2] | Fixed PID setpoint 9 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2210[0...2] | Fixed PID setpoint 10 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2211[0...2] | Fixed PID setpoint 11 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2212[0...2] | Fixed PID setpoint 12 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2213[0...2] | Fixed PID setpoint 13 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2214[0...2] | Fixed PID setpoint 14 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2215[0...2] | Fixed PID setpoint 15 [%] | -200.00 - 200.00 | 0.00 | 2 |
| P2216[0...2] | Fixed PID setpoint mode (1 = Direct selection; 2 = Binary selection) | 1-2 | 1 | 2 |
| r2224 | CO: Actual fixed PID setpoint [%] | - | - | 2 |
| P2231[0...2] | PID-MOP mode | - | 0 | 2 |

<!-- page 52 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| P2232 | Inhibit reverse direction of PID-MOP (0 = Reverse direction is allowed; 1 = Reverse direction inhibited) | 0-1 | 1 | 2 |
| P2240[0...2] | Setpoint of PID-MOP [%] | -200.00 - 200.00 | 10.00 | 2 |
| P2247[0...2] | PID-MOP ramp-up time of the RFG [s] | 0.00 - 1000.0 | 10.00 | 2 |
| P2248[0...2] | PID-MOP ramp-down time of the RFG [s] | 0.00 - 1000.0 | 10.00 | 2 |
| r2250 | CO: Output setpoint of PID-MOP [%] | - | - | 2 |
| P2253[0...2] | CI: PID setpoint | - | 0 | 2 |
| P2257 | Ramp-up time for PID setpoint [s] | 0.00 - 650.00 | 1.00 | 2 |
| P2258 | Ramp-down time for PID setpoint [s] | 0.00 - 650.00 | 1.00 | 2 |
| r2260 | CO: PID setpoint after PID-RFG [%] | - | - | 2 |
| P2264[0...2] | CI: PID feedback | - | 755[0] | 2 |
| P2265 | PID feedback filter time constant [s] | 0.00 - 60.00 | 0.00 | 2 |
| r2266 | CO: PID filtered feedback [%] | - | - | 2 |
| P2271 | PID transducer type (0 = Disabled; 1 = Inversion of PID feedback signal) | 0-1 | 0 | 2 |
| r2272 | CO: PID scaled feedback [%] | - | - | 2 |
| r2273 | CO: PID error [%] | - | - | 2 |
| P2274 | PID derivative time [s] | 0.000 - 60.000 | 0.000 | 2 |
| P2280 | PID proportional gain | 0.000 - 65.000 | 3.000 | 2 |
| P2285 | PID integral time [s] | 0.000 - 60.000 | 0.000 | 2 |
| P2291 | PID output upper limit [%] | -200.00 - 200.00 | 100.00 | 2 |
| P2292 | PID output lower limit [%] | -200.00 - 200.00 | 0.00 | 2 |
| r2294 | CO: Actual PID output [%] | - | - | 2 |
| P2350 | PID autotune enable (0 = PID autotuning disabled; 1 = PID autotuning via Ziegler Nichols (ZN) standard; 2 = PID autotuning as 1 plus some overshoot (O/S); 3 = PID autotuning as 2 little or no overshoot (O/S); 4 = PID autotuning PI only, quarter damped response) | 0-4 | 0 | 2 |
| P2360[0...2] | Enable cavitation protection (0 = Disable; 1 = Fault; 2 = Warn) | 0-2 | 0 | 2 |
| P2361[0...2] | Cavitation threshold [%] | 0.00 - 200.00 | 40.00 | 2 |
| P2362[0...2] | Cavitation protection time [s] | 0 - 65000 | 30 | 2 |
| P2365[0...2] | Hibernation enable / disable (0 = Disabled; 1 = Enabled) | 0-1 | 0 | 2 |
| P2940 | BI: Release wobble function | - | 0.0 | 2 |
| P2945 | Wobble signal frequency [Hz] | 0.001 - 10.000 | 1.000 | 2 |
| P2946 | Wobble signal amplitude [%] | 0.000 - 0.200 | 0.000 | 2 |
| P2947 | Wobble signal decrement step | 0.000 - 1.000 | 0.000 | 2 |
| P2948 | Wobble signal increment step | 0.000 - 1.000 | 0.000 | 2 |

<!-- page 53 -->

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Parameter list

| Parameter | Description | Range | Factory default | Acc. level |
|---|---|---|---|---|
| P2949 | Wobble signal pulse width [%] | 0 - 100 | 50 | 2 |
| r2955 | CO: Wobble signal output [%] | - | - | 2 |
| r3113.0...15 | CO / BO: Fault bit array | - | - | 1 |
| P3350[0...2] | Super torque mode (0 = Super torque modes disabled; 1 = Super torque enabled; 2 = Hammer start enabled; 3 = Blockage clearing enabled; Index [0]: Inverter data set 0 (DDS0); Index [1]: Inverter data set 1 (DDS1); Index [2]: Inverter data set 2 (DDS2)) | 0-3 | 0 | 2 |
| P3351[0...2] | BI: Super torque enable | - | 0 | 2 |
| P3352[0...2] | Super torque startup mode (0 = Enabled on first run after power-up; 1 = Enabled on every run; 2 = Enabled by digital input) | 0-2 | 1 | 2 |
| P3353[0...2] | Super torque ramp time [s] | 0.0 - 650.0 | 5.0 | 2 |
| P3354[0...2] | Super torque frequency [Hz] | 0.0 - 599.0 | 5.0 | 2 |
| P3355[0...2] | Super torque boost level [%] | 0.0 - 200.0 | 150.0 | 2 |
| P3356[0...2] | Super torque boost time [s] | 0.0 - 20.0 | 5.0 | 2 |
| P3357[0...2] | Hammer start boost level [%] | 0.0 - 200.0 | 150.0 | 2 |
| P3358[0...2] | Number of hammer cycles | 1 - 10 | 5 | 2 |
| P3359[0...2] | Hammer on time [ms] | 0 - 1000 | 300 | 2 |
| P3360[0...2] | Hammer off Time [ms] | 0 - 1000 | 100 | 2 |
| P3361[0...2] | Blockage clearing frequency [Hz] | 0.0 - 599.0 | 5.0 | 2 |
| P3362[0...2] | Blockage clearing reverse time [s] | 0.0 - 20.0 | 5.0 | 2 |
| P3363[0...2] | Enable rapid ramp (0 = Disable rapid ramp for blockage clearing; 1 = Enable rapid ramp for blockage clearing) | 0-1 | 0 | 2 |
| P3364[0...2] | Number of blockage clearing cycles | 1 - 10 | 1 | 2 |
| r3365 | Status word: super torque | - | - | 2 |
| P3852[0...2] | BI: Enable frost protection | - | 0 | 2 |
| P3853[0...2] | Frost protection frequency [Hz] | 0.00 - 599.00 | 5.00 | 2 |
| P3854[0...2] | Condensation protection current [%] | 0 - 250 | 100 | 2 |
| P3900 | End of quick commissioning (0 = No quick commissioning; 1 = End quick commissioning with factory reset; 2 = End quick commissioning; 3 = End quick commissioning only for motor data) | 0-3 | 0 | 1 |
| P8553 | Menu type (0 = Menus with no text; 1 = Menus with some text) | 0-1 | 0 | 1 |

<!-- page 54 -->

Parameter list

SINAMICS V20 Inverter

54

Getting Started, 11/2012, A5E31623806

<!-- page 55 -->

6

Fault and warning codes

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Fault code list

| Fault | Description |
|---|---|
| F1 | Overcurrent |
| F2 | Overvoltage |
| F3 | Undervoltage |
| F4 | Inverter overtemperature |
| F5 | Inverter I2t |
| F6 | Chip temperature rise exceeds critical levels |
| F11 | Motor overtemperature |
| F12 | Inverter temperature signal lost |
| F20 | DC ripple too high |
| F35 | Auto restart after n |
| F41 | Motor data identification failure |
| F51 | Parameter EEPROM fault |
| F52 | Inverter software fault |
| F60 | Asic timeout |
| F61 | MMC / SD card parameter cloning failed |
| F62 | Parameter cloning contents invalid |
| F63 | Parameter cloning contents incompatible |
| F64 | Inverter attempted to do an automatic clone during startup |
| F71 | USS setpoint fault |
| F72 | USS / MODBUS setpoint fault |
| F80 | AI lost input signal |
| F85 | External fault |
| F100 | Watchdog reset |
| F101 | Stack overflow |
| F221 | PID feedback below minimum value |
| F222 | PID feedback above maximum value |
| F350 | Configuration vector for the inverter failed |
| F395 | Acceptance test / confirmation pending |
| F410 | Cavitation protection failure |
| F452 | Belt failure |

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

55

<!-- page 56 -->

Fault and warning codes

Acknowledging / clearing faults
● To navigate through the current list of faults, press

or

.

● To clear / acknowledge the fault, press OK or acknowledge externally if the inverter has
been set up so.
● To ignore the fault, press M .
After you acknowledge or ignore the fault, the screen returns to the previous display. The
fault icon remains lit until the fault is cleared / acknowledged.

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

Alarm code list

| Alarm | Description |
|---|---|
| A501 | Current limit |
| A502 | Overvoltage limit |
| A503 | Undervoltage limit |
| A504 | Inverter overtemperature |
| A505 | Inverter I2t |
| A506 | IGBT junction temperature rise warning |
| A507 | Inverter temperature signal lost |
| A511 | Motor overtemperature I2t |
| A535 | Braking resistor overload |
| A541 | Motor data identification active |
| A600 | RTOS overrun warning |
| A910 | Vdc_max controller deactivated |
| A911 | Vdc_max controller active |
| A912 | Vdc_min controller active |
| A921 | AO parameters not set properly |
| A922 | No load applied to inverter |
| A923 | Both JOG left and JOG right are requested |
| A930 | Cavitation protection warn |
| A936 | PID autotuning active |
| A952 | Belt failure detected |

Acknowledging / clearing alarms
Note
Note that alarms cannot be acknowledged. They are cleared automatically once the warning
has been rectified.

SINAMICS V20 Inverter

56

Getting Started, 11/2012, A5E31623806

<!-- page 57 -->

7

Technical specifications

Electrical specifications
Line supply characteristics

Voltage range

Three phase AC 400 V inverters

Single phase AC 230 V inverters

380 V to 480 V AC (tolerance: -15 % to +10 %)

200 V to 240 V AC (tolerance: -10 % to +10 %)

47 Hz to 63 Hz

47 Hz to 63 Hz

Current derating at high input voltages:

Current derating at high input voltages:

2XWSXWFXUUHQW>@

2XWSXWFXUUHQW>@






























 

 








 

9ROWDJH 9





9ROWDJH 9

Note: For the current derating at 480 V at the
default 4kHz switching frequency and 40°C
surrounding air temperature, refer to the table
in the Section "Ordering data (Page 61)".
Overvoltage category

EN 60664-1 Category III

EN 60664-1 Category III

Permissible supply
configuration

TN, TT, IT1), TT earthed line

TN, TT

Supply environment

Second environment (private power network)

Second environment (private power network)

1)

Note that only unfiltered inverters can be operated on IT power system.

Overload capability
Average output current

100 % rated

Overload current

150 % rated for 60 seconds

Maximum overload cycle

150 % rated for 60 seconds followed by 94.5 % rated for 240 seconds (average 100 %
rated)

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

57

<!-- page 58 -->

Technical specifications

Motor control
Control methods

Linear V/F, quadratic V/F, multi-point V/F, V/F with FCC

Output frequency range

Default range: 0 Hz to 599 Hz
Resolution: 0.01 Hz

Mechanical specifications
Frame size

Net weight (kg)
unfiltered

Gross weight (kg)
filtered

unfiltered

filtered

1.0

1.1

1.4

1.4

0.9

1.0 (0.9 1))

1.3

1.4 (1.3 1))

1.6

1.8

2.1

2.3

Three phase AC 400 V inverters
A

with fan
without fan

B
C
D

2.4

2.6

3.1

3.3

7.5 kW

3.7

4.0

4.3

4.6

11 kW

3.7

4.1

4.5

4.8

15 kW

3.9

4.3

4.6

4.9

Single phase AC 230 V inverters
A

1.0

1.1

1.3

1.4

B

1.6

1.8

2.0

2.1

C

2.5

2.8

3.0

3.2

1)

Weight of Flat Plate inverter (400 V 0.75 kW variant only).

Environmental conditions
Surrounding air
temperature

0 °C to 40 °C: without derating
40 °C to 60 °C: with derating

Storage temperature

- 40 °C to + 70 °C

Protection class

IP 20

Maximum humidity
level

95 % (non-condensing)

Shock and vibration

Long-term storage in the transport packaging according to EN 60721-3-1 Class 1M2
Transport in the transport packaging according to EN 60721-3-2 Class 2M3
Vibration during operation according to EN 60721-3-3 Class 3M2

SINAMICS V20 Inverter

58

Getting Started, 11/2012, A5E31623806

<!-- page 59 -->

Technical specifications

Operating altitude

Up to 4000 m above sea level
1000 m to 4000 m: output current derating
2000 m to 4000 m: input voltage derating
3HUPLVVLEOHRXWSXWFXUUHQW>@

3HUPLVVLEOHLQSXWYROWDJH>@

100

100

90

90
80
77
70

80
70
60

0

1000

2000

3000

4000

60

,QVWDOODWLRQDOWLWXGHDERYHVHDOHYHO>P@

Environmental
classes

0

1000

2000

3000

4000

,QVWDOODWLRQDOWLWXGHDERYHVHDOHYHO>P@

Pollution class: 3S2
Gas class: 3C2 (SO2, H2S)
Climate class: 3K3

Minimum mounting
clearance

Top: 100 mm
Bottom: 100 mm (85 mm for fan-cooled frame size A)
Side: 0 mm

Standards
European Low Voltage Directive
The SINAMICS V20 product range complies with the requirements of the Low Voltage Directive
2006/95/EC as amended by Directive 98/68/EEC. The units are certified for compliance with the
following standards:
EN 61800-5-1 — Semiconductor inverters – General requirements and line commutated inverters
European EMC Directive
When installed according to the recommendations described in this manual, the SINAMICS V20
fulfills all requirements of the EMC Directive as defined by the EMC Product standard for Power Drive
Systems EN 61800-3
UL certification (UL508C)
The SINAMICS V20 complies with the appropriate C-tick EMC standard.
ISO 9001

Siemens plc operates a quality management system, which complies with the requirements of ISO
9001.

Certificates can be downloaded from the internet under the following link:
Website for certificates
(http://support.automation.siemens.com/WW/view/en/60668840/134200)

EMC requirements
For more information about the EMC-compliant installation of the inverter, refer to the
SINAMICS V20 Inverter Operating Instructions.

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

59

<!-- page 60 -->

Technical specifications

SINAMICS V20 Inverter

60

Getting Started, 11/2012, A5E31623806

<!-- page 61 -->

8

Ordering data

Three phase AC 400 V variants
Rated
output
power

Rated
input
current

Rated
output
current

Output current
at 480 V at
4kHz / 40°C

Order number

Frame size A

0.37 kW

1.7 A

1.3 A

1.3 A

6SL3210-5BE13-7UV0

6SL3210-5BE13-7CV0

(without fan)

0.55 kW

2.1 A

1.7 A

1.6 A

6SL3210-5BE15-5UV0

6SL3210-5BE15-5CV0

0.75 kW

2.6 A

2.2 A

2.2 A

6SL3210-5BE17-5UV0

6SL3210-5BE17-5CV0

0.75 kW

2.6 A

2.2 A

2.2 A

-

6SL3216-5BE17-5CV0

1.1 kW

4.0 A

3.1 A

3.1 A

6SL3210-5BE21-1UV0

6SL3210-5BE21-1CV0

(with single fan) 1.5 kW

5.0 A

4.1 A

4.1 A

6SL3210-5BE21-5UV0

6SL3210-5BE21-5CV0

2.2 kW

6.4 A

5.6 A

4.8 A

6SL3210-5BE22-2UV0

6SL3210-5BE22-2CV0

3.0 kW

8.6 A

7.3 A

-

6SL3210-5BE23-0UV0

6SL3210-5BE23-0CV0

(with single fan) 4.0 kW

11.3 A

8.8 A

8.24 A

6SL3210-5BE24-0UV0

6SL3210-5BE24-0CV0

Frame size C

5.5 kW

15.2 A

12.5 A

11 A

6SL3210-5BE25-5UV0

6SL3210-5BE25-5CV0

Frame size D

7.5 kW

20.7 A

16.5 A

16.5 A

6SL3210-5BE27-5UV0

6SL3210-5BE27-5CV0

(with two fans)

11 kW

30.4 A

25 A

21 A

6SL3210-5BE31-1UV0

6SL3210-5BE31-1CV0

15 kW

38.1 A

31 A

31 A

6SL3210-5BE31-5UV0

6SL3210-5BE31-5CV0

Component

1)

Frame size A

Frame size B

unfiltered

filtered

(with single fan)

1)

This variant refers to the Flat Plate inverter with a flat plate heatsink.

Single phase AC 230 V variants
Component

Rated output
power

Rated input
current

Rated output
current

Order number

Frame size A

0.12 kW

2.3 A

0.9 A

6SL3210-5BB11-2UV0

6SL3210-5BB11-2AV0

(without fan)

0.25 kW

4.5 A

1.7 A

6SL3210-5BB12-5UV0

6SL3210-5BB12-5AV0

0.37 kW

6.2 A

2.3 A

6SL3210-5BB13-7UV0

6SL3210-5BB13-7AV0

0.55 kW

7.7 A

3.2 A

6SL3210-5BB15-5UV0

6SL3210-5BB15-5AV0

0.75 kW

10 A

3.9 A

6SL3210-5BB17-5UV0

6SL3210-5BB17-5AV0

Frame size B

1.1 kW

14.7 A

6.0 A

6SL3210-5BB21-1UV0

6SL3210-5BB21-1AV0

(with single fan)

1.5 kW

19.7 A

7.8 A

6SL3210-5BB21-5UV0

6SL3210-5BB21-5AV0

Frame size C

2.2 kW

27.2 A

11 A

6SL3210-5BB22-2UV0

6SL3210-5BB22-2AV0

(with single fan)

3.0 kW

32 A

13.6 A

6SL3210-5BB23-0UV0

6SL3210-5BB23-0AV0

unfiltered

filtered

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

61

<!-- page 62 -->

Ordering data

Options and spare parts
Option / spare part

Available for

Parameter Loader

Frame sizes A to D

6SL3255-0VE00-0UA0

External BOP

Frame sizes A to D

6SL3255-0VA00-4BA0

BOP Interface Module

Frame sizes A to D

6SL3255-0VA00-2AA0

Connecting cable (external BOP to BOP
Interface Module)

Frame sizes A to D

6SL3256-0VP00-0VA0

Dynamic braking module

Frame sizes A to C

6SL3201-2AD20-8VA0

Braking resistor

Three phase AC 400 V inverters
Frame size A

Order number

0.37 to 1.5 kW

6SE6400-4BD11-0AA0

2.2 kW

6SE6400-4BD12-0BA0

Frame size B
6SE6400-4BD16-5CA0

Frame size C
Frame size D

7.5 to 11 kW
15 kW

6SE6400-4BD21-2DA0

Single phase AC 230 V inverters
Frame size A

6SE6400-4BC05-0AA0

Frame size B

6SE6400-4BC11-2BA0

Frame size C

2.2 kW
3 kW

Line reactor

6SE6400-4BC12-5CA0

Three phase AC 400 V inverters
Frame size A

Frame size B

0.37 to 0.55 kW

6SE6400-3CC00-2AD3

0.75 to 1.1 kW

6SE6400-3CC00-4AD3

1.5 kW

6SE6400-3CC00-6AD3

2.2 kW

6SE6400-3CC01-0BD3

3 kW
4 kW

Frame size D

6SE6400-3CC01-4BD3
6SE6400-3CC02-2CD3

Frame size C
7.5 kW
11 kW

6SE6400-3CC03-5CD3

15 kW
Single phase AC 230 V inverters
Frame size A

0.12 to 0.25 kW

6SE6400-3CC00-4AB3

0.37 to 0.75 kW

6SE6400-3CC01-0AB3
6SE6400-3CC02-6BB3

Frame size B
Frame size C

2.2 kW
3 kW

Output reactor

6SE6400-3CC03-5CB3

Three phase AC 400 V inverters
Frame size A

0.37 to 1.5 kW

6SE6400-3TC00-4AD2

2.2 kW

6SE6400-3TC01-0BD3

Frame size B
Frame size C

6SE6400-3TC03-2CD3

SINAMICS V20 Inverter

62

Getting Started, 11/2012, A5E31623806

<!-- page 63 -->

Ordering data

Option / spare part

Available for

Order number

Frame size D
Single phase AC 230 V inverters
Frame size A

6SE6400-3TC00-4AD3

Frame size B

6SE6400-3TC01-0BD3

Frame size C

2.2 kW
3 kW

External EMC filter

6SE6400-3TC03-2CD3

Three phase AC 400 V inverters
Frame size A

6SL3203-0BE17-7BA0

Frame size B

6SL3203-0BE21-8BA0

Frame size C
Frame size D

6SL3203-0BE23-8BA0

Single phase AC 230 V inverters
Frame size A

6SE6400-2FL01-0AB0

Frame size B

6SE6400-2FL02-6BB0

Frame size C

2.2 kW
3 kW

Shield connection kit

Memory card

Frame size A

MMC card

Not yet identified
6SL3266-1AA00-0VA0

Frame size B

6SL3266-1AB00-0VA0

Frame size C

6SL3266-1AC00-0VA0

Frame size D

6SL3266-1AD00-0VA0

Frame sizes A to D

6SL3254-0AM00-0AA0

SD card

6ES7954-8LB01-0AA0

Operating Instructions (Chinese version)

Frame sizes A to D

6SL3298-0AV02-0FP0

Replacement fan

Frame size A

6SL3200-0UF01-0AA0

Frame size B

6SL3200-0UF02-0AA0

Frame size C

6SL3200-0UF03-0AA0

Frame size D

6SL3200-0UF04-0AA0

SINAMICS V20 Inverter
Getting Started, 11/2012, A5E31623806

63

<!-- page 64 -->

Ordering data

SINAMICS V20 Inverter

64

Getting Started, 11/2012, A5E31623806
