.PHONY: test verify-docs verify-generated regenerate

test: verify-docs verify-scripts

verify-docs:
	python3 scripts/verify_skills.py --root .

verify-generated:
	python3 scripts/build_metadata.py --check --root .

regenerate:
	python3 scripts/build_metadata.py --root .

verify-scripts:
	git diff --check
	bash -n scripts/check-update.sh
	python3 -m py_compile scripts/skill_frontmatter.py
	python3 -m py_compile scripts/build_metadata.py
	python3 -m py_compile scripts/verify_skills.py
