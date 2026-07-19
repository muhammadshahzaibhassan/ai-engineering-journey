# Matplotlib Guide - Chat Conversation

## User Request 1
**User:** "Matplotlib"

---

## Assistant Response 1

# Matplotlib: Comprehensive Guide

## What is Matplotlib?

**Matplotlib** is a comprehensive Python library for creating static, animated, and interactive visualizations. It's the foundation of data visualization in the Python ecosystem, offering MATLAB-like plotting capabilities with full Python control.

## Quick Start

```python
import matplotlib.pyplot as plt
import numpy as np

# Basic line plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Sine Wave')
plt.grid(True)
plt.show()
