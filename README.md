# 🎐 AILivePet – 智能桌面宠物助手

一个探索性项目，旨在构建一个集 **自然语言交互、Web3 钱包查询 和 Live2D 动态展示** 于一体的 AI 桌面应用。  
项目结合了 **AI Agent、Prompt 工程优化、Qt 框架和 Live2D 技术**，为用户提供一个生动有趣的智能桌面伴侣。

--- 

## ✨ 项目亮点

- 🧠 **AI Agent 构建**  
通过精心的 Prompt 工程设计，让 Agent 具备自然语言理解与精准回答能力。  

- 🪙 **Web3 钱包信息查询**  
支持自然语言查询链上数据（如钱包余额、NFT 资产），轻松管理数字资产。  

- 🐾 **Live2D 动态展示**  
将 AI Agent 与 Live2D 结合，赋予助手生动的视觉表现，提升交互的沉浸感。  

--- 

## 🛠 技术栈

- **语言**: Python 3.9+  
- **框架**: PySide6 / PyQt5/6, HuggingFace Transformers  
- **技术**: Live2D Cubism SDK, Ethers.js/Web3.js  
- **工具**: Accelerate, Wandb  

--- 

## 📂 项目结构

```text
├── modules/               # AI Agent 模块
│   └── chain_info/        # Web3 钱包信息查询
├── utils/                 # 工具函数
│   └── fetch.py           # 数据获取工具
├── venv/                  # Python 虚拟环境
├── model_use.py           # 模型调用与推理
├── main.py                # 主程序入口 (包含 Qt UI 逻辑)
├── Qt_show.pyproject      # 项目文件
├── requirements.txt       # 依赖
└── README.md              # 项目说明
