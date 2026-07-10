#!/usr/bin/env python3
"""Numerical verification chains for the relativistic no-go theorem paper.
Every number printed here is cited in the paper. SI units unless noted."""
import math

c      = 2.99792458e8        # m/s
G      = 6.674e-11           # m^3 kg^-1 s^-2
sigma  = 5.670374419e-8      # W m^-2 K^-4 Stefan-Boltzmann
m_p    = 1.67262192e-27      # kg proton mass
mpc2_J = m_p * c**2          # J
mpc2_MeV = 938.272           # MeV
eV     = 1.602176634e-19     # J
Msun   = 1.98892e30          # kg
AU     = 1.495978707e11      # m
pc     = 3.0857e16           # m
ly     = 9.4607e15           # m
yr     = 3.15576e7           # s

def gamma(b): return 1.0/math.sqrt(1.0-b*b)

print("="*72)
print("SECTION A: KINEMATIC ANCHORS")
print("="*72)
for b in (0.1, 0.2, 0.5, 0.9, 0.99):
    g = gamma(b)
    ke = (g-1)               # in units of mc^2
    print(f"beta={b:5.2f}  gamma={g:7.4f}  KE/mc^2={ke:8.4f}  KE={ke*c*c:.3e} J/kg")

b = 0.99; g = gamma(b)
print(f"\nAt 0.99c: gamma = {g:.4f}, KE = {(g-1):.3f} mc^2 = {(g-1)*c*c:.3e} J/kg")
print(f"Reflected-beam Doppler factor (1-b)/(1+b) = {(1-b)/(1+b):.5f} = 1/{(1+b)/(1-b):.1f}")
print(f"Sail-frame incident redshift over 0->0.99c: sqrt((1+b)/(1-b)) = {math.sqrt((1+b)/(1-b)):.2f}x")
# momentum-transfer: photon reflected from mirror at beta: energy efficiency
# fraction of photon energy converted to sail KE = 1 - (1-b)/(1+b) = 2b/(1+b)
print(f"Photon->sail momentum-transfer energy efficiency 2b/(1+b) = {2*b/(1+b):.4f}")
# incident beam energy per kg to reach 0.99c (integrate in lab frame):
# dE_kin = eta(beta) dE_inc with eta = 2beta/(1+beta) instantaneous
# E_inc = integral dE_kin/eta. dE_kin = c^2 d(gamma). Do numerically:
N = 2000000
E_inc = 0.0
for i in range(1, N+1):
    b1 = 0.99*i/N; b0 = 0.99*(i-1)/N
    dEk = (gamma(b1)-gamma(b0))*c*c
    bm  = 0.5*(b0+b1)
    eta = 2*bm/(1+bm) if bm > 0 else 1e-12
    E_inc += dEk/eta
print(f"Incident beam energy to reach 0.99c: {E_inc:.3e} J/kg  (KE={((g-1)*c*c):.3e})")

print()
print("="*72)
print("SECTION B: TIER 1 -- ISM FRONTAL HEATING (thick body, full stopping)")
print("="*72)
n_ism = 1.0e6  # atoms/m^3  (1 cm^-3)
print(f"ISM density n = 1 cm^-3 = {n_ism:.1e} m^-3 (warm neutral medium)")
print(f"{'beta':>6} {'gamma':>8} {'E/atom(GeV)':>12} {'flux(m-2 s-1)':>14} "
      f"{'P(W/m^2)':>11} {'T_eq,1face(K)':>13} {'T_eq,2face(K)':>13}")
for b in (0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99):
    gm = gamma(b)
    Eatom = (gm-1)*mpc2_MeV/1000.0            # GeV
    flux  = n_ism*gm*b*c                       # ship-frame number flux (n'=gamma n)
    P     = flux*(gm-1)*mpc2_J                 # W/m^2 if fully stopped
    T1    = (P/sigma)**0.25                    # radiate from front face only
    T2    = (P/(2*sigma))**0.25                # front+back
    print(f"{b:6.2f} {gm:8.3f} {Eatom:12.3f} {flux:14.3e} {P:11.3e} {T1:13.0f} {T2:13.0f}")

