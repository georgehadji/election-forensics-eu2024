Repository rules (non-negotiable):

- data/raw is read-only and never modified.
- All data transformations go to data/processed.
- All code lives in methods/ or pipelines/.
- experiments/ contains configurations and outputs, not logic.
- No analysis is considered valid unless reproducible via pipelines.
- Notebooks are allowed only for inspection, never as canonical sources.
