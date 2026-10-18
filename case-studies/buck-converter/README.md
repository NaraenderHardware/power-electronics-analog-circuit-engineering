# Engineering Case Study: 36V to 18V (24W) DC-DC Buck Converter

## 1. Executive Summary

This case study documents the comprehensive design, technical audit, and hardware implementation review of an open-loop **DC-DC Step-Down (Buck) Converter** designed to convert a **36V DC nominal input** down to an **18V DC output** at **24W nominal power (1.33A load)** with a switching frequency of **50 kHz**.

The system comprises three physical functional subsystems:
1. **Embedded Microcontroller PWM Generator:** ATmega328P (Arduino Nano) utilizing Timer1 in Fast PWM Mode 14 to synthesize a 50 kHz, 50% fixed duty-cycle switching signal.
2. **Optically Isolated Gate Drive Subsystem:** Toshiba TLP350 photocoupler driver with push-pull output designed to switch a high-side N-channel power MOSFET.
3. **Power Stage Subsystem:** Single-layer PCB assembly featuring an IRLZ44N N-channel MOSFET, freewheeling Schottky diode, power inductor, and filter capacitor.

```
       +36V DC Input Rail
             |
             +---------------+
                             |
                      [Q1: IRLZ44N] (High-Side NMOS Switch)
                             |
            Switch Node (Vsw)+---------+--------[L1: Inductor]--------+--------> +18V DC Output
                             |         |                              |
                          [D1: Diode] [J2: Gate Drive]             [C1: Cap] [Load: 13.5 Ohm]
                          (Freewheel) (Source Ref)                    |         |
                             |         |                              |         |
      GND Return ------------+---------+------------------------------+---------+--------> Power GND
```

---

## 2. Specification Matrix: Design Targets vs. Verified Source Reality

| Parameter | Target / Stated Claim | Audited / Verified Reality | Engineering Evaluation & Verification Notes |
| :--- | :--- | :--- | :--- |
| **Input Voltage ($V_{in}$)** | 36.0 V DC | 36.0 V DC (Nominal design) | Unregulated bench input target. Requires local bypass capacitance ($C_{in}$) absent on power PCB. |
| **Output Voltage ($V_{out}$)** | 18.0 V DC | 17.17 V DC (Calculated real under 1.33A load at $D=0.5$) | At open-loop $D=0.5$, forward diode drop ($V_F \approx 0.55\text{V}$), $R_{DS(on)}$ drop, and inductor DCR induce $\approx 0.83\text{V}$ droop below 18.0V. |
| **Output Current ($I_{out}$)** | 1.33 A DC | 1.333 A DC at full load | Stated target $P_{out} / V_{out} = 24\text{W} / 18\text{V} = 1.333\text{A}$. |
| **Output Power ($P_{out}$)** | 24.0 W | Theoretical design rating | Requires $13.5\ \Omega$ load resistor capable of continuously dissipating 24W. |
| **Switching Frequency ($f_s$)** | 50 kHz | **50.000 kHz** (Verified in Timer1 registers) | $f_{PWM} = \frac{16\text{ MHz}}{1 \times (319 + 1)} = 50.000\text{ kHz}$. Exactly verified. |
| **Duty Cycle ($D$)** | 50% ($D = 0.50$) | **50.00%** (Verified in Timer1 registers) | $\text{OCR1A} = 160$, $\text{TOP} = 319$ ($\frac{160}{320} = 0.5000$). Open-loop only; no closed-loop voltage regulation. |
| **Control Architecture** | Microcontroller PWM | Open-loop hardware PWM | Code runs on Arduino Nano Pin 9 (OC1A). Loop is empty; no ADC voltage/current feedback implemented. |
| **Gate Driver IC** | Toshiba TLP350 | Toshiba TLP350F (DIP-8) | Photocoupler driver ($I_{out} = \pm 2.5\text{A}$). **Requires isolated floating supply** referenced to MOSFET Source. |
| **Power Switch ($Q_1$)** | IRLZ44N | IRLZ44N (TO-220) | Logic-level N-channel MOSFET ($V_{DSS} = 55\text{V}$, $R_{DS(on)} = 0.022\ \Omega$ at $10\text{V}$, $0.028\ \Omega$ at $5\text{V}$, $I_D = 47\text{A}$). |
| **Catch Diode ($D_1$)** | 1N5819 Schottky | 1N5819 (DO-41 package) | **CRITICAL AUDIT HAZARD:** $V_{RRM} = 40\text{ V}$, $I_{F(AV)} = 1.0\text{ A}$ continuous average. Operating at $36\text{ V}$ input leaves only $10.0\%$ ($4\text{ V}$) static reverse margin, highly vulnerable to switching transients. In CCM ($D=0.5$), calculated average forward current is $0.667\text{ A}$ (within 1.0A average rating) and peak current reaches $\approx 1.564\text{ A}$. Specific peak, surge, and thermal derating limits are unverified without the exact manufacturer datasheet. Diode replacement alone does not make the converter safe. |
| **Storage Inductor ($L_1$)** | $680\ \mu\text{H}$ | $390\ \mu\text{H}$ on hardware (`PCV-2-394-05L`) | Design calculation PDF states $680\ \mu\text{H}$ ($\Delta I_L = 20\%$). Physical hardware photograph shows `PCV-2-394-05L` ($390\ \mu\text{H}$, $\Delta I_L = 34.6\%$). |
| **Output Filter Cap ($C_1$)** | $100\ \mu\text{F}$ | **Unpopulated / Missing on physical hardware** | Design calls for $100\ \mu\text{F}$ electrolytic. In `front_view.jpg`, $C_1$ mounting holes are empty. |
| **Physical PCB Status** | Fabricated & Assembled | Hand-routed single-layer copper prototype | Copper-clad board with hand-soldered bridges; extensive solder pooling on traces. Unsnubbed switch node. |