# Range of 6 GeV proton in rock (SiO2, rho=2.65 g/cm3):
# CSDA range at ~6 GeV: ~ 2400 g/cm^2 ionization-only; but nuclear collision
# length in SiO2 ~ 66 g/cm^2 -> hadronic cascade develops within ~25 cm.
print("\n6 GeV proton in SiO2: nuclear interaction length ~66 g/cm^2 ~ 25 cm;")
print("hadronic cascade deposits bulk of energy within ~1 m: 'thick' = anything >~1 m.")
print("Thin films (1 g/m^2 = 1e-4 g/cm^2): minimum-ionizing dE/dx ~ 2 MeV/(g/cm^2)")
dep = 2e6*1e-4   # eV per proton in 1 g/m^2 film
print(f" -> deposited per proton ~ {dep:.0f} eV; deposited power at 0.99c:")
b=0.99; gm=gamma(b); flux=n_ism*gm*b*c
print(f"    {flux*dep*eV:.3f} W/m^2  (tiny -- but see sputtering/track damage below)")

# Sputtering erosion estimate at 0.99c (order of magnitude, cited to Hoang et al. for 0.1-0.3c):
# take effective sputtering+spallation yield Y atoms removed per incident H
for Y in (1, 10):
    # column to erode 1 mm of rock (rho=3000 kg/m3, mean atomic mass ~20 amu)
    n_target = 3000/(20*1.66054e-27)   # atoms/m^3 in rock
    col_per_mm = n_target*1e-3         # atoms/m^2 removed for 1 mm
    dist = col_per_mm/(Y*n_ism)        # m of travel per mm eroded
    print(f"Erosion: Y={Y:>2} atoms/ion -> 1 mm eroded per {dist/pc:.2f} pc traveled")

print()
print("="*72)
print("SECTION C: TIER 3a -- THERMAL/DIFFRACTION SCISSORS (beamed sail)")
print("="*72)
# Sail: areal density rho_A (kg/m^2), absorptivity alpha, emissivity eps,
# max temperature T_max, payload beta target 0.99.
# Thermal floor on burn time:
#   absorbed energy per kg:  E_abs = alpha * E_inc(beta)  [E_inc ~ 1e18 J/kg]
#   max radiated power per kg: P_rad = 2 eps sigma T^4 / rho_A
#   t_burn >= E_abs/P_rad
# Diffraction ceiling on burn time:
#   spot must fit sail of side s at distance d: d <= s D / (2.44 lambda) (Airy)
#   distance grown during burn to 0.99c ~ integral beta c dt ; average beta ~0.9
#   => t_burn <= s D/(2.44 lambda * <beta> c)
lam = 1.064e-6
E_inc_val = E_inc  # from section A, ~1e18 J/kg
def scissors(rho_A, alpha, eps, T_max, s, D, avg_beta=0.87):
    E_abs = alpha*E_inc_val
    P_rad = 2*eps*sigma*T_max**4/rho_A
    t_min = E_abs/P_rad
    d_max = s*D/(2.44*lam)
    t_max = d_max/(avg_beta*c)
    return t_min, t_max, d_max

print("Case 1: handoff baseline. rho_A=1 g/m^2, alpha=1e-6, eps=1, T=1000K, s=30m, D=100km")
tmin,tmax,dmax = scissors(1e-3, 1e-6, 1.0, 1000.0, 30.0, 1e5)
print(f"  t_min(thermal) = {tmin:.3e} s ({tmin/3600:.2f} h); "
      f"d_max = {dmax/AU:.1f} AU; t_max(diffraction) = {tmax:.3e} s ({tmax/3600:.2f} h)")
# distance actually covered in t_min:
# integrate motion under constant incident power? just report avg-beta distance
print(f"  distance covered in t_min at <beta>~0.87: {0.87*c*tmin/AU:.1f} AU")
# aperture needed to keep focus for t_min:
D_need = 2.44*lam*0.87*c*tmin/30.0
print(f"  aperture needed for s=30 m sail: D = {D_need/1000:.0f} km")

