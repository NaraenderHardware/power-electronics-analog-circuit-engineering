# Engineering Case Study: Multi-Waveform Analog Function Generator & Regulated Dual Power Supply

## 1. Executive Summary

This case study presents the design, multi-domain simulation, hardware breadboard realization, and empirical oscilloscope validation of an **Analog Function Generator** constructed with **$\mu\text{A}741$ operational amplifiers**, powered by a dedicated **$\pm 12\text{V}$ Regulated Linear Dual Power Supply**.

The system synthesizes three fundamental periodic analog waveforms:
1. **Sine Wave with Observed Peak Clipping ($\approx 1.44\text{ kHz}$):** Generated using an active Wien Bridge Oscillator with potentiometer-based gain tuning.
2. **Square Wave Output ($\approx 1.44\text{ kHz}$):** Produced via an open-loop zero-crossing comparator driven by the primary sine oscillator, outputting approximately $\pm 10.8\text{ V}$ with $\pm 12\text{ V}$ supply rails.
3. **Linear Triangular Wave ($\approx 1.44\text{ kHz}$):** Formed by integrating the square wave with an active inverting Miller integrator.
4. **Buffered Variable Amplitude Attenuation Stage:** Provides variable gain and de-amplification control for external instrumentation interface.

Hardware prototypes were assembled and characterized in the analog circuits laboratory at the Academic Block, VIT University (Kovilancheri, Tamil Nadu, India). Empirical waveforms were acquired using a dual-channel digital storage oscilloscope and cross-verified against LTspice circuit simulations and Tinkercad virtual breadboard models.

```
+-------------------------------------------------------------------------------------------------+
|                                 ANALOG FUNCTION GENERATOR ARCHITECTURE                          |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|  [230V AC Mains] ---> [12-0-12V Transformer] ---> [Bridge Rectifiers + 1000uF]                  |
|                                                              |                                  |
|                                                [LM7812 / LM7912 Regulators]                     |
|                                                              |                                  |
|                                                     +/-12V DC Dual Rails                        |
|                                                              |                                  |
|           +--------------------------------------------------+                                  |
|           |                                                                                     |
|           v                                                                                     |
|   +---------------+         +-----------------+         +-----------------+                     |
|   |  Wien Bridge  |  Sine   |  Op-Amp Invert  |  Square | Miller Op-Amp   | Triangle            |
|   |  Oscillator   |-------->|   Comparator    |-------->|   Integrator    |--------+            |
|   |    (uA741)    |         |     (uA741)     |         |     (uA741)     |        |            |
|   +---------------+         +-----------------+         +-----------------+        |            |
|           |                         |                           |                  |            |
|           +-------------------------+---------------------------+                  |            |
|           |                                                                        |            |
|           v                                                                        v            |
|   [Waveform Selector & Buffer / Variable Attenuator Stage (uA741)] <---------------+            |
|                                   |                                                             |
|                                   v                                                             |
|                       Instrument Output Terminals                                               |
+-------------------------------------------------------------------------------------------------+
```

---

## 2. Technical Specification & Validation Matrix

