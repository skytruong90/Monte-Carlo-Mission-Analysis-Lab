from __future__ import annotations
import argparse,csv,json,math,random,statistics
from pathlib import Path

def one_run(rng:random.Random,i:int):
    mass=rng.gauss(1200,60); drag=max(.7,rng.gauss(1.0,.08)); wind=rng.gauss(0,5); sensor_bias=rng.gauss(0,8)
    climb_alt=3000 + 420*(1-drag) - .18*(mass-1200) + 4*wind
    fuel_used=145 + .055*(mass-1200) + 32*(drag-1) + abs(wind)*.7
    nav_error=abs(sensor_bias)+abs(wind)*.35+rng.random()*3
    reserve=260-fuel_used; success=climb_alt>2850 and reserve>85 and nav_error<25
    return {"run":i,"mass_kg":mass,"drag_factor":drag,"wind_mps":wind,"sensor_bias_m":sensor_bias,"final_altitude_m":climb_alt,"fuel_reserve_kg":reserve,"nav_error_m":nav_error,"success":int(success)}

def percentile(values,p):
    s=sorted(values); idx=(len(s)-1)*p; lo=int(math.floor(idx)); hi=int(math.ceil(idx)); return s[lo] if lo==hi else s[lo]*(hi-idx)+s[hi]*(idx-lo)

def analyze(rows):
    alts=[r["final_altitude_m"] for r in rows]; reserves=[r["fuel_reserve_kg"] for r in rows]; nav=[r["nav_error_m"] for r in rows]
    return {"runs":len(rows),"success_rate":round(sum(r["success"] for r in rows)/len(rows),4),"altitude_mean_m":round(statistics.fmean(alts),2),"altitude_std_m":round(statistics.pstdev(alts),2),"fuel_reserve_p05_kg":round(percentile(reserves,.05),2),"nav_error_p95_m":round(percentile(nav,.95),2)}

def simulate(runs,seed):
    rng=random.Random(seed); return [one_run(rng,i) for i in range(runs)]

def main():
    p=argparse.ArgumentParser(); p.add_argument("--runs",type=int,default=500); p.add_argument("--seed",type=int,default=42); p.add_argument("--output",type=Path,default=Path("artifacts")); a=p.parse_args()
    if a.runs<1: raise SystemExit("runs must be positive")
    rows=simulate(a.runs,a.seed); a.output.mkdir(parents=True,exist_ok=True)
    with (a.output/"runs.csv").open("w",newline="",encoding="utf-8") as f: w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    report=analyze(rows); (a.output/"summary.json").write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
