# List of features

Once these list will become less numerous, it should be migrated to github issues.

## Milestones

All tasks under milestone name should be completed prior to this release.

### Alpha-release blockers

* Inputs table
    * Multiline table, filled by lookup. Always has at least one row for users input.
    * Row can be submitted with input row removed
    * Row can be submitted without input row removed
    * Can be cleaned completely
    * Question or answer word can be looked up
    * If answer is being looked up, it should be cut to the nearest line break.
    * Highlight the first row to indicate it is a filter row
* Overview table
    * Multiline table, contains current deck data. First row of an input can be used as a filter.
    * Rows can be removed
    * Rows can be altered in place
    * Rows can be moved to the input, to create altered version or to look them up. Focus is also moving to the input
      table.
* Finalize set of shortcuts and way to display them
* Proper lookup from answer
* Proper lookup from question
* Settings page

### Beta-release blockers

* Show prompt when app is being closed with unsaved changes
* Show indicator that deck has unsaved changes
* Show prompt when deck is being unloaded with unsaved changes
* Simple words deduplication
* Immediate words lookup
* Words lookup by button
* Automated tests for `master`
* 75% tests coverage

### Stable release blockers

* Refine UI
* Support for German language words lookup
* Support for English language words lookup
* `stable` branch
* Automated release version update? Or at least checklist for the new release.
* Automated tests and releases for `stable`
* 90% tests coverage
* Download instructions in [README](README.md)
* Proper description in [README](README.md)

### Future features

* Support for Russian language words lookup
* Pronunciation
* Way to customize shortcuts