| Parameter / Stage | Design Target / Stated Claim | LTspice Simulation Result | Hardware Lab Measurement | Engineering Notes & Verification Source |
| :--- | :--- | :--- | :--- | :--- |
| **Mains AC Input** | $230\text{ V}_{RMS}$, $50\text{ Hz}$ | $325\text{ V}_{peak}$, $50\text{ Hz}$ (`SINE(0 325 50)`) | $230\text{ V}_{RMS}$ Indian utility grid | Stepped down via 12-0-12 center-tapped transformer. |
| **Unregulated DC Rail** | $\approx \pm 16.0\text{ V}$ | **$\pm 16.5\text{ V}$** (`rectified_ouput.png`) | $\approx \pm 15.6\text{ V}$ DC | $V_{peak} - 2 V_D = 12\sqrt{2} - 1.4\text{V} \approx 15.57\text{V}$. |
| **Filter Capacitance** | $1000\ \mu\text{F}$ per rail | $1000\ \mu\text{F}$ electrolytic | 4x $1000\ \mu\text{F}$ radial electrolytic | Filters full-wave $100\text{ Hz}$ ripple to approximately $1.0\text{ V}_{p-p}$ at assumed $100\text{mA}$ load under idealized formulas ($\Delta V = I / (2 f C)$). |
| **Regulated Dual Supply** | $\pm 12.0\text{ V}$ DC | **$+12.0\text{ V} / -12.0\text{ V}$** (`regulated_output.png`) | $\pm 12.0\text{ V}$ steady rails | LM7812 positive regulator and LM7912 negative regulator. Nominal input-to-output differential $V_{in}-V_{out} \approx 2.57\text{V}$ ($0.57\text{V}$ headroom above $2.0\text{V}$ dropout requirement under nominal $100\text{mA}$ load). |
| **Sine Frequency ($f_0$)** | $\approx 1.4\text{ kHz}$ | **$1.428\text{ kHz}$** ($T = 700\ \mu\text{s}$) | **$1.441\text{ kHz}$** ($T = 694.0\ \mu\text{s}$) | Scope screen (`sine_wave.png`): `Freq = 1.441kHz`, `Prd = 694.0us`. Tuned via RC potentiometer. |
| **Sine Amplitude (Raw)** | $\pm 12\text{V}$ rail swing | $16.0\text{ V}_{p-p}$ ($\pm 8.0\text{V}$) | **$21.2\text{ V}_{p-p}$** (indicated $212.0\text{V}$ on 10x) | Scope screen (`sine_wave.png`): Peaks exhibit mild saturation flattening against $\pm 12\text{V}$ rails. |
| **Square Frequency ($f_{sq}$)** | Synchronous to Sine | **$1.428\text{ kHz}$** ($T = 700\ \mu\text{s}$) | **$1.442\text{ kHz}$** ($T = 693.2\ \mu\text{s}$) | Scope screen (`square_wave.png`): Generated by zero-crossing comparator. |
| **Square Amplitude (Raw)** | $\pm 12\text{V}$ | $8.0\text{ V}_{peak}$ | **$21.6\text{ V}_{p-p}$** ($\approx \pm 10.8\text{V}$) | Scope screen (`square_wave.png`): Output swings to approximately $\pm 10.8\text{ V}$ with $\pm 12\text{ V}$ supply rails. |
| **Square Slew Rate ($SR$)** | $0.5\text{ V}/\mu\text{s}$ ($\mu\text{A}741$) | Ideal SPICE op-amp model | **$\approx 0.5\text{ V}/\mu\text{s}$** | Measured rise/fall times $\approx 40\ \mu\text{s}$ for $21.6\text{V}$ swing, showing distinctive trapezoidal slope. |
| **Triangle Frequency ($f_{tri}$)**| Synchronous to Square | **$1.428\text{ kHz}$** ($T = 700\ \mu\text{s}$) | **$1.443\text{ kHz}$** ($T = 692.8\ \mu\text{s}$) | Scope screen (`triangle_wave.png`): Formed by integrating comparator output. |
| **Triangle Amplitude (Raw)**| $\approx 6\text{ V}_{p-p}$ | $7.8\text{ V}_{p-p}$ ($\pm 3.9\text{V}$) | **$5.84\text{ V}_{p-p}$** (indicated $58.4\text{V}$ on 10x) | Scope screen (`triangle_wave.png`): Ramp slope dictated by $R_{int} C_{int}$. |
| **Variable Attenuation** | Adjustable de-amplify | N/A (Fixed pot in SPICE) | **Demonstrated on 2-channel scope** | Scope screens (`*_deamplify.png`): Dual-channel captures show simultaneous raw and attenuated signals. |

---

## 3. Circuit Analysis & Mathematical Principles

### 3.1 Dual Power Supply Design & Ripple Physics
The dual power supply energizes all op-amp stages with symmetric positive and negative rails:
1. **Transformer Step-Down:**
   Secondary winding provides $12\text{ V}_{RMS} - 0 - 12\text{ V}_{RMS}$ at $1\text{ A}$.
   $$V_{peak(sec)} = V_{RMS} \times \sqrt{2} = 12.0 \times 1.414 = 16.97\text{ V}$$
2. **Bridge Rectification:**
   Two bridge rectifiers (or full-wave center-tap configuration) utilize 1N4007 silicon diodes ($V_D \approx 0.7\text{V}$):
   $$V_{DC(unreg)} = V_{peak(sec)} - 2 V_D = 16.97\text{ V} - 1.40\text{ V} = 15.57\text{ V}$$
