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
#   make ci          — pre-PR structural sanity check (no LLM dispatch)
#
# Per-review targets pass REVIEW=<path>:
#   make stats REVIEW=reviews/my-paper

.PHONY: help install demo demo-clean graph stats highlight usage ci

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
	@echo ""
	@echo "  ci              pre-PR structural check (demo + schema + hook smokes)"
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

# One-shot pre-PR sanity check. Does not exercise the LLM pipeline —
# that requires a real `claude` session at the repo root (see README §
# "Verifying the rework end-to-end").
#
# Forces a fresh demo build (not a no-op against stale outputs), asserts
# both jsonschema and PyMuPDF (fitz) are importable so that
# highlight_text.py's PDF synthesis is exercised, and confirms each of
# the 4 phase-3 artifacts ends up newly written.
ci:
	@echo "[1/7] deps: jsonschema + bibtexparser + PyMuPDF importable..."
	@python3 -c "import jsonschema, bibtexparser, fitz" \
		|| { echo "      MISSING — run: pip install -r requirements.txt" >&2; exit 1; }
	@echo "      OK"
	@echo "[2/7] make demo-clean (force fresh build; no stale-output reuse)..."
	@$(MAKE) -s demo-clean > /dev/null
	@echo "      OK"
	@echo "[3/7] make demo (deterministic Python pipeline)..."
	@$(MAKE) -s demo > /dev/null
	@for f in paper.highlighted.pdf graph.final.html STATS.md paper.highlighted.html; do \
		test -f $(DEMO_REVIEW)/phase3/outputs/$$f \
			|| { echo "      MISSING $$f — demo did not produce it" >&2; exit 1; }; \
	done
	@echo "      OK (4/4 phase-3 outputs present)"
	@echo "[4/7] graph_schema.json validates demo/graph.v2.json..."
	@python3 -c "import json,jsonschema; jsonschema.validate(json.load(open('demo/graph.v2.json')), json.load(open('src/conventions/graph_schema.json')))" \
		&& echo "      OK"
	@echo "[5/7] hooks: validate_graph on the demo graph (should pass)..."
	@echo '{"tool_name":"Write","tool_input":{"file_path":"reviews/__demo__/phase3/outputs/graph.final.json"}}' \
		| .claude/hooks/validate_graph.py && echo "      OK (exit 0)"
	@echo "[6/7] hooks: validate_bib on a non-review path (should noop)..."
	@echo '{"tool_name":"Write","tool_input":{"file_path":"src/something.py"}}' \
		| .claude/hooks/validate_bib.py && echo "      OK (exit 0)"
	@echo "[7/7] hooks: usage_log defensive (always exit 0)..."
	@echo '{"agent_type":"test","cwd":"/tmp"}' \
		| .claude/hooks/usage_log.py && echo "      OK (exit 0)"
	@echo ""
	@echo "All structural checks pass. Live LLM smoke is NOT covered — see README."
