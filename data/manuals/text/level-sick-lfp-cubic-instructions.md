---
id: level-sick-lfp-cubic-instructions
product: SICK LFP Cubic
component: Sensore di livello igienico a radar guidato
tags: LT1, LT2, LT3, LT4
---

<!-- page 1 -->

O P E R AT I N G I N S T R U C T I O N S

LFP CUBIC

TDR level sensor

en

<!-- page 2 -->

﻿

Described product
LFP Cubic
Manufacturer
SICK AG
Erwin-Sick-Str. 1
79183 Waldkirch, Germany
Germany
Legal notices
This work is protected by copyright. The associated rights are reserved by SICK AG.
Reproduction of this document or parts of this document is only permissible within
the limits of the legal determination of Copyright Law.
Any modification, expurgation, or translation of this document is prohibited without
the express written permission of SICK AG.
The trademarks stated in this document are the property of their respective owner.
© SICK AG. All rights reserved.
Original document
This document is an original document of SICK AG.

2

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 3 -->

﻿

Contents
1

About this document........................................................................................6
1.1
1.2
1.3
1.4
1.5

2

Safety information............................................................................................8
2.1
2.2
2.3
2.4
2.5
2.6
2.7
2.8

3

3.2

3.3

Transport. ..................................................................................................................14
Transport inspection.................................................................................................14
Storage.......................................................................................................................14

Mounting. ........................................................................................................ 15
5.1

5.2
5.3

5.4

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

Product ID..................................................................................................................11
3.1.1
Information on the housing. .....................................................................11
3.1.2
Type code...................................................................................................11
Product characteristics.............................................................................................12
3.2.1
Device view................................................................................................12
3.2.2
Operating buttons. ....................................................................................12
Product features and functions. ..............................................................................12
3.3.1
Principle of operation................................................................................12
3.3.2
Fields of application..................................................................................13

Transport and storage................................................................................... 14
4.1
4.2
4.3

5

Intended use. .............................................................................................................. 8
Incorrect use. .............................................................................................................. 8
Limitation of liability.................................................................................................... 8
Modifications and conversions. ................................................................................. 8
Requirements for skilled persons and operating personnel.................................... 9
Operational safety and particular hazards................................................................ 9
General safety notes.................................................................................................10
Repairs.......................................................................................................................10

Product description. ...................................................................................... 11
3.1

4

Information on the operating instructions................................................................. 6
Scope........................................................................................................................... 6
Explanation of symbols............................................................................................... 6
Further information..................................................................................................... 7
Customer service. ....................................................................................................... 7

Installation conditions. .............................................................................................15
5.1.1
Installation in a container.........................................................................15
5.1.2
Installation in a metal immersion tube or metal bypass........................16
5.1.3
Rope probe in the metallic container. .....................................................17
Mounting the coaxial tube........................................................................................18
Shortening or replacing the probe rod/rope probe. ...............................................18
5.3.1
Procedure. .................................................................................................18
5.3.2
Shortening the rope probe. ......................................................................19
Mounting the probe rod............................................................................................20

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

3

<!-- page 4 -->

﻿

6

Electrical installation..................................................................................... 21
6.1
6.2

7

Commissioning. ............................................................................................. 24
7.1
7.2
7.3

8

Quick commissioning (with factory settings)...........................................................24
Advanced commissioning.........................................................................................24
Foam commissioning (with factory settings)...........................................................26

Operation. ....................................................................................................... 28
8.1

8.2

8.3

8.4

4

Safety.........................................................................................................................21
6.1.1
Notes on the electrical installation. .........................................................21
Electrical connection. ...............................................................................................22
6.2.1
Overview of the electrical connections....................................................22
6.2.2
Pin assignment, M12 plug connector, 5-pin. ..........................................22
6.2.3
Pin assignment, M12 plug connector, 8-pin. ..........................................23

Display and pushbuttons..........................................................................................28
8.1.1
Variants with two switching outputs.........................................................28
8.1.2
Variants with four switching outputs........................................................28
8.1.3
IO-Link........................................................................................................28
Configuring the switching outputs............................................................................29
8.2.1
Switching hysteresis and window function..............................................29
8.2.2
Normally open with adjustable hysteresis...............................................30
8.2.3
N/C output with configurable hysteresis. ................................................31
8.2.4
N/O output with window function. ...........................................................32
8.2.5
N/C output with window function.............................................................33
8.2.6
N/O output with error signal.....................................................................34
8.2.7
N/C output with error signal ....................................................................34
Configure the analog output.....................................................................................35
8.3.1
Automated signal detection......................................................................35
8.3.2
Current output 4 mA ... 20 mA.................................................................35
8.3.3
Voltage output 0 V ... +10 V......................................................................35
Advanced functions. .................................................................................................36
8.4.1
Expert mode. .............................................................................................36
8.4.2
Filtering measured values. .......................................................................36
8.4.3
Automated adjustment of the interference signal limit..........................37
8.4.4
Blanking the interference signals in the masked zone. .........................37
8.4.5
Selection of evaluation method. ..............................................................38
8.4.6
Testing the configuration. .........................................................................38
8.4.7
Configuring the probe length....................................................................39
8.4.8
Teaching in static interference signals. ...................................................40
8.4.9
Evaluating signal quality. ..........................................................................40
8.4.10 Changing the coaxial cable length ..........................................................41
8.4.11 Activating the display lock. .......................................................................42
8.4.12 Selecting the display unit (millimeter/inch).............................................42
8.4.13 Setting the offset ......................................................................................43
8.4.14 Resetting the calibration. .........................................................................44

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 5 -->

﻿

9

Menu overview. .............................................................................................. 45

10

Overview of parameters................................................................................ 48

11

Troubleshooting.............................................................................................. 52
11.1
11.2
11.3
11.4

12

Error message on the display...................................................................................52
Operating the display................................................................................................53
Outputs......................................................................................................................54
Error behavior............................................................................................................54

Repair work..................................................................................................... 55
12.1 Maintenance. ............................................................................................................55
12.2 Returns. .....................................................................................................................55

13

Disposal........................................................................................................... 56

14

Technical data. ............................................................................................... 57
14.1
14.2
14.3
14.4
14.5
14.6
14.7

Features.....................................................................................................................57
Performance..............................................................................................................57
Mechanics/materials................................................................................................58
Reference conditions................................................................................................58
Ambient conditions...................................................................................................58
Electrical connection values. ...................................................................................59
Measurement accuracy............................................................................................60

15

Dimensional drawings. ................................................................................. 62

16

Factory setting................................................................................................ 65

17

Accessories..................................................................................................... 66

18

Media list......................................................................................................... 67

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

5

<!-- page 6 -->

1

ABOUT THIS DOCUMENT

1

About this document

1.1

Information on the operating instructions
These operating instructions provide important notes on how to use sensors from SICK AG.
Prerequisites for safe work are:
••

Compliance with all safety notes and handling instructions supplied.

••

Compliance with local work safety regulations and general safety regulations for
sensor applications.

The operating instructions are intended to be used by qualified personnel and electrical
specialists.
Note:
Read these operating instructions carefully before starting any work on the device,
in order to familiarize yourself with the device and its functions.
The instructions constitute an integral part of the product and are to be stored in the
immediate vicinity of the device so they remain accessible to staff at all times. Should
the device be passed on to a third party, these operating instructions should be handed
over with it.
These operating instructions do not provide information on operating the machine
in which the sensor is integrated. For information about this, refer to the operating
instructions of the particular machine.

1.2

Scope
These operating instructions serve to incorporate a sensor into a customer system.
Instructions are given by stages for all actions required.
These instructions apply to all available device variants of the sensor. For more detailed
information for the identification of the available device types, see “3.1.2 Type code”.
Available device variants are listed on the online product page:
bb

www.sick.com

Various device variants are used as examples for commissioning, based on the default
parameter settings for the relevant device.
Simplified device name in the document: In the following, the sensor is referred to in
simplified form as LFP. Exceptions occur where a distinction between device variants is
required due to different technical features or functions. In this case, the complete type
designation (e.g. LFP Cubic) is used.

1.3

Explanation of symbols
Warnings and important information in this document are labeled with symbols.
The warnings are introduced by signal words that indicate the extent of the danger.
These warnings must be observed at all times and care must be taken to avoid
accidents, personal injury, and material damage.
DANGER
… indicates a situation of imminent danger, which will lead to a fatality or serious
injuries if not prevented.

6

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 7 -->

ABOUT THIS DOCUMENT

1

WARNING
… indicates a potentially dangerous situation, which may lead to a fatality or serious
injuries if not prevented.
CAUTION
… indicates a potentially dangerous situation, which may lead to minor/slight injuries
if not prevented.
IMPORTANT
… indicates a potentially harmful situation, which may lead to material damage if
not prevented.
NOTE
… highlights useful tips and recommendations as well as information for efficient
and trouble-free operation.

1.4

Further information
NOTE
All the documentation available for the sensor can be found on the online product
page at:
www.sick.com
The following information is available for download there:
•• Model-specific online data sheets for device variants, containing technical data,
dimensional drawings and diagrams
•• EU declaration of conformity for the product family
•• Dimensional drawings and 3D CAD dimension models in various electronic formats
•• These operating instructions, available in English and German, and in other languages if necessary
•• Other publications related to the sensors described here (e.g. IO-Link)
•• Publications dealing with accessories

1.5

Customer service
If you require any technical information, our customer service department will be happy
to help. To find your representative, see the final page of this document.
NOTE
Before calling, make a note of all sensor data such as type code, serial number, etc. to
ensure faster processing.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

7

<!-- page 8 -->

2

SAFETY INFORMATION

2

Safety information

2.1

Intended use
The LFP is designed for both continuous level measurement and point level measurement
in nearly all liquids (a list of the possible media can be found in the appendix).
The sensor is not affected by changes in the properties of the liquids to be measured.
The LFP can be used in metal containers or bypass/immersion pipes. A coaxial tube is
required for use in plastic containers.

2.2

Incorrect use
Any use outside of the stated areas, in particular use outside of the technical
specifications and the requirements for intended use, will be deemed incorrect use.
If the operator wishes to use the sensor in other conditions or in different environments, then the manufacturing service may issue an operating license in consultation
with the customer and in exceptional cases.

2.3

Limitation of liability
Applicable standards and regulations, the latest state of technological development,
and our many years of knowledge and experience have all been taken into account
when assembling the data and information contained in these operating instructions.
The manufacturer accepts no liability for damage caused by:
••

Failing to observe the operating instructions

••

Incorrect use

••

Use by untrained personnel

••

Unauthorized conversions

••

Technical modifications

••

Use of unauthorized spare parts, consumables, and accessories

With special variants, where optional extras have been ordered, or owing to the latest
technical changes, the actual scope of delivery may vary from the features and illustrations shown here.

2.4

Modifications and conversions
IMPORTANT
Modifications and conversions to the sensor and/or the installation may result in
unforeseeable dangers.
Interrupting or modifying the sensor or SICK software will invalidate any warranty claims
against SICK AG. This applies in particular to opening the housing, even as part of
mounting and electrical installation.
Before technical modifications to and expansions of the sensor, the prior written
approval of the manufacturer must be obtained.

8

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 9 -->

SAFETY INFORMATION

2.5

2

Requirements for skilled persons and operating personnel
WARNING
Risk of injury due to insufficient training.
Improper handling of the sensor may result in considerable personal injury and material
damage.
•• All work must only ever be carried out by the stipulated persons.
The operating instructions state the following qualification requirements for the various
areas of work:
••

Instructed personnel have been briefed by the operator about the tasks assigned
to them and about potential dangers arising from improper action.

••

Skilled personnel have the specialist training, skills, and experience, as well as
knowledge of the relevant regulations, to be able to perform tasks delegated to
them and to detect and avoid any potential dangers independently.

••

