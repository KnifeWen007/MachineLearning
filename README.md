# Machine Learning 项目集合

这个仓库包含多个机器学习相关的项目和实现，涵盖了不同的算法和技术。

## 项目结构

```
MachineLearning/
├── knn_color_transfer/     # KNN 颜色迁移项目
├── environment.yml         # Conda 环境配置文件
├── README.md              # 根目录说明文件
├── Test.ipynb             # 测试笔记本
└── .gitignore             # Git忽略文件配置
```

## 环境搭建

本项目使用 Conda 管理依赖环境。请按照以下步骤搭建开发环境：

### 1. 安装 Anaconda 或 Miniconda

如果尚未安装，请先下载并安装 [Anaconda](https://www.anaconda.com/products/distribution) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)。

### 2. 创建项目环境

使用提供的 `environment.yml` 文件创建项目环境：

```bash
conda env create -f environment.yml
```

这将创建一个名为 `HandsOnMachineLearning` 的环境，其中包含了所有必要的依赖项。

### 3. 激活环境

```bash
conda activate HandsOnMachineLearning
```

### 4. 验证安装

激活环境后，可以通过以下命令验证关键库是否正确安装：

```bash
python -c "import numpy, pandas, sklearn, cv2; print('环境配置成功')"
```

## 项目列表

### 1. KNN 颜色迁移 (knn_color_transfer)

基于 K-近邻算法的颜色风格迁移工具，可以将一张图片的颜色风格迁移到另一张图片上。

进入项目目录查看详细说明：

```bash
cd knn_color_transfer
cat README.md
```

或者在 GitHub 中直接查看 [knn_color_transfer/README.md](knn_color_transfer/README.md)

## 更新环境

如果 `environment.yml` 文件有更新，可以使用以下命令更新现有环境：

```bash
conda env update -f environment.yml --prune
```

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这些项目。