---

## 3. Power Stage Topology & Operating Physics

The buck converter operates in Continuous Conduction Mode (CCM) under nominal load conditions. The switching cycle is split into two intervals over the period $T_s = \frac{1}{f_s} = 20\ \mu\text{s}$:

```
     ON-State (0 <= t < Ton):                      OFF-State (Ton <= t < Ts):
     Q1 Conducting, D1 Reverse-Biased              Q1 OFF, D1 Forward-Biased (Freewheeling)
     
        +Vin                                          +Vin
         o                                             o
         |                                             |
       [Q1: ON]                                      [Q1: OFF]
         |                                             |
         +----[ L1 ]----+----> +Vout                   +----[ L1 ]----+----> +Vout
         |              |                              |              |
      [D1: OFF]       [C1] [Rload]                  [D1: ON]        [C1] [Rload]
         |              |                              |              |
        GND            GND                            GND            GND
```

### 3.1 Ideal Steady-State Voltage Conversion
By applying volt-second balance to inductor $L_1$:
$$\int_{0}^{T_s} v_L(t) \, dt = (V_{in} - V_{out}) T_{on} + (-V_{out}) T_{off} = 0$$
$$(V_{in} - V_{out}) D T_s = V_{out} (1 - D) T_s \implies V_{out} = D \cdot V_{in}$$
For $V_{in} = 36.0\text{ V}$ and $D = 0.50$:
$$V_{out(ideal)} = 0.50 \times 36.0\text{ V} = 18.00\text{ V}$$

