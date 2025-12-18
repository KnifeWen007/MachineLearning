import sys
import os
import argparse

# 动态将项目根目录添加到模块搜索路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# 从src包中导入处理模块
from src.advanced_knn_matcher import run_advanced_color_transfer


def main():
    parser = argparse.ArgumentParser(description="Advanced KNN Color Transfer with Window-based Matching")

    # 路径参数
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument("--source",
                        type=str,
                        default=os.path.join(base_dir, "data/source/SummerForest.jpg"),
                        help="路径: 待转换的目标图像")
    parser.add_argument("--reference",
                        type=str,
                        default=os.path.join(base_dir, "data/reference/AutumnForest.jpg"),
                        help="路径: 风格参考图像")
    parser.add_argument("--output",
                        type=str,
                        default=os.path.join(base_dir, "data/output/advanced_transferred_image3.png"),
                        help="路径: 结果图像保存路径")
    
    # 算法参数
    parser.add_argument("-k", type=int, default=10, help="KNN 算法中的 K 值 (近邻数)")
    parser.add_argument("--sigma", type=float, default=50.0, help="高斯核函数的标准差参数")
    parser.add_argument("--window-size", type=int, default=1, help="窗口大小 (1表示3x3窗口)")

    args = parser.parse_args()

    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"源图像路径: {args.source}")
    print(f"参考图像路径: {args.reference}")
    print(f"输出路径: {args.output}")
    print(f"K值: {args.k}")
    print(f"Sigma: {args.sigma}")
    print(f"窗口大小: {args.window_size}")

    try:
        run_advanced_color_transfer(
            source_path=args.source,
            ref_path=args.reference,
            output_path=args.output,
            k=args.k,
            sigma=args.sigma,
            window_size=args.window_size
        )
        print("高级颜色迁移完成!")
    except FileNotFoundError as e:
        print(f"错误: 找不到文件。请检查路径是否正确: {e}")
    except Exception as e:
        print(f"发生未预期错误: {e}")


if __name__ == "__main__":
    main()