Electricians have the specialist training, skills, and experience, as well as
knowledge of the relevant standards and provisions to be able to carry out work on
electrical systems and to detect and avoid any potential dangers independently.
In Germany, electrical specialists must meet the specifications of the BGV A3 Work
Safety Regulations (e.g., Master Electrician). Other relevant regulations applicable
in other countries must be observed.

The following qualifications are required for various activities:

2.6

Activities
Mounting, maintenance

Qualification

Electrical installation,
device replacement

• Practical electrical training
• Knowledge of current electrical safety regulations
• Knowledge of device control and operation in the particular
application concerned (e.g.conveying line)

Commissioning,
configuration

• Basic knowledge of the control system in use
• Basic knowledge of the design and setup of the described
connections and interfaces
• Basic knowledge of data transmission

Operation of the device for
the particular application

• Knowledge of device control and operation in the particular
area of application concerned (e.g. bottling plant)
• Knowledge of the software and hardware environment for the
particular application concerned (e.g. bottling plant)

• Basic practical technical training
• Knowledge of the current safety regulations in the workplace

Operational safety and particular hazards
Please observe the safety notes and the warnings listed here and in other chapters
of these operating instructions to reduce the possibility of risks to health and avoid
dangerous situations.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

9

<!-- page 10 -->

2

2.7

2.8

SAFETY INFORMATION

General safety notes
••

Read the operating instructions prior to commissioning.

••

These operating instructions are valid for devices with a firmware version higher
than V4.00.

••

The LFP is not a safety component under the EU Machinery Directive.

••

Observe national safety and work safety regulations.

••

Wiring work and the opening and closing of electrical connections may only be
carried out when the power is switched off.

••

The radiated power is far lower than that from telecommunication equipment.
According to current scientific research, the operation of this device can be
classified as safe and nonhazardous.

Repairs
Repair work on the sensor may be performed only by qualified and authorized
personnel from SICK AG. Interruptions or modifications to the sensor on the part
of the customer will invalidate any warranty claims against SICK AG.

10

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 11 -->

PRODUCT DESCRIPTION

3

Product description

3.1

Product ID

3.1.1

Information on the housing
There is information printed on the housing identifying the sensor and its
electrical connection.

3.1.2

Type code
LFP
1

x
2

Position
1
2

3

4

5

6
7

-

x
3

x
4

x
5

M
6

3

x
7

Description
Product group
LFP (level sensors)
Probe length in mm
0025: without probe
0200: in 10 mm increments; rope probe in 1000 mm increments
4000: 4000 mm
Process connection/probe version
A:		
G ¾ A / single-rod probe 1.4404 interchangeable, 100 °C; 10 bar
B:		
¾" NPT / single-rod probe 1.4404 interchangeable, 100 °C; 10 bar
E:		
G ¾ A / 3 mm rope probe, 1.4404 interchangeable, 100 °C; 10 bar
F:		
¾" NPT / 3 mm rope probe, 1.4404 interchangeable, 100 °C; 10 bar
Housing, display/device connection
4:		
Plastic housing with display / M12 x 1 / 5-pin male connector
5:		
Plastic housing with display / M12 x 1 / 8-pin male connector
Application/design
B:		
Remote amplifier; length of cable 1 m
C:		
Remote amplifier; length of cable 2 m
D:		
Remote amplifier; length of cable 3.3 m
N:		
Standard
Signal output
M:
4 mA ... 20 mA / 0 V ... +10 V reversible
Switching output
B:		
1 x PNP + 1 x PNP/NPN
C:		
1 x PNP + 3 x PNP/NPN

Not all variants of the type code can be combined with each other!

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

11

<!-- page 12 -->

3

PRODUCT DESCRIPTION

3.2

Product characteristics

3.2.1

Device view

4
3
2

1
1
Fig. 1: LFP Cubic (standard version)

3.2.2

1

Sample probe

2

Electrical connection

3

Operating buttons

4

Display

Operating buttons
The sensor is operated using the display and operating buttons.
For a detailed description of the pushbuttons and their functions, see “8.1 Display and
pushbuttons”.

3.3

Product features and functions

3.3.1

Principle of operation
The LFP uses TDR (Time Domain Reflectometry) technology.
This is a process to determine transit times of electromagnetic waves. The sensor
electronics generate a low-energy electromagnetic pulse, which is linked to and runs
along the probe.
If this pulse strikes the surface of the liquid to be measured, a portion of the pulse
is reflected there and is conducted back up along the probe path to the electronics,
which then calculate the level based on the time difference between the sent and the
received pulse.
The sensor can output this level as a continuous measured value (analog output) and
can also derive two and/or four freely positionable switching points from it (switching
outputs).
IO-Link communication is also available for the switching output (Q1),
see “8.1.3 IO-Link”.

12

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 13 -->

PRODUCT DESCRIPTION

3.3.2

3

Fields of application
The innovative TDR technology enables reliable level measurement which is largely
application-independent. The LFP is suitable for both continuous level measurement
and point level measurement in nearly all liquids.
The sensor is not affected by changes in the properties of the liquids to be measured.
The LFP can be used in metal containers or bypass/immersion pipes. A coaxial tube is
required for use in plastic containers.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

13

<!-- page 14 -->

4

TRANSPORT AND STORAGE

4

Transport and storage

4.1

Transport
For your own safety, please read and observe the following notes:
IMPORTANT
Damage to the sensor due to improper transport.
•• The device must be packaged for transport with protection against shock and damp.
•• Recommendation: Use the original packaging as it provides the best protection.
•• Transport should be performed by specialist staff only.
•• The utmost care and attention is required at all times during unloading and
transportation on company premises.
•• Note the symbols on the packaging.
•• Do not remove packaging until immediately before you start mounting.

4.2

Transport inspection
Immediately upon receipt at the receiving work station, check the delivery for
completeness and for any damage that may have occurred in transit. In the case of
transit damage that is visible externally, proceed as follows:
••

Do not accept the delivery or only do so conditionally.

••

Note the scope of damage on the transport documents or on the transport
company's delivery note.

••

File a complaint.

Note:
Complaints regarding defects should be filed as soon as these are detected. Damage
claims are only valid before the applicable complaint deadlines.

4.3

Storage
Store the device under the following conditions:

14

••

Recommendation: Use the original packaging.

••

Do not store outdoors.

••

Store in a dry area that is protected from dust.

••

To ensure that any residual moisture present can escape, do not store
in airtight containers.

••

Do not expose to any aggressive substances.

••

Protect from sunlight.

••

Avoid mechanical shocks.

••

Storage temperature: see “12 Repair work”.

••

Relative humidity: see “12 Repair work”.

••

For storage periods of longer than 3 months, check the general condition
of all components and packaging on a regular basis.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 15 -->

MOUNTING

5

Mounting

5.1

Installation conditions

5

The LFP is mounted vertically from above into the container or bypass, using its process
connection. The LFP level sensor has a G ¾ or ¾" NPT threaded connection. A minimum
connecting piece diameter in accordance with the diagrams below must be observed.
The LFP must be installed so that after mounting there is sufficient distance to other tank
components (e.g. supply tubes, other measurement devices), the container wall or the
container bottom. These minimum distances are also specified in the diagrams.
The LFP can also be used in a metal immersion pipe or bypass. The installation
conditions are shown in the Figure on page 15.
Ensure that there is a good metallic connection between the LFP measuring device and
the tank/bypass. When operating the sensor, ensure that the ambient temperature is not
above or below the limits.
Insulating the sensor housing is not permitted for tanks with hot media.
When positioning the device, ensure that the sensor is not directly exposed to the filling flow.
The sensor housing can be rotated 360°, allowing for the cable outlet to be positioned
freely.
5.1.1

Installation in a container
Note:
The distances are identical for the sensor with remote amplifier.

D



A

B

B

C



Fig. 2:

LFP Cubic

1 Mono-probe with metallic containers
Installation in the nozzle
D ≥ DN 25
Distance to container wall/container
bottom:
A ≥ 50 mm
B ≥ 10 mm
Distance to components built into the
container
≥ 100 mm

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

2 Coaxial tube in metallic and non-metallic
containers

C = In the case of a coaxial probe there
are no minimum distances from the container wall and built-in components to be
observed.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

15

<!-- page 16 -->

5

5.1.2

MOUNTING

Installation in a metal immersion tube or metal bypass


D

B


Fig. 3:

LFP Cubic

1 Centering
2 D ≥ DN 40
Distance to bypass/container bottom
B ≥ 10 mm

Centering: To prevent contact between the probe and the bypass pipe during
oscillations, the probe should be centered according to its length and depending on the
diameter of the bypass pipe. To do this, it is necessary to insert one or two centering
pieces, see “17 Accessories”.

16

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 17 -->

MOUNTING

5.1.3

5

Rope probe in the metallic container

D





max.

X

F = 250 N

M

A

Fig. 4:

LFP Cubic

1
2

Rope weight
Bracket rope tension

Installation in the nozzle: D ≥ DN 25
Container wall/container bottom distance: A ≥ 50 mm
Distance from components built into container: ≥ 100 mm
Mounting the mono-probe
M = Measuring range
X = No measurement is possible in this area
Container welding seams may affect the measurement accuracy.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

17

<!-- page 18 -->

5

5.2

MOUNTING

Mounting the coaxial tube
See the operating instructions for the coaxial tube (8015674) at www.sick.com.

5.3

Shortening or replacing the probe rod/rope probe
If the probe rod or rope probe is too long for the application, it can be shortened to the
container height. In this case, you should not shorten the probe beyond its minimum
length of 100 mm. If the LFP is to be used in a hygienic application, then be sure that
the roughness of Ra≤0.8 µm is reestablished on the shortened machined surfaces of
the mono-probe.

5.3.1

Procedure
Shorten the probe rod and/or rope probe as desired. Adjust the new probe length in the
LFP, see “8.4.7 Configuring the probe length”. Ensure that this correction corresponds
to the probe length, because an incorrect value in the Length menu has a direct effect
on measurement accuracy and can lead to faults. The probe length L is set out in
Chapter “15 Dimensional drawings”.
The probe rod and/or the rope probe can be swapped. Use a suitable tool. If the system
experiences strong vibrations, secure the probe with thread-locking lacquer.

18

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 19 -->

MOUNTING

5.3.2

5

Shortening the rope probe





1
2
3

2 mm hexagon screw
Loosen the setscrews (3x)
Rope weight









4
New probe length
5
Shift the rope weight to the desired length
2	Setscrews* (tighten according to desired length 1.5 Nm, 3x)

*It is recommended that the setscrews be secured with a thread-locking lacquer

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

19

<!-- page 20 -->

5

5.4

MOUNTING

Mounting the probe rod

With the LFP Cubic, the probe rod can be modified by the customer. The specifications
for the probe rod should be as follows:
Probe rod diameter:

7 mm … 8 mm

Female thread on the probe rod: M5
min. 10 mm

Material:

Stainless steel
Ø 7...8 mm
( Ø 0.27... 0.31)

Female thread length:

M5

min. 10 (0.39)


1

Probe rod length

Total probe length: 100 mm … 4000 mm
Total probe length = 15 mm + probe rod length
Set the total probe length as described in Chapter “8.4.7 Configuring the probe length”.
The EXPRT-Config-Length menu is password protected. If the system experiences strong
vibrations, secure the probe with thread-locking lacquer.


100 (3.94) ... 4000 (157.48)



15 (0.59)

20

1

Total probe length

2

Probe rod length

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 21 -->

ELECTRICAL INSTALLATION

6

Electrical installation

6.1

Safety

6.1.1

Notes on the electrical installation

6

IMPORTANT
Equipment damage due to incorrect supply voltage!
An incorrect supply voltage may result in damage to the equipment.
•• Only operate the device using a protected low voltage and safe electrical insulation
as per protection class III.
IMPORTANT
Equipment damage or unpredictable operation due to working with live parts.
Working with live parts may result in unpredictable operation.
•• Only carry out wiring work when the power is off.
•• Only connect and disconnect electrical connections when the power is off.
••

The electrical installation must only be performed by electrically qualified personnel.

••

Standard safety requirements must be met when working in electrical systems.

