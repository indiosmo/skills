# Audio buffers: name the quantity before its unit

A developer describes a callback configuration: "The buffer size is 480, the
sample rate is 48,000, and stereo is enabled. Can I call the computed value
`latency_ms`?" The intended calculation divides 480 by 48,000. This is a direct
naming request based on a description; the application implementation and device
measurements have not been supplied.

## Establish the contract

The first useful question is what 480 counts. In this original scenario the
developer confirms that it counts frames, with one sample per channel in each
frame. Stereo therefore supplies 960 scalar samples in the buffer. The displayed
quantity is the duration of that buffer's audio at the configured sample rate.
There is no measured input-to-output interval in the supplied description.

PortAudio's V19 API distinguishes `sampleRate`, `channelCount`, and
`framesPerBuffer`. Its frame and latency terminology supports this distinction;
the supplementary V18 latency discussion has a narrower historical scope.
See the [accepted source and scope](../references/sources.md#con-portaudio) and
[quantity evidence](../references/evidence.md#con-011).

The naming brief is now precise: name an integer frame count, a scalar sample
rate, and a calculated scalar duration in a settings presenter. Readers see the
values together, but logging also prints the duration independently. The
scenario adopts full words and snake_case for local identifiers. Typed duration
objects remain a possible future representation, requiring a separate design
decision.

## Select names in use

Illustrative pseudocode for the described calculation:

```text
buffer_frames = 480
sample_rate_hz = 48000
channel_count = 2
buffer_sample_count = buffer_frames * channel_count
buffer_duration_seconds = buffer_frames / sample_rate_hz
display_buffer_duration(buffer_duration_seconds)
```

| Candidate for the calculated scalar | Reading at the use site | Decision |
| --- | --- | --- |
| `buffer_duration_seconds` | Duration represented by the buffer, expressed in seconds | Recommend |
| `buffer_duration_ms` | Duration expressed in milliseconds | Would require multiplying the current result by 1,000 |
| `latency_ms` | A latency interval expressed in milliseconds | Requires both a different unit and an established latency boundary |

`buffer_duration_seconds` is the clear winner for the supplied scalar contract:
the calculation establishes both duration and seconds. The candidates identify
substantive quantity questions that the initial request left open. Changing the
formula to make another candidate fit would enlarge the task.

Keep `buffer_frames` for the count. `buffer_size_samples` could lead a stereo
reader to expect 960 where the configuration requires 480. In a typed interface,
the following alternate representation could make a shorter member name clear:

```text
AudioBuffer.duration: Duration
AudioBuffer.frame_count: FrameCount
```

This is illustrative type pseudocode. A `Duration` type whose display conversion
supplies units changes the naming context; the present scalar recommendation
applies to the first representation. See
[units and typed context](../references/variables-and-state.md).

## Review the recommendation separately

The review revisits the source vocabulary, the stipulated configuration, the
formula, the isolated display call, and a mono/stereo boundary comparison.
Independent exact arithmetic gives:

| Frames | Sample rate in hertz | Channels | Scalar samples | Buffer duration in seconds |
| --- | --- | --- | --- | --- |
| 480 | 48,000 | 1 | 480 | 0.010 |
| 480 | 48,000 | 2 | 960 | 0.010 |
| 960 | 48,000 | 2 | 1,920 | 0.020 |

The unchanged duration when channels increase supports `buffer_frames` as the
numerator. Doubling frames doubles duration. The resulting 0.010 seconds equals
10 milliseconds, so the unconverted scalar also rejects a millisecond suffix.
These calculations were checked with Python's standard-library exact fractions;
the pseudocode itself was reviewed as a description, not executed as an API.

Outcome: recommend `buffer_duration_seconds`, with `buffer_frames`,
`sample_rate_hz`, and `channel_count` preserving the input quantities. Confidence
covers this description and arithmetic. Adopting the names in a real application
requires inspecting the parser, callback arguments, display conversion, and
representative logs. Any measured latency field needs its measurement endpoints
and timing evidence before naming. Human acceptance remains pending.
