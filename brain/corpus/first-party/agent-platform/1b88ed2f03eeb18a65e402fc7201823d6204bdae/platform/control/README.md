# Provider-neutral control contract

This is a local, standard-library-only contract layer for admission, checkpoints,
exact candidate identity, review eligibility, stop/recovery, takeover, and teardown.
It deliberately does not call Git, GitHub, services, runtimes, or the network.

`revision` and `cas_token` model the compare-and-swap precondition that a real
transport adapter must persist to its authoritative remote lease surface. Local JSON
files and this simulator are not distributed locks.

Run the deterministic suite from the repository root:

```sh
python3 -m unittest discover -s platform/control/tests -p 'test_*.py' -v
```

Validate a contract fixture:

```sh
python3 platform/control/validate.py validate candidate platform/control/fixtures/candidate.json
python3 platform/control/validate.py validate gate-receipt platform/control/fixtures/gate-receipt.json
python3 platform/control/validate.py validate review platform/control/fixtures/review.json
```

Simulate a sequence without mutating task state:

```sh
python3 platform/control/validate.py simulate platform/control/fixtures/valid-sequence.json
python3 platform/control/validate.py simulate platform/control/fixtures/stale-race-sequence.json
python3 platform/control/validate.py simulate-admission-race platform/control/fixtures/admission-race.json
```

The second simulation intentionally fails because two transitions present the same
revision/CAS token.  Candidate identities accept only exact base/head/tree SHAs and
artifact hashes; moving branch/ref names are rejected by the schema and validator.
Each candidate also declares a non-empty map of content-addressed gate receipt
hashes. A gate receipt canonically binds the exact base/head/tree identity and
artifact hashes to its command, exit result, and output artifact hash. Candidate,
review, and promotion checkpoints must carry the same complete receipt map; each
checkpoint check must reconcile to one receipt's command, result, and hash. The
validator checks receipt integrity but deliberately does not execute commands; a
receipt-producing adapter must persist authentic command output on the authoritative
surface.

A failed or blocked teardown remains durably recorded but cannot release a lease or
close an attempt. The admission-race command publishes the first local result into a
fixture registry and rejects the second contender's stale precondition; a remote
transport adapter remains responsible for any real distributed compare-and-swap.