••

Only switch on the supply voltage for the device when the connection tasks have
been completed and the wiring has been thoroughly checked.

••

When using extension cables with open ends, ensure that bare wire ends do not
come into contact with each other (risk of short-circuit when supply voltage is
switched on!). Wires must be appropriately insulated from each other.

••

Wire cross-sections in the supply cable from the customer's power system must be
designed in accordance with the applicable standards. In Germany, observe the
following standards: DIN VDE 0100 (Part 430) and DIN VDE 0298 (Part 4) and/or
DIN VDE 0891 (Part 1).

••

Circuits connected to the device must be designed as SELV circuits
(SELV = Safety Extra Low Voltage).

••

Protect the device with a separate fuse at the start of the supply circuit.

Instructions for laying data cables:
•• Use screened data cables with twisted-pair wires.
•• Implement the screening design correctly and completely.
•• To avoid interference, e.g. from switching power supplies, motors, clocked drives,
and contactors, always use cables and layouts that are suitable for EMC.
•• Do not lay cables over long distances in parallel with voltage supply cables and
motor cables in cable channels.
The IP67 protection class for the device is only achieved under the following conditions:
••

The cable connected at the M12 connection is screwed on.

If this is not done, the device does not fulfill any specified IP enclosure rating!

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

21

<!-- page 22 -->

6

ELECTRICAL INSTALLATION

6.2

Electrical connection

6.2.1

Overview of the electrical connections
The sensor is connected using a pre-assembled female cable connector with
M12 x 1 plug connector (5/8-pin). With the power switched off, plug the female
cable connector into the sensor and screw it tight.
Connect the cable according to its function. After the supply voltage is set up, the
sensor performs a self-test. Once installed, the sensor is ready for operation upon
completion of the self-test (< 5 s). The display shows the current measured value.

Fig. 5:

6.2.2

LFP Cubic

Pin assignment, M12 plug connector, 5-pin
4

3

1

2

5

Fig. 6: M12 x 1 plug connector, 5-pin

22

Contact

Marking

Wire color

Description

1

L+

Brown

Supply voltage

2

QA

White

Analog current/voltage output

3

M

Blue

Ground, reference potential for
current/voltage output

4

C/Q1

Black

Switching output 1, PNP/ IO-Link
communication

5

Q2

Gray

Switching output 2, PNP/ NPN

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 23 -->

ELECTRICAL INSTALLATION

6.2.3

6

Pin assignment, M12 plug connector, 8-pin
8

2

7

3
4

1

5

6

Fig. 7: M12 x 1 plug connector, 8-pin

Contact

Marking

Description

1

L+

Supply voltage

2

Q2

Switching output 2, PNP/ NPN

3

M

Ground, reference potential for current/voltage output

4

C/Q1

Switching output 1, PNP/IO-Link communication

5

Q3

Switching output 3, PNP/NPN

6

Q4

Switching output 4, PNP/NPN

7

QA

Analog current/voltage output

8

No function

The wire colors for 8-pin cables are not standardized. Always note the pin assignment
of the sensor.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

23

<!-- page 24 -->

7

COMMISSIONING

7

Commissioning

7.1

Quick commissioning (with factory settings)
Quick commissioning is used in applications under reference conditions
see “5 Mounting”.
The following rules apply:
••

Use in metallic containers or immersion/bypass pipes

••

Use in plastic container with a coaxial tube, see “17 Accessories”

••

The liquid to be measured has a DK value of > 5, see “18 Media list”

Commissioning
1.

Mount the sensor in accordance with the installation conditions, see “5 Mounting”.

2.

The container must be empty and/or the level must be at least 200 mm below the
end of the probe.

3.

Log in to expert mode, see “8.4.1 Expert mode”.

4.

After mounting, launch the AutCal menu item.

5.

••

Press and hold the Set pushbutton for at least 3 seconds.

••

Use the Set pushbutton to confirm the AutCal menu item and then
use it again to confirm the “OK?” confirmation prompt.

••

The AutCal function is confirmed with !CalOK.

Configure outputs, see “8.2 Configuring the switching outputs”.

Note:
If the AutCal function has been confirmed with !NoSig, relaunch AutCal.
If problems occur during commissioning, see “11 Troubleshooting”.

7.2

Advanced commissioning
Advanced commissioning is required when quick commissioning is not sufficient or if
one of the following situations applies:

24

••

The liquid to be measured has a DK value of < 5, see “18 Media list”.

••

There are tank components which can interfere with the measurement signal
(in the case of the LFP Cubic).

••

In the event of significant ripples in the surface of the liquid.

••

If there are variations in the installation conditions, see “5 Mounting”.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 25 -->

COMMISSIONING

7

Commissioning
1.

Mount the sensor in accordance with the installation conditions, see “5 Mounting”.

2.

Log in to expert mode, see “8.4.1 Expert mode”.

3.

Select the measuring mode.

4.

5.

6.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

••

Access the EXPRT-CONFIG-MeasMd menu using the arrow and Set pushbuttons.

••

HiSpd: max. length = 2005 mm, response time < 400 ms.

••

HiAcc: max. length = 6,005 mm, response time < 2,800 ms, more stable
measured values recommended for liquids with low DKs and where
TrsHld is < 70.

Teach-in the static sources of interference in the tank.
••

Static sources of interference in the tank generated by tubes, beams,
couplings, or a cleaning ball are taught into the system as standard.

••

Access the EXPRT-CONFIG-CalRng menu using the arrow and Set pushbuttons.
The following rules apply:
••

Teach-in depth starts from the LFP process connection

••

Teach-in depth should cover all interference signals

••

Maximum teach-in depth (recommended) = probe length

••

Set the value range between 95 mm … 6,005 mm

••

If the tank cannot be emptied completely, the CalRng teach-in depth must be
adapted accordingly.

••

The level must be at least 200 mm below the CalLen and/or the end of the
probe.

Launch the AutCal function.
••

Access the AutCal menu using the arrow and Set pushbuttons.

••

The following information applies: The probe must not be covered with liquid
in the CalRng set in step 4 (teach-in depth + 200 mm).

••

Use the Set pushbutton to confirm the AutCal menu item and then use it again
to confirm the “Ok?” confirmation prompt.

••

The AutCal function is confirmed with !CalOK.

Analyze the signal quality.
••

The signal quality can be analyzed when the device is installed,
see “8.4.9 Evaluating signal quality”.

••

In the event of problems:
••

Reduce the value in the EXPRT-CONFIG-TrsHld menu.

••

Set the parameter to HiAcc in the EXPRT-CONFIG-MeasMd menu.

••

Switch on the filters in the Set filters menu.

••

Reduce the parameter in the EXPRT-CONFIG-MaxCol menu.

7.

Configure the filter (see Chapter “8.4.2 Filtering measured values”).

8.

Perform maximum change of level/plausibility check
(see Chapter “8.4.2 Filtering measured values”).

9.

Configure outputs (“8.2 Configuring the switching outputs”).

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

25

<!-- page 26 -->

7

COMMISSIONING

Note:
•• Use the foam commissioning instructions for applications with foam.
•• The sensor automatically quits expert mode after 5 minutes of inactivity on
the display.
•• Any of the following processes voids the configuration (AutCal):
•• Changing the probe length
•• Changing the measuring mode
•• Changing the teach-in depth
If problems occur during commissioning, see “11 Troubleshooting”.

7.3

Foam commissioning (with factory settings)
For use in applications with a significant buildup of foam.
Performing foam calibration
1.

Mount the sensor in accordance with the installation conditions, see “5 Mounting”.

2.

Log in to expert mode, see “8.4.1 Expert mode”.

3.

Empty the tank completely.

4.

••

The probe rod must be completely free from medium and foam.

••

Buildup must be removed from the probe.

••

The end of the probe must not be fixed to the bottom of the tank.

Select the measuring mode.
••

5.

Select mode
Access the EXPRT-Config-Mode using the arrow and Set pushbuttons, and configure to Foam.

6.

Perform the empty calibration.
••

Access the EXPRT-Foam-CalEmp menu using the arrow and Set pushbuttons.

••

!CalOk: Proceed to step 7.

••

!faild: Ensure that the tank is empty and repeat step 6.

7.

Fill with medium (without foam) until the probe is covered by at least 200 mm.
The maximum level must remain 200 mm from the process connection, howeve

8.

Perform EXPRT-Foam-CalMed.

9.

26

Access the EXPRT-Config-MeasMd menu using the arrow and Set
pushbuttons, and configure to HiAcc.

••

!CalOk: Everything in working order, proceed to step 9.

••

!faild: Carry out step 8 again.
The LFP must now display a valid measured value.

Check the foam calibration in EXPRT-INFO-CalSta.
••

FomCal: Foam commissioning was completed successfully.

••

CalMis: Commissioning unsuccessful. Please repeat the process.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 27 -->

COMMISSIONING

7

Note:
•• Measurement deviation can be higher.
•• Signal quality 1 and 2 are not counted.
•• The sensor automatically quits expert mode after 5 minutes of inactivity on
the display.
•• Configuration (foam teach) does not take place in the following processes:
•• Changing the probe length
•• Changing the measuring mode
•• Changing the teach-in depth
•• Performing AutCal
If problems occur during commissioning, see “11 Troubleshooting”.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

27

<!-- page 28 -->

8

OPERATION

8

Operation

8.1

Display and pushbuttons
All lengths specified in the menu refer to the end of the probe and/or, for a configured
offset (for LFP Cubic see “8.4.7 Configuring the probe length”), to the tank bottom.
You can access the menu by pressing the Set pushbutton for at least three seconds.

8.1.1

Variants with two switching outputs
Q1 Q2

1000 mm

39,4 in

Arrow pushbuttons:

Navigating in the menu and changing values

Set pushbutton:

Saving and confirming

Esc pushbutton:

Exiting the operating menu step-by-step

Note:
A bar graph above the unit symbol indicates the statuses of the switching outputs
when using millimeters as the unit. This display is not available when inches are
selected as the unit.
8.1.2

Variants with four switching outputs
Q1/2/3/4

1000 mm

8.1.3

39,4 in

Arrow pushbuttons:

Navigating in the menu and changing values

Set pushbutton:

Saving and confirming

Esc pushbutton:

Exiting the operating menu step-by-step

IO-Link
For operation over IO-Link, an IODD file and a description of the available telegram
parameters are available for download at www.sick.com.

28

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 29 -->

OPERATION

8.2

Configuring the switching outputs

8.2.1

Switching hysteresis and window function

8

Depending on 2 or 4 output variants
Level
SP
RP
t

high

HNO

low

high
low

If the level is fluctuating around the
target value (e.g. ripple movement
during filling), the hysteresis keeps the
switching status of the outputs stable.
When the level is increasing, the
output switches when the respective
switching point (SP) is reached; if the
level sinks again, the output switches
back only after the reset switching
point (RP) has been reached.

HNC

Depending on 2 or 4 output variants
Level

FH
FL
t

high
low

high
low

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

FNC
FNO

The window function enables monitoring of a defined range. If the level
is between window high (FH) and
window low (FL), the output will be
active (normally open) and/or inactive
(normally closed).
The error status of the measuring
device reflects the cable break
monitoring. During an error status,
the measuring device switches to
a safe state; i.e. the switching outputs
become inactive.
As far as the downstream signal
evaluation is concerned, this
corresponds to a cable break.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

29

<!-- page 30 -->

8

8.2.2

OPERATION

Normally open with adjustable hysteresis
Applications
••

Dry run protection

••

Empty signal

Configuration
1.

Configure the Qx switching output as normally open.
••

2.

Set the parameter in the QxMENU-OUx menu to Qx_Hno.

Set the switching point.
••

3.

Set the value in the QxMENU-SPx menu to the level in mm (e.g. 500 mm).

Set the reset point.
••

4.

Set the value in the QxMENU-RPx menu to the level in mm (e.g. 450 mm).

