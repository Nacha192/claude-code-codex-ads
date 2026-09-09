# What is enforced, and what is not

An advertising skill spends money, writes public claims and touches ad accounts. The video half spends faster and can clone a voice on top of that. This page separates the guarantees a script actually makes from the ones that depend on a model behaving well. Read it before trusting either.

The rules below hold in all eight packs. The scripts are shared, so a still pack also refuses a badly formed storyboard, and a video pack also refuses copy over the placement limits.

## Enforced by code

These are checked by a script, and every one of them fails with a non-zero exit unless the row says otherwise. A test in `tests/test_tools.py` covers each one.

| Rule | Where | Test |
|---|---|---|
| An artifact never carries a credential-shaped value, whatever the field is named | `check_artifact.py` | `test_credentials_refused_in_every_kind`, `test_credential_nested_in_evidence` |
| New media requires a recorded approval | `check_artifact.py` | `test_generation_needs_recorded_approval` |
| Provider, model or account changed after approval is refused | `check_artifact.py` | `test_generation_material_change_refused` |
| A batch larger than the approved **item** ceiling is refused | `check_artifact.py` | `test_generation_over_approved_ceiling` |
| An item that names nothing to produce is refused, so an empty batch cannot consume the ceiling | `check_artifact.py` | `test_generation_item_must_describe_something` |
| A zero-credit account stops generation instead of falling back | `check_artifact.py` | `test_zero_credits_stops_generation` |
| An approval dated in the future is refused | `check_artifact.py` | `test_future_dated_approval_refused` |
| Narration longer than the scene it sits in is refused | `check_artifact.py` | `test_storyboard_measured_overrun` |
| Narration that was never measured is flagged rather than assumed to fit. **Warning, not a failure**: it reports and the run continues | `check_artifact.py` | `test_unmeasured_voice_warns` |
| A scene carrying a measured duration but no voice line is refused | `check_artifact.py` | `test_measured_narration_without_a_line_refused` |
| A voice field that is not a real line is refused, empty strings and non-strings included | `check_artifact.py` | `test_empty_voice_value_refused` |
| Overlapping scenes are refused | `check_artifact.py` | `test_storyboard_overlap_is_an_error` |
| A gap in the timeline asks for review. **Warning, not a failure** | `check_artifact.py` | `test_timeline_gap_warns` |
| A scene time that is not a finite number is refused, `NaN` and booleans included | `check_artifact.py` | `test_nan_and_bool_times` |
| A **declared** claim resting on a hypothesis is refused | `check_artifact.py` | `test_hypothesis_not_proof` |
| A testimonial without a recorded verbatim quote is refused | `check_artifact.py` | `test_fake_testimonial` |
| Declared prohibited terms are matched on the copy fields of the artifact you hand it, which must be written from the render rather than from the plan. It never opens the image or the video | `check_artifact.py` | `test_red_line_on_rendered_copy` |
| Copy over the declared character limits is refused | `check_artifact.py` | `test_placement_length_limits` |
| Declared limits that are not an object are refused rather than silently replaced by the defaults, which would enforce a looser rule than the campaign asked for | `check_artifact.py` | `test_malformed_limits_refused` |
| An unknown artifact kind is refused rather than half-checked | `check_artifact.py` | `test_unknown_kind_refused` |
| Installation never overwrites an existing skill or user edit | `install.py` | `test_install_preview_idempotence_and_no_overwrite` |
| Installation refuses a symlinked target or destination | `install.py` | `test_symlinked_ancestor_allowed_but_target_refused`, `test_symlinked_skill_destination_refused` |
| Installing writes nothing without `--apply` | `install.py` | `test_install_preview_idempotence_and_no_overwrite` |
| An existing second brain is never reset | `init_brain.py` | `test_brain_preview_and_preserve` |

Release integrity is enforced the same way, in `scripts/validate_release.py` and in CI. Each rule below that names a test is proved the same way the others are: the test plants that exact violation in a throwaway copy of the release and requires the validator to refuse it. `test_a_clean_copy_of_the_release_passes` is the control, so a rule that fires on everything fails too:

