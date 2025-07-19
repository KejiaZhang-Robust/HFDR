<div align="center">
  <h2 style="font-size: 36px; font-weight: bold; color: #333;">
    Mitigating Low-Frequency Bias: Feature Recalibration and Frequency Attention Regularization for Adversarial Robustness
  </h2>
</div>

<div align="center" style="margin-top: 20px;">
  <!-- arXiv Badge -->
  <a href="https://arxiv.org/abs/2408.06079">
    <img src="https://img.shields.io/badge/arXiv-2408.06079-b31b1b?style=flat-square" alt="arXiv" />
  </a>
  <!-- License Badge -->
  <img alt="GitHub License" src="https://img.shields.io/github/license/KejiaZhang-Robust/HFDR?style=flat-square">
  <!-- Language Badge -->
  <img alt="Language" src="https://img.shields.io/github/languages/top/KejiaZhang-Robust/HFDR?style=flat-square&color=9acd32">
</div>

---

## 🔧 Installation

To begin using HFDR, set up your environment by following the steps below:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/KejiaZhang-Robust/HFDR
   cd HFDR
   ```

2. **Requirements**
   A suitable [conda](https://conda.io/) environment named `HFDR` can be created
   and activated with:

   ```
   conda env create -f environment.yaml
   conda activate HFDR
   ```

---

## 🏋️‍♂️ Training

1. Modify the training configuration:

```bash
configs_train.yml
```

2. Start training:

```bash
python train.py
```

---

## 🧪 Robustness Evaluation

1. Edit the testing configuration:

```bash
configs_test.yml
```

2. Launch evaluation:

```bash
python test_robust.py
```

---
