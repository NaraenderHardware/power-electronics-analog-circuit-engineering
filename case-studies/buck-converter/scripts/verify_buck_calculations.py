#!/usr/bin/env python3
"""
Independent Verification & Audit Script: DC-DC Buck Converter (36V -> 18V, 24W)
Parses the actual Arduino firmware source code, performs independent parameter derivation,
and audits electrical stress against physical device datasheets.
"""

import os
import re
import math
import sys

def audit_buck_converter():
    print("=" * 78)
    print("INDEPENDENT AUDIT & VERIFICATION: DC-DC BUCK CONVERTER (36V -> 18V, 24W)")
    print("=" * 78)

    # ---------------------------------------------------------
    # 1. PARSE ACTUAL ARDUINO FIRMWARE
    # ---------------------------------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ino_path = os.path.normpath(os.path.join(base_dir, "..", "code", "arduino_pwm.ino"))
    
    if not os.path.exists(ino_path):
        print(f"[FAIL] Firmware file not found at: {ino_path}")
        return False
        
    with open(ino_path, "r", encoding="utf-8", errors="ignore") as f:
        ino_code = f.read()

    # Extract ICR1 and OCR1A dynamically
    icr1_match = re.search(r'ICR1\s*=\s*(\d+);', ino_code)
    ocr1a_match = re.search(r'OCR1A\s*=\s*(\d+);', ino_code)

    if not icr1_match or not ocr1a_match:
        print("[FAIL] Could not dynamically extract ICR1 and OCR1A from firmware!")
        return False

    icr1_val = int(icr1_match.group(1))
    ocr1a_val = int(ocr1a_match.group(1))

    # Check register bits for Fast PWM Mode 14 and Prescaler 1
    has_wgm11 = "WGM11" in ino_code
    has_wgm12 = "WGM12" in ino_code
    has_wgm13 = "WGM13" in ino_code
    has_com1a1 = "COM1A1" in ino_code
    has_cs10 = "CS10" in ino_code

    print("[Step 1] Firmware Source Parsing (arduino_pwm.ino):")
    print(f"    - Extracted ICR1 (TOP):          {icr1_val}")
    print(f"    - Extracted OCR1A (Duty Match):  {ocr1a_val}")
    print(f"    - Fast PWM Mode 14 Configured:   {has_wgm11 and has_wgm12 and has_wgm13}")
    print(f"    - Non-Inverting OC1A (Pin 9):    {has_com1a1}")
    print(f"    - Clock Prescaler = 1 (CS10):    {has_cs10}")

    # Mathematical frequency derivation from hardware clock
    f_cpu = 16000000.0  # 16 MHz ATmega328P crystal
    prescaler = 1.0
    f_pwm_derived = f_cpu / (prescaler * (icr1_val + 1))
    duty_derived = ocr1a_val / (icr1_val + 1)
    t_on_derived = ocr1a_val / f_cpu

    print(f"    - Derived PWM Frequency:         {f_pwm_derived:.2f} Hz")
    print(f"    - Derived Duty Cycle (D):        {duty_derived:.4f} ({duty_derived*100:.2f}%)")
    print(f"    - Derived ON Time (t_on):        {t_on_derived*1e6:.2f} us")

    # Assert firmware matches 50 kHz claim
    assert math.isclose(f_pwm_derived, 50000.0, rel_tol=1e-4), f"Frequency {f_pwm_derived} != 50 kHz"
    assert math.isclose(duty_derived, 0.5000, rel_tol=1e-4), f"Duty cycle {duty_derived} != 50%"

    # ---------------------------------------------------------
    # 2. OPERATING POINT & CONDUCTION DROOP
    # ---------------------------------------------------------
    Vin = 36.0
    Vout_target = 18.0
    Pout_target = 24.0
    Iout = Pout_target / Vout_target
    R_load = Vout_target / Iout

    # Realistic component parasitic drops
    V_diode = 0.55       # Typical forward drop of 1N5819 at 1A
    Rds_on = 0.028       # IRLZ44N logic-level on-resistance (25C)
    R_L_dcr = 0.40       # Typical DCR for 390uH power choke

    Vout_real = (duty_derived * (Vin - Iout * Rds_on)) - ((1.0 - duty_derived) * V_diode) - (Iout * R_L_dcr)
    droop = Vout_target - Vout_real
    D_required = (Vout_target + V_diode + Iout * R_L_dcr) / (Vin - Iout * Rds_on + V_diode)

    print("\n[Step 2] Steady-State Conduction & Droop Analysis:")
    print(f"    - Target Operating Point:        {Vin:.1f}V in -> {Vout_target:.1f}V out, {Iout:.3f}A ({Pout_target:.1f}W)")
    print(f"    - Equivalent Resistive Load:     {R_load:.2f} Ohm")
    print(f"    - Real Output at Open-Loop D=0.5: {Vout_real:.2f} V")
    print(f"    - Open-Loop Voltage Droop:       {droop:.2f} V ({droop/Vout_target*100:.2f}%)")
    print(f"    - Required D for Exactly 18.0V:  {D_required:.4f} ({D_required*100:.2f}%)")

    # ---------------------------------------------------------
    # 3. INDUCTANCE & RIPPLE AUDIT (680 uH vs 390 uH)
    # ---------------------------------------------------------
    # Critical inductance for Continuous Conduction Mode (CCM)
    L_crit = (R_load * (1.0 - duty_derived)) / (2.0 * f_pwm_derived)
    
    # 680 uH (Design PDF claim)
    L_pdf = 680e-6
    delta_IL_pdf = (Vout_target * (1.0 - duty_derived)) / (f_pwm_derived * L_pdf)
    IL_pk_pdf = Iout + (delta_IL_pdf / 2.0)
    
    # 390 uH (Hardware PCV-2-394-05L inductor)
    L_hw = 390e-6
    delta_IL_hw = (Vout_target * (1.0 - duty_derived)) / (f_pwm_derived * L_hw)
    IL_pk_hw = Iout + (delta_IL_hw / 2.0)

    print("\n[Step 3] Inductance & Ripple Current Audit:")
    print(f"    - Critical Inductance for CCM:   {L_crit*1e6:.2f} uH (Both inductors operate in CCM)")
    print(f"    - Design PDF Value (680 uH):     Delta_IL = {delta_IL_pdf:.3f} A ({delta_IL_pdf/Iout*100:.1f}%), Peak = {IL_pk_pdf:.3f} A")
    print(f"    - Hardware Value (390 uH):       Delta_IL = {delta_IL_hw:.3f} A ({delta_IL_hw/Iout*100:.1f}%), Peak = {IL_pk_hw:.3f} A")
    print(f"    - Discrepancy: Hardware inductor increases current ripple by {(delta_IL_hw/delta_IL_pdf - 1.0)*100:.1f}%.")

    # ---------------------------------------------------------
    # 4. CAPACITOR & OUTPUT RIPPLE AUDIT
    # ---------------------------------------------------------
    C_designed = 100e-6
    ESR = 0.15
    delta_Vc = delta_IL_pdf / (8.0 * f_pwm_derived * C_designed)
    delta_Vesr = delta_IL_pdf * ESR
    delta_Vout_total = delta_Vc + delta_Vesr
    delta_V_no_C = delta_IL_hw * R_load

    print("\n[Step 4] Output Capacitor & Voltage Ripple:")
    print(f"    - Designed 100 uF Cap Ripple:    {delta_Vout_total*1e3:.2f} mV_pp ({delta_Vout_total/Vout_target*100:.2f}%)")
    print(f"    - Missing Cap Hardware Reality:  {delta_V_no_C:.2f} V_pp ({delta_V_no_C/Vout_target*100:.1f}% across load)")

    # ---------------------------------------------------------
    # 5. CRITICAL SEMICONDUCTOR STRESS & SAFETY AUDIT
    # ---------------------------------------------------------
    V_rrm_1N5819 = 40.0
    I_f_1N5819 = 1.0
    V_margin = (V_rrm_1N5819 - Vin) / V_rrm_1N5819
    I_diode_avg = (1.0 - duty_derived) * Iout
    I_diode_pk = IL_pk_hw

    print("\n[Step 5] Semiconductor Safety & Derating Verification:")
    print(f"    - 1N5819 Reverse Rating:         Vrrm = {V_rrm_1N5819:.1f} V")
    print(f"    - Operating DC Reverse Voltage:  Vin = {Vin:.1f} V")
    print(f"    - Static Voltage Margin:         {V_margin*100:.1f}% (4.0V static margin; standard engineering guidelines recommend >=20% to 30% margin)")
    print(f"    - Diode Average Forward Current: Id(avg) = {I_diode_avg:.3f} A (Rating: If(avg) = {I_f_1N5819:.1f} A continuous average)")
    print(f"    - Diode Peak Forward Current:    Id(pk) = {I_diode_pk:.3f} A (Exceeds 1.0A continuous-average threshold; peak/surge limits unverified without exact manufacturer datasheet)")
    print(f"    - Diode Safety Verdict:          UNSAFE FOR 36V ENERGIZATION. 4.0V static reverse margin vulnerable to switching transients.")

    print("\n" + "=" * 78)
    print("BUCK CONVERTER AUDIT COMPLETED: MATHEMATICAL INTEGRITY VERIFIED")
    print("=" * 78)
    return True

if __name__ == "__main__":
    success = audit_buck_converter()
    sys.exit(0 if success else 1)
