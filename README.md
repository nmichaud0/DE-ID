# DE-ID — Multilingual Audio De-Identification (Summary)

**What this is:** A practical way to anonymize conversational audio so it can be shared safely. The aim is to remove or mask anything that could reveal who is speaking, while preserving as much scientific value as possible.

**Why:** Datasets with real patients are valuable for research but can’t be released if a listener could infer a person’s identity. The project follows the spirit of the *18 HIPAA identifiers* as a concrete checklist to decide what must be censored.

**Key constraint:** Conversations are multilingual and may switch language mid-sentence. Methods must be language-agnostic and robust to code-switching.

---

## What “de-identification” means here

* Take natural conversation audio.
* Find words or short spans that carry personal identifiers.
* Censor only those moments (mute/bleep/replace), not whole sentences.
* Public figures are **not** treated as exempt; name mentions can still enable re-identification when combined with place/time context.

---

## Policy baseline (HIPAA-informed)

**Identifiers we target in audio/transcripts**

1. Names
2. Addresses below state (street, city, ZIP, etc.)
3. Dates related to an individual (day/month; year alone is allowed)
4. Telephone and fax numbers
5. Email addresses
6. Numbers tied to identity (SSN, medical record, health plan beneficiary, account, license, etc.)
7. Any other unique characteristic that could identify someone

**Identifiers left out (unlikely in speech or not removable by audio edits)**

* Vehicle identifiers
* Device identifiers / serial numbers
* Web URLs
* IP addresses
* Fingerprints or *voiceprints*
* Photographic images

> Note: voice identity itself is not “removed” by mild audio processing; releasing raw voices can still be identifying.

---

## Approach (high level)

1. **Transcribe first.** Use speech-to-text with word-level alignment so single words can be removed precisely.
2. **Run two complementary passes over the transcript:**

   * **Rule-based:** deterministic patterns and tags (e.g., person names, fine-grained locations, dates, emails, phone formats, ID-like numbers). Easy to audit; behaves the same every time.
   * **LLM-driven:** a context-aware pass that judges each word in its sentence window as “safe” or “sensitive” according to the HIPAA list. Better at subtle, multilingual cases, but less predictable and needs careful review.
3. **Produce a list of timestamps to censor** and apply minimal edits to the audio to preserve content outside sensitive spans.

---

## What was tried and dropped

* **Semantic embeddings & clustering** (projecting words/contexts into multilingual embedding space and measuring distances to prebuilt “sensitive” clusters) did **not** separate sensitive from non-sensitive reliably. Distributions overlapped too much, even with context. Without large supervised training data per language, this path was not promising.

---

## Evaluation plan (pragmatic)

* Generate **fake conversations** that mimic the real data, including code-switching.
* **Annotate** sensitive words (human + model-assisted).
* Translate and remix to test multilingual behavior.
* Report simple **classification metrics** (accuracy/precision/recall/F1) at the word level, plus confusion matrices and examples of misses (e.g., local place names or multi-word entities).

---

## Limitations & cautions

* No automatic system can guarantee perfect de-identification. **Human review is recommended** before any release.
* **Voice identity remains** in raw audio; this project focuses on textual identifiers aligned to audio.
* Legal duties vary by jurisdiction (e.g., GDPR). This is research tooling, **not legal advice**.

---

## Current direction

* Favor a **hybrid** strategy: use rules for precision and LLM judgments for recall, with a simple policy to combine them.
* Keep edits **surgical** (word-level spans with small safety padding) to maximize data utility.
* Continue improving multilingual coverage and reduce false positives/negatives through clearer instructions and better examples.