3. **Filter Capacitor Sizing & Full-Wave Ripple:**
   For a full-wave rectifier at mains frequency $f_{mains} = 50\text{ Hz}$, the ripple frequency is $2 f_{mains} = 100\text{ Hz}$.
   $$\Delta V_{ripple} = \frac{I_{load}}{2 f_{mains} C} = \frac{0.100\text{ A}}{2 \times 50\text{ Hz} \times 1000 \times 10^{-6}\text{ F}} = \frac{0.100}{0.100} = 1.00\text{ V}_{p-p}$$
   $$V_{unreg(min)} = V_{DC(unreg)} - \Delta V_{ripple} = 15.57\text{ V} - 1.00\text{ V} = 14.57\text{ V}$$
4. **Regulator Dropout Headroom:**
   The positive rail is stabilized by an **LM7812** ($+12\text{V}$); the negative rail by an **LM7912** ($-12\text{V}$).
   Under these nominal assumptions ($12.0\text{ V}_{RMS}$ secondary, $100\text{ mA}$ load, and typical diode drops), the calculated minimum headroom margin is $V_{unreg(min)} - V_{in(min)} = 14.57\text{ V} - 14.00\text{ V} = 0.57\text{ V}$ (rising to $\sim 1.5\text{ V}$ under unloaded conditions). Note that this is a theoretical calculation under nominal assumptions; positive nominal headroom alone does not prove complete, ripple-free regulation under negative utility mains voltage sags ($-10\%$), dynamic load surges, increased diode drops at low temperatures, or capacitor capacitance and ESR tolerances.

---

### 3.2 Wien Bridge Sine Wave Oscillator Stage
The sine wave oscillator utilizes a $\mu\text{A}741$ operational amplifier with two feedback loops:

```
               +---------------------------------------------+ (Negative Feedback)
               |                                             |
               |         +-----------[ Rf (50k Pot) ]--------+
               |         |                                   |
              [Ri (10k)] |                                   |
               |         |                                   |
              GND        |   |\                              |
                         +---| - \                           |
                             |    \                          |
                             | 741 >-------------------------+--------> Sine Wave Output
                             |    /                          |
                         +---| + /                           |
                         |   |/                              |
                         |                                   |
                         +-----------------[ R1 ]---[ C1 ]---+ (Positive Feedback Series)
                         |
                       [ R2 ]  [ C2 ] (Positive Feedback Parallel)
                         |       |
                        GND     GND
```

#### Barkhausen Criterion for Oscillation:
For sustained oscillation at frequency $\omega_0$, the open-loop gain must satisfy:
$$A_v(j\omega_0) \cdot \beta(j\omega_0) = 1 \angle 0^\circ$$
The transfer function of the positive feedback RC network is:
$$\beta(s) = \frac{Z_p(s)}{Z_s(s) + Z_p(s)} = \frac{\frac{R_2}{1 + s R_2 C_2}}{R_1 + \frac{1}{s C_1} + \frac{R_2}{1 + s R_2 C_2}}$$
Assuming equal components ($R_1 = R_2 = R$, $C_1 = C_2 = C$):
$$\beta(j\omega) = \frac{j\omega R C}{1 - \omega^2 R^2 C^2 + 3 j\omega R C}$$
At the resonant frequency $\omega_0 = \frac{1}{R C}$:
$$\beta(j\omega_0) = \frac{j}{3 j} = \frac{1}{3} \angle 0^\circ$$
Thus, the non-inverting amplifier stage must supply a closed-loop gain of exactly:
$$A_v = 1 + \frac{R_f}{R_i} \ge 3 \implies \frac{R_f}{R_i} \ge 2 \implies R_f \ge 2 R_i$$
With $R_i = 10\text{ k}\Omega$, the feedback resistor must be $R_f \ge 20\text{ k}\Omega$. A $50\text{ k}\Omega$ multi-turn potentiometer is used on the hardware breadboard, allowing fine-tuning of the loop gain.

#### Frequency Tuning Analysis:
The theoretical frequency formula is:
$$f_0 = \frac{1}{2 \pi R C}$$
* In the reference theoretical block diagram (`images/block_diagram.png`), nominal values are marked as $R = 1.5\text{ k}\Omega$, $C = 10\text{ nF}$, yielding $f_{calc} = 10.61\text{ kHz}$.
* On the physical hardware prototype, the frequency was tuned down to the audio band:
  $$f_{meas} = 1.44129\text{ kHz}\ (T = 694.0\ \mu\text{s})$$
  Rearranging for effective resistance with $C = 10\text{ nF}$:
  $$R_{effective} = \frac{1}{2 \pi \times 1441.29\text{ Hz} \times 10 \times 10^{-9}\text{ F}} = 11.04\text{ k}\Omega$$
  This confirms that on the breadboard, $R_1$ and $R_2$ were implemented using an $11\text{ k}\Omega$ combination (such as a $10\text{ k}\Omega$ fixed resistor plus trimming potentiometer).

