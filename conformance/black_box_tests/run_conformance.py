#!/usr/bin/env python3
import argparse, json, pathlib, shlex, subprocess, sys

ROOT=pathlib.Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'vectors'/'VECTOR_MANIFEST.json'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--candidate',required=True)
    ap.add_argument('--json-out')
    args=ap.parse_args()
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    base=shlex.split(args.candidate,posix=(sys.platform!='win32'))
    results=[]; passed=True
    for vector in manifest['vectors']:
        cmd=base+['verify','--kind',vector['kind'],'--input',str(ROOT/vector['path'])]
        cp=subprocess.run(cmd,text=True,capture_output=True)
        item={'id':vector['id'],'kind':vector['kind'],'expected':vector['expected'],'exit_code':cp.returncode}
        if cp.returncode!=0:
            item['pass']=False; item['error']='candidate_nonzero_exit'; item['stderr']=cp.stderr[-2000:]; passed=False
        else:
            try:
                out=json.loads(cp.stdout.strip())
            except Exception as exc:
                item['pass']=False; item['error']='candidate_output_not_json'; item['detail']=str(exc); passed=False
            else:
                actual=out.get('accepted')
                item['actual']=out
                item['pass']=isinstance(actual,bool) and actual==vector['expected']['accepted']
                expected_facts=vector['expected'].get('facts') or {}
                actual_facts=out.get('facts') if isinstance(out.get('facts'),dict) else {}
                fact_mismatches={}
                for key,value in expected_facts.items():
                    if actual_facts.get(key) != value:
                        fact_mismatches[key]={'expected':value,'actual':actual_facts.get(key)}
                if fact_mismatches:
                    item['pass']=False
                    item['fact_mismatches']=fact_mismatches
                if not item['pass']: passed=False
        results.append(item)
        print(('PASS' if item['pass'] else 'FAIL'),vector['id'])
    report={'schema':'entity-external-conformance-run-v1','protocol':'ENTITY-1.0','kit_version':manifest['kit_version'],'pass':passed,'results':results}
    if args.json_out:
        pathlib.Path(args.json_out).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'pass':passed,'passed':sum(1 for r in results if r['pass']),'total':len(results)},sort_keys=True))
    return 0 if passed else 2

if __name__=='__main__':
    raise SystemExit(main())
