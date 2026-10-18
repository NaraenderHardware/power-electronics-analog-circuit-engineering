# Power Electronics & Analog Circuit Engineering Portfolio

This repository documents two circuit engineering case studies:
1. **Power Electronics:** [36V to 18V (24W, 50 kHz) DC-DC Buck Converter](case-studies/buck-converter/README.md)
2. **Linear & Analog Circuits:** [Multi-Waveform Analog Function Generator & Regulated Dual Power Supply](case-studies/opamp-function-generator/README.md)

The project includes original design records, circuit schematics, PCB layout exports, Arduino firmware, hardware photographs, exported simulation plots, oscilloscope captures, Python verification scripts, and an audit of circuit limitations and safety considerations.

---

## Portfolio Architecture & Case Studies Overview

```
02_Power_Electronics_and_Analog_Circuit_Engineering/
├── README.md                                  <-- Master portfolio documentation
├── LICENSE                                    <-- MIT open-source license
├── case-studies/
│   ├── buck-converter/                        <-- CASE STUDY 1: Switched-mode power electronics
│   │   ├── README.md                          <-- Comprehensive technical audit & calculations
│   │   ├── HISTORICAL_NOTES.md                <-- Summary of original student records
│   │   ├── code/
│   │   │   ├── arduino_pwm.ino                <-- Curated ATmega328P Timer1 50 kHz PWM firmware
│   │   │   └── arduino_pwm.original.ino       <-- Preserved original firmware (Markdown-wrapped)
│   │   ├── control/                           <-- TLP350 driver pinout & breadboard photos
│   │   ├── docs/design_calculations.pdf       <-- Original design calculation document
│   │   ├── hardware/                          <-- Fabricated PCB front & back photographs
│   │   ├── images/                            <-- Schematics, PCB layout & 3D board rendering
│   │   └── scripts/verify_buck_calculations.py<-- Standalone automated verification script
│   │
│   └── opamp-function-generator/              <-- CASE STUDY 2: Linear & non-linear analog circuits
│       ├── README.md                          <-- Comprehensive technical audit & oscilloscope validation
│       ├── HISTORICAL_NOTES.md                <-- Summary of original student records
│       ├── images/                            <-- Circuit diagrams, block diagrams & scope captures
│       ├── simulation/                        <-- Exported simulation plots & Tinkercad virtual breadboard
│       └── scripts/verify_analog_calculations.py <-- Standalone automated verification script
│
├── docs/
│   └── PORTFOLIO_VERIFICATION.md              <-- Portfolio verification and engineering limitations report
└── assets/                                    <-- System architecture diagram
```

---

## Executive Engineering Comparison

| Engineering Domain | Case Study 1: DC-DC Buck Converter | Case Study 2: Op-Amp Function Generator |
| :--- | :--- | :--- |
| **Circuit Topology** | High-Side N-MOSFET Step-Down Switched Regulator | Multi-Stage Active Analog Waveform Generator |
| **Primary Active Devices** | IRLZ44N Power MOSFET (TO-220), TLP350 Opto-Driver | 5x $\mu\text{A}741$ Operational Amplifiers, LM7812 / LM7912 Regulators |
| **Input Power Source** | $36.0\text{ V}$ DC Bench Supply (Unregulated) | $230\text{ V}_{RMS}$, $50\text{ Hz}$ AC Mains $\to$ 12-0-12 VAC Transformer |
| **Operating Frequency** | **$50.000\text{ kHz}$** (ATmega328P Timer1 Fast PWM) | **$1.441\text{ kHz}$** (Tuned Wien Bridge Resonant Tank) |
| **Output Characteristics**| Target: $18.0\text{ V}$ DC @ $1.33\text{ A}$ ($24\text{ W}$) | Sine ($21.2\text{V}_{pp}$), Square ($21.6\text{V}_{pp}$), Triangle ($5.84\text{V}_{pp}$) |
| **Control Method** | Open-Loop Fixed PWM ($D = 0.50$, no ADC feedback) | Linear Positive/Negative Feedback, Slew-Rate Limited Comparator |
| **Primary Failure Modes**| Diode reverse breakdown, gate-driver ground loops, capacitor ripple | Op-amp rail clipping (no AGC), 741 slew-rate trapezoidal distortion |
| **Physical Status** | Single-sided copper PCB prototype fabricated; $C_1$ unpopulated | Breadboard prototype assembled; characterized via lab digital oscilloscope |