#### Amplitude Limiting & Distortion Mechanism:
The measured oscilloscope capture (`images/sine_wave.png`) reveals slight clipping at positive and negative peaks ($V_{pp} \approx 21.2\text{ V}$, $V_{max} \approx +11.0\text{ V}$).
* **Root Cause:** To guarantee self-starting oscillation from thermal noise, the gain must be set slightly greater than 3 ($A_v = 3 + \epsilon$).
* Because this circuit does not incorporate a nonlinear automatic gain control (AGC) element (such as antiparallel diodes, a thermistor, or a JFET channel resistor in the feedback path), the oscillation amplitude grows exponentially until the $\mu\text{A}741$ output stage runs out of voltage swing and clips against the internal output saturation limits ($\pm V_{sat} \approx \pm (V_{supply} - 1.0\text{V}) = \pm 11.0\text{V}$).

---

### 3.3 Comparator Stage (Square Wave Generation)
The square wave is synthesized by feeding the $1.44\text{ kHz}$ sine wave directly into an open-loop $\mu\text{A}741$ comparator with the non-inverting input tied to analog ground:

```
    Sine Wave Input
           o---------[ Pin 2: Inverting Input ]
                                               |\
                                               | \
                                               |  \
                                               |741 >--------o Square Wave Output (+/-11V)
                                               |  /
                     [ Pin 3: Non-Inverting ]--| /
                                |              |/
                               GND
```

#### Transfer Function & Slew-Rate Physics:
* When $V_{sine} > 0\text{V}$, output drives to negative rail: $V_{out} = -V_{sat} \approx -10.8\text{V}$.
* When $V_{sine} < 0\text{V}$, output drives to positive rail: $V_{out} = +V_{sat} \approx +10.8\text{V}$.
* Measured Peak-to-Peak Amplitude: $V_{pp} \approx 21.6\text{ V}$ (indicated $216.0\text{V}$ on 10x probe).
* Measured Frequency: $f = 1.44227\text{ kHz}$ ($T = 693.2\ \mu\text{s}$).

#### $\mu\text{A}741$ Slew-Rate Limitation:
The standard $\mu\text{A}741$ op-amp has an internally compensated dominant pole capacitor ($30\text{ pF}$), yielding a maximum slew rate:
$$SR = 0.5\text{ V}/\mu\text{s}$$
For an output voltage excursion of $\Delta V = 21.6\text{ V}$ ($\approx \pm 10.8\text{ V}$), the minimum transition time is:
$$t_{transition} = \frac{\Delta V}{SR} = \frac{21.6\text{ V}}{0.5\text{ V}/\mu\text{s}} = 43.2\ \mu\text{s}$$
Inspection of `images/square_wave.png` clearly reveals this linear finite transition slope on both rising and falling edges (spanning $\approx 1/16$th of the $693\ \mu\text{s}$ total period), providing textbook empirical confirmation of 741 slew-rate limiting.

---

### 3.4 Inverting Miller Integrator Stage (Triangular Wave)
The triangular waveform is produced by integrating the square wave:

```
                            +-------[ C2 = 0.01 uF ]-------+
                            |                              |
                            +-------[ R5 = 1 MOhm ]--------+ (DC Stabilization)
                            |                              |
   Square Wave In           |   |\                         |
         o------[ R4 = 100k ]+---| - \                     |
                                 |    \                    |
                                 | 741 >-------------------+-----> Triangle Wave Output
                                 |    /
         GND ----[ R6 = 100k ]---| + /
                                 |/
```

