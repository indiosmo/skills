# Explore newline counts

In this fictional Text Workshop activity, you will inspect a sample and compare
its count with an empty file. You need a terminal, Bash 4.4 or later, wc and cat,
and the checked-in samples. Run commands from this document's directory.

## Inspect the prepared sample

Run:

```bash
cat evidence/sample.txt
```

The output has alpha on the first line and beta on the second.

## Count the sample

Run the workshop counter:

```bash
bash evidence/count_lines.sh evidence/sample.txt
```

The count is 2. Each prepared line ends with a newline.

## Try an empty file

Run:

```bash
bash evidence/count_lines.sh evidence/empty.txt
```

The count is 0. You have observed the counter on two prepared inputs.

Continue with the [multipart activity](multipart-tutorial/index.md) to compare
a sample whose final text has no terminating newline. All activities read the
prepared samples; the checkout remains ready for another attempt.
