Wrappers for Python standard library that enable fuzzing of various
modules with [python-afl](https://github.com/jwilk/python-afl).

## Purpose

Fuzzing augments the regular human driven testing processes by
generating inputs that usually catch the corner cases that test
writers miss. The goal of this repository is to search for following
behaviors:

* To find internal implementation issues. These show up as functions
  in various modules throwing undocumented exceptions and making life
  harder for all users of such functions. Especially as catch-all
  exception handlers are generally shunned upon.
* To catch infinite loops or other undesired behaviors where a tiny
  amount of data can result in large processing time
  requirements. Unless such things are explicitly documented, as
  [in the case of XML parsing modules](https://docs.python.org/3/library/xml.html#xml-vulnerabilities).
* To catch large memory allocations with tiny amount of data. Large
  memory allocations are quite undesirable for long-running processes,
  especially if the amount of processed data is small. The virtual
  memory limit for each fuzz target is set to 200 megabytes.
* Some modules provide the same implementation in pure Python and in
  more optimized C. If there are any differences in implementation
  that are not explicitly documented, they should show up as different
  results from the calculation that these modules perform.

## Pre-requisites

These wrappers require to have
[american fuzzy lop](http://lcamtuf.coredump.cx/afl/),
[python-afl](https://github.com/jwilk/python-afl), and their
pre-requisites installed. Also the wrapper shell scripts are written
in [bash](https://www.gnu.org/software/bash/) and they are only
expected to work on GNU/Linux based systems. No BSD, Windows, or macOS
support is provided.

## Usage

This provides wrapper scripts for the most used operations that are
involved in fuzzing. This provides 200 megabyte virtual memory limit
for each Python instance, so any large memory allocations will result
in MemoryError exception to be thrown.

A fuzz target for a specific Python standard library module is
expected to provide `fuzz.py` file that includes calls required by
`python-afl` and a seed corpus at `<target>/in` directory that
consists of at least one file that the fuzz target is expected to
successfully process. `fuzz.py` takes 1 parameter that is the current
input file name.

The usual sequence of commands is following:

```bash
$ ./test.sh target-name
# Start possibly multiple afl-fuzz sessions in tmux or screen:
$ ./run.sh target-name
# If there are any crashes found, collect the initial list under
# <target-name>/crashes-raw/ directory. You can keep fuzzing sessions
# running while analyzing crashes.
$ ./crashes.sh target-name
# Further deduplicate and minimize the found crashes to
# <target-name>/crashes/ directory.
$ ./py-afl-tmin-crashes.sh target-name
# Create a seed corpus from the previous corpus and new non-crashing
# inputs.
$ ./corpus.sh target-name
# Minimize the files inside the corpus. This is very expensive
# operation with no execution avoidance.
$ ./py-afl-tmin-corpus.sh target-name
```

Then if any bugs are found and there is a supposed fix for them, one
can run some regression tests to catch the remaining issues:

```bash
$ ./regression.sh target-name
```

### Crashes

The scripts that process these crashes do some rudimentary stack
backtrace normalization and crash deduplication in addition to what
`py-afl-fuzz` does by default. The crash files are initially named by
the checksum of the stack backtrace but can be then symbolically
linked to the issue ID number that bug reports from
[Python bug tracker](https://bugs.python.org/) generate.

If a fuzz target is resulting in needless exceptions and the failures
that can result from invalid inputs are allowed, then the fuzz target
should be modified to just ignore such exceptions. Of course invalid
function calls or call sequences in fuzz targets should be fixed.