---

## Key Technical Findings & Engineering Audits

### 1. DC-DC Buck Converter (36V to 18V, 24W)
* **PWM Frequency & Duty Cycle Verification:** The ATmega328P Timer1 configuration (`WGM14`, `CS10=1`, `ICR1=319`, `OCR1A=160`) mathematically synthesizes an exact $50.000\text{ kHz}$ PWM signal on Pin 9 (OC1A) with an exact $50.00\%$ duty cycle ($t_{on} = 10.0\ \mu\text{s}$).
* **Conduction Droop & Open-Loop Reality:** Accounting for Schottky forward drop ($0.55\text{V}$), $R_{DS(on)}$ ($0.028\ \Omega$), and inductor winding resistance ($0.40\ \Omega$), the estimated output voltage droops to **$17.17\text{ V}$** at full $1.33\text{ A}$ load (calculated estimate, not physically measured on bench). A duty cycle of $52.26\%$ is mathematically calculated to deliver 18.00V.
* **Catch Diode Voltage Stress:** The 1N5819 Schottky diode operates at $V_{in} = 36\text{V}$ against a $40\text{V}$ reverse rating, leaving only a $10.0\%$ ($4\text{V}$) static margin. While calculated continuous average off-time current is $0.667\text{A}$ (within the $1.0\text{A}$ continuous average rating) and peak current reaches $\approx 1.564\text{A}$, peak/surge limits and thermal derating are unverified without the exact manufacturer datasheet. Theoretical calculations indicate switching transients could reach $43\text{V} - 54\text{V}$ (a calculated estimate, not a measured result), creating high risk of overvoltage breakdown. Upgrading the diode to $\ge 60\text{V}, 3\text{A}$ (e.g., MBR360) is recommended, but diode replacement alone does not render the converter safe.
* **Inductor Value Discrepancy:** Design documents specified $680\ \mu\text{H}$ ($\Delta I_L = 0.265\text{A}$, $19.9\%$ ripple). Physical hardware photograph proves an installed choke labeled `PCV-2-394-05L` ($\approx 390\ \mu\text{H}$), yielding $\Delta I_L = 0.462\text{A}$ ($34.6\%$ ripple).
* **Missing Output Capacitor:** The physical board photograph (`hardware/front_view.jpg`) confirms output filter capacitor $C_1$ was unpopulated during assembly, which exposes the load to full inductor ripple current ($6.23\text{ V}_{p-p}$ calculated estimate).
* **Floating Gate Drive Requirement:** Because the N-MOSFET is placed on the high side, its source rises to 36V when ON. The TLP350 photocoupler driver output stage must be powered from a floating, isolated auxiliary 12V supply referenced to the MOSFET source.

**Detailed case study:** [`case-studies/buck-converter/README.md`](case-studies/buck-converter/README.md)

---

### 2. Op-Amp Function Generator & Regulated Dual Power Supply
* **Dual Linear Power Supply:** 12-0-12 VAC transformer with dual bridge rectifiers and $1000\ \mu\text{F}$ filter capacitors produces an estimated $\pm 15.6\text{ V}$ raw DC. LM7812 and LM7912 regulators output $\pm 12.0\text{ V}$ DC with an estimated $0.57\text{ V}$ nominal dropout headroom under assumed 100mA load. (This calculated nominal headroom does not guarantee ripple-free regulation under negative utility sags, load transients, or capacitor degradation).
* **Wien Bridge Sine Wave Generation:** Measured frequency on laboratory digital storage oscilloscope is **$1.44129\text{ kHz}$** ($T = 694.0\ \mu\text{s}$), corresponding to $R_{eff} = 11.04\text{ k}\Omega, C = 10\text{ nF}$. Barkhausen condition ($A_v \ge 3$) is tuned using a $50\text{ k}\Omega$ feedback potentiometer. Waveform exhibits slight peak flattening due to op-amp rail saturation in the absence of AGC.
* **Comparator Stage & $\mu\text{A}741$ Slew-Rate Limiting:** Zero-crossing comparator converts the sine wave to a $21.6\text{ V}_{p-p}$ square wave ($1.442\text{ kHz}$). The $0.5\text{ V}/\mu\text{s}$ slew rate of the $\mu\text{A}741$ imposes a $43.2\ \mu\text{s}$ transition time, producing clearly visible trapezoidal slopes.
* **Miller Integrator Stage:** Converts the square wave into a symmetric $5.84\text{ V}_{p-p}$ triangular wave ($1.443\text{ kHz}$) with a $1\text{ M}\Omega$ parallel feedback resistor preventing DC saturation drift. Nominal formula at $R_4=100\text{ k}\Omega$ calculates $3.74\text{ V}_{p-p}$; a tuned wiper setting of $R_4 \approx 64.1\text{ k}\Omega$ mathematically yields $5.84\text{ V}_{p-p}$, but is cataloged strictly as an unmeasured mathematical hypothesis.
* **Variable Output Attenuation:** Dual-channel oscilloscope measurements verify successful variable de-amplification across all three waveforms.