### 3.2 Real Voltage Conversion with Conduction Losses
Accounting for forward voltage drop across diode $D_1$ ($V_F \approx 0.55\text{V}$), MOSFET channel resistance ($R_{DS(on)} = 0.028\ \Omega$), and inductor DC resistance ($R_{DCR} \approx 0.40\ \Omega$):
$$V_{out} = D \left( V_{in} - I_{out} R_{DS(on)} \right) - (1 - D) V_F - I_{out} R_{DCR}$$
Substituting $V_{in} = 36.0\text{ V}$, $D = 0.50$, $I_{out} = 1.333\text{ A}$:
$$V_{out} = 0.50 \times (36.0 - 1.333 \times 0.028) - 0.50 \times (0.55) - (1.333 \times 0.40)$$
$$V_{out} = 17.981 - 0.275 - 0.533 = 17.173\text{ V}$$
$$\text{Output Voltage Droop} = 18.00\text{ V} - 17.17\text{ V} = 0.83\text{ V}\ (4.6\%)$$
To recover exactly $18.00\text{ V}$ under full load, the required duty cycle is:
$$D_{real} = \frac{V_{out} + V_F + I_{out} R_{DCR}}{V_{in} - I_{out} R_{DS(on)} + V_F} = \frac{18.00 + 0.55 + 0.533}{36.0 - 0.037 + 0.55} = \frac{19.083}{36.513} = 52.26\%$$

---

## 4. Inductor Design & Ripple Current Audit

### 4.1 CCM Boundary Inductance ($L_{crit}$)
The minimum inductance required to maintain Continuous Conduction Mode at nominal load ($R_{load} = 13.5\ \Omega$) occurs when inductor ripple current $\Delta I_L = 2 I_{out}$:
$$L_{crit} = \frac{R_{load} (1 - D)}{2 f_s} = \frac{13.5\ \Omega \times (1 - 0.50)}{2 \times 50,000\text{ Hz}} = \frac{6.75}{100,000} = 67.5\ \mu\text{H}$$
Both the theoretical design value ($680\ \mu\text{H}$) and the physical hardware component ($390\ \mu\text{H}$) operate safely above $L_{crit}$, ensuring CCM at full load.

### 4.2 Comparison: Designed ($680\ \mu\text{H}$) vs. Physical Hardware ($390\ \mu\text{H}$)
The inductor current ripple is governed by:
$$\Delta I_L = \frac{V_{out} (1 - D)}{f_s \cdot L}$$

```
Inductor Current Waveform in CCM:

   IL (Amperes)
      ^
IL_pk |      /\          /\          /\
      |     /  \        /  \        /  \
 Iout |----/----+------/----+------/----+----> Average DC = 1.333 A
      |   /      \    /      \    /      \
IL_vly|  /        \  /        \  /        \
   0  +--+--------+--+--------+--+--------+--> Time
         |<--Ton->|  |<--Toff>|
         |<------- Ts ------->|
```

* **Theoretical Designed Inductor ($L = 680\ \mu\text{H}$):**
  $$\Delta I_L = \frac{18.0\text{ V} \times (1 - 0.50)}{50,000\text{ Hz} \times 680 \times 10^{-6}\text{ H}} = \frac{9.0}{34.0} = 0.2647\text{ A}\ (19.85\%\text{ of } I_{out})$$
  $$I_{L(peak)} = I_{out} + \frac{\Delta I_L}{2} = 1.333 + 0.132 = 1.466\text{ A}$$
  $$I_{L(valley)} = I_{out} - \frac{\Delta I_L}{2} = 1.333 - 0.132 = 1.201\text{ A}$$

* **Physical Hardware Component (`PCV-2-394-05L`, nominal $390\ \mu\text{H}$):**
  $$\Delta I_L = \frac{18.0\text{ V} \times (1 - 0.50)}{50,000\text{ Hz} \times 390 \times 10^{-6}\text{ H}} = \frac{9.0}{19.5} = 0.4615\text{ A}\ (34.62\%\text{ of } I_{out})$$
  $$I_{L(peak)} = 1.333 + 0.231 = 1.564\text{ A}$$
  $$I_{L(valley)} = 1.333 - 0.231 = 1.103\text{ A}$$

---

## 5. Output Capacitor & Ripple Analysis

