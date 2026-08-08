# Dangling Pointer

A **dangling pointer** is a pointer that still holds the address of a memory location that has already been **freed**, **deallocated**, or gone **out of scope** — so it's pointing to memory that's no longer valid, but the pointer itself doesn't know that.

> **Analogy:** imagine you write down someone's hotel room number, but they check out and someone else moves in later. Your note (the pointer) still says "Room 204" — but the room's contents have completely changed. If you walk in expecting the original person's stuff, you'll find garbage (or someone else's data) instead.

---

## Three common ways dangling pointers happen

### 1. Pointing to a freed heap variable

```c
int *ptr = malloc(sizeof(int));
*ptr = 10;
free(ptr);        // memory is freed
// ptr is now dangling — it still holds the old address, but that memory is gone
printf("%d", *ptr);   // undefined behavior — could crash, print garbage, or "work" by luck
```

### 2. Returning the address of a local variable from a function

```c
int *getValue() {
    int x = 10;
    return &x;   // x is a LOCAL variable — destroyed when the function ends
}

int main() {
    int *p = getValue();
    printf("%d", *p);   // p is dangling — x no longer exists
}
```

> This is exactly the bug in the `slice()` function example — `newstr` was a local array, and returning a pointer to it created a dangling pointer once the function returned.

### 3. Pointer outliving the scope of the variable it points to

```c
int *ptr;
{
    int y = 5;
    ptr = &y;
}   // y goes out of scope here, memory reused/invalidated
printf("%d", *ptr);   // ptr is dangling
```

---

## Why it's dangerous

Using a dangling pointer (dereferencing it, i.e. `*ptr`) is **undefined behavior** — it might:

- **Crash the program** (segmentation fault)
- **Silently print garbage/wrong data**
- **Appear to work fine** (misleadingly) because the memory hasn't been reused yet — this is the scariest case, since the bug might not show up until later, in production, when memory happens to get reused differently

---

## How to avoid / fix dangling pointers

**1. After `free()`, set the pointer to `NULL`:**

```c
free(ptr);
ptr = NULL;   // now if you accidentally use ptr later, you get a clear crash (NULL dereference) instead of silent corruption
```

**2. Never return the address of a local variable** — instead:

- Return the value itself (not its address), **or**
- Use `malloc` to allocate memory that survives beyond the function, **or**
- Pass in a buffer from the caller (like in the `slice()` fix)

---

## Quick summary table

| Pointer type | Problem |
|---|---|
| **Dangling pointer** | points to memory that's already freed/invalid |
| **Wild pointer** | never initialized at all, points to random garbage from the start |
| **NULL pointer** | intentionally points to nothing — safe to check, unsafe to dereference |
