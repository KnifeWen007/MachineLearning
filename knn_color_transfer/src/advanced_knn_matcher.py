import numpy as np
from sklearn.neighbors import NearestNeighbors
from .color_utils import load_image, save_image, rgb_to_lab, lab_to_rgb


class AdvancedKNNColorMatcher:
    def __init__(self, k=10, sigma=50.0, window_size=1):
        """
        高级KNN颜色匹配器
        
        参数:
        k: KNN中的邻居数量
        sigma: 高斯核函数的标准差
        window_size: 窗口大小（1表示3x3窗口，2表示5x5窗口等）
        """
        self.k = k
        self.sigma = sigma
        self.window_size = window_size
        self.model = None
        self.reference_features = None
        self.reference_ab = None

    def _extract_windows(self, img_lab):
        """
        从Lab图像中提取窗口特征（完全向量化版本）
        """
        H, W, C = img_lab.shape
        size = self.window_size
        
        # 提取L通道作为特征
        l_channel = img_lab[:, :, 0]
        
        # 使用滑动窗口视图技术提取所有窗口
        window_size = 2 * size + 1
        
        # 创建滑动窗口视图
        shape = (H - 2 * size, W - 2 * size, window_size, window_size)
        strides = l_channel.strides + l_channel.strides
        window_view = np.lib.stride_tricks.as_strided(
            l_channel, 
            shape=shape, 
            strides=strides
        )
        
        # 展平窗口特征
        features = window_view.reshape(-1, window_size * window_size)
        
        # 提取对应的ab值
        center_indices_x = np.arange(size, H - size)
        center_indices_y = np.arange(size, W - size)
        xx, yy = np.meshgrid(center_indices_x, center_indices_y, indexing='ij')
        ab_values = img_lab[xx, yy, 1:].reshape(-1, 2)
        
        return features, ab_values

    def build_model(self, ref_image_lab):
        """
        根据参考图像建立KNN模型
        """
        print(f"--- 构建高级KNN模型 (窗口大小: {2*self.window_size+1}x{2*self.window_size+1}) ---")
        
        # 提取参考图像的窗口特征
        self.reference_features, self.reference_ab = self._extract_windows(ref_image_lab)
        
        # 使用NearestNeighbors建立查找模型
        self.model = NearestNeighbors(n_neighbors=self.k, algorithm='auto', metric='euclidean')
        self.model.fit(self.reference_features)
        
        print(f"KNN模型建立完成，参考窗口数: {len(self.reference_features)}")

    def transfer_colors(self, target_image_lab):
        """
        对目标图像进行颜色迁移
        """
        H, W, C = target_image_lab.shape
        size = self.window_size
        
        print(f"--- 开始颜色迁移 (窗口大小: {2*size+1}x{2*size+1}) ---")
        
        # 提取目标图像的窗口特征
        print("提取目标图像窗口特征...")
        target_features, _ = self._extract_windows(target_image_lab)
        
        print(f"开始查找 {len(target_features)} 个目标窗口的最近邻...")
        
        # 查找K个最近邻
        distances, indices = self.model.kneighbors(target_features)
        
        # 计算权重（使用高斯核函数）
        weights = np.exp(-distances**2 / (2 * self.sigma**2))
        normalized_weights = weights / np.sum(weights, axis=1, keepdims=True)
        
        # 获取邻居的颜色值并进行加权平均
        neighbor_colors = self.reference_ab[indices]
        weighted_colors = neighbor_colors * normalized_weights[:, :, np.newaxis]
        new_ab = np.sum(weighted_colors, axis=1)
        
        print("颜色迁移计算完成。")
        
        # 重构图像
        new_image_lab = np.copy(target_image_lab)
        
        # 向量化填充内部区域的颜色（边界区域保持原样）
        # 创建索引网格
        x_indices, y_indices = np.meshgrid(
            np.arange(size, H - size),
            np.arange(size, W - size),
            indexing='ij'
        )
        
        # 展平索引
        flat_x_indices = x_indices.ravel()
        flat_y_indices = y_indices.ravel()
        
        # 向量化赋值
        new_image_lab[flat_x_indices, flat_y_indices, 1:] = new_ab.reshape(-1, 2)
                
        return new_image_lab


def run_advanced_color_transfer(source_path, ref_path, output_path, k=10, sigma=50.0, window_size=1):
    """
    运行高级KNN颜色迁移流程
    """
    print("--- 高级KNN颜色迁移开始 ---")
    
    # 1. 加载图像
    source_rgb = load_image(source_path)
    ref_rgb = load_image(ref_path)
    print(f"加载图像：源图 {source_rgb.shape}, 参考图 {ref_rgb.shape}")
    
    # 2. 转换为Lab空间
    source_lab = rgb_to_lab(source_rgb)
    ref_lab = rgb_to_lab(ref_rgb)
    print("图像转换为Lab空间。")
    
    # 3. 构建和执行KNN匹配
    matcher = AdvancedKNNColorMatcher(k=k, sigma=sigma, window_size=window_size)
    matcher.build_model(ref_lab)
    
    # 4. 迁移颜色
    transferred_lab = matcher.transfer_colors(source_lab)
    
    # 5. 转换回RGB空间
    transferred_rgb = lab_to_rgb(transferred_lab)
    
    # 6. 保存结果
    save_image(transferred_rgb, output_path)
    print(f"结果已保存到: {output_path}")
    print("--- 高级KNN颜色迁移完成 ---")