### 5.1 Capacitive Charge Ripple ($\Delta V_C$)
For a triangular inductor ripple current, the charge accumulated by the capacitor during the upper half of the ripple triangle is $\Delta Q = \frac{1}{2} \times \frac{T_s}{2} \times \frac{\Delta I_L}{2} = \frac{\Delta I_L}{8 f_s}$. The resulting capacitive voltage ripple is:
$$\Delta V_C = \frac{\Delta I_L}{8 f_s C}$$
For $C = 100\ \mu\text{F}$ and $\Delta I_L = 0.265\text{ A}$ (with $680\ \mu\text{H}$):
$$\Delta V_C = \frac{0.265\text{ A}}{8 \times 50,000\text{ Hz} \times 100 \times 10^{-6}\text{ F}} = \frac{0.265}{40} = 6.62\text{ mV}_{p-p}\ (0.037\%)$$

### 5.2 Real Ripple Dominated by Equivalent Series Resistance (ESR)
A standard general-purpose electrolytic capacitor ($100\ \mu\text{F}, 50\text{V}$) exhibits an ESR of approximately $R_{ESR} \approx 0.15\ \Omega$ at 50 kHz:
$$\Delta V_{ESR} = \Delta I_L \times R_{ESR} = 0.265\text{ A} \times 0.15\ \Omega = 39.75\text{ mV}_{p-p}$$
$$\Delta V_{out(total)} \approx \Delta V_C + \Delta V_{ESR} = 6.62\text{ mV} + 39.75\text{ mV} \approx 46.37\text{ mV}_{p-p}\ (0.26\%)$$

### 5.3 Critical Hardware Discrepancy: Missing Capacitor $C_1$
In the physical hardware photograph (`hardware/front_view.jpg`), the footprint for $C_1$ is unpopulated. If energized without $C_1$, the entire inductor AC ripple current flows directly through the load resistor ($13.5\ \Omega$):
$$\Delta V_{load(no\ C1)} = \Delta I_L \times R_{load} = 0.4615\text{ A} \times 13.5\ \Omega = 6.23\text{ V}_{p-p}$$
This represents an intolerable $34.6\%$ peak-to-peak output ripple, confirming that the circuit was unpopulated and incomplete during board assembly.

---

## 6. Semiconductor Stress & Thermal Derating Audit

### 6.1 Freewheeling Diode ($D_1$): Critical Safety Evaluation
The design specification and calculation document specify a **1N5819 Schottky diode** in an axial DO-41 package.
* **Datasheet Baseline (1N5819):**
  - Maximum Peak Repetitive Reverse Voltage ($V_{RRM}$): **$40\text{ V}$**
  - Average Rectified Forward Current ($I_{F(AV)}$): **$1.0\text{ A}$** (typically specified at lead temperature $T_L \approx 75^\circ\text{C}$ to $90^\circ\text{C}$, depending on manufacturer)
  - Thermal Resistance Junction-to-Ambient ($R_{\theta JA}$): **$80\ ^\circ\text{C/W}$ to $105\ ^\circ\text{C/W}$**