Select the electrical property (NPN/PNP/DRV (push/pull)).
Select the parameter in the QxMENU-TYPx menu.
The following rules apply:
••

Qx-PNP = Switching output in PNP circuit

••

Qx-NPN = Switching output in NPN circuit

••

Qx-Drv = Switching output in push/pull function

Switching output behavior
Level

SP

RP

t

Error signal
Active
Inactive

Switching output
Normally open/HNO

30

1)

Pulldown only.

2)

Pullup only.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

PNP

NPN

DRV

active

Uv

0V

Uv (PNP switched)

Error status

inactive

0 V 1) Uv 2)

0 V (NPN switched)

inactive

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 31 -->

OPERATION

8.2.3

8

N/C output with configurable hysteresis
Applications
••

Overfill protection

••

Full signal

Configuration
1.

Configure the Qx switching output as normally closed.
••

2.

Set the parameter in the QxMENU-OUx menu to Qx_Hnc.

Set the switching point.
••

3.

Set the value in the QxMENU-SPx menu to the level in mm (e.g. 500 mm).

Set the reset point.
••

4.

Set the value in the QxMENU-RPx menu to the level in mm (e.g. 450 mm).

Select the electrical property (NPN/PNP/DRV (push/pull))
Select the parameter in the QxMENU-TYPx menu.
The following rules apply:
••

Qx-PNP = Switching output in PNP circuit

••

Qx-NPN = Switching output in NPN circuit

••

Qx-Drv = Switching output in push/pull function

Switching output behavior
Level

SP

RP

t

Error signal
Active

Inactive

Switching output
Normally closed/
HNC

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

1)

Pulldown only.

2)

Pullup only.

PNP

NPN

DRV

Error status

active

Uv

inactive

0 V1)

0V

Uv (PNP switched)

inactive

Uv2)

0 V (NPN switched)

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

31

<!-- page 32 -->

8

8.2.4

OPERATION

N/O output with window function
Application
The critical filling level for the application is within the FHx
and FLx window thresholds.
Configuration
1.

Configure the Qx switching output as normally open.
••

2.

Set the parameter in the QxMENU-OUx menu to Qx_Fno.

Set the switching point.
••

3.

Set the value in the QxMENU-FHx menu to the level in mm (e.g. 500 mm).

Set the reset point.
••

4.

Set the value in the QxMENU-FLx menu to the level in mm (e.g. 400 mm).

Select the electrical property (NPN/PNP/DRV (push/pull)).
Select the parameter in the QxMENU-TYPx menu.
The following rules apply:
••

Qx-PNP = Switching output in PNP circuit

••

Qx-NPN = Switching output in NPN circuit

••

Qx-Drv = Switching output in push/pull function

Switching output behavior
Level

FH

FL

t

Error signal
Active

Inactive

Switching output
Normally open/FNO

32

1)

Pulldown only.

2)

Pullup only.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

PNP

NPN

DRV

Error status

active

Uv

0V

Uv (PNP switched)

inactive

0 V 1) Uv 2)

0 V (NPN switched)

inactive

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 33 -->

OPERATION

8.2.5

8

N/C output with window function
Application
The critical filling level for the application is outside the FHx and
FLx window thresholds.
Configuration
1.

Configure the Qx switching output as normally closed.
••

2.

Set the parameter in the QxMENU-OUx menu to Qx_Fnc.

Set the switching point.
••

3.

Set the value in the QxMENU-FHx menu to the level in mm (e.g. 500 mm).

Set the reset point.
••

4.

Set the value in the QxMENU-FLx menu to the level in mm (e.g. 400 mm).

Select the electrical property (NPN/PNP/DRV (push/pull)).
Select the parameter in the QxMENU-TYPx menu.
The following rules apply:
••

Qx-PNP = Switching output in PNP circuit

••

Qx-NPN = Switching output in NPN circuit

••

Qx-Drv = Switching output in push/pull function

Switching output behavior
Level

FH

FL

t

Error signal
Active

Inactive

Switching output
Normally closed/FNC

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

1)

Pulldown only.

2)

Pullup only.

PNP

NPN

DRV

active

Uv

0V

Uv (PNP switched)

inactive

0V

Uv

0 V (NPN switched)

1)

2)

Error status
inactive

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

33

<!-- page 34 -->

8

8.2.6

OPERATION

N/O output with error signal
Application
If there is an error message at the LFP, this can be transferred using a switching contact.
Configuration
1.

Configure the Qx switching output as normally open.
••

2.

8.2.7

Set the parameter in the QxMENU-OUx menu to Qx_Eno.

Select the electrical property (NPN/PNP/DRV (push/pull)).
Select the parameter in the QxMENU-TYPx menu.
The following rules apply:
••

Qx-PNP = Switching output in PNP circuit

••

Qx-NPN = Switching output in NPN circuit

••

Qx-Drv = Switching output in push/pull function

N/C output with error signal
Application
If there is an error message at the LFP, this can be transferred using a switching contact.

Configuration
1.

Configure the Qx switching output as normally closed.
••

2.

34

Set the parameter in the QxMENU-OUx menu to Qx_Enc.

Select the electrical property (NPN/PNP/DRV (push/pull)).
Select the parameter in the QxMENU-TYPx menu.
The following rules apply:
••

Qx-PNP = Switching output in PNP circuit

••

Qx-NPN = Switching output in NPN circuit

••

Qx-Drv = Switching output in push/pull function

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 35 -->

OPERATION

8.3

Configure the analog output

8.3.1

Automated signal detection
The LFP can automatically detect which signal is required based on the connected
output load.

8

The following rules apply:
••

4 mA ... 20 mA < 500 ohms at Uv > 15 V

••

4 mA ... 20 mA < 350 ohms at Uv > 12 V

••

0 V ... +10 V > 750 ohms at Uv ≥ 14 V

Configuration
1.

Access the QAMENU-TYP menu using the arrow and Set pushbuttons.

2.

Set the QAMENU-TYP menu to Auto?.

Note:
Automated signal detection is only active when the device is switched on for the first time.
After this the function can be activated again in the QAMENU-TYP menu with Auto?.

8.3.2

Current output 4 mA ... 20 mA
Configuration
1.

Set the upper limit value (20 mA).
••

2.

Set the lower limit value (4 mA).
••

3.

8.3.3

Set the value in the QAMENU-QAHIGH menu to the level in mm
(e.g. 500 mm).
Set the value in the QAMENU-QALOW menu to the level in mm
(e.g. 10 mm).

Invert the signal.
The analog signal can be inverted in the QAPOL menu.
Set the parameter in the QxMENU-QAPOL menu to QA-INV.
••

QA-NRM = Analog output signal as configured

••

QA-INV = Analog output signal is inverted; QAHIGH 4 mA and
QALOW 20 mA

4.

Select the electrical signal.

5.

Set the parameter in the QxMENU-QATYP menu to 4 mA ... 20 mA.

Voltage output 0 V ... +10 V
Configuration
1.

Set the upper limit value (10 V).
••

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

Set the value in the QAMENU-QAHIGH menu to the level in mm
(e.g. 500 mm).

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

35

<!-- page 36 -->

8

OPERATION

2.

Set the lower limit value (0 V).
••

3.

4.

Set the value in the QAMENU-QALOW menu to the level in mm
(e.g. 10 mm).

Invert the signal.
The analog signal can be inverted in the QAPOL menu.
Set the parameter in the QxMENU-QAPOL menu to QA-INV.
••

QA-NRM = Analog output signal as configured

••

QA-Inv = Analog output signal is inverted: QAHIGH 0 V and QALOW 10 V

Select the electrical signal.
Set the parameter in the QxMENU-QATYP menu to 0 V ... +10 V.

8.4

Advanced functions

8.4.1

Expert mode
Expert mode must first be set in order to activate special functions.
Logging into expert mode
1.

Access the PASSW menu using the arrow pushbuttons.

2.

Enter the password 000537 (LFP on the mobile keypad: L=5 / F=3 / P=7).

Expert mode may be locked again if the password is entered incorrectly or if the voltage
supply is disconnected.
8.4.2

Filtering measured values
Activating filtering
Smoothing of the measured value; e.g. in the case of ripples on level surfaces. For fast
level changes, the average of the measured values over X seconds is indicated.
bb

Parameters in the Set filters menu.
The possible values are Off, 400 ms, 600 ms, 1000 ms, 1400 ms, 2 s, 5 s, 10 s.

Maximum change of level (plausibility check)
For applications which cause level jumps as a result of significant interference on the
LFP. Entry for the maximum level dynamic in the application and/or the maximum permissible change rate of the level.
1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

Reduce the parameter in the EXPRT-CONFIG-MaxCol menu.
AnySpd (50 cm/s) (default), 10 cm/s, 5 cm/s, 2 cm/s

Note:
•• For MeasMd = HiSpd, any max. change rate is possible
•• For MeasMd = HiAcc, max. is 10 cm/s

36

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 37 -->

OPERATION

8.4.3

8

Automated adjustment of the interference signal limit
The adjustment of the interference signal limit (TrsHld) can be carried out automatically
in many applications.
Configuration
1.

Set a fill level of 30%.

2.

Log in to expert mode; see “8.4.1 Expert mode”.

3.

Perform in the EXPRT-Pulse-AutoTn menu.

The sensor calculates a suitable value for TrsHld.
Note:
This setting can be used only in pulse mode.

8.4.4

Blanking the interference signals in the masked zone
To blank interference signals from the range above the maximum expected fill level,
a zone can be masked (dead zone). This zone begins at the process connection
and continues up to the configured point. If signal values above the defined limit
value (TrsHld) occur within this range, the sensor enters a safe state and signals the
error !MaskZ.
MaskTr

A
DZ

1

2
MR

DZ

20%

DZ
x



100%

x



200%

x



3
DZ



MR
x



MR
x

x





x

x



x



  

MR

E

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

1

No reflection/very weak reflection

2

Weak reflection (e.g. spray water)

3

Strong reflection (e.g. thick layer of ketchup)

DZ

Dead zone

MR

Active measuring range

x

No detection/measurement



Detection/measurement

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

37

<!-- page 38 -->

8

OPERATION

Configuration
1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

Define the parameter in the EXPRT-Pulse-MaskZn menu.

Note:
This setting can be used only in pulse mode.

8.4.5

Selection of evaluation method
You can switch between pulse mode and foam mode as an evaluation method.
Depending on the selected mode, other evaluation algorithms are used.
Configuration
1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

In the EXPRT-Config-Mode menu, select between Pulse and Foam.

The following rules apply:
••

Mode = Pulse: The sensor measures either with or without AutCal.

••

Mode = Foam: The sensor measures only with valid CalEmp+CalMed. If no valid
calibration is available, the CalPls message is displayed and the sensor enters
a safe state.

Note:
If AutCal is called up while the sensor is in foam mode, then AutCal is denied and
the error message !Denid is shown.
8.4.6

Testing the configuration
Testing outputs
Switching/analog outputs can be simulated. This makes it possible to check the wiring
and signal values on the connected systems, such as the PLC control, relay and lamps.
Configuration
Activate the Qx switching output
bb

Set the parameter in the QxMENU-SimQx menu to QxOn.

Additional options:
••

QxOff = switching output off

••

QxNorm = switching output in measuring operation

••

QxOn = switching output is active

Note:
The simulation is automatically deactivated if the supply voltage is interrupted.

38

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 39 -->

OPERATION

8

Activate the QA analog output
bb

Set the parameter in the QAMENU-SimCur or SimVol menu to the desired signal
value.
••

SimCur for current output

••

SimVol for voltage output

Note:
The simulation is automatically deactivated if the supply voltage is interrupted.

Simulating the level
Even if there is no liquid in the container yet, it is possible to select a filling level in the
menu in order to test the sensor configuration. When simulating a level value, all outputs on the LFP are set according to the defined configuration. The function should not
be selected until a configuration is complete.
Configuration
bb

Set the parameter to the desired filling level as a % in the SimLev menu.

