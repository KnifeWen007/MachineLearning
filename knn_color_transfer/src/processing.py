from .color_utils import load_image, save_image, rgb_to_lab, lab_to_rgb
from .knn_matcher import KNNColorMatcher


def run_color_transfer_pipeline(source_path, ref_path, output_path, k=10, sigma=50.0):
    """
    KNN 色彩迁移主流程。
    """
    print("--- KNN 色彩迁移开始 ---")

    # 1. 加载图像
    source_rgb = load_image(source_path)
    ref_rgb = load_image(ref_path)
    print(f"加载图像：源图 {source_rgb.shape}, 参考图 {ref_rgb.shape}")

    # 2. 转换为 Lab 空间
    source_lab = rgb_to_lab(source_rgb)
    ref_lab = rgb_to_lab(ref_rgb)
    print("图像转换为 Lab 空间。")

    # 3. 构建和执行 KNN 匹配
    matcher = KNNColorMatcher(k=k, sigma=sigma)
    matcher.build_model(ref_lab)

    # 4. 迁移颜色
    transferred_lab = matcher.transfer_colors(source_lab)

    # 5. 转换回 RGB 空间
    transferred_rgb = lab_to_rgb(transferred_lab)

    # 6. 保存结果
    save_image(transferred_rgb, output_path)
    print(f"结果已保存到: {output_path}")
    print("--- KNN 色彩迁移完成 ---")