* **Operating Electrical Stress in This Converter:**
  - Operating DC Reverse Voltage: $V_R = V_{in} = 36.0\text{ V}$.
  - Static Reverse Voltage Margin: $\frac{40\text{V} - 36\text{V}}{40\text{V}} = 10.0\%$ (only $4.0\text{ V}$ of static margin). Standard high-reliability power derating guidelines (such as IPC-9592B Class 2, MIL-HDBK-1547A, and NAVSEA TE000-AB-GTP-010) recommend maintaining at least 20% to 30% reverse voltage derating ($\ge 52\text{V}$ to $60\text{V}$ rating). While these standards are not legally mandatory for an academic prototype, operating with only 4V of static headroom provides inadequate margin for inductive switching transients.
  - Switch-Node Transients: Unsnubbed hard-switching parasitics (layout loop inductance ringing with diode junction and MOSFET output capacitance) introduce potential inductive overshoot. Theoretical estimates suggest possible voltage spikes of $1.2\times$ to $1.5\times V_{in}$ ($43\text{V} - 54\text{V}$). This $43\text{V} - 54\text{V}$ range is a calculated theoretical estimate based on typical parasitic inductances, NOT a measured circuit result or validated simulation. Nevertheless, even modest switching transients can easily exceed the 40V static limit, placing the unconfirmed 1N5819 at risk of reverse breakdown.
  - Forward Current Stress: Under nominal CCM assumptions ($D = 0.50$, $I_{out} = 1.333\text{ A}$), the calculated average forward current during off-time is $I_{D(avg)} = (1 - D) I_{out} = 0.667\text{ A}$, which is within the $1.0\text{ A}$ continuous average rating. Peak forward current reaches $I_{D(pk)} \approx 1.564\text{ A}$. This peak current alone does not violate a 1.0 A continuous average rating, as peak current ratings, repetitive peak surge limits ($I_{FRM}$), non-repetitive surge ratings ($I_{FSM}$), and thermal derating curves are manufacturer- and test-condition-specific. Because the exact manufacturer and lot of the installed diode cannot be confirmed from the hardware photograph, those specific limits remain unverified. At $0.55\text{V}$ forward drop, conduction dissipation of $\approx 0.367\text{ W}$ will induce a junction rise of $30^\circ\text{C}$ to $40^\circ\text{C}$ in still air, approaching thermal limits in enclosed operating conditions.
* **Remediation & System Safety Context:** Upgrading the diode to a $60\text{V}$, $3\text{A}$ Schottky diode (e.g., MBR360 or SS36) is an essential first step. However, **changing the diode alone does NOT make the complete converter safe**. The system remains strictly blocked from 36V energization until the unpopulated output capacitor is installed, the gate driver is powered from a floating isolated supply, inductor saturation margin is validated, and switching transients are adequately suppressed.

### 6.2 Power MOSFET ($Q_1$): IRLZ44N Conduction & Switching Losses
* **Device Ratings:** $V_{DSS} = 55\text{ V}$, $R_{DS(on)} = 0.028\ \Omega$ ($V_{GS} = 5\text{V}$), $I_D = 47\text{ A}$, $R_{\theta JA} = 62\ ^\circ\text{C/W}$ (without heatsink).
* **Conduction Loss ($P_{cond}$):**
  $$P_{cond} = D \times I_{out}^2 \times R_{DS(on)} = 0.50 \times (1.333\text{ A})^2 \times 0.028\ \Omega = 24.9\text{ mW}$$
* **Switching Loss ($P_{sw}$):**
  Assuming switching transition times $t_r = t_f \approx 30\text{ ns}$ (driven by TLP350 at 2.5A peak):
  $$P_{sw} = \frac{1}{2} V_{in} I_{out} (t_r + t_f) f_s = \frac{1}{2} \times 36\text{ V} \times 1.333\text{ A} \times (60 \times 10^{-9}\text{ s}) \times 50,000\text{ Hz} = 72.0\text{ mW}$$
* **Total MOSFET Dissipation:**
  $$P_{MOS(total)} = P_{cond} + P_{sw} = 24.9\text{ mW} + 72.0\text{ mW} = 96.9\text{ mW}\ (\approx 0.1\text{ W})$$
  Temperature rise without heatsink: $\Delta T_J = 0.097\text{W} \times 62\ ^\circ\text{C/W} \approx 6.0\ ^\circ\text{C}$. The TO-220 package operates thermally cool at 24W output.

---

## 7. Gate-Driver Circuit Architecture & Floating Drive Requirements

The power stage employs a **high-side N-channel MOSFET**. Understanding the gate drive topology is vital to operating this converter safely.

