# Anderson — convenience targets.
#
#   make help        — list targets
#   make install     — pip install -r requirements.txt
#   make demo        — render the bundled demo paper end-to-end
#   make demo-clean  — remove the regenerated demo review tree
#   make graph       — re-render graph HTML for REVIEW=<dir>
#   make stats       — re-render STATS.md  for REVIEW=<dir>
#   make highlight   — re-render highlighted PDF for REVIEW=<dir>
#   make usage       — aggregate subagent token usage for REVIEW=<dir>
#   make phase1-large-smoke
#                    — validate deterministic Phase 1 shard merge helpers
#   make ci          — pre-PR structural sanity check (no LLM dispatch)
#
# Per-review targets pass REVIEW=<path>:
#   make stats REVIEW=reviews/my-paper

.PHONY: help install demo demo-clean graph stats highlight usage phase1-large-smoke ci

REVIEW ?= reviews/__demo__
DEMO_REVIEW := reviews/__demo__

help:
	@echo "Anderson — make targets"
	@echo ""
	@echo "  install         pip install -r requirements.txt"
	@echo "  demo            render the bundled demo paper end-to-end"
	@echo "  demo-clean      delete the regenerated demo review tree"
	@echo ""
	@echo "  graph           re-render graph HTML for REVIEW=<dir>"
	@echo "  stats           re-render STATS.md  for REVIEW=<dir>"
	@echo "  highlight       re-render highlighted PDF for REVIEW=<dir>"
	@echo "  usage           aggregate subagent token usage for REVIEW=<dir>"
	@echo "  phase1-large-smoke"
	@echo "                  deterministic Phase 1 shard merge helper smoke"
	@echo ""
	@echo "  ci              pre-PR structural check (demo + schema + shard + hook smokes)"
	@echo ""
	@echo "  REVIEW defaults to $(REVIEW)"
	@echo ""

install:
	pip install -r requirements.txt

demo: $(DEMO_REVIEW)/phase3/outputs/paper.highlighted.pdf
	@echo ""
	@echo "Demo outputs in $(DEMO_REVIEW)/phase3/outputs/:"
	@ls -1 $(DEMO_REVIEW)/phase3/outputs/

$(DEMO_REVIEW)/phase3/outputs/paper.highlighted.pdf: \
		demo/paper.txt demo/CLAIMS.md demo/VERIFICATION.md demo/graph.v2.json \
		src/scaffold_review.py src/render_graph.py \
		src/highlight_paper.py src/highlight_text.py src/claim_stats.py
	python3 src/scaffold_review.py --text demo/paper.txt --slug __demo__ --force
	cp demo/CLAIMS.md         $(DEMO_REVIEW)/phase1/outputs/CLAIMS.md
	cp demo/VERIFICATION.md   $(DEMO_REVIEW)/phase2/outputs/VERIFICATION.md
	cp demo/graph.v2.json     $(DEMO_REVIEW)/phase2/outputs/graph.v2.json
	cp demo/graph.v2.json     $(DEMO_REVIEW)/phase3/outputs/graph.final.json
	python3 src/render_graph.py    $(DEMO_REVIEW)/phase3/outputs/graph.final.json
	python3 src/highlight_text.py  $(DEMO_REVIEW)
	python3 src/claim_stats.py     $(DEMO_REVIEW)

demo-clean:
	rm -rf $(DEMO_REVIEW)

graph:
	@if [ -f $(REVIEW)/phase3/outputs/graph.final.json ]; then \
		python3 src/render_graph.py $(REVIEW)/phase3/outputs/graph.final.json; \
	elif [ -f $(REVIEW)/phase2/outputs/graph.v2.json ]; then \
		python3 src/render_graph.py $(REVIEW)/phase2/outputs/graph.v2.json; \
	else \
		echo "no graph.json found under $(REVIEW)" >&2; exit 2; \
	fi

stats:
	python3 src/claim_stats.py $(REVIEW)

highlight:
	@if [ -f $(REVIEW)/paper/paper.pdf ]; then \
		python3 src/highlight_paper.py $(REVIEW); \
	elif [ -f $(REVIEW)/paper/paper.txt ]; then \
		python3 src/highlight_text.py $(REVIEW); \
	else \
		echo "no paper.pdf or paper.txt found under $(REVIEW)/paper/" >&2; exit 2; \
	fi

usage:
	python3 src/token_log.py $(REVIEW)