Note:
•• The level simulation refers to the probe length and/or container level
(probe length + offset) if an offset is configured.
•• The simulation is only active when there are no error messages.
The simulation is automatically deactivated if the supply voltage is interrupted.

Parameter selection

8.4.7

••

SimOff: Off

••

Filling level 0%

••

Filling level 25%

••

Filling level 50%

••

Filling level 75%

••

Filling level 100%

Configuring the probe length
1. Log in to expert mode; see “8.4.1 Expert mode”.
2.

Access the EXPRT-Config-Length menu using the arrow and Set pushbuttons.

3.

Enter the probe length in the Length menu. Please note the defined probe length in
Chapter “15 Dimensional drawings”.

Note:
•• HiSpd: max. length = 2005 mm, response time < 400 ms
•• HiAcc: max. length = 6,005 mm, response time < 2,800 ms

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

39

<!-- page 40 -->

8

8.4.8

OPERATION

Teaching in static interference signals
Static interference signals in the tank generated by tubes, beams, couplings,
or a cleaning ball can be taught-in. The probe length provides the value for the
teach-in depth.
1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

Access the EXPRT-Pulse-CalRng menu using the arrow and Set pushbuttons.

3.

Set the value range between 95 and 6005 mm.

Note:
•• The value starts from the LFP process connection.
•• The value should cover all interference signals.
•• Maximum value = probe length – 100 mm.
•• The AutCal must then be carried out, see “7 Commissioning”.
•• The CalRng parameter should always correspond to the probe length for LFPs with
remote amplifier.

8.4.9

Evaluating signal quality
Parameters describe the quality of the measuring signal.
bb

Log in to expert mode, see “8.4.1 Expert mode”.

SigQa1
Characteristic for the robustness of the EXPRT-Pulse-TrsHld setting.
Not active in foam mode. The displayed value is only valid if the sensor displays the
correct level value.

bb

••

Value range: 0% ... 100%

••

Good signal: > 40% (a high pulse reserve is provided with the current
TrsHld setting.)

Measures: Reduce EXPRT-Pulse-TrsHld to increase SigQa1.

Note:
•• Changing TrsHld will have an impact on SigQa2 and SigQa3.
•• If a satisfactory SigQa1 value cannot be achieved by adjusting TrsHld in conjunction
with the SigQa values, the installation condition must be checked. Using a coaxial
tube improves signal detection, particularly in media with low DK values (e.g. oil).

40

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 41 -->

OPERATION

8

SigQa2
Characteristic for the robustness of echo pulse detection in relation to interference
pulses.
Not active in foam mode. The displayed value is only valid if the sensor displays the
correct level value.

bb

••

Value range: 0% ... 100%

••

Good signal: > 50%

Measures: Run AutCal; check installation conditions; remove deposits from probe
and process connection.

SigQa3
Characteristic for signal noise and electromagnetic interference.
••

Value range: 0% ... 100%

••

Good signal: > 75%

••

Poor signal: < 50%

Not active in foam mode. The displayed value is only valid if the sensor displays the
correct level value.
••
bb

8.4.10

Value range: 0% ... 100%

Measures:
••

Increase EXPRT-Config-TrsHld

••

EXPRT-Config-MeasMd = HiAcc

••

Improve filtering

••

Switch on filter

••

Reduce EXPRT-Config-MaxCol

Changing the coaxial cable length
••

Valid for versions with remote amplifier.

••

This setting makes it possible to configure the coaxial cable length between the
sensor head and process connection.

Configuration
Predefined coaxial cable length (1,000 mm, 2,000 mm, or 3,300 mm)

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

Configure the coaxial cable length in the EXPRT-Config-CblLen menu
(1,000 mm ... 3,300 mm).

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

41

<!-- page 42 -->

8

OPERATION

Note:
Only the following configurations are permitted:

Max. probe length [mm]
Coaxial cable length [mm]

8.4.11

Foam mode inactive

Foam mode active

1,000

4,000

2,000

2,000

3,000

1,500

3,300

1,000

500

Activating the display lock
To prevent the sensor from being tampered with, password protection can be activated
for the display.
When the protection is active, the expert password (000537) must be entered before
the menu can be accessed.
The menu is only unlocked once the correct password is entered.
Configuration
1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

The protection can be (de)activated via the EXPRT-Config-Lock menu.

Note:
•• The user is logged out again after 5 minutes of inactivity.
•• When the display is locked, only the configured measured value display (DspVal) can
be seen.
8.4.12

Selecting the display unit (millimeter/inch)
This setting makes it possible to display and configure all length measurements in
either millimeters or inches.
Configuration

42

1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

Set the unit in the EXPRT-Config-Unit menu (mm/inch).

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 43 -->

OPERATION

8.4.13

8

Setting the offset
This setting makes it possible to indicate the level value on the display in relation to
the tank bottom instead of the end of the probe. The actual container level is then
indicated on the display.
Configuration
Log in to expert mode; see “8.4.1 Expert mode”.

2.

Set the offset in the EXPRT-Config-Offset menu (0 mm … +3,000 mm).

M

L

IA

1.



O

IAE



Fig. 8:

LFP Cubic

1 Level
2 QALOW/ QAHIGH
SPx/RPx
FHx/FI x
Can be set only in this zone
O: Offset
L: Probe length
M: Measurement length
IA: Inactive area at process connection
IAE: Inactive area at probe end

Note:
If the offset parameter is changed, the SPx/RPx/FLx/FHx/QALOW/QAHIGH parameters
are automatically adjusted.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

43

<!-- page 44 -->

8

OPERATION

8.4.14

Resetting the calibration
Resetting AutCal
1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

Reset AutCal in the EXPRT-Pulse-Reset menu.

Resetting CalEmp+CalMed

44

1.

Log in to expert mode; see “8.4.1 Expert mode”.

2.

Reset CalEmp+CalMed in the EXPRT-Foam-Reset menu.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 45 -->

MENU OVERVIEW

9

9

Menu overview
RUN

1000 mm

3s

Q1MENU

SP1

Value

RP1

Value

OU1

Para

SimQ1

Para

SP2/3/4

Value

RP2/3/4

Value

FH2/3/4

Value

FL2/3/4

Value

OU2/3/4

Para

TYP2/3/4

Para

SimQ2/3/4

Para

QAHIGH

Value

QALOW

Value

QAPOL

Para

QATYP

Para

QAFAIL

Para

1)

Q2/3/4MENU

QAMENU

2)

SimCur

Para

2)

Para

SimVol

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

DspVal

Para

Filter

Para

SimLev

Para

RstFac

OK?

EXPRT

Conf ig

CALL..
3)

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

Lock

Para

45

<!-- page 46 -->

2)

9

SimCur

MENU OVERVIEW

Para

2)

Para

SimVol

DspVal

Para

Filter

Para

SimLev

Para

RstFac

OK?

EXPRT

Conf ig

CALL..
3)

Pulse

Foam

Probe

46

Lock

Para

Unit

Para

Offset

Value

Mode

Para

MeasMd

Para

MaxCol

Value

AutCal

OK?

TrsHld

Value

AutoTu

OK?

CalRng

Value

MaskZn

Value

MaskTr

Value

Reset

OK?

Cal.OK

CalEmp

OK?

Cal.OK

CalMed

OK?

Cal.OK

Limit

Value

Reset

OK?

Length

Value

CblLen

Value

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

Type

Cal.OK

Cal.OK

Cal.OK

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

Para

<!-- page 47 -->

MaskZn

MaskTr

Foam

Probe

Info

SigQua

PASSW

Value

MENU
Value OVERVIEW

Reset

OK?

Cal.OK

CalEmp

OK?

Cal.OK

CalMed

OK?

Cal.OK

Limit

Value

Reset

OK?

Length

Value

CblLen

Value

Type

Para

FrmVer

Value

SerNo

Value

CalSta

Value

AppTag

Value

DevTag

Value

SigQa1

Value

SigQa2

Value

SigQa3

Value

9

Cal.OK

Value

1) Visible elements depend on the OUx parameter selection
2) Visible elements depend on the QATYP parameter selection.
3) Password-protected measuring range.
Q3 and Q4 are only available for an LFP with four switching outputs.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

47

<!-- page 48 -->

10 OVERVIEW OF PARAMETERS

10

Overview of parameters
Parameter

Q1MENU, Q2MENU,
Q3MENU, Q4MENU
SPx

RPx

FHx
FLx

OUx

SimQx
TYP2/3/4

QAMENU
QAHIGH
QALOW
QAPOL

48

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

Description

See “8.2 Configuring the switching outputs”.
Switching point, switching output 1 or 2 or 3 or 4
(SPx > RPx).
Note: Not displayed if the switching output in the
OUx menu is set to Error or Window.
Reset switching point, switching output 1 or 2 or 3 or 4.
Note: Not displayed if the switching output in the
OU2/3/4 menu is set to error or window.
•• Upper threshold (high) window function, switching
output 2/3/4 (FHx > FLx)
•• Lower threshold (low) window function, switching
output 2/3/4
Note: Not displayed if the switching output in the
OU2/3/4 menu is set to error or hysteresis.
Switching output switching function.
•• Qx-Hno = Hysteresis function, normally open
•• Qx-Hnc = Hysteresis function, normally closed
•• Qx-Fno = Window function, normally open (function only
available for Q2/3/4)
•• Qx-Fnc = Window function, normally closed (function
only available for Q2/3/4)
•• Qx-Eno = Error signal, normally open (function only
available for Q2/3/4)
•• Qx-Enc = Error signal, normally closed (function only
available for Q2/3/4)
If Qx is used as an error signal, SPx/FHx and RPx/FLx are
hidden in the menu.
See “8.4.6 Testing the configuration”.
•• Qx-PNP = Switching output in PNP circuit
•• Qx-NPN = Switching output in NPN circuit
•• Qx-Drv = Switching output executed in push/pull function
See “8.3 Configure the analog output”.
Input of the filling level in mm for 20 mA/10 V signal
(QAHIGH > QALOW).
Input of the filling level in mm for 4 mA/0 V signal.
The analog output signal can be inverted.
•• QA-Nrm = Analog output signal as configured
•• QA-Inv = Analog output signal is inverted:
QAHigh 4 mA/0 V and QALow 20 mA/10 V

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 49 -->

OVERVIEW OF PARAMETERS 10

Parameter
QATYP

QAFAIL

SimCur
SimVol
DspVal

Filter
SimLev
RstFac
EXPRT
Lock
Unit
Offset
Mode
MaxCol
MeasMd

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

Description

Setting for the output signal.
•• 4 mA ... 20 mA
•• 0 V ... +10 V
•• Auto V = Qa operated with voltage output of 0 V … +10 V
•• Auto A = Qa operated with current output of
4 mA … 20 mA
•• Auto? = Automated signal detection based on
the existing load resistance
During a menu query, either 4 mA ... 20 mA or
0 V ... +10 V is displayed.
Output behavior as per NE43 in the event of a fault (function only available when current output has been selected
under QATYP).
•• 3.5 mA = Analog current output is set to 3.5 mA in the
event of a fault.
•• 21.5 mA = Analog current output is set to 21.5 mA in
the event of a fault.
See “8.4.6 Testing the configuration”.
See “8.4.6 Testing the configuration”.
Setting the display.
•• Distan = The display shows the distance in mm in
relation to the end of the probe.
•• QaPerc = The display shows the fill level in % in relation
to the QA analog output with the corresponding QAHIGH
and QALOW thresholds.
•• QaBarG = The display shows a bar graph in relation to
the QA analog output with the corresponding QAHIGH
and QALOW thresholds.
•• QaSign = The display shows the current QA output value
in mA or V.
•• QxSign = The display shows the output states.
See “8.4.2 Filtering measured values”.
See “8.4.6 Testing the configuration”.
Resetting the set parameters to the factory settings.
See “8.4.1 Expert mode”.
See “8.4.11 Activating the display lock”.
See “8.4.12 Selecting the display unit (millimeter/inch)”.
See “8.4.13 Setting the offset”.
See “8.4.5 Selection of evaluation method”.
See “8.4.2 Filtering measured values”.
Measuring mode.
•• HiSpd: max. length = 2,005 mm,
response time < 400 ms
•• HiAcc: max. length = 6,005 mm,
response time < 2,800 ms,
(more stable measured values, recommended for
liquids with low DKs and where TrsHld is < 70)
•• mode-1: not supported; deactivates current AutCal/
foam calibration

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