```
       +36V DC Rail
            |
         [Drain]
      +--| Q1: IRLZ44N
      |  [Source] ---------+------------------> Switch Node (Vsw = 0V when OFF, 36V when ON)
      |     |              |
      |     |       [Pin 2 of J2]
      |     |              |
      |     +-------+      |
      |             |      |
 [Pin 1 of J2]      |      |
      |             |      |
      |     [Toshiba TLP350F Isolated Gate Driver]
      |     +-----------------------------------+
      |     | Pin 8: VCC (Floating Aux Supply)  |
      +-----| Pin 6: VO (Gate Drive Output)     |
            | Pin 5: GND (Driver Reference) ----+ (Must connect to MOSFET Source!)
            |                                   |
            | Pin 2: Anode (LED Input via Rlim) | <--- Driven by Arduino Pin 9 (PWM)
            | Pin 3: Cathode (LED Return) ------+ <--- Arduino GND
            +-----------------------------------+
```

### 7.1 High-Side Drive Physics
* When $Q_1$ turns ON, its source rises to $V_{in} = 36.0\text{ V}$.
* To sustain $V_{GS} = 10\text{ V}$ and keep $Q_1$ fully saturated, the gate must be driven to:
  $$V_G = V_S + V_{GS} = 36.0\text{ V} + 10.0\text{ V} = 46.0\text{ V (relative to system power ground!)}$$
* The Toshiba TLP350 optocoupler driver provides galvanic isolation (isolation voltage $2500\text{ V}_{RMS}$).
* **Operating Constraint:** TLP350 Pin 5 (GND) must be tied directly to the MOSFET Source (the switching node). Pin 8 ($V_{CC}$) must be powered from a **floating auxiliary supply** (such as an isolated 12V DC-DC converter, e.g., Mornsun B1212S, or a bootstrap diode/capacitor circuit).
* **Power Supply Rating Warning:** TLP350 has an absolute maximum supply voltage rating of $35\text{ V}$, with a recommended operating range of $15\text{ V}$ to $30\text{ V}$. Connecting TLP350 Pin 8 directly to the $36\text{ V}$ input rail violates manufacturer absolute maximum ratings.

---

## 8. Microcontroller PWM Firmware Verification

The active curated firmware resides in [`code/arduino_pwm.ino`](code/arduino_pwm.ino), formatted as plain Arduino C++ source code without Markdown wrapper fences. The historical wrapped version is preserved separately in [`code/arduino_pwm.original.ino`](code/arduino_pwm.original.ino) for source provenance. The firmware configures 16-bit Timer1 on the ATmega328P.

```cpp
// 50 kHz PWM on Arduino Nano (Pin 9)

void setup() {
  pinMode(9, OUTPUT);

  // Clear Timer1 control registers
  TCCR1A = 0;
  TCCR1B = 0;

  // Set Fast PWM mode with ICR1 as TOP (Mode 14: WGM13=1, WGM12=1, WGM11=1, WGM10=0)
  TCCR1A |= (1 << WGM11);
  TCCR1B |= (1 << WGM12) | (1 << WGM13);

  // Non-inverting mode on OC1A (Pin 9): Clear OC1A on compare match, set at BOTTOM
  TCCR1A |= (1 << COM1A1);

  // Clock select: No prescaling (N = 1, CS10 = 1)
  TCCR1B |= (1 << CS10);

  // Set TOP value for 50 kHz: f = f_clk / (N * (1 + ICR1))
  ICR1 = 319;   // 16MHz / (1 * (319 + 1)) = 50,000 Hz

  // 50% duty cycle: OCR1A = 160 / 320 = 0.50
  OCR1A = 160;  // 160 clock cycles ON time = 10.0 us
}

void loop() {
  // Pure open-loop; hardware timer runs continuously in background
}
```