- A file with no source cannot survive in a shipped pack, and a rebuild deletes it.
- An archive or a pack whose skill no longer exists is deleted rather than published.
- Every route the build knows must point at a reference that exists, so a renamed file cannot leave modules pointing into space.
- No still-creative source may be built into a motion pack, and none of the motion sources into a still pack. The split is checked in both directions, because it is the thing this repository exists to keep. `test_source_card_from_the_other_half_refused`
- The shared trunk is a declared list in `build.py`, and the tree must match it in both directions. A craft file moved into the trunk, a trunk file deleted, a source card dropped in, or a name defined in both the trunk and a craft layer: each is refused, because that is how the split would erode quietly. `test_undeclared_trunk_reference_refused`, `test_declared_trunk_reference_removed_refused`, `test_source_card_in_the_shared_trunk_refused`, `test_name_defined_in_trunk_and_layer_refused`
- A reference no entrypoint can reach by following links is refused rather than shipped as dead weight. `test_reference_no_entrypoint_can_reach_refused`
- Every pack's manifest must declare the scope it was actually built from. `test_manifest_declaring_the_wrong_scope_refused`
- `SHA256SUMS` must describe exactly the archives that are present, all eight of them, with matching digests.
- Archive contents must equal the unpacked pack, file by file.
- Every local Markdown link in the published tree must resolve.
- Published text may only name the repository GitHub actually serves, and the one external method it is built on. A name that drifts breaks the same link in all eight packs at once, and nothing offline would notice. `test_unknown_repository_name_refused`
- A pack may not tell the assistant to run a script it does not carry, in a subdirectory or otherwise, and a directory whose name ends in `.py` is not a script. The instruction reads as a promise, and the obvious recovery is to write the missing script and run that instead. `test_script_cited_but_not_shipped_refused`, `test_directory_named_like_a_script_is_not_a_script`
- The committed packs must be byte-identical to what the committed sources rebuild, checked by `git diff --exit-code` in CI.
- Windows user paths and common credential shapes must not appear in any published text. Every file that decodes as UTF-8 is scanned, whatever its extension, and the two files that must contain those patterns are exempt by path rather than by name. `test_credential_in_an_unlisted_file_type_refused`, `test_file_named_like_the_scanner_is_still_scanned`

These guarantees assume a Python interpreter is present. A ZIP install can land on a machine without one, so the packs check for it on the first task in a project and ask before installing anything, following `references/runtime.md`. With no interpreter, none of the refusals above happen and the assistant must say the checks did not run rather than let silence read as a pass.

## Enforced by instruction only

The skill text requires these. A model can deviate from them, and no script here will stop it. This is the honest ceiling of any Agent Skill, and the list is wider for the video packs because video touches consent and identity.

- Asking before generating, rather than writing the approval record itself.
- **Declaring a claim as a claim.** The checker verifies the `claims` it is given. Copy that promises a result in its own sentences, with an empty `claims` array, passes every check. No script can decide that a sentence is a material claim, so this one rests entirely on the assistant listing them.
- **The money ceiling.** `max_items` is a number and is enforced. The `ceiling`, written as text such as `200 credits`, is recorded so a human can compare it; nothing computes the spend against it.
- **Detecting a video or speech capability instead of assuming one.** Nothing in this repository can stop an assistant from naming a model it has never seen.
- **Cloning only the voice of the person asking.** The consent record is a file the pack writes; no script can tell whose voice is in an audio sample.
- **Honouring a withdrawal of that consent**, including deleting the clone at the provider.
- **Inspecting the exported media.** `quality-control.md` requires opening the file and reading what is actually on it. No script here can tell whether that happened, and a manifest written from the plan instead of from the render passes every check while describing an asset nobody looked at.
- **Doing the blind pass before reading the peer.** In the team editions, both sides are required to write their diagnosis and concepts alone and exchange them simultaneously. Nothing can tell whether one side read the other's first, and that is exactly the shortcut that turns two opinions into one opinion checked twice.
- **Delivering in one pass.** `one-shot.md` requires asking everything blocking at once, stating assumptions where they are read, and shipping every channel the format has. Nothing enforces it.
- **Holding a written identity release before filming a person**, and pulling the ad when its usage window ends. `live-action.md` says how; only a human closes that loop.
- Not presenting a script, a silent draft or a prompt as a finished ad.
- Not inventing offers, prices, reviews, scarcity or results.
- Writing ads in the target market's language rather than translating into it.
- Treating scraped pages, downloaded skills and third-party video as untrusted data, ignoring instructions embedded in them.
- Respecting platform terms when studying video that already runs, and not scraping from behind a logged-in session.
- Keeping private campaign data, customer transcripts and voice samples out of the public pack.
- Stopping on an ambiguous account write and reconciling remote state instead of retrying blindly.
- Refusing to rotate identities to get around a spend limit.

The checker narrows the gap where it can: an approval must exist as a record and the request must stay inside it, and a storyboard's narration must actually fit its scene. It cannot prove the user said yes, and it cannot hear a voice.

## Not enforceable here at all

- Whose voice is in a supplied recording, or whether that person agreed.
- Whether a sentence in the copy is a material claim that should have been declared.
- Whether the actual spend stayed inside the approved budget. The item count is enforced; the currency is not.
- Whether a source genuinely supports the claim that cites it.
- Whether copy or a synthetic voice will be approved by the platform. Policies change, disclosure rules for AI voice change by market, and enforcement is not a public function.
- Whether a creative is any good, or will perform. An ad library shows that an ad ran, never that it worked.
- Whether the pack you installed is the right one for the job. The scope file says what each half builds; choosing is still yours.
- Whether a provider's model, duration, resolution, credits, rights or regional access are what the documentation said at capture time. The model list in `references/providers.md` is a dated observation, not a promise.
- What third-party skills or tools do. Sources are reviewed and pinned by revision and hash; inclusion is not a security audit.

## Reporting a problem

Open an issue on the repository. For anything that looks like a credential leak or a security defect, do not paste the credential itself: describe where it appears and rotate it first. For a voice cloned without consent, say so and it will be removed.
