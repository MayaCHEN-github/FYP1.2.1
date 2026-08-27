**Language:** English · [简体中文](../../zh-CN/modules/detection.md) · [繁體中文（香港）](../../zh-HK/modules/detection.md)

# Detection layer

Evidence: unless noted, confirmed against current source.

## Plain-language model

After the model finishes, this layer answers two questions:

1. **Did it leak?** Does the output contain real field values from `database.json` (name, ID number, phone, …)?
2. **Did it refuse?** Does the output contain refusal phrasing such as 「不能」「无法」「不提供」?

Batch tests combine leak + refusal into a defense-oriented confusion matrix. The Gradio demo only shows regex leak detection.

## Code model

Implementation: [`utils/jailbreak_detector.py`](../../../utils/jailbreak_detector.py).

### Leak detection

| Class | Mechanism | Used by |
| --- | --- | --- |
| `JailbreakDetector` | GPT-3.5-instruct semantic judge with a long system prompt | Base class; not on the main path |
| `RegexJailbreakDetector` | `re.search` on each record field | `app.py`, `leak_test.py` |

`RegexJailbreakDetector.detect` returns:

- `contains_leak`: true if the first record is complete, the whole store is complete, or any field hits
- `result`: Chinese description of leak scope
- `confidence`: always `High`

### Refusal detection

| Class | Mechanism | Used by |
| --- | --- | --- |
| `RegexRefusalDetector` | OR of 18 Chinese refusal words | Implemented; **not** used by `leak_test.py` |
| `ModelRefusalDetector` | `qwen-72b` structured Yes/No | `leak_test.py` |

`ModelRefusalDetector` constructs a fresh `ModelManager` per call, streams the full reply, then parses the `Detection Result:` line.

### Tie-in to the confusion matrix

[`leak_test.py`](../../../leak_test.py) `calculate_confusion_matrix` maps each trial to TP/FP/TN/FN (defense view). See [confusion-matrix definition](../references/confusion-matrix.md).

## Next

- How metrics are printed and saved: [batch testing](batch-testing.md)
- Cell definitions: [confusion matrix](../references/confusion-matrix.md)
