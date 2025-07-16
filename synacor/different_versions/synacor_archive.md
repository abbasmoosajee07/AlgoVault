## Synacor Archive

With the original Synacor challenge site no longer available and the main archive containing only a single version of `challenge.bin`, I have collected and organized multiple versions of the challenge binary.

Each version is stored in its own subdirectory under `different_versions/`, and includes:

- `arch-spec`
- `challenge.bin`
- `README.md` containing:
  - The MD5 hash of the binary
  - A link to the GitHub repository where the version was sourced

### Verifying a Code

To verify the integrity of a `challenge.bin`, use the following command:

```bash
echo -n "<Code Here>" | md5sum
6fcd818224b42f563e10b91b4f2a5ae8 *-
````
echo -n "" | md5sum


### Challenge Codes
| Code No | Puzzle Code   |
|---------|---------------|
| 1       | Spec          |
| 2       | Running VM    |
| 3       | Self Test     |
| 4       | Use Tablet    |
| 5       | Lit Lantern   |
| 6       | Teleport(1)   |
| 7       | Teleport(2)   |
| 8       | Mirror        |