49

<!-- page 50 -->

10 OVERVIEW OF PARAMETERS

Parameter
Pulse
AutCal
TrsHld

AutoTn
CalRng

Description

See “8.4.5 Selection of evaluation method”.
See “7 Commissioning”.
This value describes a factor which determines how strong
an echo has to be in order to be recognized by the device.
The value range lies between 20% and 500%. The default
is 100% in this case. Only shown if password entered.
•• 20% = high sensitivity
•• 100% = standard
•• 500% = low sensitivity
See “8.4.3 Automated adjustment of the interference
signal limit”.
Calibration range.
•• Value range: 95 mm … 6005 mm
Range starting from the process connection in which
static interference signals (coupling sections, welds, spray
balls, etc.) are hidden during the AutCal process. During
the AutCal process, there must not be any medium in the
defined area of +200 mm.

MaskZn
MaskTr
Reset
Foam
CalEmp
CalMed
Limit

Reset
Probe
Length
CblLen
Type
Info
FrmVer
SerNo
CalSta

AppTag

50

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

See “8.4.8 Teaching in static interference signals”.
See “8.4.4 Blanking the interference signals in the
masked zone”.
See “8.4.4 Blanking the interference signals in the
masked zone”.
Resets the value for AutCal.
See “7.3 Foam commissioning (with factory settings)”.
See “7.3 Foam commissioning (with factory settings)”.
See “7.3 Foam commissioning (with factory settings)”.
Limit between foam and fluid.
•• Range: 20 to 100%
•• Factory setting: 90%
•• Medium surface: 90%
•• Foam surface: < 90%
When measuring the foam surface, it may be necessary to
reduce the limit. If the sensor displays a limit value that is
too low, it is necessary to reduce the limit.
Resets the values for CalEmp and CalMed.
Special settings.
•• See “7.3 Foam commissioning (with factory settings)”
(LFP Cubic).
See “8.4.10 Changing the coaxial cable length”.
Choosing between rod and rope.
Sensor information.
Shows the firmware version.
Shows the serial number.
Displays the status of the tank calibration.
•• Pulse = AutCal (calibrated), NoCal (not calibrated)
•• Foam = FomCal (calibrated), CalMis (not calibrated)
Measuring point name, can only be described via IO-Link.

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 51 -->

OVERVIEW OF PARAMETERS 10

Parameter
DevTag
SigQua

SigQa1
SigQa2
SigQa3
PASSW

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

Description

Device name, can only be written over IO-Link.
Parameter describes the quality of the measurement
signal.
See “8.4.9 Evaluating signal quality”.
See “8.4.9 Evaluating signal quality”.
See “8.4.9 Evaluating signal quality”.
See “8.4.1 Expert mode”.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

51

<!-- page 52 -->

11 TROUBLESHOOTING

11

Troubleshooting

11.1

Error message on the display

Error

Cause

Possible solution

!InvEc &
level present

AutCal not executed; interference superimposes
medium reflection.

Perform commissioning
(See “7.1 Quick commissioning (with factory
settings)”).

TrsHld setting is not suitable for the medium.

Perform advanced commissioning
(See “7.2 Advanced commissioning”).

Probe length configured incorrectly.

Check probe length and compare against
configuration in EXPRT-Config-LENGTH.

Probe not available.

Check the probe.

A parameter was written outside of the valid value
range and therefore adjusted

Rewrite the value in the valid range.

Another parameter was automatically adjusted
due to a dependency (SPx, RPx).

Check the parameter again.

!WRONG

Incorrect password entered.

Enter the correct password.

!NoCal

Information: The AutCal process and/or foam
Perform commissioning again if necessary.
calibration was rejected because the probe length,
teach-in depth or measuring mode was changed.

!Denid

AutCal was called up in Foam sensor mode.

AutCal is available only in Pulse mode. Perform
foam calibration in Foam mode.

CalPIs

No valid calibrations for CalEmp and CalMed.

Perform foam calibration.

!CalOk

The teach-in process was successful.

!NoSig

AutCal failed.

Repeat commissioning.

!faild

Foam-CalEmp or FoamCalMed menu item failed.

Follow the foam commissioning instructions.

!SC-Q1
!SC-Q2
!SC-Q3
!SC-Q4
!SC-Qa

Short-circuit at the output.

Remove short-circuit.

Load resistance at the output is too low.

Increase the load resistance.

!IOLOf

Supply voltage too low for IO-Link communication.

Increase the supply voltage to achieve the desired
functionality.

!QaOff

Supply voltage too low for analog output.

Increase the supply voltage to achieve the desired
functionality.

!QxOff

Supply voltage too low for switching outputs.

Increase the supply voltage to achieve the desired
functionality.

!QaOvf

The ohmic load at the analog current output Qa is
too high.

Reduce the load at Qa.

!InvEc &
empty tank
!ATTNT

The analog current output Qa is not wired.

Connect the load to Qa.

!MaskZ

Interference/pulse exceeds value for MaskTr.

Increase MaskTr or identify and eliminate
interference.

!Range

The maximum allowable measuring range was
exceeded. Measurement in this configuration is
not possible.

Reduce the probe length and/or coaxial cable
length; see “8.4.10 Changing the coaxial cable
length”.

!Cable

The display only
shows RUN. It is
otherwise empty.

52

The coaxial cable is damaged/defective.

Replace the coaxial cable.

The coaxial cable length was configured incorrectly.

See “8.4.10 Changing the coaxial cable length”.

The DspVal menu parameter is at QaBarG and the
level is below QALOW.

Change QALOW or DspVal.

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 53 -->

TROUBLESHOOTING 11

Error

Cause

Possible solution

Display off

Temperature is too high.

Reduce the temperature.

Temperature is too low.

Increase the temperature.

No supply voltage.

Connect the sensor correctly.

!Err[xx]
!ErM[xx]
!ErI[xx]
!ErO[xx]

System error.

The device is defective and must be replaced.

NVFail

Memory error.

The device is defective and must be replaced.

11.2

Operating the display

Error

Cause

Possible solution

The menu item SPx/ QxMENU/OUx is not
RPx is not displayed. configured to Qx-Hno and/or Qx-Hnc.

Configure Qx (see “8.2 Configuring the switching
outputs”).

The menu item FHx/ QxMENU/OUx is not
FLx is not displayed. configured to Qx-Fno and/or Qx-Fnc.

Configure Qx (see “8.2 Configuring the switching
outputs”).

QAFAIL Is not
displayed.

The analog output Qa is in voltage mode
(QATYP = 0 to 10 V).

Configure Qa (see “8.3 Configure the analog
output”).

SimVol is not
displayed.

The analog output Qa is in current mode
(QATYP = 4 to 20 mA).

Configure Qa (see “8.3 Configure the analog
output”).

SimCur is not
displayed.

The analog output Qa is in voltage mode
(QATYP = 0 to 10 V).

Configure Qa (see “8.3 Configure the analog
output”).

EXPRT-Config-… is
not displayed.

Correct password not entered.

See “8.4.1 Expert mode”.

EXPRT-Foam-… is
not displayed.

Correct password not entered.

See “8.4.1 Expert mode”.

Lengths are
expressed as
decimal numbers.

Inch is activated as the display unit.

Configure the unit (see“8.4.12 Selecting the
display unit (millimeter/inch)”).

The menu only
shows PASSW.

The display lock is activated.

See “8.4.11 Activating the display lock”.

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

53

<!-- page 54 -->

11 TROUBLESHOOTING

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

11.3 Outputs

| Error | Cause | Possible solution |
|---|---|---|
| Switching output does not behave as expected | Configuration incorrect. | Perform configuration of the switching output (see “8.2 Configuring the switching outputs”). |
| Switching output does not behave as expected | An error is pending; the sensor outputs are in a safe state. | Remove the cause of the error. |
| Switching output does not behave as expected | Cable break. | Check the cable. |
| Analog output does not behave as expected | Configuration incorrect. | Configure the analog output (see “8.3 Configure the analog output”). |
| Analog output does not behave as expected | An error is pending; the sensor outputs are in a safe state. | Remove the cause of the error. |
| Analog output does not behave as expected | Cable break. | Check the cable. |

<!-- table fixed by hand, checked on the PDF: do not regenerate with --force -->

11.4 Error behavior

| Error | Cause | Possible solution |
|---|---|---|
| After installation, the sensor indicates a high level although the tank is empty. | AutCal not performed. | Perform commissioning (see “7 Commissioning”). |
| When used with a coaxial tube, the sensor indicates a high level although the tank is empty. | AutCal not performed. | Perform commissioning (see “7 Commissioning”). |
| Level value fluctuates on the display. | Medium surface unsettled. | Activate filtering (see “7.1 Quick commissioning (with factory settings)”). |
| The displayed level value/SPx/RPx/FHx/FLx/QALOW/QAHIGH is greater than the probe length. | An offset was configured for the level value. | Adjust the offset (see “8.4.13 Setting the offset”). |
| The displayed level value/SPx/RPx/FHx/FLx/QALOW/QAHIGH is greater than the probe length. | Incorrect probe length configured. | Adjust the probe length (see “8.4.7 Configuring the probe length”). |
| Level occasionally jumps to a higher value. | Contamination in the vicinity of the process connection. | Cleaning. |
| Level occasionally jumps to a higher value. | Spray ball or supply system wets the probe with medium above the medium surface. | Observe the installation conditions. Configure the MaxCoL plausibility filter (see “8.4.2 Filtering measured values”). |
| Level occasionally jumps to a higher value. | Change in the ambient conditions regarding the situation during the AutCal process. | Perform commissioning again (see “7 Commissioning”). |
| Level occasionally jumps to a higher value. | Significant buildup of foam. | Perform foam commissioning (see “7.3 Foam commissioning (with factory settings)”). |
| Level occasionally jumps to a higher value. | TrsHld set too low, the echo algorithm detects interference reflections. | Increase TrsHld. |
| Level occasionally jumps to 0 mm. | TrsHld set too high. | Perform advanced commissioning (see “7 Commissioning”). |
| Level occasionally jumps to 0 mm. | Significant buildup of foam. | Perform foam commissioning. |
| No measurement of low levels for media with low DKs. | Increased inactive range at the probe end for media with a low DK. |  |
| Increased measurement inaccuracy. | Use of foam algorithm. |  |

54

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 55 -->

REPAIR WORK 12

12

Repair work

12.1

Maintenance
The LFP is maintenance-free. We recommend doing the following regularly:

12.2

bb

Checking the probe for contamination.

bb

Checking the screw connections and plug connections

Returns
Rinse off and/or clean removed devices before returning them in order to protect
our employees and the environment from dangers posed by residue from measured
materials. Faulty devices can only be examined when accompanied by a completed
return form. A declaration of this type includes information about all materials which
have come into contact with the device, including those which were used for testing purposes, operation, or cleaning. The return form is available on our website
(www.sick.com).

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

55

<!-- page 56 -->

13 DISPOSAL

13

Disposal
Dispose of device components and packaging materials in compliance with applicable
country-specific waste treatment and disposal regulations of the region of use.

56

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 57 -->

TECHNICAL DATA 14

14

Technical data

14.1

Features
Medium

Liquids

Detection type

Limit, continuous

Probe length
Mono-rod probe 200 mm … 2,000 mm
Cable probe 1,000 mm, 2,000 mm, 3,000 mm, 4,000 mm

14.2

Adjustable measuring range

95 mm … 6,005 mm

Process pressure

–1 bar … +10 bar

Process temperature

–20 °C … +100 °C

GOST certificate



RoHS certificate



IO-Link