### 8.1 Register-Level Mathematical Verification
* **Oscillator Clock Frequency ($f_{clk\_I/O}$):** $16.000\text{ MHz}$
* **Prescaler ($N$):** $1$ (`CS10 = 1`, `CS11 = 0`, `CS12 = 0`)
* **Timer Mode:** Fast PWM Mode 14 (`WGM13:10 = 1110`). The counter $TCNT1$ increments from $0$ up to $ICR1$, resets to $0$, and asserts the overflow flag.
* **Frequency Formula:**
  $$f_{PWM} = \frac{f_{clk\_I/O}}{N \times (1 + \text{ICR1})} = \frac{16,000,000\text{ Hz}}{1 \times (1 + 319)} = \frac{16,000,000}{320} = 50,000\text{ Hz}\ (50.0\text{ kHz})$$
* **Duty Cycle Formula:**
  $$\text{Duty Cycle } D = \frac{\text{OCR1A}}{1 + \text{ICR1}} = \frac{160}{320} = 0.5000\ (50.0\%)$$
  $$\text{Pulse ON Time } t_{on} = \frac{\text{OCR1A}}{f_{clk\_I/O}} = \frac{160}{16,000,000\text{ Hz}} = 10.0\ \mu\text{s}$$
* **Mathematical Verification vs. Hardware Build Status:** The timer register calculations are verified mathematically with zero frequency error against ATmega328P datasheet specifications. However, this mathematical register derivation does not constitute an actual microcontroller compilation build (as Arduino CLI was not available in this environment) or a physical bench oscilloscope measurement of the pin output. Furthermore, generating a 50 kHz open-loop PWM signal does not prove DC-DC regulation, circuit efficiency, or closed-loop stability under dynamic load.

---

## 9. PCB Layout & Fabrication Audit

Inspecting `images/pcb_layout.png`, `hardware/front_view.jpg`, and `hardware/back_view.jpg`:

```
PCB Layout Observations:
1. Routing: Single-sided copper board, through-hole components.
2. High-Di/Dt Loop: The loop formed by input capacitor (missing), MOSFET Q1, and freewheeling diode D1
   spans over 45 mm of unshielded trace length. This high-inductance loop causes excessive EMI ringing.
3. Ground Plane: No continuous ground copper pour beneath the high-frequency switching path.
4. Assembly Quality: The fabricated hardware demonstrates manual trace routing with substantial solder
   pooling across tracks. Output capacitor C1 is absent from the populated board.
```

---

## 10. Hardware Evidence & Visual Gallery

All assets are preserved directly within this case study:

| View | Artifact Path | Description |
| :--- | :--- | :--- |
| **Power Stage Schematic** | [`images/schematic.png`](images/schematic.png) | Schematic export showing J1 (Input), Q1 (IRLZ44N), J2 (Gate drive header), D1 (Schottky), L1, C1, J3 (Output). |
| **Single-Layer PCB** | [`images/pcb_layout.png`](images/pcb_layout.png) | Exported single-layer track routing and footprint placements. |
| **3D Board Model** | [`images/3d_view.png`](images/3d_view.png) | 3D rendering of the single-sided PCB substrate and copper tracks. |
| **Assembled Front** | [`hardware/front_view.jpg`](hardware/front_view.jpg) | Populated prototype showing PCV-2-394-05L inductor, diode, MOSFET, screw terminals, and unpopulated C1 hole. |
| **Fabricated Back** | [`hardware/back_view.jpg`](hardware/back_view.jpg) | Hand-etched/milled copper tracks with manual solder bridging. |
| **Breadboard PWM Setup** | [`control/pwm_circuit.jpg`](control/pwm_circuit.jpg) | Arduino Nano wired with TLP350 photocoupler gate driver, resistors, and bypass capacitors. |
| **TLP350 Pinout** | [`control/tlp350_driver.jpg`](control/tlp350_driver.jpg) | Toshiba TLP350 functional pinout and totem-pole output stage. |
| **Design Calculations** | [`docs/design_calculations.pdf`](docs/design_calculations.pdf) | Original design calculations PDF document. |
| **Curated Firmware** | [`code/arduino_pwm.ino`](code/arduino_pwm.ino) | Clean Arduino C++ firmware for Timer1 50 kHz Fast PWM generation. |
| **Original Firmware** | [`code/arduino_pwm.original.ino`](code/arduino_pwm.original.ino) | Preserved historical firmware file with original Markdown wrapper. |
| **Historical Notes** | [`HISTORICAL_NOTES.md`](HISTORICAL_NOTES.md) | Summary of historical student documentation and reported claims. |

