# Portfolio Verification and Engineering Limitations Report

**Target Repository:** [power-electronics-analog-circuit-engineering](https://github.com/NaraenderHardware/power-electronics-analog-circuit-engineering)  
**Historical Project References:** `Buck_Converter_36V_to_18V-main.zip`, `Function_Generator_OpAmp_741-main.zip`  
**Date of Audit:** October 18, 2026  
**Scope of Review:** Technical audit, parameter reconciliation, and publication readiness assessment  
**Engineering Domains:** Power Electronics (DC-DC Switched Conversion) & Analog Circuit Engineering (Waveform Generation & Dual Linear Supply)  

---

## 1. Executive Statement & Engineering Scope

This report documents the independent technical review, calculation audit, and repository hygiene assessment for two separate student engineering projects:
1. **Case Study 1:** 36V to 18V (24W, 50 kHz) DC-DC Buck Converter with ATmega328P PWM control and TLP350 photocoupler gate drive.
2. **Case Study 2:** Multi-Waveform Analog Function Generator ($\mu\text{A}741$) with Regulated Dual Power Supply ($\pm 12\text{V}$).

### Engineering Principles:
* **Evidence-Based Documentation:** Statements are categorized strictly as design targets, calculated estimates, historical recorded values, or unverified assumptions. No synthetic bench data, fake test captures, or unverified claims have been added.
* **Separation of Disciplines:** The buck converter and analog function generator represent two distinct projects and are documented separately.
* **Simulation & CAD File Transparency:** The repository contains exported raster PNG plots and screenshots from prior LTspice and Tinkercad sessions. Native CAD/EDA project files (`.kicad_sch`, `.kicad_pcb`, `.asc`, `.raw`) were not supplied in the original project files.
* **Safety Evaluation:** Component stress, voltage margins, isolation constraints, and energization hazards are evaluated against established engineering derating principles (such as IPC-9592B Class 2 and MIL-HDBK-1547A literature). These provide engineering benchmarks rather than mandatory certifications for an academic prototype.

---

## 2. Repository Inventory & Provenance Tracking

### 2.1 Workspace Provenance Notice
The original upstream zip archives (`Buck_Converter_36V_to_18V-main.zip` and `Function_Generator_OpAmp_741-main.zip`) were not present in the local workspace during this review pass; therefore, direct cryptographic comparison against those external archives could not be independently repeated in this pass. Provenance is tracked from the preserved source files and their documented cryptographic hashes.

### 2.2 Complete File Inventory by Category (39 Total Files)

#### Category 1: Preserved Original Historical Files (27 Files)
These files represent preserved historical source files, photographs, circuit graphics, design documents, and original licenses:

| File Path in Repository | SHA-256 Hash | Provenance Description |
| :--- | :--- | :--- |
| `case-studies/buck-converter/code/arduino_pwm.original.ino` | `115ce0d79f8870831a2001d3845512512cabc60c1f2dc09db2ae15ae0f4f66dc` | Original student firmware with Markdown wrapper fences |
| `case-studies/buck-converter/control/pwm_circuit.jpg` | `17dea2eae7bb63fdab6df0819886914ba91876a2d790e36e93d6bb01a88a746d` | Photograph of Arduino Nano and TLP350 breadboard circuit |
| `case-studies/buck-converter/control/tlp350_driver.jpg` | `327081feaebcb9659d93c908778d72714a49b91c2a02b0a56884e0600fdfcd61` | Reference diagram of Toshiba TLP350 pinout |
| `case-studies/buck-converter/docs/design_calculations.pdf` | `fde6dd012a14a20ebc53a8bbba6a05906928d1b5bd6489ba23036431101ae789` | Original design calculation document |
| `case-studies/buck-converter/hardware/back_view.jpg` | `b3efa51f5bdfc4746e784e24cdd844ea322a5c509c20695b96a60af163cf8d4c` | Prototype PCB rear copper tracks photograph |
| `case-studies/buck-converter/hardware/front_view.jpg` | `3efe35087f919fde33c9d02f84ca5204bcaac5baea79bb9f6799abc29878e4e2` | Prototype PCB front populated components photograph |
| `case-studies/buck-converter/images/3d_view.png` | `035606749265e7f1501f9923ac312f32c302f24d7897cfb04e4d8b80d8ef82d8` | Exported 3D board rendering |
| `case-studies/buck-converter/images/block_diagram.png` | `44cac46b5c380733f82814233fb3378275ddb3cde46c96b3133660597e8f876d` | System block diagram graphic |
| `case-studies/buck-converter/images/pcb_layout.png` | `9759d57a1add4162345be568180ce1c60699b201b9be8762c34ffe481df74147` | Exported PCB layout routing graphic |
| `case-studies/buck-converter/images/schematic.png` | `0013652bbee2b8a57a86e433849d56d19a95987d2c6595efceef84c7e00ec2f6` | Exported schematic diagram graphic |
| `case-studies/buck-converter/LICENSE` | `bb35f3c533585d6501b3921c42d242e8052d9bec6bb1825d37ecbc56151eaff7` | Preserved MIT license file |
| `case-studies/opamp-function-generator/images/block_diagram.png` | `ed8a9f9e533dc071e63ed687b7076940191cf1531f6507e581391c572ae44eff` | Exported schematic and block diagram graphic |
| `case-studies/opamp-function-generator/images/circuit_diagram.png` | `fbf12dea6ee88199edacd830c5f850622c7612ea1cd6600684ac0dd184b7abf2` | Photograph of breadboard lab setup at VIT University |
| `case-studies/opamp-function-generator/images/sine_wave.png` | `0c7de6a122c1989a389065849ac0bd163fec13cdc2895f1fa01507c85608279e` | Digital oscilloscope screenshot: sine wave |
| `case-studies/opamp-function-generator/images/sine_wave_deamplify.png` | `c7a3eb5a7761e2ef9740a1be7f9c9dd9ea1d72be6955f3fbeb56bdbd721d7e44` | Digital oscilloscope screenshot: attenuated sine wave |
| `case-studies/opamp-function-generator/images/square_wave.png` | `2d5c5b4a95227ca60440c876569991e5b774ebddf449c23f34a2fb4fbe5c8dc9` | Digital oscilloscope screenshot: square wave |
| `case-studies/opamp-function-generator/images/square_wave_deamplify.png` | `9cd892e11605b606d4f8105dd2a2bcc4740c02263afc3f3cc12f2611ff8b45f3` | Digital oscilloscope screenshot: attenuated square wave |
| `case-studies/opamp-function-generator/images/triangle_wave.png` | `1c124b221c563b3178991236a2f1d10b4585b61b28d76e09aab385ab63726916` | Digital oscilloscope screenshot: triangle wave |
| `case-studies/opamp-function-generator/images/triangle_wave_deamplify.png` | `7d9648f7158eb4140fa5513260905faf7990bc9bcc5c0dcd4073ebed0a890141` | Digital oscilloscope screenshot: attenuated triangle wave |
| `case-studies/opamp-function-generator/simulation/function_generator.png` | `f64884ec68e37d5fd58a920f4791e3eb08707bba2c0690b556fb28d000b969c7` | Screenshot of Tinkercad virtual breadboard model |
| `case-studies/opamp-function-generator/simulation/rectified_ouput.png` | `71e416f2d8138d76619cc59ee3cb890df1ad174df8390ebbfce00a23ea8a394d` | Exported LTspice simulation plot: bridge rectifier DC |
| `case-studies/opamp-function-generator/simulation/regulated_output.png` | `ec81e52da49837ccfac486bff57e4d780d104c3de642559d337ca7255bcd83e4` | Exported LTspice simulation plot: +/-12V regulator output |
| `case-studies/opamp-function-generator/simulation/sine_simulation.png` | `dafa4134abb2a008c77253cadd1a52ba9bb835270223dc1bc55a6a4fa2ae8f49` | Exported LTspice simulation plot: sine oscillator |
| `case-studies/opamp-function-generator/simulation/square_simulation.png` | `be925dbc996b7628ed777a39ca0ea235abcc9afd9ef07f6987087ea531a84514` | Exported LTspice simulation plot: comparator square wave |
| `case-studies/opamp-function-generator/simulation/thinkercad_link.txt` | `cadaf7d06209be0d94ca846a0ffaac955a6db31e95052e7b24813cfc031c57f5` | Text link to Tinkercad online simulation |
| `case-studies/opamp-function-generator/simulation/triangle_simulation.png` | `6eb4db22fd0243d67bb67cf50cc464e8baab9153d9c7b2f046d0f4bdd599cbfb` | Exported LTspice simulation plot: integrator triangle wave |
| `case-studies/opamp-function-generator/LICENSE` | `bb35f3c533585d6501b3921c42d242e8052d9bec6bb1825d37ecbc56151eaff7` | Preserved MIT license file |

#### Category 2: Curated Firmware Formatted for Compilation (1 File)

| File Path in Repository | SHA-256 Hash | Provenance & Formatting Description |
| :--- | :--- | :--- |
| `case-studies/buck-converter/code/arduino_pwm.ino` | `1df9017af8d07f537a5cc1306bb6bb968919d6091287d6202ceba2d055468250` | Active curated firmware. Created by stripping markdown code fences (` ```cpp ` and ` ``` `) from the historical file so it compiles directly in Arduino toolchains. Because the markdown wrappers were removed, its hash differs from `arduino_pwm.original.ino` and it is not byte-identical. |

#### Category 3: Rewritten Historical Documentation (2 Files)

| File Path in Repository | Purpose & Status |
| :--- | :--- |
| `case-studies/buck-converter/HISTORICAL_NOTES.md` | Rewritten summary of original student README; emojis and unverified promotional claims removed. |
| `case-studies/opamp-function-generator/HISTORICAL_NOTES.md` | Rewritten summary of original student README; emojis and unverified promotional claims removed. |

#### Category 4: Duplicate Root License (1 File)

| File Path in Repository | SHA-256 Hash | Description |
| :--- | :--- | :--- |
| `LICENSE` | `bb35f3c533585d6501b3921c42d242e8052d9bec6bb1825d37ecbc56151eaff7` | Bitwise copy of the case study MIT license placed at root for repository license detection. |

#### Category 5: Curated Portfolio Documentation & Verification Scripts (8 Files)

| File Path in Repository | Purpose |
| :--- | :--- |
| `.gitignore` | Comprehensive ignore rules for OS caches, build artifacts, environments, and secrets |
| `README.md` | Master portfolio overview, comparative analysis, and safety notices |
| `assets/portfolio_architecture.svg` | Standalone SVG block diagram illustrating system architecture |
| `case-studies/buck-converter/README.md` | Technical dossier, component audits, and safety blockers for the buck converter |
| `case-studies/buck-converter/scripts/verify_buck_calculations.py` | Standalone Python calculation script verifying buck converter equations |
| `case-studies/opamp-function-generator/README.md` | Technical dossier, stage derivations, and scope analysis for the function generator |
| `case-studies/opamp-function-generator/scripts/verify_analog_calculations.py` | Standalone Python calculation script verifying analog circuit equations |
| `docs/PORTFOLIO_VERIFICATION.md` | This technical verification and engineering limitations report |

### 2.3 Mathematical Summary Reconciliation
$$\begin{aligned}
\text{Preserved Original Historical Files (Category 1)} &= 27 \\
\text{Curated Firmware (Category 2)} &= 1 \\
\text{Rewritten Historical Notes (Category 3)} &= 2 \\
\text{Duplicate Root License (Category 4)} &= 1 \\
\text{Curated Documentation & Scripts (Category 5)} &= 8 \\
\hline
\mathbf{\text{Total Files on Disk in Repository}} &= \mathbf{39\ \text{files}}
\end{aligned}$$

---

## 3. Repository Hygiene & Secret Scan

A recursive scan across the workspace directory confirmed:
* **Virtual Environments (`venv`, `.venv`, `env`):** None detected.
* **Credentials & Secrets (`.env`, `.pem`, tokens):** None detected.
* **Compilation Caches (`__pycache__`, `*.pyc`):** None detected.
* **Hidden VCS / Metadata (`.git`, `.svn`):** None detected inside project working directory.
* **Accidental Local Absolute Paths:** Regex scan confirmed zero absolute machine paths in Markdown documentation.
* **Emojis & Decorative Badges:** Confirmed zero emojis or decorative badges across all curated Markdown files.

---

## 4. Toolchain Availability & Compilation Status

| Engineering Tool | Path / Command | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Python 3.14** | `python.exe` | **Passed** | Successfully executed both verification scripts without dependencies. |
| **Arduino CLI** | `where.exe arduino-cli` | **Not run** | Tool not installed. Timer1 register math verified algebraically against ATmega328P datasheet. |
| **KiCad EDA** | `where.exe kicad-cli` | **Not run** | Tool not installed. Source files contain only exported raster PNG images; no native `.kicad_sch` or `.kicad_pcb` files exist. |
| **LTspice** | `where.exe ltspice` | **Not run** | Tool not installed. Source files contain only exported simulation plots (PNG); no native `.asc` schematic or `.raw` dataset files exist. |

---

## 5. Execution of Independent Verification Scripts

Both verification scripts were executed from the repository root:

### 5.1 Buck Converter Verification Script
```bash
python case-studies/buck-converter/scripts/verify_buck_calculations.py
```
**Exit Code:** `0`  
**Captured Output:**
```
==============================================================================
INDEPENDENT AUDIT & VERIFICATION: DC-DC BUCK CONVERTER (36V -> 18V, 24W)
==============================================================================
[Step 1] Firmware Source Parsing (arduino_pwm.ino):
    - Extracted ICR1 (TOP):          319
    - Extracted OCR1A (Duty Match):  160
    - Fast PWM Mode 14 Configured:   True
    - Non-Inverting OC1A (Pin 9):    True
    - Clock Prescaler = 1 (CS10):    True
    - Derived PWM Frequency:         50000.00 Hz
    - Derived Duty Cycle (D):        0.5000 (50.00%)
    - Derived ON Time (t_on):        10.00 us

[Step 2] Steady-State Conduction & Droop Analysis:
    - Target Operating Point:        36.0V in -> 18.0V out, 1.333A (24.0W)
    - Equivalent Resistive Load:     13.50 Ohm
    - Real Output at Open-Loop D=0.5: 17.17 V
    - Open-Loop Voltage Droop:       0.83 V (4.59%)
    - Required D for Exactly 18.0V:  0.5226 (52.26%)

[Step 3] Inductance & Ripple Current Audit:
    - Critical Inductance for CCM:   67.50 uH (Both inductors operate in CCM)
    - Design PDF Value (680 uH):     Delta_IL = 0.265 A (19.9%), Peak = 1.466 A
    - Hardware Value (390 uH):       Delta_IL = 0.462 A (34.6%), Peak = 1.564 A
    - Discrepancy: Hardware inductor increases current ripple by 74.4%.

[Step 4] Output Capacitor & Voltage Ripple:
    - Designed 100 uF Cap Ripple:    46.32 mV_pp (0.26%)
    - Missing Cap Hardware Reality:  6.23 V_pp (34.6% across load)

[Step 5] Semiconductor Safety & Derating Verification:
    - 1N5819 Reverse Rating:         Vrrm = 40.0 V
    - Operating DC Reverse Voltage:  Vin = 36.0 V
    - Static Voltage Margin:         10.0% (4.0V static margin; standard engineering guidelines recommend >=20% to 30% margin)
    - Diode Average Forward Current: Id(avg) = 0.667 A (Rating: If(avg) = 1.0 A continuous average)
    - Diode Peak Forward Current:    Id(pk) = 1.564 A (Exceeds 1.0A continuous-average threshold; peak/surge limits unverified without exact manufacturer datasheet)
    - Diode Safety Verdict:          UNSAFE FOR 36V ENERGIZATION. 4.0V static reverse margin vulnerable to switching transients.

==============================================================================
BUCK CONVERTER AUDIT COMPLETED: MATHEMATICAL INTEGRITY VERIFIED
==============================================================================
```

### 5.2 Analog Function Generator Verification Script
```bash
python case-studies/opamp-function-generator/scripts/verify_analog_calculations.py
```
**Exit Code:** `0`  
**Captured Output:**
```
==============================================================================
INDEPENDENT AUDIT & VERIFICATION: ANALOG FUNCTION GENERATOR (uA741)
==============================================================================
[Step 1] Dual Regulated Power Supply Stage (+/-12V):
    - Secondary Peak Voltage:        16.97 V
    - Unregulated Peak DC Rail:      15.57 V (Matches ~16.5V simulated in LTspice)
    - 100 Hz Ripple at 100mA:        1000.0 mV_pp
    - LM7812 Dropout Headroom:       0.57 V (Calculated nominal margin at 100mA)
      Note: Calculated positive headroom does not guarantee regulation across load spikes, mains sag, or thermal drift.

[Step 2] Wien Bridge Oscillator Stage:
    - Theoretical (1.5k, 10nF):      10.61 kHz
    - Measured Scope Frequency:      1441.29 Hz (Period = 694.0 us)
    - Derived Effective Tank R:      11.04 kOhm (Matches tuned ~11k pot/resistor branch)
    - Barkhausen Gain Criterion:     Av >= 3.0 requires Rf >= 20.0 kOhm (50k pot installed)
    - Distortion Mechanism:          Mild peak clipping (+/-10.6V saturation) due to absence of AGC.

[Step 3] Comparator Stage (Square Wave):
    - Measured Scope Frequency:      1442.27 Hz
    - Peak-to-Peak Amplitude:        21.6 V_pp
    - uA741 Slew-Rate Transition:    43.2 us (Linear slope visible on 250us/div scope)

[Step 4] Integrator Stage & Ramp Discrepancy Investigation:
    - Driving Square Half-Period:    346.4 us (V_sat = 10.8 V)
    - Nominal Formula at R4=100k:    3.74 V_pp (Theoretical with full-scale 100k)
    - Actual Scope Measurement:      5.84 V_pp
    - Discrepancy Delta:             +2.10 V
    --- TECHNICAL INVESTIGATION FINDINGS ---
    1. Schematic Analysis: R4 is explicitly shown with a trimmer/arrow (Potentiometer).
    2. Mathematical Hypothesis: If R4 was tuned to 64.07 kOhm (~64% of 100k pot),
       the output ramp mathematically evaluates to exactly 5.84 V_pp.
    3. Capacitance Tolerance: If R4 was 100k, a capacitor of 6.41 nF produces 5.84V.
    4. Audit Conclusion: The ~64.1 kOhm potentiometer setting is strictly a MATHEMATICAL HYPOTHESIS.
       Because no independent in-situ multimeter measurement of R4 was recorded in the source,
       this discrepancy cannot be claimed as physically resolved.

==============================================================================
ANALOG FUNCTION GENERATOR AUDIT COMPLETED: MATHEMATICAL INTEGRITY VERIFIED
==============================================================================
```

---

## 6. Technical Safety Audit & Operational Constraints

### 6.1 Buck Converter Safety Evaluation

```
+-------------------------------------------------------------------------------------------------------------------------+
| PARAMETER             | VALUE            | EVIDENCE CATEGORY      | ENGINEERING EVALUATION / PROVENANCE                 |
+-----------------------+------------------+------------------------+-----------------------------------------------------+
| Input Voltage (Vin)   | 36.0 V DC        | Design Target          | Target design bus voltage specified in README/PDF.  |
| Ideal Output (Vout)   | 18.0 V DC        | Calculated Estimate    | Ideal steady-state: Vout = D * Vin = 0.5 * 36V.     |
| Real Output under Load| 17.17 V DC       | Calculated Estimate    | Conduction droop (Vf, Rds_on, Rdcr) = -0.83V.       |
| Output Power (Pout)   | 24.0 W           | Design Target          | Requires 13.5 Ohm power resistor dissipating 24W.   |
| PWM Frequency         | 50.000 kHz       | Calculated from Source | Derived from ICR1=319 in arduino_pwm.ino.           |
| Duty Cycle (D)        | 50.00%           | Calculated from Source | Derived from OCR1A=160 in arduino_pwm.ino.          |
| Control Architecture  | Open-Loop PWM    | Source-Parsed Fact     | Empty loop(); no ADC or closed-loop feedback code.  |
| Active Switch (Q1)    | IRLZ44N (TO-220) | Source-Parsed Fact     | High-side N-channel MOSFET; source on switch node.  |
| Catch Diode (D1)      | 1N5819 (DO-41)   | Source-Parsed Fact     | 40V, 1A rated Schottky diode. INADEQUATE MARGIN.    |
| Inductor (Designed)   | 680 uH           | Source-Parsed Fact     | Calculated in design_calculations.pdf (20% ripple). |
| Inductor (Installed)  | PCV-2-394-05L    | Photographic Evidence  | Visible in hardware photograph (~390 uH, 34.6% rip).|
| Output Capacitor (C1) | 100 uF (Missing) | Photographic Evidence  | Footprint exists in PCB; UNPOPULATED in photograph. |
| Gate Driver IC        | TLP350F          | Source-Parsed Fact     | DIP-8 photocoupler driver; requires isolated Vcc.   |
| Bench Efficiency      | UNVERIFIED       | No Evidence in Source  | Stated "verification in progress". No data exists.  |
| New Bench Measurements| NONE             | Review Fact            | No physical hardware energization conducted.        |
+-------------------------------------------------------------------------------------------------------------------------+
```

#### Detailed Breakdown of Safety Hazards:
1. **Diode Voltage Rating & Margin:**
   - Bus voltage is $36.0\text{ V}$ DC. The 1N5819 diode has a maximum reverse breakdown rating of $V_{RRM} = 40.0\text{ V}$.
   - Static margin is only $4.0\text{ V}$ ($10\%$).
   - Standard power electronics engineering guidelines recommend maintaining $\ge 20\%$ to $30\%$ reverse voltage derating ($\ge 52\text{V}$ rating).
   - In hard-switching operation, stray loop inductance produces voltage spikes that can easily exceed 40V, causing avalanche breakdown.
   - Forward current: average off-time current $I_{D(avg)} = (1 - D) I_{out} = 0.667\text{ A}$ is within the $1.0\text{ A}$ continuous rating, but peak current reaches $\approx 1.564\text{ A}$. Specific peak, repetitive surge, and thermal derating limits are unverified without the exact manufacturer datasheet.
2. **Missing Output Capacitor:**
   - In `hardware/front_view.jpg`, footprint $C_1$ is unpopulated.
   - Without $C_1$, the entire inductor ripple current flows directly through the load resistor, producing an estimated $6.23\text{ V}_{p-p}$ ripple across an $18\text{V}$ nominal output.
3. **Inductor Mismatch & Saturation:**
   - Installed toroid is stamped `PCV-2-394-05L` ($\approx 390\ \mu\text{H}$), whereas calculations assumed $680\ \mu\text{H}$.
   - Current ripple increases from $0.265\text{ A}$ to $0.462\text{ A}$ ($74.4\%$ increase).
   - Core saturation rating under $1.33\text{A}$ DC load is unconfirmed, creating risk of inductance collapse.
4. **High-Side Floating Gate Drive:**
   - The IRLZ44N is arranged in a high-side configuration. When ON, its source rises to $+36\text{V}$.
   - To keep $V_{GS} = 10\text{V}$, the gate must reach $+46\text{V}$ relative to ground.
   - The TLP350 output stage must be referenced to the floating source (Pin 5) and powered by an isolated auxiliary supply. Exceeding the $35\text{V}$ maximum rating or incorrectly referencing ground prevents normal operation or destroys the driver.
5. **Open-Loop Operation:**
   - Fixed 50% PWM without feedback results in an estimated output of $17.17\text{V}$ under full load due to semiconductor and winding resistance drops.

> [!CAUTION]
> **ENERGIZATION PROHIBITION AT 36 V**  
> The current buck converter prototype **MUST NOT BE ENERGIZED AT 36 V**. The design presents critical voltage margin, transient, filtering, gate-drive isolation, and control deficiencies. Upgrading the catch diode alone does not render the circuit safe. All interdependent deficiencies must be remediated before power can be applied.

---

### 6.2 Analog Function Generator Audit

```
+-------------------------------------------------------------------------------------------------------------------------+
| PARAMETER             | VALUE            | EVIDENCE CATEGORY      | ENGINEERING EVALUATION / PROVENANCE                 |
+-----------------------+------------------+------------------------+-----------------------------------------------------+
| AC Mains Supply       | 230V RMS, 50 Hz  | Design Specification   | Stepped down via 12-0-12 center-tapped transformer. |
| Transformer Secondary | 12-0-12 VAC, 1A  | Hardware Specification | Center-tapped step-down transformer.                |
| Unregulated DC Rail   | +/-15.6V nominal | Calculated Estimate    | Peak AC minus bridge drop; simulated in LTspice.   |
| Regulated DC Rails    | +/-12.0 V DC     | Hardware Lab Record    | LM7812 positive and LM7912 negative regulators.     |
| Filter Capacitance    | 1000 uF per rail | Hardware Specification | Ripple estimated at ~1.0 V_pp at 100mA load.        |
| Sine Wave Frequency   | 1.44129 kHz      | Scope Source Record    | Measured on digital oscilloscope at VIT University. |
| Sine Wave Amplitude   | 21.2 V_pp        | Scope Source Record    | Mild rail clipping observed in absence of AGC.      |
| Square Frequency      | 1.44227 kHz      | Scope Source Record    | Synchronized to primary oscillator.                 |
| Square Amplitude      | 21.6 V_pp        | Scope Source Record    | Output swings to approx +/-10.8V with +/-12V rails. |
| Square Slew Rate      | 0.5 V/us (uA741) | Datasheet Spec / Scope | Transition time ~43 us; trapezoidal edges visible.  |
| Triangle Frequency    | 1.44324 kHz      | Scope Source Record    | Synchronized to square wave frequency.              |
| Triangle Ramp (Meas)  | 5.84 V_pp        | Scope Source Record    | Measured on oscilloscope (indicated 58.4V on 10x).  |
| Triangle Ramp (Calc)  | 3.74 V_pp        | Calculated Estimate    | Evaluated at nominal full-scale R4 = 100 kOhm.      |
| Variable Attenuation  | Scaled waveforms | Scope Source Record    | Dual-trace captures demonstrate attenuation.        |
| New Bench Measurements| NONE             | Review Fact            | No physical hardware re-testing performed in audit. |
+-------------------------------------------------------------------------------------------------------------------------+
```

#### Detailed Breakdown of Analog Circuit Nuances:
1. **Mains Safety vs Low-Voltage Rails:**
   - The dual supply is connected to 230V AC mains. The presence of working +/-12V regulator outputs in laboratory records does not verify mains isolation, creepage distance compliance, primary-side fusing, or thermal endurance under prolonged operation.
2. **Regulator Dropout Margin:**
   - Under nominal 12.0V RMS secondary voltage, rectified peak DC is $15.57\text{ V}$.
   - At assumed $100\text{ mA}$ load, $1000\ \mu\text{F}$ filtering yields $\approx 1.0\text{ V}_{p-p}$ ripple, pulling minimum raw voltage to $14.57\text{ V}$.
   - The LM7812 requires $\ge 14.0\text{ V}$ ($2.0\text{ V}$ dropout), leaving $0.57\text{ V}$ nominal headroom.
   - A $-10\%$ mains sag reduces secondary peak to $15.27\text{ V}$, pulling minimum input to $13.27\text{ V} < 14.0\text{ V}$, inducing 100 Hz ripple pass-through.
3. **Wien Bridge Amplitude Stabilization:**
   - The oscillator lacks an automatic gain control (AGC) network. Amplitude stabilization occurs via soft saturation against the $\mu\text{A}741$ power supply rails, producing the peak flattening visible in oscilloscope captures.
4. **Slew-Rate Limiting:**
   - The internal compensation of the $\mu\text{A}741$ limits slew rate to $0.5\text{ V}/\mu\text{s}$. For a $21.6\text{ V}_{p-p}$ square wave, transition takes $43.2\ \mu\text{s}$, giving the square wave trapezoidal slopes.
5. **Integrator Ramp Discrepancy:**
   - Calculated nominal ramp at $R_4 = 100\text{ k}\Omega$ is $3.74\text{ V}_{p-p}$.
   - Measured oscilloscope ramp is $5.84\text{ V}_{p-p}$.
   - Setting $R_4 \approx 64.1\text{ k}\Omega$ (achievable on the marked $100\text{ k}\Omega$ trimming potentiometer) mathematically reconciles the output to $5.84\text{ V}_{p-p}$.
   - In the absence of documented in-situ multimeter measurements, this remains strictly an **unmeasured mathematical hypothesis**.

---

## 7. Verified Facts vs. Outstanding Limitations

### Verified Technical Facts:
1. **PWM Register Mathematics:** ATmega328P Timer1 configuration in `arduino_pwm.ino` mathematically evaluates to an exact $50.000\text{ kHz}$ Fast PWM signal at $50.00\%$ duty cycle on Pin 9.
2. **Cryptographic Inventory:** All 27 historical source files have documented SHA-256 hashes. Curated firmware and rewritten notes have distinct provenance.
3. **Reported Oscilloscope Evidence:** Digital oscilloscope screenshots document generation of sine, square, and triangle waveforms at $\approx 1.44\text{ kHz}$ with variable attenuation stages.
4. **Circuit Dynamics:** Slew-rate equations for the $\mu\text{A}741$ directly explain the trapezoidal square wave transitions.
5. **Hygiene & Standards:** Clean directory structure, zero emojis in curated documentation, zero leaked credentials, and validated relative links.

### Outstanding Limitations & Unverified Items:
1. **No Closed-Loop Buck Control:** Firmware does not sample output voltage or adjust duty cycle.
2. **Missing Bench Power Data for Buck Stage:** No oscilloscope waveforms, thermal images, or efficiency curves exist in the source records for the buck converter.
3. **Buck Converter Hardware Incomplete:** Footprint $C_1$ is unpopulated, diode reverse margin is inadequate, gate drive auxiliary supply is unverified, and inductor saturation margin is unconfirmed.
4. **Integrator Resistance Setting:** The $64.1\text{ k}\Omega$ potentiometer setting is a mathematical hypothesis, not an empirically documented multimeter reading.
5. **Simulation & CAD Native Files:** No native KiCad schematic/layout files or LTspice schematic/data files exist; only exported raster images are present.

---

## 8. Portfolio Readiness Verdicts

| Review Domain | Status | Evidence Basis & Summary |
| :--- | :--- | :--- |
| **1. Public Engineering Portfolio Suitability** | **VERIFIED** | Thorough documentation, preserved original hardware evidence, curated firmware with explicit provenance tracking, reproducible calculation scripts, and transparent technical disclosure. |
| **2. Buck Converter Calculation Verification** | **VERIFIED** | Independent verification of Timer1 50 kHz register math, CCM inductance, conduction droop, ripple, and semiconductor stresses matches formulas and firmware. |
| **3. Buck Converter Energization Readiness** | **BLOCKED** | **CRITICAL MULTI-FACTOR SAFETY BLOCKER.** 1N5819 diode operates with only 4V static margin against 40V breakdown rating; $C_1$ is unpopulated; TLP350 driver lacks an isolated floating supply; inductor saturation margin is unconfirmed; and no closed-loop control exists. Upgrading the diode alone does not resolve all safety risks. **Do not energize at 36V.** |
| **4. Analog Function Generator Calculation & Measurement Verification** | **PARTIALLY VERIFIED** | Lab oscilloscope traces confirm $\pm 12\text{V}$ power rails and $1.44\text{ kHz}$ waveforms. The $64.1\text{ k}\Omega$ setting reconciling the $3.74\text{ V}$ calculation with the $5.84\text{ V}$ scope reading is an unmeasured mathematical hypothesis. |
| **5. Native CAD and Physical Validation Status** | **NOT VERIFIED** | Only raster PNG graphics, calculation PDF, and Arduino firmware were provided in source; no native CAD/EDA project files (`.kicad_sch`, `.kicad_pcb`, `.asc`) exist, and physical bench efficiency / closed-loop validation was not conducted. |