UL certificate



Performance
Accuracy1)
Reproducibility1)
Resolution
Response time2)
Dielectric constant
Conductivity
Maximum level change3)
Inactive area at end of probe1)

± 5 mm
≤ 2 mm
< 2 mm
< 400 ms
≥ 5 for mono-rod probe/rope probe
≥ 1.8 with coaxial tube
No limitation
500 mm/s
10 mm

With water under reference conditions, see “14.7 Measurement accuracy”.
Depends on measuring mode (high-speed < 400 ms, high accuracy < 2,800 ms)
3)
Depends on configuration (MaxCol - maximum change of level)
1)
2)

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

57

<!-- page 58 -->

14 TECHNICAL DATA

14.3

14.4

Mechanics/materials
Materials in contact with media:

1.4404, PTFE

Process connection

G 3/4 A,
3/4'' NPT

Housing material

Plastic PBT

Max. probe load

≤ 6 Nm

Enclosure rating

IP67: EN 60529

Weight

Max. 1.3 kg

Coaxial cable insulation

PVC

Reference conditions
Container with diameter

14.5

1m

Minimum distance to built-in components

> 300 mm

Distance from end of probe to tank bottom

> 15 mm

Air humidity

65% ± 20%

Temperature

+20 °C ± 5 °C

Pressure

1,013 mbar abs. ± 20 mbar

Medium

Water, DK = 80

Centered installation of sensor



Container parameterization carried out



Ambient conditions
Ambient temperature, operation1)

–20 °C … +60 °C

Ambient temperature, warehouse

–40 °C ... +80 °C

According to UL listing: degree of contamination 3 (UL61010-1: 2012-05); air humidity: 80%
at temperatures up to 31 °C; installation height: max. 3,000 m above sea level; only for indoor
applications

1)

58

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 59 -->

TECHNICAL DATA 14

14.6

Electrical connection values
Supply voltage.

12 V DC ... 30 V DC

Current consumption

≤ 100 mA at 24 V without output load

Initialization time

≤5s

Protection class

III

Connection type

M12 x 1, 5-pin
M12 x 1, 8-pin

hysteresis

Min. 3 mm, freely configurable

Output signal

4 mA ... 20 mA / 0 V ... +10 V automatically
switchable depending on output load1)
1 PNP transistor output (Q1) and 1 PNP/NPN
transistor output (Q2) switchable, or 1 PNP
transistor output (Q1) and 3 PNP/ NPN transistor
outputs (Q2 to Q4) switchable (type-dependent)1)

Signal voltage HIGH

Uv –2 V

Signal voltage LOW

≤2V

Output current

< 100 mA

Inductive load

<1H

Capacitive load

100 nF

Temperature drift

< 0.1 mm/K

Output load

4 mA ... 20 mA < 500 ohms at Uv > 15 V
4 mA ... 20 mA < 350 ohms at Uv > 2 V
0 V ... +10 V > 750 ohms at Uv ≥ 14 V

Lower signal level

3.8 mA ... 4 mA

Upper signal level

20 mA ... 20.5 mA

EMC

EN 61326-2-3, 2014/30/EU

1)

1)
2)

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

All connections are reverse polarity protected. All outputs are overload and short-circuit protected.
Use an energy-limited circuit for the voltage supply as per UL61010-1 3rd Ed., Section 9.3

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

59

<!-- page 60 -->

14 TECHNICAL DATA

14.7

Measurement accuracy

14.7.1

Measurement accuracy with parameterized container
L

0

25



5
0
-5

-25



L

L-25

L-180

10

L

0

0

25



5
0
-5

-25



L

L-25

L-180

100

0

1 Accuracy in mm
2 Level in mm

60

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 61 -->

TECHNICAL DATA 14

14.7.2

Measurement accuracy without parameterized container
L

0

50


20



5
0
-5

-20

-50



L

L-40

L-180

10 0

L

0

50





5
0
-5

-50



L

L-40

L-180

100

0

1 Accuracy in mm
2 Level in mm
3 Inactive area

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

61

<!-- page 62 -->

15 DIMENSIONAL DRAWINGS

15

Dimensional drawings

15.7.1

LFP Cubic with rod probe

32
(1.26)

43
(1.69)

IA

22

15
IA

G 3/4 A
3/4" NPT
G 3/4 A
3/4" NPT

M

M

L

L

5
(0.20)

M12x1
(0.87)

36 (1.42)
22
(0.87)

33
(1.30)

126
(4.96)

71
(2.80)

104
(4.09)

50
(1.97)

Mono-probe		

20 (0.79)

IAE

IAE

7 (0.28)

with coaxial tube

M Measuring range
L Probe length
IA Inactive area at process connection 25 mm
IAE Inactive area at probe end 10 mm

62

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 63 -->

DIMENSIONAL DRAWINGS 15

15.7.2

LFP Cubic with cable probe

36 (1.42)

43
(1.69)

33
(1.30)

71
(2.80)

104
(4.09)

50
(1.97)

IA

22
(0.87)

M12x1

5
(0.20)

G 3/4 A
3/4" NPT

12
(0.47)

100
(3.93)

M

L

3 (0.11) 3

IAE

M6

24

M Measuring range
L Probe length
IA Inactive area at process connection 25 mm
IAE Inactive area at probe end 10 mm

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

63

<!-- page 64 -->

15 DIMENSIONAL DRAWINGS

LFP Cubic with remote amplifier
120
(4.72)

n.

R5

0

45
(1.77)

mi

IA

14
(0.55)

5
(0.20)

36 (1.42)

M

L

6,5 (0.26)

22
(0.87)

G 3/4 A
3/4" NPT

121
(4.76)

83
(3.27)

36
(1.42)

7 (0.28)

40
(1.57)
IAE

70 (2.76)

40
(1.57)

73

50

M12x1

5 (0.20)

43 (1.69)

C

33
(1.30)

C Length of cable
M Measuring range
L Probe length
IA Inactive area at process connection 20 mm/40 mm
IAE Inactive area at probe end 10 mm

64

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 65 -->

FACTORY SETTING 16

16

Factory setting

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

Parameter
SP1

Factory setting
80% of the probe length measured from the end of the probe

RP1

5 mm below SP1

OU1

Q1_Hno

SP2

For 5-pin versions: 20% of the probe length measured from the end of the probe
For 8-pin versions: 60% of the probe length measured from the end of the probe

RP2

5 mm below SP2

OU2

Q2_Hno

TYP2

Q2_PNP

SP3

40% of probe length measured from end of probe

RP3

5 mm below SP3

OU3

Q3_Hno

SP4

20% of the probe length measured from the end of the probe

RP4

5 mm below SP4

OU4

Q4_Hno

TYP3

Q3_PNP

TYP4

Q4_PNP

QAHigh

50 mm below start of probe

QALOW

10 mm above end of probe

QAPOL

QA_Nrm

QATYP

Auto

QAFAIL

3.5 mA

SimCur

SimOff

SimVol

SimOff

DspVal

Distan

Filter

Off

SimLev

SimOff

TrsHld

100

MaskZn

0 mm

MaskTr

50%

Mode

Pulse

CalSta

noCal

Probe/Type

Depending on probe type: Rod/Rope

MaxCol

Depending on measuring mode: HiSped = AnySped, HiAcc = 10 cm/s

MeasMd

HiSpd

CalRng

6,005 mm

FomSta

Inactive

Limit

90

Offset

0 mm

Unit

mm

Lock

Inactive

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

65

<!-- page 66 -->

17 ACCESSORIES

17

Accessories
bb

66

Accessories can be found online at www.sick.com

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 67 -->

MEDIA LIST 18

18

Media list

This list of media provides a guide to the DK values of liquids. Water-based liquids always have a DK value > 5,
which makes it easy to use the LFP. For DK values < 5, a coaxial tube or a metallic immersion tube/bypass is
always required.
Substance

Substance

Acetal (25 °C)

DK
value
3.8

Substance

Amyl amine

DK
value
4.5

Hydrogen cyanide

DK
value
158

Acetaldehyde

15

Aniline

7

Bore oil emulsion

25

Acetamide (77 °C)

59.2

Anisaldehyde

22.3

Bornylacetate

4.6

Acetoacetic acid ethyl ester

15

Anisole

4.5

Bromine

3.1

Acetone

21.5

Anthracite

3.2

Butanoic acid

3

Acetophenone

18

Antimony hydride

1.8

Camphene

2.3

Acetylacetone

23

Malic acid diethylester

10

Caproic acid (71 °C)

2.6

Acetyl bromide

16.2

Argon

1.5

Caprylic acid

2.5

Acetyl chloride

15.9

Arsine

2.1

Carbazole

1.3

Acetylene dibromide

7.2

Arsole

2.3

Carbonylcyanide

10.7

Acetylene tetrabromide

5.6

Asbestos

10

Cellite

1.6

Aconite acid ester

6.3

Ascorbic acid (vitamin C)

2.1

Cetyl alcohol (60 °C)

3.6

Adipic acid

1.8

Azelaic acid diethylester

5

Quinoline

8.8

Aerosile

1

Azoxybenzene (36 °C)

5.2

Chlorine, liquid

2.1

Activated carbon

12

Basalt

2.5

Chloral

6.7

Alums (60 °C)

4.2

Cotton fiber flour

3.2

Chlorobenzine

5.7

Allyl alcohol

20.6

Bauxite

2.5

Chloracetic acid

33.4

Allyl chloride

8.2

Bentonite

8.1

Chlorohydrin

31

Allyl iodide

6.1

Benzal chloride

6.9

Chlorinated lime

2.3

Aluminum bromide (100 °C)

3.4

Benzaldehyde

17.6

Chloroform (trichlormethane)

4.8

Aluminum foil

10.8

Benzil (80 °C)

10

Cola essence

17.3

Aluminum hydroxide

2.5

Benzine

2

Cream (skin)

19

Aluminum splinters

7.3

Benzene

2.3

Cuminaldehyde

10.7

Aluminum sulfate

2.6

Benzene, heavy

3.2

Cyanogen

2.5

Formic acid

57.9

Benzyl alcohol

13.5

Decalin

2.1

Ammonia

15

Benzyl amine

4.6

Degalan

3.1

Ammonia solution (25%)

31.6

Benzyl chloride

7

Desmodur

10

Ammonia salt

4.3

Beer brew

25

Diacetone alcohol

18.2

Pentanol

14.8

Bitumen

2.8

Diamylether

3

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

67

<!-- page 68 -->

18 MEDIA LIST

Substance

Substance

Dibenzofuran (100 °C)

DK
value
3

Substance

Ferrous sulfate (80 °C)

DK
value
32.4

Urea

DK
value
2.9

Dibenzyl (60 °C)

2.5

Ferrozell

18.3

Resin

1.5

Diesel fuel

2.1

Fat coal

3.4

Hazelnuts

2

Diethylamine

3.8

Fatty acid (35 °C)

1.7

Hot glue (150 °C)

2.3

Dimethylether (methyl ether)

5

Fish oil

2.6

Heating oil

2.1

Diofan

32

Flax pellets

1.4

Helium

1.1

Dioxane

2

Meat and bone meal

1.9

Heptane

1.9

Diphenyl (75 °C)

2.5

Tankage

1.9

Heptanal

9.1

Printing ink

4.6

Fly ash

3.3

Heptanoic acid (71 °C)

2.6

Ice cream (–20 °C)

16.5

Fluorine

1.5

Heptene

2.1

Iron (III) oxide red

1.9

Fluorbenzene

6.4

Hexane

1.9

Emulphor

4

Hydrogen fluoride (0 °C)

83.6

Hexene

2.1

Epichlorhydrin

23

Calcium fluoride

2.5

Hexanol

12.5

Peanuts, dried

3.1

Formamide

109

Hibiscus

2.8

Peanut expeller

2.4

Furan

3

Wood chips

2.3

Vinegar

24

Furfurol

41.7

Charcoal

1.3

Acetic acid

6.2

Animal feed grist

2.4