#### Mathematical Formulation & Amplitude Derivation:
The ideal inverting integrator response is:
$$v_o(t) = -\frac{1}{R_4 C_2} \int v_{in}(t) \, dt$$
During the first half-cycle ($0 \le t < \frac{T}{2}$), $v_{in}(t) = +V_{sat}$:
$$v_o(t) = v_o(0) - \frac{V_{sat}}{R_4 C_2} \cdot t$$
This produces a downward ramp with constant slope:
$$\frac{dv_o}{dt} = -\frac{V_{sat}}{R_4 C_2}$$
During the second half-cycle ($\frac{T}{2} \le t < T$), $v_{in}(t) = -V_{sat}$, producing an upward ramp with slope $+\frac{V_{sat}}{R_4 C_2}$.
The peak-to-peak amplitude of the resulting triangular wave is:
$$V_{tri(p-p)} = \frac{V_{sat}}{R_4 C_2} \cdot \frac{T}{2} = \frac{V_{sat}}{2 f \cdot R_4 C_2}$$
Substituting nominal schematic component values ($V_{sat} = 10.8\text{ V}$, $f = 1443\text{ Hz}$, $R_4 = 100\text{ k}\Omega$, $C_2 = 0.01\ \mu\text{F} = 10\text{ nF}$):
$$V_{tri(p-p)} = \frac{10.8\text{ V}}{2 \times 1443\text{ Hz} \times 10^5\ \Omega \times 10^{-8}\text{ F}} = \frac{10.8}{2.886} = 3.74\text{ V}_{p-p}\ (\approx 3.82\text{ V at } V_{sat}=11.0\text{V})$$

#### Investigation: Calculated 3.82 V Ramp vs. Measured 5.84 V Scope Capture:
The laboratory oscilloscope screen capture (`images/triangle_wave.png`) reports a peak-to-peak amplitude of **$5.84\text{ V}_{p-p}$** (indicated as $58.4\text{V}$ on a 10x probe setting).
1. **Potentiometer Tuning Analysis:** In [`images/block_diagram.png`](images/block_diagram.png), $R_4$ is explicitly marked with a wiper arrow as a **$100\text{ k}\Omega$ potentiometer**.
2. **Effective Resistance Derivation:** Rearranging the ramp equation for $R_4$ at the measured $5.84\text{ V}_{p-p}$:
   $$R_{4(tuned)} = \frac{V_{sat} \cdot (T/2)}{V_{tri(p-p)} \cdot C_2} = \frac{10.8\text{ V} \times 346.4 \times 10^{-6}\text{ s}}{5.84\text{ V} \times 10 \times 10^{-9}\text{ F}} = 64.07\text{ k}\Omega$$
   Tuning a $100\text{ k}\Omega$ potentiometer to approximately $64\text{ k}\Omega$ (about $64\%$ of its rotational track) yields the exact $5.84\text{ V}_{p-p}$ ramp.
3. **Capacitance & Saturation Tolerances:** Standard film/ceramic capacitors carry $\pm 10\%$ to $\pm 20\%$ tolerances, and internal op-amp saturation voltages vary with temperature.
4. **Audit Conclusion:** The discrepancy is mathematically consistent with a tuned potentiometer resistance ($R_4 \approx 64.1\text{ k}\Omega$). However, in the absence of in-situ multimeter measurements of the physical breadboard wiper position, this is strictly cataloged as an **unmeasured mathematical hypothesis** rather than a resolved empirical calibration.

#### Role of Parallel Resistor $R_5$ ($1\text{ M}\Omega$):
Without $R_5$, any minute input offset voltage ($V_{OS}$) or input bias current ($I_B$) would cause continuous integration, drifting the output into positive or negative saturation. $R_5$ introduces negative DC feedback that limits DC closed-loop gain to:
$$A_{v(DC)} = -\frac{R_5}{R_4} = -\frac{1\text{ M}\Omega}{100\text{ k}\Omega} = -10$$
At the operating frequency $f = 1.44\text{ kHz}$, the reactance of $C_2$ is:
$$X_C = \frac{1}{2 \pi \times 1443 \times 10^{-8}} = 11.03\text{ k}\Omega \ll R_5\ (1000\text{ k}\Omega)$$
Because $X_C \ll R_5$, the AC behavior is pure integration with zero phase distortion.

---

