import sys
import os
import argparse

# --- 关键修正代码 START ---
# 动态将项目根目录 (即 main.py 所在的目录) 添加到模块搜索路径
# 这样 Python 就能识别并导入 'src' 目录作为一个包
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)
# --- 关键修正代码 END ---

# 现在可以从 src 包中正确导入 processing 模块
from src.processing import run_color_transfer_pipeline


def main():
    parser = argparse.ArgumentParser(description="KNN K-Nearest Neighbors Color Transfer")

    # *** 路径默认值修正 START ***
    # 修正: 设置默认值为项目目录结构中的文件路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument("--source",
                        type=str,
                        default=os.path.join(base_dir, "data/source/730x576x2.jpg"),  # 默认使用 source/fushishan.jpg
                        help="路径: 待转换的目标图像")
    parser.add_argument("--reference",
                        type=str,
                        default=os.path.join(base_dir, "data/reference/grass.jpg"),  # 默认使用 data/reference/grass.jpg
                        help="路径: 风格参考图像")
    parser.add_argument("--output",
                        type=str,
                        default=os.path.join(base_dir, "data/output/transferred_image.png"),  # 默认输出到 data/output/
                        help="路径: 结果图像保存路径")
    # *** 路径默认值修正 END ***

    parser.add_argument("-k", type=int, default=10, help="KNN 算法中的 K 值 (近邻数)")
    parser.add_argument("--sigma", type=float, default=50.0, help="高斯核函数的标准差参数")

    args = parser.parse_args()

    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir:
        # 确保 data/output 目录存在
        os.makedirs(output_dir, exist_ok=True)

    print(f"源图像路径: {args.source}")
    print(f"参考图像路径: {args.reference}")
    print(f"输出路径: {args.output}")

    try:
        run_color_transfer_pipeline(
            source_path=args.source,
            ref_path=args.reference,
            output_path=args.output,
            k=args.k,
            sigma=args.sigma
        )
        print("颜色迁移完成!")
    except FileNotFoundError as e:
        print(f"错误: 找不到文件。请检查路径是否正确: {e}")
    except Exception as e:
        # 捕获其他运行时错误
        print(f"发生未预期错误: {e}")


if __name__ == "__main__":
    main()