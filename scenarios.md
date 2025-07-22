# SCR Scenarios

## Rules
* Never-alone means
  * any 2 committers from a branch approve PR, or a 3rd person 

      
## Open questions
* Who is part of the approved list for a specific repository? Is this in-scope for Kosli?
  * need to understand what's possible within the constraints of Github / Bitbucket etc.
  * From the existing control's perspective, it doesn't matter M
* How are service accounts treated?
* 

## A simple pull-request

Git graph:

```
* c1 - Faye
|\
| * c2 - Sami
|/
* c3 - Sami - merge commit -[PR #1 Authored by Sami, Approved by Faye]
```

PR #1 covers `[c2]`

The current baseline commit is: `c1`

=> Checking for never-alone-review evidence for `c1..c3` 

```
c2 - Sami (reviewed by Faye in PR #1)
c3 - Sami (result of merging PR #1 reviewed by Faye)
```

## A squashed pull-request merge

Git graph
```
* c1 - Faye
|\
| * c2 - Sami
|
* s3 - Sami - squash commit -[PR #1 Authored by Sami, Approved by Faye]
```

PR #1 covers `[c2]`

The current baseline commit is: `c1`

=> Checking for never-alone-review evidence for `c1..s3` 

```
s3 - Sami (result of merging PR #1 reviewed by Faye)
```

## A squashed pull-request merge (with multiple commits)

Git graph
```
* c1 - Faye
|\
| * c2 - Jacob
| |
| * c3 - Sami
|
* c4 - Sami - squash commit -[PR #1 Authored by Sami, Approved by Jacob]
```

PR #1 covers `[c2,c3]`

The current baseline commit is: `c1`

=> Checking for never-alone-review evidence for `c1..c4` 

```
c4 - Sami (result of merging PR #1 reviewed by Jacob) => non-compliant
```

-> Is result compliant / **non-compliant**?

## Trunk based

Git graph
```
* c1 - Faye
|
* c2 - Sami
|
* c3 - Jacob
|
* c4 - Mohan
|
* c5 - Mohan
```

The current baseline commit is: `c1`

=> Checking for never-alone-review evidence for `c1..c5` 

```
c2 - Sami (no evidence) => non-compliant
c3 - Jacob (no evidence) => non-compliant
c4 - Mohan (no evidence) => non-compliant
c5 - Mohan (no evidence) => non-compliant
```


## Multiple committers on merge commit  - Committers as approver

Git graph:

```
* c1 - Faye
|\
| * c2 - Sami
| |
| * c3 - Faye
|/
* c4 - Sami - merge commit -[PR #1 Authored by Faye, Approved by Sami]
```

PR #1 covers `[c2,c3]`

The current baseline commit is: `c1`
=> Checking for never-alone-review evidence for `c1..c4` 
```
c2 - Sami (...)
c3 - Faye (...)
c4 - Sami (...)
```
 
## Multiple committers on merge commit - PR author as approver?

Git graph:

```
* c1 - Faye
|\
| * c2 - Sami
| |
| * c3 - Faye
|/
* c4 - Sami - merge commit -[PR #1 Authored by Sami, Approved by Sami]
```

PR #1 covers `[c2,c3]`

The current baseline commit is: `c1`
=> Checking for never-alone-review evidence for `c1..c4` 
```
c2 - Sami (...)
c3 - Faye (...)
c4 - Sami (...)
```

## Multiple committers on merge commit - PR author not a committer?

Git graph:

```
* c1 - Faye
|\
| * c2 - Sami
| |
| * c3 - Faye
|/
* c4 - Jon - merge commit -[PR #1 Authored by Jon, Approved by Jon]
```

PR #1 covers `[c2,c3]`

The current baseline commit is: `c1`
=> Checking for never-alone-review evidence for `c1..c4` 
```
c2 - Sami (...)
c3 - Faye (...)
c4 - Jon (...)
```


## Multiple committers on merge commit - multiple approvers (no one else left to approve)?

Git graph:

```
* c1 - Faye
|\
| * c2 - Sami
| |
| * c3 - Faye
| |
| * c4 - Jon
|/
* c5 - Jon - merge commit -[PR #1 Authored by Sami, Approved by Jon, Faye]
```

PR #1 covers `[c2,c3,c4]`

The current baseline commit is: `c1`
=> Checking for never-alone-review evidence for `c1..c5` 
```
c2 - Sami (...)
c3 - Faye (...)
c4 - Jon (...)
c5 - Jon (...)
```


## Pull request is approved but branch is merged manually



## Squash commits locally 


## Hotfix branch

Git graph
```
* c1 - Faye
|\
| * c2 - Jacob
| |
| * c3 - Sami
*c4
```

check `c1..c3`