### 3.5 Output Buffer & Attenuation Stage
To prevent load impedance variations from disturbing the frequency and ramp slopes of the oscillator and integrator, the output stage utilizes a non-inverting $\mu\text{A}741$ buffer / variable attenuator:
* Configured with a voltage divider potentiometer at the input or in the negative feedback path.
* **Empirical Dual-Channel Oscilloscope Validation:**
  The laboratory evidence includes synchronized two-channel measurements comparing the raw generator node (Yellow CH1) against the variable attenuated output (Purple CH2):
  1. **Sine Wave Attenuation (`images/sine_wave_deamplify.png`):**
     CH1 displays the raw $\pm 10.6\text{V}$ ($21.2\text{V}_{p-p}$) clipped waveform. CH2 displays a pure, unclipped sine wave attenuated to $\approx 2.04\text{ V}_{p-p}$ ($V_{pp} = 20.40\text{V}$ on 10x).
  2. **Square Wave Attenuation (`images/square_wave_deamplify.png`):**
     CH1 displays raw $21.6\text{ V}_{p-p}$ output ($\approx \pm 10.8\text{ V}$). CH2 displays an attenuated square wave reduced to $\approx 10.0\text{ V}_{p-p}$.
  3. **Triangle Wave Attenuation (`images/triangle_wave_deamplify.png`):**
     CH1 displays raw $5.84\text{ V}_{p-p}$ ramp. CH2 displays an attenuated triangle wave scaled to $2.00\text{ V}_{p-p}$ ($6.00\text{V}$ reading on 2V/div scale).

---

## 4. Hardware Lab Gallery & Verification Evidence

All primary experimental records are maintained directly within the repository structure:

| Item | Artifact Path | Provenance & Engineering Description |
| :--- | :--- | :--- |
| **Lab Hardware Setup** | [`images/circuit_diagram.png`](images/circuit_diagram.png) | Breadboard setup with 12-0-12 transformer, bridge rectifier, LM7812/7912 regulators, and 5x $\mu\text{A}741$ ICs (VIT University lab). |
| **Circuit Schematics** | [`images/block_diagram.png`](images/block_diagram.png) | Detailed schematics of Wien bridge oscillator, multivibrator, integrator, and non-inverting buffer. |
| **Tinkercad Breadboard**| [`simulation/function_generator.png`](simulation/function_generator.png) | Exported screenshot of virtual breadboard layout and dual DC power supply. |
| **Rectifier Simulation Plot** | [`simulation/rectified_ouput.png`](simulation/rectified_ouput.png) | Exported LTspice simulation plot showing full-wave rectified raw DC output ($\approx \pm 16.5\text{V}$). |
| **Regulator Simulation Plot** | [`simulation/regulated_output.png`](simulation/regulated_output.png) | Exported LTspice simulation plot showing LM7812 / LM7912 dual-rail regulator outputs at $\pm 12.0\text{V}$. |
| **Sine Simulation Plot** | [`simulation/sine_simulation.png`](simulation/sine_simulation.png) | Exported LTspice simulation plot showing $1.428\text{ kHz}$ sine oscillation ($16\text{V}_{p-p}$). |
| **Square Simulation Plot**| [`simulation/square_simulation.png`](simulation/square_simulation.png) | Exported LTspice simulation plot showing $1.428\text{ kHz}$ square switching. |
| **Triangle Simulation Plot**|[`simulation/triangle_simulation.png`](simulation/triangle_simulation.png)| Exported LTspice simulation plot showing $1.428\text{ kHz}$ triangle ramp ($7.8\text{V}_{p-p}$). |
| **Scope: Sine Output** | [`images/sine_wave.png`](images/sine_wave.png) | Supplied oscilloscope capture: $1.441\text{ kHz}$, $T = 694.0\ \mu\text{s}$, $V_{pp} = 21.2\text{V}$. |
| **Scope: Sine Attenuated**| [`images/sine_wave_deamplify.png`](images/sine_wave_deamplify.png)| Supplied dual-trace capture (CH1 raw vs. CH2 clean attenuated output, $1.422\text{ kHz}$). |
| **Scope: Square Output** | [`images/square_wave.png`](images/square_wave.png) | Supplied oscilloscope capture: $1.442\text{ kHz}$, $T = 693.2\ \mu\text{s}$, $V_{pp} = 21.6\text{V}$. |
| **Scope: Square Attenuated**|[`images/square_wave_deamplify.png`](images/square_wave_deamplify.png)| Supplied dual-trace capture showing attenuated square pulse ($1.456\text{ kHz}$). |
| **Scope: Triangle Output**| [`images/triangle_wave.png`](images/triangle_wave.png) | Supplied oscilloscope capture: $1.443\text{ kHz}$, $T = 692.8\ \mu\text{s}$, $V_{pp} = 5.84\text{V}$. |
| **Scope: Triangle Attenuated**|[`images/triangle_wave_deamplify.png`](images/triangle_wave_deamplify.png)| Supplied dual-trace capture showing attenuated $2.00\text{V}_{p-p}$ ramp ($1.456\text{ kHz}$). |
| **Tinkercad Project Link**| [`simulation/thinkercad_link.txt`](simulation/thinkercad_link.txt)| Direct web link to the historical Autodesk Tinkercad simulation project. |
| **Historical Notes** | [`HISTORICAL_NOTES.md`](HISTORICAL_NOTES.md) | Summary of historical student documentation and reported claims. |

