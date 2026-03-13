# List of features

Once these list will become less numerous, it should be migrated to github issues.

## Milestones

All tasks under milestone name should be completed prior to this release.

### Beta-release blockers

* Refactor lookup logic
  * Better realign logic parts
  * Fetch one level of subpages (e.g. `en-woman` article)
  * Fetch one level of derived forms (e.g. `drive` for `driving`)
* Start extracting either IPA or sounds
* Create binaries in Gitlab CI
* Progress bar for lookup in statusbar / overview
* Show indicator that deck has unsaved changes and track all of them
* Show prompt when deck is being unloaded with unsaved changes
* Words lookup by button
* Overview table sorting per column
* Find proper icons set
* 75% tests coverage
* See if Wiktionary API can be migrated to REST version

### Stable release blockers

* Create separate release with optimization flags
* Settings page
* Write log file
* Allow setting log verbosity in settings
* Highlight current row with different color if input is not valid
* Highlight full duplicates in overview table
* Update icons and stuff
* Allow switching search mode from immediate to shortcut
* Refine UI
* Full support for German language words lookup
    * Meaning notes
* Full support for English language words lookup
    * Meaning notes
* `stable` branch
* Automated release version update? Or at least checklist for the new release.
* Automated tests and releases for `stable`
* 90% tests coverage
* Download instructions in [README](README.md)
* Proper description in [README](README.md)
* Check .json version on read
* Undo/Redo for card operations

### Future features

* Deduplication mode
* Support for Russian language words lookup
* Pronunciation / IPA
* Way to customize shortcuts
    * Do not allow duplicate shortcuts
