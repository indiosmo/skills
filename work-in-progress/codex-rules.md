add rules for basic allowed commands like ls, cat, etc so we don't get asked all the time.

project specific rules

```
prefix_rule(
    pattern = ["./build.sh"],
    decision = "allow",
    justification = "Trusted project build entrypoint",
    match = [
        "./build.sh",
        "./build.sh test",
        "./build.sh --release",
    ],
)
```
