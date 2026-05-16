# S2 · Network Reachability [Atlas Coordinate]

**Tier:** All  
**Prerequisite:** S1  
**Next:** S3

## ACTION (Builder)
```bash
ping -c 3 8.8.8.8
curl -I https://api.github.com
```

## WHY (Operator)
Intermittent connectivity is normal for Tier 0/1. The Field Kit is designed to tolerate it.

## BLUEPRINT SLICE (Architect)
Network is the **conductor** between Host and Channel.

**Next:** [S3 · Channel Selection](../S3-channel.md)