**Detailed case study:** [`case-studies/opamp-function-generator/README.md`](case-studies/opamp-function-generator/README.md)

---

## Automated Verification & Reproducibility

Two self-contained Python scripts are provided to verify all governing equations and electrical deratings without third-party dependencies:

```bash
# 1. Run Buck Converter mathematical audit
python case-studies/buck-converter/scripts/verify_buck_calculations.py

# 2. Run Analog Function Generator mathematical audit
python case-studies/opamp-function-generator/scripts/verify_analog_calculations.py
```

---

## Verification Summary

An audit of the calculations, firmware, and physical hardware records yields the following status across the five project areas:

| Verification Category | Verdict | Core Finding & Safety Status |
| :--- | :--- | :--- |
| **1. Public Engineering Portfolio Suitability** | **VERIFIED** | Thorough documentation, preserved original hardware evidence, curated firmware with explicit provenance tracking, reproducible calculation scripts, and transparent technical disclosure. |
| **2. Buck Converter Calculation Verification** | **VERIFIED** | Independent verification of Timer1 50 kHz register math, CCM inductance, conduction droop, ripple, and semiconductor stresses matches formulas and firmware. |
| **3. Buck Converter Energization Readiness** | **BLOCKED** | **CRITICAL MULTI-FACTOR SAFETY BLOCKER.** 1N5819 diode operates with only 4V static margin against 40V breakdown rating; $C_1$ is unpopulated; TLP350 driver lacks an isolated floating supply; inductor saturation margin is unconfirmed; and no closed-loop control exists. Upgrading the diode alone does not resolve all safety risks. **Do not energize at 36V.** |
| **4. Analog Function Generator Calculation & Measurement Verification** | **PARTIALLY VERIFIED** | Lab oscilloscope traces confirm $\pm 12\text{V}$ power rails and $1.44\text{ kHz}$ waveforms. The $64.1\text{ k}\Omega$ setting reconciling the $3.74\text{ V}$ calculation with the $5.84\text{ V}$ scope reading is an unmeasured mathematical hypothesis. |
| **5. Native CAD and Physical Validation Status** | **NOT VERIFIED** | Only raster PNG graphics, calculation PDF, and Arduino firmware were provided in source; no native CAD/EDA project files (`.kicad_sch`, `.kicad_pcb`, `.asc`) exist, and physical bench efficiency / closed-loop validation was not conducted. |

For the complete itemized audit matrix, component stress evaluations, toolchain analysis, and explicit declarations of verified vs. unverified physical claims:

**Verification report:** [`docs/PORTFOLIO_VERIFICATION.md`](docs/PORTFOLIO_VERIFICATION.md)

---

## Engineering Notices & Safety Warnings

> [!CAUTION]
> **POWER ELECTRONICS ENERGIZATION PROHIBITION (36V BUCK CONVERTER)**  
> The 36V to 18V Buck Converter documented herein is an experimental laboratory prototype. Because of critical semiconductor voltage limitations (1N5819 40V rating on a 36V bus leaving only 4V static margin), un-snubbed switching transients, floating gate-driver ground reference requirements, inductor core saturation risks under 1.33A DC load, and the unpopulated output capacitor on the physical prototype, **this power stage must NOT be energized at 36V. Diode upgrade alone is insufficient; all interdependent safety remediations must be implemented and verified before bench power is applied.**

> [!WARNING]
> **MAINS VOLTAGE SAFETY NOTICE (DUAL POWER SUPPLY)**  
> The dual linear power supply utilizes an open 230V AC mains transformer. The presence of operational DC regulator outputs or waveform oscilloscope captures does not independently establish electrical safety, enclosure isolation, creepage distances, or primary fusing. Proper mains isolation and protective earthing are mandatory for physical construction.