print("\nCase 2: realistic broadband alpha=1e-4 (14x Doppler sweep), eps=0.05 (thin film):")
tmin,tmax,dmax = scissors(1e-3, 1e-4, 0.05, 1000.0, 30.0, 1e5)
print(f"  t_min = {tmin:.3e} s = {tmin/yr:.1f} yr -> aperture D = "
      f"{2.44*lam*0.87*c*tmin/30/1000:.2e} km  (absurd)")

print("\nGeneral scissors condition: t_min <= t_max  =>  D >= 2.44 lam <beta> c alpha E_inc rho_A/(2 eps sigma T^4 s)")
def D_required(rho_A, alpha, eps, T_max, s, avg_beta=0.87):
    return 2.44*lam*avg_beta*c*alpha*E_inc_val*rho_A/(2*eps*sigma*T_max**4*s)
print(f"{'alpha':>8} {'eps':>5} {'T(K)':>6} {'s(m)':>6} {'rho_A':>8} {'D_req':>12}")
for (a_,e_,T_,s_,r_) in [(1e-6,1.0,1000,30,1e-3),(1e-6,0.5,1500,30,1e-3),
                          (1e-5,0.1,1500,100,1e-3),(1e-4,0.05,1000,30,1e-3),
                          (1e-6,1.0,2000,1000,1e-3),(1e-7,1.0,2000,1000,1e-3)]:
    Dr = D_required(r_,a_,e_,T_,s_)
    print(f"{a_:8.0e} {e_:5.2f} {T_:6.0f} {s_:6.0f} {r_:8.0e} {Dr/1000:9.0f} km")

# beam power requirement (baseline t_min = 5.19e3 s from Case 1)
t_base = 5194.0
print(f"\nBeam power: E_inc/t_min per kg, baseline: {E_inc_val/t_base:.2e} W/kg")
print(f"Mean acceleration baseline ~ 0.99c/{t_base:.0f}s = {0.99*c/t_base/9.81:.0f} g")

print()
print("="*72)
print("SECTION D: TIER 0 -- GRAVITATIONAL SLINGSHOT CEILING")
print("="*72)
for M_bh in (10, 1e6):
    M = M_bh*Msun
    r_isco = 6*G*M/c**2
    v_isco_frac = 0.5  # local orbital speed at Schwarzschild ISCO = c/2
    print(f"BH {M_bh:.0e} Msun: r_ISCO = {r_isco/1000:.1f} km; local orbital speed at ISCO = c/2")
    # tidal gradient at ISCO
    tide = 2*G*M/r_isco**3
    print(f"  tidal gradient 2GM/r^3 at ISCO = {tide:.3e} s^-2 (per meter separation)")
    # stress on rock of half-length L=0.5 m, rho=3000
    L=0.5; rho=3000
    stress = rho*tide*L**2/2
    print(f"  tidal stress on 1-m rock ~ rho*tide*L^2/2 = {stress:.1f} Pa vs strength 1e8-1e9 Pa")
    # strength-limited minimum radius for 1-m rock, S=1e8 Pa
    S=1e8
    r_strength = (rho*2*G*M*L**2/(2*S))**(1/3.)
    print(f"  strength-limited r_min (S=1e8Pa, 1m rock) = {r_strength/1000:.2f} km "
          f"({'inside' if r_strength<r_isco else 'outside'} ISCO -> ISCO governs)" )
# Kerr: prograde ISCO -> r_g, orbital speeds up to ~0.7c region for a*->1
print("Kerr a*->1 prograde: ISCO -> GM/c^2, circular-orbit speeds push toward ~0.7c (extremal heroics)")
print("Hills-type ejection from binary: v_ej ~ sqrt(v_orb * v_binary) geometric mean;")
print("ejection at infinity <~ pericenter orbital speed; ceiling ~0.5c Schwarzschild.")
# gamma at 0.5c:
print(f"gamma(0.5c) = {gamma(0.5):.3f}, KE = {(gamma(0.5)-1):.3f} mc^2 -- vs required gamma 7.09: shortfall x{(gamma(0.99)-1)/(gamma(0.5)-1):.0f} in energy")

