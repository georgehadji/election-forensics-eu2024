Architecture Rationale

The architecture is designed around failure modes, not around specific model brands.

Distinct components are assigned to minimize correlated errors:
- Reasoning and formal derivation are separated from narrative construction.
- Writing and refactoring are separated from logical and numerical verification.
- Cross-checking and redundancy detection are handled independently.

Model assignments are substitutable in principle.
The critical constraint is functional separation, not vendor identity.

This architecture is intentionally over-specified relative to a single case study.
The objective is not minimalism, but repeatability across elections, countries, and datasets.

The same pipeline can be reused without redesign, reducing methodological drift across studies.
