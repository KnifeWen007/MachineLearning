# KNN 颜色迁移 (KNN Color Transfer)

基于 K-近邻算法的颜色风格迁移工具，可以将一张图片的颜色风格迁移到另一张图片上。

## 项目简介

本项目实现了两种基于 KNN（K-Nearest Neighbors）算法的颜色迁移方法：

1. **基础 KNN 颜色迁移** (`knn_matcher.py`)：

   - 在 Lab 颜色空间中对每个像素进行颜色匹配
   - 使用简单的像素级特征进行匹配

2. **高级 KNN 颜色迁移** (`advanced_knn_matcher.py`)：
   - 使用窗口级别的特征进行匹配（考虑周围像素信息）
   - 可调节窗口大小，提供更好的迁移效果

## 目录结构

```
knn_color_transfer/
├── data/
│   ├── source/           # 源图像目录
│   ├── reference/        # 参考图像目录
│   └── output/           # 输出图像目录
├── src/
│   ├── knn_matcher.py         # 基础 KNN 匹配器
│   ├── advanced_knn_matcher.py # 高级 KNN 匹配器
│   ├── processing.py          # 基础处理流程
│   ├── color_utils.py         # 颜色空间转换工具
│   └── __init__.py
├── main.py              # 基础颜色迁移入口
├── advanced_main.py     # 高级颜色迁移入口
└── README.md
```

## 使用方法

### 基础颜色迁移

```bash
python main.py [--source SOURCE_PATH] [--reference REF_PATH] [--output OUTPUT_PATH] [-k K] [--sigma SIGMA]
```

参数说明：

- `--source`: 源图像路径（待转换图像）
- `--reference`: 参考图像路径（提供颜色风格的图像）
- `--output`: 输出图像路径
- `-k`: KNN 中的近邻数，默认为 10
- `--sigma`: 高斯核函数标准差，默认为 50.0

示例：

```bash
python main.py --source data/source/fushishan.jpg --reference data/reference/grass.jpg --output data/output/result.png
```

### 高级颜色迁移

```bash
python advanced_main.py [--source SOURCE_PATH] [--reference REF_PATH] [--output OUTPUT_PATH] [-k K] [--sigma SIGMA] [--window-size SIZE]
```

额外参数：

- `--window-size`: 窗口大小（1 表示 3x3 窗口，2 表示 5x5 窗口等）

示例：

```bash
python advanced_main.py --source data/source/730x576x2.jpg --reference data/reference/boat.jpg --output data/output/advanced_result.png --window-size 2
```

## 算法原理

### 基础 KNN 方法

1. 将参考图像和目标图像都转换到 Lab 颜色空间
2. 从参考图像中提取所有像素的 a、b 通道值作为训练样本
3. 对目标图像中的每个像素，在参考样本中找到 K 个最相似的颜色
4. 使用高斯核函数根据距离计算权重，对 K 个邻居的颜色进行加权平均
5. 将计算出的新颜色应用到目标图像对应位置

### 高级 KNN 方法

1. 在基础方法的基础上，不仅考虑单个像素的颜色值，还考虑其周围窗口内的亮度信息
2. 使用滑动窗口提取特征，使得匹配更加符合人眼感知
3. 通过调整窗口大小来控制考虑的上下文范围

## 参数调优建议

- **K 值**：较小的 K 值会产生更接近参考图像的效果，但可能引入噪声；较大的 K 值会产生更平滑的结果，但可能丢失细节。推荐值：5-20。
- **Sigma 值**：控制高斯权重的衰减速度。较小的 Sigma 值使距离近的邻居权重更大，较大则权重分布更均匀。推荐值：30-100。
- **窗口大小**（仅高级方法）：控制考虑上下文信息的范围。值越大，迁移效果越全局化，但也可能丢失局部特征。推荐值：1-3。

## 示例结果

| 源图像                               | 参考图像                             | 迁移结果                                            |
| ------------------------------------ | ------------------------------------ | --------------------------------------------------- |
| ![源图像](data/source/730x576x2.jpg) | ![参考图像](data/reference/boat.jpg) | ![结果](data/output/advanced_transferred_image.png) |

## 注意事项

1. 输入图像格式支持常见的 JPG、PNG 等格式
2. 输出图像默认保存为 PNG 格式以保证质量
3. 处理大尺寸图像时可能需要较长时间，请耐心等待
4. 如果遇到内存不足问题，可尝试减小 K 值或使用较小尺寸的图像

## 许可证

MIT License

## 贡献者

该项目由机器学习爱好者开发，欢迎提出改进建议和贡献代码。
