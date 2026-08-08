# Memory Leak

Memory that's **allocated** (`malloc`) but **never freed** — and the pointer to it is **lost**, so it can never be freed or used again.

> **Analogy:** you check into a hotel room (`malloc`), then throw away the key without checking out (`free`). The room stays reserved forever — unusable, unreachable.

---

## Common causes

**1. Pointer goes out of scope before freeing**
```c
void createLeak() {
    int *ptr = malloc(sizeof(int));   // allocated
    *ptr = 10;
}   // ptr destroyed here — memory never freed, now unreachable
```

**2. Overwriting a pointer before freeing the old memory**
```c
int *ptr = malloc(sizeof(int));
ptr = malloc(sizeof(int));   // old block's address lost — leaked
```

---

## Why it matters

- Short programs: OS reclaims memory on exit, mostly harmless
- Long-running programs (servers, games): leaks **accumulate** → can exhaust memory → crash

---

## Fix

```c
int *ptr = malloc(sizeof(int));
*ptr = 10;
free(ptr);    // always pair malloc with free
ptr = NULL;   // avoid dangling pointer too
```

**Rule:** every `malloc` needs exactly one matching `free`.

---

## Leak vs Dangling Pointer

| | Memory Leak | Dangling Pointer |
|---|---|---|
| Cause | forgot `free()` / lost pointer | used pointer **after** `free()` |
| Effect | memory never released | memory released, pointer still points to it |
| Symptom | memory usage grows over time | garbage values / crashes |
