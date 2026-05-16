# S0 · Tier Classify [Atlas Coordinate]

**Tier:** 0 / 1 / 2  
**Prerequisite:** None  
**Next:** S1

## ACTION (Builder)
```bash
free -h && df -h && nproc
```

## WHY (Operator)
This is the **branch point**. All later instructions adapt to your actual hardware.

## BLUEPRINT SLICE (Architect)
(See ATLAS.md)

### Tier Matrix
| Tier | Name         | RAM Floor | Model Strategy     | Example Hardware     |
|------|--------------|-----------|--------------------|----------------------|
| 0    | Phone-home   | 4 GB      | Cloud only         | Old laptop / Pi 4    |
| 1    | Hybrid       | 8 GB      | Cloud + Local      | Modern used laptop   |
| 2    | Sovereign    | 16 GB+    | Fully Local        | Desktop / Jetson     |

**Done.** Proceed to **[S1 · Host Setup](../S1-host-setup.md)**.