print()
print("="*72)
print("SECTION E: TIER 4 -- ONBOARD PROPULSION ARITHMETIC")
print("="*72)
# Relativistic rocket equation: Delta-v with exhaust speed w:
# m0/m1 = [ (1+b)/(1-b) ]^{c/(2w)}
print("Mass ratios m0/m1 to reach beta (relativistic rocket eqn):")
print(f"{'beta':>6} {'w=1.5e-5c(chem)':>18} {'w=0.05c(fission frag)':>22} {'w=0.1c(fusion)':>16} {'w=c(photon)':>12}")
for b in (0.1,0.5,0.9,0.99):
    row=[]
    for w in (1.5e-5,0.05,0.1,1.0):
        log10MR = math.log10((1+b)/(1-b))/(2*w)
        row.append(log10MR)
    def fmt(l):
        return f"{10**l:.3e}" if l < 15 else f"10^{l:.0f}"
    print(f"{b:6.2f} {fmt(row[0]):>18} {fmt(row[1]):>22} {fmt(row[2]):>16} {10**row[3]:12.2f}")

print("\nWaste-heat table (onboard conversion at efficiency eta_c, radiate at P_rej):")
print("KE(beta) per kg payload; waste heat W = KE*(1-eta)/eta; time = W/P_rej")
print(f"{'beta':>6} {'KE (J/kg)':>11} | {'eta=0.8 W(J/kg)':>16} {'t@200W/kg':>12} {'t@1kW/kg':>10} | {'eta=0.99 W':>11} {'t@1kW/kg':>10}")
for b in (0.1,0.5,0.9,0.99):
    ke=(gamma(b)-1)*c*c
    w80=ke*0.2/0.8; w99=ke*0.01/0.99
    print(f"{b:6.2f} {ke:11.3e} | {w80:16.3e} {w80/200/yr:10.1f}yr {w80/1000/yr:8.1f}yr | {w99:11.3e} {w99/1000/yr:8.1f}yr")

# photon rocket energy: E_beam emitted for gamma: total emitted energy per final kg
# photon rocket: m0/m1 = gamma(1+b); energy emitted = (m0-m1)c^2 - KE...
for b in (0.99,):
    MR = gamma(b)*(1+b)
    print(f"\nPhoton rocket to {b}c: m0/m1 = gamma(1+beta) = {MR:.2f}")
    E_emitted = (MR-1)*c*c - (gamma(b)-1)*c*c   # per kg final mass
    print(f"  energy radiated as exhaust per kg final: {E_emitted:.3e} J = {E_emitted/c/c:.2f} mc^2")

print()
print("="*72)
print("SECTION F: DOPPLER BAND / EMISSIVITY")
print("="*72)
print(f"Sail-frame frequency sweep 0->0.99c: factor sqrt((1+b)/(1-b)) = {math.sqrt(1.99/0.01):.1f}")
for epsv in (1.0,0.1,0.05,0.01):
    # equilibrium T for absorbed 1e12 J over 8850 s baseline: P_abs=1.13e8 W/kg*? recompute:
    P_abs = 1e-6*E_inc_val/8850.0   # W/kg absorbed in baseline burn
    # T with area 2000 m^2/kg (two faces of 1g/m^2):
    T = (P_abs/(2000*epsv*sigma))**0.25
    print(f"eps={epsv:5.2f}: equilibrium T for baseline absorbed power {P_abs:.2e} W/kg = {T:6.0f} K")

