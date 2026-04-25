# Anderson — convenience targets.
#
#   make help        — list targets
#   make install     — pip install -r requirements.txt
#   make demo        — render the bundled demo paper end-to-end
#   make demo-clean  — remove the regenerated demo review tree
#   make graph       — re-render graph HTML for REVIEW=<dir>
#   make stats       — re-render STATS.md  for REVIEW=<dir>
#   make highlight   — re-render highlighted PDF for REVIEW=<dir>
#
# Per-review targets pass REVIEW=<path>:
#   make stats REVIEW=reviews/my-paper

.PHONY: help install demo demo-clean graph stats highlight

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
