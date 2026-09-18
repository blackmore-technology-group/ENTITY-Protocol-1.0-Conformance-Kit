# Phase-One Conformance

Phase one is offline. The independent implementation receives fixed public vectors and returns its own conclusions.

Run:

```bash
python conformance/black_box_tests/run_conformance.py --candidate "<candidate command>"
```

PASS requires every required valid vector accepted, every required invalid vector rejected, no omissions and no crash/indeterminate result.

Phase-one PASS is not the full external interoperability PASS. Bidirectional live communication and sovereign export survival remain separate gates.