phase1-large-smoke:
	@tmp=$$(mktemp -d); \
	trap 'rm -rf "$$tmp"' EXIT; \
	python3 src/phase1_large.py validate-claims demo/phase1_large/CLAIMS.md > /dev/null; \
	python3 src/phase1_large.py merge-literature \
		--claims demo/phase1_large/CLAIMS.md \
		--literature-out "$$tmp/LITERATURE.md" \
		--bib-out "$$tmp/references.bib" \
		demo/phase1_large/external_batches/001 demo/phase1_large/bank_batches/001 > /dev/null; \
	diff -u demo/phase1_large/expected-LITERATURE.md "$$tmp/LITERATURE.md"; \
	diff -u demo/phase1_large/expected-references.bib "$$tmp/references.bib"; \
	python3 src/phase1_large.py validate-citations "$$tmp/LITERATURE.md" "$$tmp/references.bib" > /dev/null; \
	mkdir -p "$$tmp/empty-batch"; \
	: > "$$tmp/empty-batch/LITERATURE.part.md"; \
	: > "$$tmp/empty-batch/references.part.bib"; \
	python3 src/phase1_large.py merge-literature \
		--claims demo/phase1_large/CLAIMS.md \
		--literature-out "$$tmp/empty-ok-LITERATURE.md" \
		--bib-out "$$tmp/empty-ok-references.bib" \
		demo/phase1_large/bank_batches/001 "$$tmp/empty-batch" > /dev/null; \
	printf '%s\n' '# CLAIMS - gapped IDs' '' '| claim_id | type | sentence | hedged | confidence | page | line | section | provenance |' '|----------|------|----------|--------|------------|------|------|---------|------------|' '| C001 | result | "A." | false | high | 1 | 1 | 1 | paper.txt:1 |' '| C003 | result | "B." | false | high | 1 | 2 | 1 | paper.txt:2 |' > "$$tmp/gapped-CLAIMS.md"; \
	python3 src/phase1_large.py validate-claims "$$tmp/gapped-CLAIMS.md" > /dev/null; \
	printf '%s\n' '# LITERATURE' '' '## C001' '' '- [@dup] - supports - confidence high - bank - "x"' > "$$tmp/dup-LITERATURE.md"; \
	printf '%s\n' '@article{dup,' '  title = {One}' '}' '' '@article{dup,' '  title = {Two}' '}' > "$$tmp/dup-references.bib"; \
	if python3 src/phase1_large.py validate-citations "$$tmp/dup-LITERATURE.md" "$$tmp/dup-references.bib" > /dev/null 2>&1; then \
		echo "duplicate BibTeX key validation did not fail" >&2; \
		exit 1; \
	fi

# One-shot pre-PR sanity check. Does not exercise the LLM pipeline —
# that requires a real `claude` session at the repo root (see README §
# "Verifying end-to-end").
#
# Forces a fresh demo build (not a no-op against stale outputs), asserts
# both jsonschema and PyMuPDF (fitz) are importable so that
# highlight_text.py's PDF synthesis is exercised, and confirms each of
# the 4 phase-3 artifacts ends up newly written.
ci:
	@echo "[1/8] deps: jsonschema + bibtexparser + PyMuPDF importable..."
	@python3 -c "import jsonschema, bibtexparser, fitz" \
		|| { echo "      MISSING — run: pip install -r requirements.txt" >&2; exit 1; }
	@echo "      OK"
	@echo "[2/8] make demo-clean (force fresh build; no stale-output reuse)..."
	@$(MAKE) -s demo-clean > /dev/null
	@echo "      OK"
	@echo "[3/8] make demo (deterministic Python pipeline)..."
	@$(MAKE) -s demo > /dev/null
	@for f in paper.highlighted.pdf graph.final.html STATS.md paper.highlighted.html; do \
		test -f $(DEMO_REVIEW)/phase3/outputs/$$f \
			|| { echo "      MISSING $$f — demo did not produce it" >&2; exit 1; }; \
	done
	@echo "      OK (4/4 phase-3 outputs present)"
	@echo "[4/8] graph_schema.json validates demo/graph.v2.json..."
	@python3 -c "import json,jsonschema; jsonschema.validate(json.load(open('demo/graph.v2.json')), json.load(open('src/conventions/graph_schema.json')))" \
		&& echo "      OK"
	@echo "[5/8] phase1_large shard merge smoke..."
	@$(MAKE) -s phase1-large-smoke > /dev/null
	@echo "      OK"
	@echo "[6/8] hooks: validate_graph on the demo graph (should pass)..."
	@echo '{"tool_name":"Write","tool_input":{"file_path":"reviews/__demo__/phase3/outputs/graph.final.json"}}' \
		| .claude/hooks/validate_graph.py && echo "      OK (exit 0)"
	@echo "[7/8] hooks: validate_bib on a non-review path (should noop)..."
	@echo '{"tool_name":"Write","tool_input":{"file_path":"src/something.py"}}' \
		| .claude/hooks/validate_bib.py && echo "      OK (exit 0)"
	@echo "[8/8] hooks: usage_log defensive (always exit 0)..."
	@echo '{"agent_type":"test","cwd":"/tmp"}' \
		| .claude/hooks/usage_log.py && echo "      OK (exit 0)"
	@echo ""
	@echo "All structural checks pass. Live LLM smoke is NOT covered — see README."
