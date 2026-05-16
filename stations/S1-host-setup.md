# S1 · Host Setup [Atlas Coordinate]

**Tier:** All  
**Prerequisite:** S0  
**Next:** S2

## ACTION (Builder)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install basics
sudo apt install curl git -y
```

## WHY (Operator)
A clean, updated host prevents 90% of mysterious failures.

## BLUEPRINT SLICE (Architect)
Host → Network → Channel → Models → OpenClaw

**Next:** [S2 · Network Reachability](../S2-network.md)
