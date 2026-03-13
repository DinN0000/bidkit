# Quality Criteria

Verification checklist defining "top-tier SI firm" quality for each category of proposal content. Critics and the Overseer use these criteria to decide whether an SSOT section passes or requires revision.

## Product Specifications

- Model names with exact vendor part numbers.
- Quantities tied to sizing calculations (not arbitrary).
- Throughput / TPS figures with cited source or test basis.
- Certifications listed where applicable: CC EAL4+, FIPS 140-2, KCMVP, etc.
- End-of-sale / end-of-support dates included for time-sensitive products.

## Solution Architecture

- Complete component list — nothing referenced elsewhere that is missing here.
- Installation targets (physical hosts, VMs, containers) explicitly mapped.
- License policies stated: per-core, per-node, per-user, subscription term.
- High-availability and disaster-recovery topology described.

## Platform Details

- Feature comparison tables with clear yes/no or version-gated indicators.
- Pricing breakdown: perpetual vs. subscription, with annual maintenance costs.
- Total Cost of Ownership (TCO) calculation covering at least 3- and 5-year horizons.
- Scalability limits and upgrade paths documented.

## Implementation Plans

- Milestone timelines with calendar-realistic durations.
- Staged rollout plan: pilot -> partial -> full, with go/no-go criteria per stage.
- Rollback procedures for each stage.
- Resource requirements: team size, skill sets, client-side dependencies.

## Reference Cases

- Delivery history entries include: project name, client name, contract period, delivery date.
- Current usage status: active / decommissioned / migrated.
- Quantified outcomes where available (e.g., "reduced incident response from 4h to 30min").

## Maintenance and Support

- Support conditions: business-hours vs. 24/7, on-site vs. remote.
- SLA metrics: response time, resolution time, availability percentage.
- EOL/EOS policy with migration path for expiring products.
- Patch and update cadence.

## Regulatory Compliance

- Financial security guidelines referenced by clause number.
- Network separation requirements mapped to architecture diagrams.
- Data classification and handling rules addressed.
- Audit trail and logging requirements satisfied.
