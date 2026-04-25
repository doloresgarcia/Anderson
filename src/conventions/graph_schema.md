# Graph schema (PLACEHOLDER — fill in before serious use)

> **Status: PLACEHOLDER.** Until this file is written by the project owner, the
> `graph_builder` agent emits a minimal one-node-per-claim graph and reviewers
> raise a Category B finding noting the gap.

## What this file must specify

A complete graph schema, sufficient for `graph_builder` to validate its output and
for the highlighter to traverse the graph. At minimum:

### Node types

For each node kind:

- name (e.g. `claim`, `evidence`, `reference`, `assumption`, …)
- required properties
- optional properties
- id format

### Edge types

For each edge kind:

- name (e.g. `supports`, `contradicts`, `depends_on`, `cites`, …)
- allowed (source kind, target kind) pairs
- whether directed
- required properties (e.g. `weight`, `verdict`, `confidence`)

### Verdict layer

How verification verdicts are attached to nodes/edges in `graph.v2.json` and
later. Suggested options the owner can choose between:

- as a property on the claim node (`verdict`, `evidence_refs`, `notes`)
- as a separate `verification` node connected by a `verifies` edge
- both

### JSON shape

A literal example of a small graph (3–5 nodes) that conforms to the schema, so
agents have a concrete target.

## Until this file is filled in

`graph_builder` will:

- create one `claim` node per `CLAIMS.md` row, with properties `id`, `sentence`,
  `page`, `line`, `section`
- create one `cites` edge per `LITERATURE.md` candidate
- in phase 2, attach `verdict`, `evidence`, `reasoning` properties from
  `VERIFICATION.md` directly onto the claim node
