# DCBD Assignment — RPC MapReduce

This project is part of the _Distributed Computing and Big Data_ course at CMI. The goal was to implement a simple MapReduce pipeline using Python and multiprocessing, where the input data is fetched from a remote server via RPC.

## Problem Overview

We are given access to publication metadata stored on a remote server. Each publication file (`pub_0.txt` to `pub_999.txt`) contains a title. The task is to:

- Retrieve all titles using the provided RPC endpoints
- Extract the **first word** from each title
- Count the frequency of these first words
- Output the **top 10 most frequent first words**
- Verify the result using the server

## Approach

The solution follows a basic MapReduce structure:

### Map Phase

- The list of filenames is split into chunks
- Each worker process:
  - Logs in to obtain a secret key
  - Fetches titles for its assigned files
  - Extracts and cleans the first word
  - Maintains a local frequency count

### Reduce Phase

- The counters from all workers are merged
- Final frequencies are computed

### Output

- The top 10 most frequent first words are selected
- These are sent to the `/verify` endpoint for scoring

## Notes on Implementation

- Used `multiprocessing.Pool` to parallelize the workload
- Handled API throttling (429 errors) with retry + delay
- Cleaned first words by removing punctuation but kept original casing (important for correctness)
- Each worker uses its own login session to avoid conflicts

## How to Run

### Locally

```bash
pip install -r requirements.txt
python main.py
```

### Using Docker

```bash
docker build -t dcbd-assignment .
docker run dcbd-assignment
```

## Expected Output

The program should print the top 10 words and a verification response like:

```
{'score': 10, 'total': 10, 'correct': True}
```

## Files Included

- `main.py` — main implementation
- `requirements.txt` — dependencies
- `Dockerfile` — container setup
- `output_screenshot.png` — Codespaces execution proof

## Final Remarks

Tested both locally and on GitHub Codespaces.

---