---

## 11. Reproducibility & Mathematical Verification Script

An automated Python verification script independently executes all governing equations:

```bash
# Execute the mathematical verification audit
python scripts/verify_buck_calculations.py
```

### Script Output Summary:
* $V_{in} = 36.00\text{V}$, $V_{out(ideal)} = 18.00\text{V}$, $P_{out} = 24.00\text{W}$, $I_{out} = 1.333\text{A}$.
* $L_{crit} = 67.50\ \mu\text{H}$.
* $L = 680\ \mu\text{H} \implies \Delta I_L = 0.265\text{A}$ ($19.9\%$ ripple).
* $L = 390\ \mu\text{H} \implies \Delta I_L = 0.462\text{A}$ ($34.6\%$ ripple).
* Output ripple with $C = 100\ \mu\text{F}$ & $150\text{m}\Omega\text{ ESR} = 46.32\text{ mV}$.
* Timer1 frequency: $50,000.0\text{ Hz}$, $D = 0.5000$.

---

## 12. Engineering Limitations & Safety Warnings

> [!CAUTION]
> **ENERGIZATION PROHIBITION AT 36 V**  
> The current physical prototype **MUST NOT BE ENERGIZED AT 36 V**. The design presents multiple critical safety and operational hazards supported by the source evidence and calculations:
> 1. **Diode Voltage Breakdown Hazard:** The installed 1N5819 Schottky diode has a $40\text{V}$ reverse breakdown rating against a $36\text{V}$ nominal DC bus, leaving only $4\text{V}$ ($10\%$) of static margin. In hard-switched converters, un-snubbed switching transients and stray inductance typically induce voltage spikes well beyond $40\text{V}$, risking immediate diode destruction.
> 2. **Uncharacterized Transients & Component Stresses:** Switching transients, high-di/dt ringing, and semiconductor thermal dissipation have not been experimentally characterized on this board.
> 3. **Unpopulated Output Capacitor:** In `hardware/front_view.jpg`, footprint $C_1$ is unpopulated. Energizing without $C_1$ forces the full inductor ripple current directly into the load resistor ($6.23\text{ V}_{p-p}$ calculated ripple).
> 4. **Inductor Mismatch & Core Saturation:** The installed inductor (`PCV-2-394-05L`, $\approx 390\ \mu\text{H}$) differs from the nominal $680\ \mu\text{H}$ design value, increasing ripple current by $74.4\%$ and risking magnetic saturation under full $1.33\text{A}$ DC load.
> 5. **High-Side Floating Gate Drive Requirement:** The TLP350 photocoupler output stage requires a dedicated, isolated auxiliary power supply referenced to the floating MOSFET Source node. Connecting the driver to system ground or exceeding its supply limits prevents proper switching or damages the IC.
> 6. **Open-Loop Control:** The firmware implements fixed open-loop PWM without closed-loop voltage or current feedback. The circuit cannot regulate against load changes or input variations.
> 7. **Unvalidated Thermal & Full-Load Performance:** Operating at 24W continuous output requires an adequately rated and heatsinked power load resistor. Thermal performance, semiconductor junction temperatures, and component deratings have not been experimentally validated.
>
> **Diode upgrade alone does not make the circuit safe.** Because these risks are interdependent, no bench energization procedure is provided for the current unverified prototype. All items above must be redesigned, fully populated, and verified before power can be applied.
