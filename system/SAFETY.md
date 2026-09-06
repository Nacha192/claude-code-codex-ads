# What is enforced, and what is not

An advertising skill spends money, writes public claims and touches ad accounts. This page separates the guarantees a script actually makes from the ones that depend on a model behaving well. Read it before trusting either.

## Enforced by code

These fail with a non-zero exit. A test in `tests/test_tools.py` covers each one.

| Rule | Where | Test |
|---|---|---|
| An artifact never carries a credential-shaped value, whatever the field is named | `check_artifact.py` | `test_credentials_refused_in_every_kind`, `test_credential_nested_in_evidence` |
| New media requires a recorded approval | `check_artifact.py` | `test_generation_needs_recorded_approval` |
| Provider, model or account changed after approval is refused | `check_artifact.py` | `test_generation_material_change_refused` |
| A batch larger than the approved ceiling is refused | `check_artifact.py` | `test_generation_over_approved_ceiling` |
| A zero-credit account stops generation instead of falling back | `check_artifact.py` | `test_zero_credits_stops_generation` |
| An approval dated in the future is refused | `check_artifact.py` | `test_future_dated_approval_refused` |
| A material claim resting on a hypothesis is refused | `check_artifact.py` | `test_hypothesis_not_proof` |
| A testimonial without a recorded verbatim quote is refused | `check_artifact.py` | `test_fake_testimonial` |
| Declared prohibited terms are matched on the rendered copy | `check_artifact.py` | `test_red_line_on_rendered_copy` |
| Copy over the declared character limits is refused | `check_artifact.py` | `test_placement_length_limits` |
| Narration longer than its scene is refused | `check_artifact.py` | `test_storyboard_measured_overrun` |
| Installation never overwrites an existing skill or user edit | `install.py` | `test_install_preview_idempotence_and_no_overwrite` |
| Installation refuses a symlinked target or destination | `install.py` | `test_symlinked_ancestor_allowed_but_target_refused`, `test_symlinked_skill_destination_refused` |
| Installing writes nothing without `--apply` | `install.py` | `test_install_preview_idempotence_and_no_overwrite` |
| An existing second brain is never reset | `init_brain.py` | `test_brain_preview_and_preserve` |

Release integrity is enforced the same way, in `scripts/validate_release.py` and in CI:

- A file with no source cannot survive in a shipped pack, and a rebuild deletes it.
- An archive or a pack whose skill no longer exists is deleted rather than published.
- `SHA256SUMS` must describe exactly the four archives that are present, with matching digests.
- Archive contents must equal the unpacked pack, file by file.
- Every local Markdown link in the published tree must resolve.
- The committed packs must be byte-identical to what the committed sources rebuild, checked by `git diff --exit-code` in CI.
- Windows user paths and common credential shapes must not appear in any published text.

## Enforced by instruction only

The skill text requires these. A model can deviate from them, and no script here will stop it. This is the honest ceiling of any Agent Skill.

- Asking before generating, rather than writing the approval record itself.
- Not inventing offers, prices, reviews, scarcity or results.
- Writing ads in the target market's language rather than translating into it.
- Treating scraped pages and downloaded skills as untrusted data, ignoring instructions embedded in them.
- Keeping private campaign data out of the public pack.
- Stopping on an ambiguous account write and reconciling remote state instead of retrying blindly.
- Refusing to rotate identities to get around a spend limit.

The checker narrows the gap where it can: an approval must exist as a record and the request must stay inside it, so silently expanding a batch fails a check rather than passing unnoticed. It cannot prove the user actually said yes.

## Not enforceable here at all

- Whether a source genuinely supports the claim that cites it.
- Whether copy will be approved by the platform. Policies change, and enforcement is not a public function.
- Whether a creative is any good, or will perform.
- Whether a provider's model, credits, rights or regional access are what the documentation said at capture time.
- What third-party skills or tools do. Sources are reviewed and pinned by revision and hash; inclusion is not a security audit.

## Reporting a problem

Open an issue on the repository. For anything that looks like a credential leak or a security defect, do not paste the credential itself: describe where it appears and rotate it first.