print()
print("="*72)
print("SECTION G: TIER 1 SUPPLEMENTS -- dust impacts, shield mass, transit dose")
print("="*72)
b=0.99; gm=gamma(b)
# dust: ~1% of ISM gas mass in grains, typical grain a=0.1um, rho_g=2000 kg/m3
a_g=1e-7; rho_g=2000.0
m_g=(4/3)*math.pi*a_g**3*rho_g
E_g=(gm-1)*m_g*c*c
rho_dust=0.01*n_ism*m_p       # kg/m^3
flux_dust=rho_dust*gm*b*c/m_g  # grains per m^2 s
print(f"0.1-um grain mass {m_g:.2e} kg; impact energy at 0.99c = {E_g:.2f} J each")
print(f"grain flux = {flux_dust:.3f} m^-2 s^-1 -> {flux_dust*3.156e7:.2e} impacts/m^2/yr")
print(f"dust kinetic power = {rho_dust*gm*b*c*(gm-1)*c*c:.2e} W/m^2 (adds to {1.93e6:.2e} gas)")
# shield to stop 6-GeV cascade: ~ 5 nuclear interaction lengths of graphite
lam_int=85.8/2.2  # g/cm^2 / (g/cm^3) -> cm, graphite lambda_I ~ 85.8 g/cm^2, rho 2.2
print(f"graphite nuclear interaction length ~{85.8:.0f} g/cm^2 = {lam_int:.0f} cm;")
print(f"5 lambda shield ~ {5*85.8*10:.0f} kg/m^2 = {5*85.8*10/1e-3:.1e}x the 1 g/m^2 sail areal budget")
# transit: 10 pc at 0.99c, fluence and total heat per m^2
d=10*pc; t=d/(b*c)
print(f"10 pc transit at 0.99c: {t/yr:.1f} yr (lab), proton fluence {n_ism*gm*d:.2e} /m^2,")
print(f"  integrated frontal energy {n_ism*gm*d*(gm-1)*mpc2_J:.2e} J/m^2")
# equilibrium temps vs density
print("Frontal equilibrium T at 0.99c vs ISM density (radiate 2 faces):")
for nn in (0.1,1.0,10.0,100.0):
    P=nn*1e6*gm*b*c*(gm-1)*mpc2_J
    print(f"  n={nn:6.1f} cm^-3: P={P:.2e} W/m^2, T_eq={(P/(2*sigma))**0.25:.0f} K")
print("Melting/sublimation anchors: silicates 1400-1900 K, Fe 1811 K, W 3695 K, graphite ~3900 K subl.")

print()
print("SECTION H: strength-limited pericenter vs BH mass (L=1 m rock, S=1e8 Pa, rho=3000)")
for Mb in (10,1e3,1e6,4.3e6):
    M=Mb*Msun; L=0.5; S=1e8; rho=3000
    r_s=(rho*2*G*M*L**2/(2*S))**(1/3.)
    r_i=6*G*M/c**2
    governs = "ISCO" if r_s < r_i else "strength"
    # local circular speed at max(r_s, r_i), Schwarzschild static-observer speed
    r=max(r_s,r_i)
    x=G*M/(r*c*c)
    v_loc=math.sqrt(x/(1-2*x))  # v/c for circular orbit measured locally
    print(f"M={Mb:9.1e} Msun: r_strength={r_s/1e3:12.1f} km, r_ISCO={r_i/1e3:12.1f} km "
          f"-> {governs:9s} governs; local v_circ at limit = {v_loc:.3f} c")


print()
print("="*72)
print("SECTION I: REVIEW-ROUND ADDITIONS")
print("="*72)
# rapidity compounding of chained boosts
w5 = math.atanh(0.5); w99 = math.atanh(0.99)
print(f"rapidity w(0.5c)={w5:.4f}, w(0.99c)={w99:.4f} -> ideal 0.5c boosts needed: {w99/w5:.2f}")
# magnetic rigidity of 5.7 GeV proton
p_MeV = math.sqrt((6.0888+1)**2 - 1)*938.272  # p*c in MeV for gamma=7.0888... total E=gamma*m
p_MeV = math.sqrt((7.0888*938.272)**2 - 938.272**2)/1.0
print(f"proton at gamma=7.089: p = {p_MeV:.0f} MeV/c, rigidity = {p_MeV/1000:.2f} GV")
p_SI = p_MeV*1e6*1.602176634e-19/c
for B in (1.0, 10.0):
    print(f"  gyroradius at B={B:.0f} T: {p_SI/(1.602176634e-19*B):.1f} m")
