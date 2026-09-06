# Check the workshop sample before a session

The training coordinator uses this fictional Text Workshop procedure to confirm
that the prepared sample still produces the agreed count. The
[fixture policy](evidence/README.md) requires a result of 2.

## Preconditions

Use the reviewed fixture checkout, Bash 4.4 or later, wc and cat. Run commands
from this document's directory with read access to the sample.

## Procedure

1. Inspect the sample:

   ```bash
   cat evidence/sample.txt
   ```

   Expect alpha and beta on separate lines.

2. Run the acceptance count:

   ```bash
   bash evidence/count_lines.sh evidence/sample.txt
   ```

   Expect 2 and a successful exit status.

## Recover or escalate

If the input diagnostic appears, confirm the checkout path and read access,
then retry. If the count differs from 2, stop preparation and preserve the sample.
The training coordinator compares it with the reviewed checkout before the
exercise resumes. The [policy](evidence/README.md) assigns that recovery decision
to the coordinator. Successful read-only checks leave the sample ready to use.
