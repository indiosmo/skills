# Apply gain

Build and run the sample from the fixture root with a C++17 compiler:

```sh
c++ -std=c++17 -Iinclude examples/gain.cpp -o /tmp/documentation-gain-example
/tmp/documentation-gain-example
```

## Verify the result

The program prints `0.5` and exits with status `0`.

!!! note "Linear gain"
    The gain factor multiplies the sample amplitude.

Read the [overview](index.md) for the signal flow diagram.
