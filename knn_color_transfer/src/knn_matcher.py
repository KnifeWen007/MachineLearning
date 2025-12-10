import numpy as np
from sklearn.neighbors import NearestNeighbors


class KNNColorMatcher:
    def __init__(self, k=10, sigma=50.0):
        self.k = k
        self.sigma = sigma
        self.model = None
        self.reference_ab = None

    def build_model(self, ref_image_lab):
        """
        根据参考图像的 a 和 b 通道建立 KNN 模型。
        """
        H, W, C = ref_image_lab.shape

        # 提取 a 和 b 通道数据，展平为 (H*W, 2) 的特征矩阵
        # ref_image_lab[:, :, 1:] 提取了 a 和 b 通道
        self.reference_ab = ref_image_lab[:, :, 1:].reshape(-1, 2)

        # 使用 NearestNeighbors 建立查找模型
        # algorithm='auto' 会自动选择 KDTree 或 BallTree
        self.model = NearestNeighbors(n_neighbors=self.k, algorithm='auto', metric='euclidean')
        self.model.fit(self.reference_ab)
        print(f"KNN 模型建立完成，参考像素数: {len(self.reference_ab)}")

    def transfer_colors(self, target_image_lab):
        """
        对目标图像的每个像素，在参考模型中查找 K 个最近邻并进行色彩迁移。
        """
        H, W, C = target_image_lab.shape

        # 提取目标图像的 a 和 b 通道，展平为 (H*W, 2)
        target_ab = target_image_lab[:, :, 1:].reshape(-1, 2)

        print(f"开始查找 {len(target_ab)} 个目标像素的最近邻...")

        # 查找 K 个最近邻的索引和距离
        distances, indices = self.model.kneighbors(target_ab)

        # --- 核心迁移逻辑 ---
        # 1. 获取邻居的颜色值
        neighbor_colors = self.reference_ab[indices]  # 形状: (H*W, K, 2)

        # 2. 计算权重 (使用高斯核函数作为权重，即越近权重越大)
        # sigma 控制高斯核的宽度，较大的sigma会使权重分布更平缓
        weights = np.exp(-distances**2 / (2 * self.sigma**2))  # 形状: (H*W, K)

        # 3. 归一化权重：每行的权重和为 1
        normalized_weights = weights / np.sum(weights, axis=1, keepdims=True)

        # 4. 加权平均： (H*W, K, 2) * (H*W, K, 1) -> (H*W, K, 2)
        weighted_colors = neighbor_colors * normalized_weights[:, :, np.newaxis]

        # 5. 求和得到最终的迁移颜色值
        new_ab = np.sum(weighted_colors, axis=1)  # 形状: (H*W, 2)

        print("色彩迁移计算完成。")

        # 重新组合 Lab 图像
        new_image_lab = np.copy(target_image_lab)
        # 保存原始L通道（亮度）
        original_l = target_image_lab[:, :, 0]
        # 替换 a 和 b 通道
        new_image_lab[:, :, 1:] = new_ab.reshape(H, W, 2)
        # 可选：稍微调整亮度以匹配参考图像的亮度均值
        # ref_l_mean = np.mean(ref_image_lab[:, :, 0])
        # target_l_mean = np.mean(original_l)
        # new_image_lab[:, :, 0] = original_l + (ref_l_mean - target_l_mean) * 0.3  # 轻微调整

        return new_image_lab