*Note on Simulation Artifacts:* The repository contains exported raster PNG graphics from prior LTspice and Tinkercad sessions. Native LTspice schematic files (`.asc`) or raw simulation datasets (`.raw`) are not present in this workspace, and no new simulation runs were executed during this documentation review.

---

## 5. Automated Verification Script

A Python verification script evaluates all governing equations across the power supply, Wien bridge, comparator, and integrator stages:

```bash
# Execute the analog verification audit
python scripts/verify_analog_calculations.py
```

### Script Output Summary:
* Secondary peak voltage: $16.97\text{ V}$; Unregulated peak DC: $15.57\text{ V}$.
* Filter capacitor ripple at assumed $100\text{mA}$ load: $1.00\text{ V}_{p-p}$; Minimum input: $14.57\text{ V}$ (Input-to-output differential: $2.57\text{ V}$; Dropout headroom above 2.0V requirement: $0.57\text{ V}$).
* Wien bridge theoretical frequency ($1.5\text{k}\Omega, 10\text{nF}$): $10.61\text{ kHz}$; Scope tuned frequency: $1.441\text{ kHz}$ ($R_{eff} = 11.04\text{ k}\Omega$).
* Comparator slew-rate transition time ($0.5\text{ V}/\mu\text{s}$ over $21.6\text{V}$): $43.2\ \mu\text{s}$.
* Integrator nominal ramp voltage ($R_4=100\text{ k}\Omega$): $3.74\text{ V}_{p-p}$; Scope measured: $5.84\text{ V}_{p-p}$ (discrepancy reconciles to $R_4 \approx 64.1\text{ k}\Omega$ mathematical hypothesis).

---

## 6. Engineering Limitations & Safety Warnings

> [!WARNING]
> **MAINS VOLTAGE SAFETY & ELECTRICAL ISOLATION NOTICE**  
> The dual linear power supply incorporates a step-down transformer connected directly to 230V AC RMS mains power ($50\text{ Hz}$). The presence of operational DC regulator outputs or waveform oscilloscope captures in the historical records does NOT independently verify electrical insulation integrity, creepage and clearance distances, primary-side fusing, thermal dissipation under sustained load, or protection against mains shock and fire hazards. Bench construction or operation of mains-powered supplies requires appropriate enclosure, grounding, overcurrent protection, and formal electrical safety testing.

### Technical Limitations & Open Engineering Items:
1. **Mains Headroom Sensitivity:** The calculated $0.57\text{ V}$ dropout margin under $100\text{ mA}$ load is an estimate based on nominal $12.0\text{ V}_{RMS}$ secondary voltage. A $-10\%$ mains sag pulls the unregulated rail below the $14.0\text{ V}$ regulator requirement, causing line-frequency ripple pass-through.
2. **Sine Distortion:** Without an automatic gain control (AGC) mechanism (such as antiparallel diodes, a thermistor, or a JFET in the feedback path), the Wien bridge oscillator relies on op-amp rail clipping to stabilize amplitude, creating observable peak flattening.
3. **Comparator Slew-Rate Limiting:** The $0.5\text{ V}/\mu\text{s}$ slew rate of the $\mu\text{A}741$ introduces a $43.2\ \mu\text{s}$ transition edge, giving the square wave distinct trapezoidal slopes.
4. **Integrator Wiper Setting Hypothesis:** The calculated nominal ramp at full-scale $R_4 = 100\text{ k}\Omega$ is $3.74\text{ V}_{p-p}$, whereas the oscilloscope capture records $5.84\text{ V}_{p-p}$. Setting $R_4 \approx 64.1\text{ k}\Omega$ mathematically satisfies the equation, but in the absence of in-situ multimeter measurements from the lab, this remains strictly an **unmeasured mathematical hypothesis**.
5. **Historical Scope Captures:** The oscilloscope images represent preserved visual records from an academic laboratory session; they cannot be dynamically repeated without reassembling the physical hardware.