# chirped-transmitter endpoint
print(f"chirped source endpoint to hold sail-frame at 1 um: 1000 nm / 14.1 = {1000/14.107:.1f} nm (VUV)")
print(f"  photon energy at 70.9 nm: {1239.8/70.9:.1f} eV (exceeds every optical-material bandgap)")
# low-density environments at 0.99c
b=0.99; gm=gamma(b)
for nn in (0.01, 1e-5):
    P = nn*1e6*gm*b*c*(gm-1)*mpc2_J
    print(f"n={nn:g} cm^-3: P = {P:.3g} W/m^2, T_eq(2-face) = {(P/(2*sigma))**0.25:.0f} K")
# chemical exponents corrected (w = 1.5e-5 c = 4.5 km/s)
for bb in (0.1,0.5,0.9,0.99):
    print(f"chemical w=1.5e-5c, beta={bb}: log10(m0/m1) = {math.log10((1+bb)/(1-bb))/(2*1.5e-5):,.0f}")
# asteroid equivalent of 3e11 kg
r = (3e11/2000/(4/3*math.pi))**(1/3)
print(f"3e11 kg at rho=2000: diameter = {2*r:.0f} m (Ceres = 9.4e20 kg, ratio {9.4e20/3e11:.1e})")

print()
print("="*72)
print("SECTION J: THE ATTAINABLE ENVELOPE (A31-A35)")
print("="*72)
# A31 ISM thermal ceiling: solve T_eq(beta;n)=T_lim, 2-face
def P_ism(b,n_cc): return gamma(b)*n_cc*1e6*b*c*(gamma(b)-1)*mpc2_J
def beta_for_T(Tlim,n_cc):
    lo,hi=0.01,0.999999
    for _ in range(200):
        mid=(lo+hi)/2
        if (P_ism(mid,n_cc)/(2*sigma))**0.25>Tlim: hi=mid
        else: lo=mid
    return (lo+hi)/2
print("A31 ISM thermal ceiling beta_max(T_lim, n):")
for name,T in [("silicate/iron 1500K",1500),("silicate 1800K",1800),
               ("tungsten 3000K",3000),("graphite 3500K",3500)]:
    print(f"    {name:20s}: n=1: {beta_for_T(T,1.0):.3f}   n=0.1: {beta_for_T(T,0.1):.3f}")
# A32 radiator-limited rocket
print("A32 radiator-limited rocket, century-mission delta-v:")
for label,R,fw in [("200 W/kg, fw=5%",200,0.05),("1 kW/kg, fw=1%",1000,0.01),
                   ("10 kW/kg, fw=0.1% (fantasy)",1e4,0.001)]:
    a_ph=R/(fw*c); a_fus=2*R/(fw*0.1*c)
    t=100*3.156e7
    print(f"    {label:28s}: photon a={a_ph:.2e} m/s2 dv={a_ph*t/c:.4f}c | fusion(w=0.1c) a={a_fus:.2e} dv={min(a_fus*t/c,0.99):.3f}c")
# A33 fusion exhaust-rapidity bound
print("A33 fusion exhaust bound beta=tanh((w/c)lnR):")
for w_c in (0.05,0.1):
    print("    w=%.2fc:"%w_c, ", ".join(f"R={R}: {math.tanh(w_c*math.log(R)):.3f}" for R in (10,100,1000)))
# A34 mass-driver beta vs track
a=1e8/3000
print("A34 mass driver (a=S/rhoL=3.3e4 m/s2, ultimate):")
for l_AU in (0.1,1,10,100):
    g_=1+a*l_AU*AU/c**2
    print(f"    track {l_AU:6.1f} AU: beta = {math.sqrt(1-1/g_**2):.3f}")
# A35 dust erosion rate scaled from Hoang 2017
mm_per_pc = 3.086e18/(3e17/0.5)
print(f"A35 dust erosion (Hoang 0.2c anchor): {mm_per_pc:.1f} mm/pc at n=1;")
print(f"    1-m body loses 0.5 m in {500/mm_per_pc:.0f} pc")