Wood swarf

1.5

Cement asbestos

3.2

Germanium tetrachloride

2.4

Splints

1.1

Ethanol (ethyl alcohol)

16.2

Grain grist

3

Honey

24

Ether

4

Gypsum

1.8

Hydrazine

58

Ethyl acetate

6

Fiber glass powder

1.1

Imidazole, pure (100 °C)

23

Ethylamine

6.9

Glass granulate

4

Isoamyl acetate

4.8

Ethyl benzoate

6

Cullet

2

Isoamyl alcohol

15.6

Ethyl benzene

2.4

Glucose (50 °C)

30

Isoamyl bromide

6

Ethylene chlorohydrin

25

Glycerol

13.2

Isoamyl chloride

6.1

Ethylene chloride

10.6

Glycerol water

37

Isoamyl ether

2.8

Ethylenediamine

15

Glycol

37

Isoamyl iodide

5.6

Ethylene oxide (–1 °C)

13.9

Glysantin

25

Isobutanoic acid

2.6

Ethyl mercaptan

6.9

Granuform

4

Isobutyl alcohol

18.1

Fenchone

12.8

Guaiacol

11

Isobutyl amine

4.4

Ferrite pellets

21

Guano (phosphate rock)

2.5

Isobutyl benzene

2.3

Ferrosilicone

10

Oat

4.9

Isobutyl bromide

7.2

68

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 69 -->

MEDIA LIST 18

Substance

Substance

Isobutyl chloride

DK
value
6.5

Substance

Coke

DK
value
3

Methylene bromide

DK
value
7

Isobutyl cyanide

18

Cork powder

1.7

Methylene chloride

9

Isobutyl iodide

6.5

Concentrated feed

3.2

Methylene chloride

9.1

Isobutyl nitrate

11.7

Chalk

2.1

Methylene iodide

5.3

Isobutyl silane

2.5

Cresol

11

Methyl nitrate

23.5

Isoquinoline

10.7

Cresol resin

18.3

Methyl cellulose

3

Isocyanate

6.1

Crystal sugar

2

Monochloremethane

9.8

Isoprene

2.1

Fertilizer

4.3

Morpholine

7.3

Isopropanol

18

Plastic pellets

1.2

Naphthenic acid

2.6

Isosafrol

3.3

Copper ore

5.6

Naphthalene

2.5

Iodine

11.1

Nitrous oxide

1.5

Sodium carbonate

3

Iodobenzene

4.6

Lanolin

4.2

Sodium methylate

1.5

Methyl iodide

7.1

Latex

24

Sodium perborate

2.2

Hydrogen iodide

2.9

Lauric acid ethyl ester

3.4

Sodium peroxide

2.7

Coffee beans

1.5

Glue

2

Sodium sulfate

2.7

Cocoa beans

1.8

Linoleic acid

2.7

Nitrobenzene

35

Caustic potash

3.3

Solvent

18

Nitroethane

29

Potash salt

2

Skim milk powder

2.3

Nitroglycol

28.3

Lime

2

Corn

3.6

Nitroglycerin

19.3

Potato starch

1.7

Corn grist

2.1

Nitro varnish

5.2

Ceramic compound

17

Corn starch syrup

18.4

Nitromethane

39

Ketchup

24

Malt

2.7

Nitrophoska

5,4

Gravel

2.6

Mandelic acid nitril

18

Nitrosyl bromide (13 °C)

15.2

Diatomaceous earth

1.4

2.5

Nitrosyl chloride

19

Silicic acid

2

Small marble stones
(grain size of 2-)
Mice feed

2.3

Pasta, milled durum

1.9

Bone fat

2.7

Flour

2.5

Octane

2

Bonemeal

1.7

Molasses

31.3

Octene

2.1

Sodium chloride

23

Menthol (42 °C)

4

Octyl bromide

5

Coal, 15% moisture

4

Mesityl oxide

15

Oil

2

Diethyl carbonate

2.8

Metal powder

6

Oileic acid

2.5

Coal dust

2.5

Methanol (methyl alcohol)

33

Water-in-oil emulsion

24.2

Coconut oil (refined)

2.9

Methyl acetate

8

Oxalo ethyl acetate

6

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

69

<!-- page 70 -->

18 MEDIA LIST

Substance

Substance

Palmitic acid

DK
value
2.3

Substance

Popcorn

DK
value
1.1

Soft soap

DK
value
32

Palm tree nuts

2.2

Pril (liquid detergent)

1.2

Chocolate powder

2

Palm tree nuts

2.8

Propanal (15 °C)

14.4

Black liquor

32

Palm seed oil

1.8

Propanol (propyl alcohol)

2.2

Sulfur

3.5

Paper scraps

1.2

Propanoic acid

3.2

14

Paraffin

1.6

Propylamine

3

Sulfur dioxide
(sulfurous acid)
Carbon disulfide, pure

2.6

Paraldehyde

15.1

Propylene, liquid

1.9

Sulfuric acid

21.9

Pelargon

2.8

Propylene chloride

9

Sulfuric acid (15%)

31

Penta borane

21

Propylether

3.3

Sulfuric acid (97%)

8.6

Penta ethyl chloride

3.8

PVC powder, pure

1.3

Sulfur trioxide

3.1

Penta chlorotoluene

4.8

Pyridine

13.2

Hydrogen sulfide

6

Pentane

1.8

Pyrrol

8

Heavy fuel oil

2.2

Pentanal (15 °C)

11.8

Silica sand

2

Soap flakes

9.2

Pentene

2

Quartz stone meal

2.7

Soap pellets

3.5

Perchlorate

3.6

Mercury diethyl

2.1

Mustard

24

Hexachlorobutadiene

2.6

Rapeseed

3.3

Mustard seeds

3.6

Perlite

1.7

Rapeseed grist

2.1

Silicone oil

2.7

PET powder

1.5

Rice

3

Silicone rubber

2.9

Phenetole

4.2

Rye

6

Soy flour

4.5

Phenol

8

Rye bran

2.2

Soy grains

2.9

Phenol resin

7.4

Beetroot seeds

3.5

Sunflower seeds

2

Phosgene

4.3

Beetroot cuttings

7.3

Chaff

1.5

Phosphate

4

Carbon black

18.8

Stearic acid

2.3

Phosphorus, liquid

3.9

Saccharose solution

20

Rock salt (0–25 mm)

4.3

Phosphorus salt

4

Sawdust

1.3

Styrene

2.4

Pinane

2.1

Nitric acid (98%)

19

Tobacco dust

1.8

Piperidine

5.8

Hydrochloric acid

5

Talcum

1.5

Polyamide pellets

1.7

Salt water

32

Tea powder

2

Polyethylene

1.2

Oxygen

1.5

Tar, raw

4

Polypropylene

1.6

Chamotte

1.8

Terephthalic acid

1.5

Polyrol

2.8

Foam flakes

1.1

White spirit

2

Polyvinyl acetals

2.8

Lard (80 °C)

2.1

Terpinene

2.7

70

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

8019918/ZJA6 / 2017-07-20 | S I C K A G
Subject to change without notice

<!-- page 71 -->

MEDIA LIST 18

Substance

Substance

Terpinolene

DK
value
2.3

Xylitol

DK
value
40

Tetrachloroethylene

2.5

Xylene

2.3

Carbon tetrachloride

2.3

Toothpaste

18.3

Thomaskali dust

3.4

Cellulose

1.2

Thujone (0 °C)

10.8

Cement

2.2

Meat and bone meal

2.2

Zinc oxide

1.5

Titan tetrachloride

2.8

Zinc powder

4.4

Toluene

2.4

Sugar

1.8

Clay

2.3

Tinder

12

Transformer oil

2.1

Trichloroethylene

3.2

Triethyl aluminum

2.9

Triptan

1.9

Dry yeast

2

Ultrasil

1.4

Undecan

2

Valeric acid

2.7

Viscose

34.5

Wax

1.8

Benzine

2

Water

80.3

Water (360 °C)

10

Water, demineralized

29.3

Water, heavy

78.3

Sodium silicate

16

Hydrogen

1.2

Hydrogen peroxide,
pure (0 °C)

84.2

Wine

25

Tartaric acid

35.9

Wheat

4

Wheat starch

2.5

8019918 /ZJA6/ 2017-07-20 | S I C K A G
Subject to change without notice

O P E R AT I N G I N S T R U C T I O N S | L F P C U B I C

71

<!-- page 72 -->

8019918/ZJA6 /2017-07-20 ∙ COMAT/ITL (2016-05) ∙ A4 4c int47

Australia
Phone +61 3 9457 0600
1800 334 802 – tollfree
E-Mail sales@sick.com.au

Israel
Phone +972 4 6881000
E-Mail info@sick-sensors.com

South Korea
Phone +82 2 786 6321
E-Mail info@sickkorea.net

Italy
Phone +39 02 274341
E-Mail info@sick.it

Spain
Phone +34 93 480 31 00
E-Mail info@sick.es

Japan
Phone +81 3 5309 2112
E-Mail support@sick.jp

Sweden
Phone +46 10 110 10 00
E-Mail info@sick.se

Malaysia
Phone +6 03 8080 7425
E-Mail enquiry.my@sick.com

Switzerland
Phone +41 41 619 29 39
E-Mail contact@sick.ch

Mexico
Phone +52 (472) 748 9451
E-Mail mario.garcia@sick.com

Taiwan
Phone +886 2 2375-6288
E-Mail sales@sick.com.tw

Netherlands
Phone +31 30 2044 000
E-Mail info@sick.nl

Thailand
Phone +66 2645 0009
E-Mail Ronnie.Lim@sick.com

Chile
Phone +56 2 2274 7430
E-Mail info@schadler.com

New Zealand
Phone +64 9 415 0459
0800 222 278 – tollfree
E-Mail sales@sick.co.nz

Turkey
Phone +90 216 528 50 00
E-Mail info@sick.com.tr

China
Phone +86 20 2882 3600
E-Mail info.china@sick.net.cn

Norway
Phone +47 67 81 50 00
E-Mail sick@sick.no

Denmark
Phone +45 45 82 64 00
E-Mail sick@sick.dk

Poland
Phone +48 22 539 41 00
E-Mail info@sick.pl

Finland
Phone +358-9-2515 800
E-Mail sick@sick.fi

Romania
Phone +40 356 171 120
E-Mail office@sick.ro

France
Phone +33 1 64 62 35 00
E-Mail info@sick.fr

Russia
Phone +7 495 775 05 30
E-Mail info@sick.ru

Germany
Phone +49 211 5301-301
E-Mail info@sick.de

Singapore
Phone +65 6744 3732
E-Mail sales.gsg@sick.com

Hong Kong
Phone +852 2153 6300
E-Mail ghk@sick.com.hk

Slovakia
Phone +421 482 901201
E-Mail mail@sick-sk.sk

Hungary
Phone +36 1 371 2680
E-Mail office@sick.hu

Slovenia
Phone +386 591 788 49
E-Mail office@sick.si

India
Phone +91 22 6119 8900
E-Mail info@sick-india.com

South Africa
Phone +27 11 472 3733
E-Mail info@sickautomation.co.za

Austria
Phone +43 22 36 62 28 8-0
E-Mail office@sick.at
Belgium/Luxembourg
Phone +32 2 466 55 66
E-Mail info@sick.be
Brazil
Phone +55 11 3215-4900
E-Mail marketing@sick.com.br
Canada
Phone +1 905 771 14 44
E-Mail information@sick.com
Czech Republic
Phone +420 2 57 91 18 50
E-Mail sick@sick.cz

SICK AG | Waldkirch | Germany | www.sick.com

United Arab Emirates
Phone +971 4 88 65 878
E-Mail info@sick.ae
United Kingdom
Phone +44 1727 831121
E-Mail info@sick.co.uk
USA
Phone +1 800 325 7425
E-Mail info@sick.com
Vietnam
Phone +84 945452999
E-Mail Ngo.Duy.Linh@sick.com

Further locations at www.sick.com
