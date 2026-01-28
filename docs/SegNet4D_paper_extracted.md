# IEEE TRANSACTIONS ON AUTOMATION SCIENCE AND ENGINEERING, VOL. 22, 2025

**作者 (Authors):** 15339, SegNet4D: Eﬃcient Instance-Aware 4D Semantic, Segmentation for LiDAR Point Cloud

---

## 论文概述 (Overview)

本文档为 SegNet4D 论文的详细解析，包含全文提取、章节划分、图片提取等内容。

This document provides a detailed analysis of the SegNet4D paper, including full text extraction, section division, and image extraction.

---

## 目录 (Table of Contents)

- [Introduction](#introduction)
- [Related Work - A. Moving Object Segmentation](#related-work---a-moving-object-segmentation)
- [Method](#method)
- [Method - A. Motion Feature Encoding Module](#method---a-motion-feature-encoding-module)
- [Method - C. Motion Head and Semantic Head](#method---c-motion-head-and-semantic-head)
- [Method - F. Loss Function](#method---f-loss-function)
- [Method - B. Evaluation for Moving Object Segmentation](#method---b-evaluation-for-moving-object-segmentation)
- [Method - D. Ablation Study](#method---d-ablation-study)
- [Method - E. Runtime Analysis](#method---e-runtime-analysis)
- [Method - V. CONCLUSION AND FUTURE WORK](#method---v-conclusion-and-future-work)
- [References](#references)

---

## Introduction

L IGHT Detection and Ranging (LiDAR) sensors, have become important for autonomous vehicles and robots to achieve autonomy due to their resilience to illumination changes, wide ﬁeld of views, and accurate range measurements [1], [2]. As a result, LiDAR-based semantic perception has garnered extensive research interest in recent years. Semantic segmentation using 3D LiDAR data aims to assign a speciﬁc semantic class label to each point in the acquired point clouds, serving as a fundamental task in 3D perception and scene understanding. This technology signiﬁcantly enhances key autonomous functions such as navigation [3], point cloud registration [4], [5], and and simultaneous localization and mapping (SLAM) [6], [7]. In practical applications, however, single-scan 3D LiDAR semantic segmentation methods [1], [8], [9], [10] face inherent limitations due to their inability to capture motion dynamics, a crucial factor for eﬀective obstacle avoidance and local path planning in autonomous systems. To address this, 4D semantic understanding is necessary. As shown in Fig. 1, it categorizes each LiDAR point while identifying its dynamic attributes [11], [12], [13]. This task typically relies on sequen- tial LiDAR scans to capture motion information. In this regard, some methods directly stack historical LiDAR scans into a single point cloud and feed it into a single-scan-based semantic network for achieving 4D segmentation [1], [9], [14], which leads to suboptimal performance due to the lack of motion information association. Other approaches use 4D convolutional neural networks [15] or recursive networks [12], [16] to extract motion features from input sequential LiDAR scans. However, these approaches impose heavy computational burdens and make real-time operations challenging. Moreover, existing methods commonly treat 4D semantic segmentation in an end-to-end fashion, directly predicting semantic labels for all categories, including those moving and static classes. This may lead to limited performance in recognizing dynamic objects because moving points are often fewer than static background points in most datasets. To address these challenges, building upon our previous work InsMOS [17], we propose an extended framework for 4D semantic segmentation. Our key idea is to tackle 4D semantic segmentation by dividing it into two subtasks: single-scan semantic segmentation (SSS) and moving object 1558-3783 © 2025 IEEE. All rights reserved, including rights for text and data mining, and training of artiﬁcial intelligence and similar technologies. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

15340 IEEE TRANSACTIONS ON AUTOMATION SCIENCE AND ENGINEERING, VOL. 22, 2025 Fig. 1. Our SegNet4D performs real-time, online prediction of semantic categories while simultaneously identifying the motion state of each point. This capability greatly aids in downstream tasks including obstacle avoidance, path planning, and navigation, thereby enhancing the autonomous capabilities of robots. segmentation (MOS). We argue that semantic classes and motion characteristics represent distinct aspects of objects. By addressing them separately and then fusing their outputs, our method achieves a more comprehensive understanding and superior performance compared to end-to-end approaches. To enhance eﬃciency, our framework converts the sequential LiDAR scans into Bird’s Eye View (BEV) images and extracts motion features by calculating BEV residuals, signiﬁcantly reducing computational cost compared to existing fashion using 4D convolutions or recursive networks. Furthermore, we ﬁnd instance information [17], [18] is crucial for the LiDAR segmentation tasks to prevent over-segmentation. However, existing methods struggle to integrate this information eﬀec- tively. To address this, we incorporate instance consistency from the current scan into the prediction pipeline at both feature and point levels, enabling instance-aware segmenta- tion. Finally, we design a novel module to fuse point-wise semantic predictions and motion states to achieve accurate 4D semantic segmentation online. We extensively evaluate SegNet4D on mainstream datasets, comparing its performance with state-of-the-art (SOTA) methods. The results conﬁrm that our approach surpasses SOTA in both 4D semantic seg- mentation and MOS. Through detailed runtime analysis, our method shows greater eﬃciency, enabling real-time operation. Additionally, we validate its practical utility on a real robotic platform, demonstrating both its eﬀectiveness and eﬃciency for autonomous applications. In summary, the contributions of this work are threefold: • We propose a novel 4D semantic segmentation framework that decomposes the task into two subtasks: Single- Scan Semantic Segmentation (SSS) and Moving Object Segmentation (MOS). The results are then combined using a motion-semantic fusion module, achieving SOTA performance in both 4D semantic segmentation and MOS. • We propose a novel instance-aware backbone that lever- ages instance information at both the feature and point levels, enhancing performance in both MOS and seman- tic segmentation tasks. Additionally, we introduce an automated method to generate instance bounding box labels directly from semantic annotations, eliminating the need for additional manual labeling. • We propose an eﬃcient 4D semantic segmentation net- work that is signiﬁcantly faster than existing methods and supports real-time operation. Furthermore, we suc- cessfully integrate the network into a real platform, demonstrating its practical utility for autonomous appli- cations. This article is an extension of our previous conference paper, i.e., InsMOS [17], which proposed to add instance information for MOS. Compared to [17], this article extends it in four critical aspects: • a fully 4D semantic segmentation method that predicts both the motion states and semantic categories. • a novel module for integrating point-wise motion states and semantic category predictions. • a more eﬃcient mechanism for encoding motion features, enabling this method to operate in real-time. • a more extensive experimental evaluation on multiple datasets and a real-world unmanned ground platform, demonstrating this method’s superior performance and practical utility.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Related Work

### A. Moving Object Segmentation

MOS refers to accurately identifying dynamic regions or objects from input data. The task has attracted exten- sive research in the ﬁeld of computer vision [19], [20]. In recent years, some research has also been paid attention to LiDAR-based MOS. We categorize these methods into projection-based and non-projection-based. The projection-based method typically converts sequential point clouds into image representations, such as range images [2], [21], [22], [23] or BEV images [24], [25], and then compute the residuals of sequential images to extract motion information in the scene. Chen et al. [21] ﬁrst released the MOS datasets and benchmark based on the SemanticKITTI dataset [14], and proposed a deep neural network to learn motion cues from sequential residual range images for online MOS. To extract motion features more comprehensively, Sun et al. [22] proposed a dual-branch network architecture that separately encodes the appearance features and temporal motion features, and then fuses them with a multi-scale motion-guided attention module. Subsequently, Cheng et al. [23] utilized a similar dual-branch architecture and proposed a distribution-based data augmentation method to improve the network robustness. Kim et al. [2] also designed a similar multi-branch network to improve MOS accuracy, where one branch performs semantic segmentation to obtain movable objects, and another branch network extracts motion fea- tures. Finally, a fusion branch network is utilized to merge these features to achieve better MOS. Unlike range images, BEV images oﬀer a top-down perspective, allowing a more intuitive observation of object movement. Based on this, Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

WANG et al.: SegNet4D: EFFICIENT INSTANCE-AWARE 4D SEMANTIC SEGMENTATION 15341 Mohapatra et al. [24] designed a lightweight network archi- tecture for extracting motion information from BEV residual images and successfully achieved real-time operation in an embedded platform. However, this method can only perform pixel-wise segmentation in the BEV space and has relatively low accuracy. Recently, Zhou et al. [25] projected 3D point clouds into the polar coordinate BEV space and designed a dual-branch network structure similar to [22] to enhance the MOS performance. Diﬀerent from the projection-based methods, the non- projection methods directly extract motion information from sequential 3D point clouds. Mersch et al. [26] utilized the Minkowski engine [15] to construct a sparse 4D convolutional network. This network is designed to extract spatio-temporal features from the input 4D point clouds and predict point-wise moving labels. They also proposed a receding horizon strategy that integrates multiple observations to reﬁne the network’s predictions. Kreutz et al. [27] proposed an unsupervised MOS method based on [26], which learns spatio-temporal occupancy changes in the local neighborhood of point cloud videos. However, it is only applicable to stationary LiDAR. Due to the lack of instance-level perception, existing methods often partially segment moving objects. Therefore, we attempt to introduce instance information into the network, enabling it to achieve complete segmentation of moving objects. B. 4D LiDAR Semantic Segmentation Unlike the MOS task, 4D LiDAR semantic segmentation not only needs to capture temporal information to predict point-wise motion state but also assign a semantic category label to each point, including moving and static points. This substantially raises the challenge of the task by evolving a binary classiﬁcation issue into a more intricate multi-class classiﬁcation scenario, necessitating the network to acquire sophisticated appearance features and associate them with motion characteristics. To address this task, some methods [1], [9], [14] try to fuse sequential LiDAR scans into a single point cloud and then utilize a 3D semantic segmentation network to predict 4D semantic labels directly. However, due to the lack of temporal perception capability in 3D networks, these methods often struggle with point-wise motion state recognition. Moreover, the fused single point cloud contains a substantial amount of data, greatly increasing the network’s computation time and making real-time operation challenging. Consequently, such methods are typically not the preferred option in real-world scenarios. Another category of

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

The framework of our proposed method is depicted in Fig. 2. SegNet4D consists of four main components: Motion Feature Encoding Module (Sec. III-A), Instance-Aware Fea- ture Extraction Backbone (Sec. III-B), two separate output heads (Sec. III-C), and Motion-Semantic Fusion Module (MSFM, Sec. III-D). We speciﬁcally introduce each module in the following section.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

### A. Motion Feature Encoding Module

4D semantic segmentation not only predicts the semantic category for each point measured by LiDAR but also identiﬁes its motion state. Therefore, it is necessary to extract motion features from the sequential point clouds. Existing methods mainly utilize 4D convolution [26], [27] to obtain motion cues, which poses a signiﬁcant computational workload. To improve the real-time performance, we adopt the BEV image representation for fast motion feature encoding, as shown in Fig. 3, which avoids computational expense processing on extensive unstructured point cloud data. The encoding process is divided into three steps as follows. 1) Point Cloud Alignment: To compensate for the ego- motion of LiDAR, spatial alignment is conducted initially on the input sequential point clouds. Speciﬁcally, given the current point cloud S0 = {pi ∈ R4}M i=1 consisting of M points represented in homogeneous coordinates as pi [xi, yi, zi, 1]T, along with the past N − 1 consecutive point= clouds S1, S2, . . . , SN−1 with their relative transformations T0 1, T1 2, . . . , TN−2 N−1, we transform the past N−1 consecutive point clouds into the current viewpoint by S j→0 = {p′ i = T0 j pi|pi ∈ S j}, T0 j= j−1 Y k=0 T j−k−1 j−k . (1) Fig. 4. Motion features visualization. (a) and (b) represent the motion features obtained from the current and past N-th scan. We compare the features with the network’s predictions as well as ground truth. In practical applications, the relative transformations can be easily obtained through the existing LiDAR odome- try approach [4], [7]. We use the poses estimated by SuMa [7]. 2) BEV Projection: After alignment, we project the aligned point clouds into single-channel BEV images. For each point p′ j = (x′ j, y′ j, z′ j) ∈ S j→0, we ﬁrst restrict it within x′ j ∈ [Xmin, Xmax], y′ j ∈ [Ymin, Ymax], z′ j ∈ [Zmin, Zmax] and then convert it into the pillar space, given by 8 ˆˆˆˆ< ˆˆˆˆ: I(u,v), j = {z′ j|z′ j ∈ p′ j}, u = ⌊ x′ j − Xmin g ⌋, v = ⌊ y′ j − Ymin g ⌋, (2) where I(u,v), j stores a set of point’s height in the pillar located at (u, v), and g denotes grid resolution. Following [25], we project the Ij into a single-channel BEV image B j of size H×W. For each pixel value B(u,v),j, we use the diﬀerence between the maximum and minimum height within the same pillar, calculating as: B(u,v), j = Max{I(u,v), j} − Min{I(u,v), j} (3) 3) Motion Features Encoding: We take the BEV residuals R ∈ RH×W×(N−1) between B0 and B1, . . . , BN−1 as the motion features in the BEV space, calculated by R(u,v), j→0 = B(u,v),0 − B(u,v),j, j ∈ 1, . . . , N − 1, (4) where R(u,v) represents the residual value for pixel at (u, v). To obtain motion features for each point in the 3D space, we perform back-projection by assigning the BEV residual value to all points projected to the BEV pixel. Points within the same pillar will share the same residual value for each residual image. Finally, we obtain point-wise motion fea- tures Fm ∈ RM×(N−1). We concatenate the Fm and current scan’s spatial features, i.e., [x, y, z, intensity], generating a new features Fsp ∈ RM×(N+3) as the input for subsequent backbone. The extracted motion features visualization is presented in Fig. 4. Our approach can obtain initial motion cues for Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

WANG et al.: SegNet4D: EFFICIENT INSTANCE-AWARE 4D SEMANTIC SEGMENTATION 15343 Fig. 5. The architecture of the Instance-Aware Feature Extraction Backbone. 3 × 3 × 3 indicates a kernel size for 3D sparse convolution. [32,64,128,256] represents the dimensions of the output feature channels. M and N are deﬁned in the motion feature encoding process. M′ denotes the number of non-empty voxels in the last layer. O is the number of object detection categories. moving objects in the scene. As the time interval for residual computation extends, the motion features become increas- ingly prominent. Inevitably, some points might be erroneously assigned motion characteristics because of changes in LiDAR viewpoint or inaccuracies in odometry estimation. However, through our network’s subsequent learning process, which utilizes the scene’s spatial features to distinguish movable from immovable objects and learning multi-channel motion features to identify true moving objects, these points still are correctly categorized, as shown in the Fig. 4 (c). Our network is capable of learning spatial features for semantic classiﬁcation from the current LiDAR scan, as well as motion cues for motion segmentation. This is also a signiﬁcant diﬀerence from purely projection-based methods, as we still leverage valuable spatial features inherent in the original point cloud. B. Instance-Aware Feature Extraction Backbone In semantic segmentation, over-segmentation is a common issue, where a single instance is incorrectly divided into mul- tiple segments. Especially in the MOS task, existing methods lack instance awareness, often erroneously dividing an instance into two diﬀerent motion states. To tackle such issues, we design the Instance-Aware Feature Extraction Backbone to extract instances information and incorporate them into our prediction pipeline. As shown in Fig. 5. It consists of the Instance Detection Module and the Upsample Fusion Module. 1) Instance Detection Module: In this module, We use 3D sparse convolution blocks [34] to voxelize the current point cloud and then perform convolution only on non-empty voxels, greatly improving the processing speed. Moreover, to capture more crucial features, we add a window self-attention [35] layer after each sparse convolution block to improve the receptive ﬁeld. Our key ﬁnding is that instance information is crucial for LiDAR segmentation, as also shown in panoptic segmentation methods [36], [37]. However, these methods typically require additional point-wise instance labels, which may not always be accessible. To address this, we propose a method to automatically generate instance bounding boxes using existing semantic annotations. This process begins by generating each instance cluster from the semantic point cloud using the Euclidean clustering algorithm in PCL library [38]. Subsequently, these clusters are projected into the BEV space, and their orientation is determined using principal component analysis (PCA) [39]. We then combine the height of the cluster to obtain the minimum bounding box and further reﬁne it by L-Shape method [40]. Finally, we utilize CenterHead [41] trained with automatically generated instance labels, to predict instance bounding boxes of O categories online, such as cars, pedestrians, and cyclists. These predicted boxes are then used to enhance feature extraction within our backbone, as described in the upsample fusion module. 2) Upsample Fusion Module: To introduce instance con- sistency into feature-level fusion, we ﬁnd and extract points within the instance bounding box as instance feature masks. Subsequently, we concatenate it with the point embeddings from the Instance Detection Module as input for the Upsample Fusion Module. Unlike InsMOS [17], we integrate the instance features only once to enhance eﬃciency. The Upsample Fusion Module serves the main purpose of integrating instance fea- tures into the prediction pipeline, as well as recovering the scale of the features hierarchically through 3D deconvolution blocks. It is formed by a fully U-Net network structure together with the Instance Detection Module and main- tains more details from diﬀerent scale features through skip connection.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

### C. Motion Head and Semantic Head

Existing 4D semantic segmentation methods usually predict all semantic class labels in an end-to-end manner, including those moving and static classes. However, since static points typically outnumber moving ones in existing datasets, these approaches often result in suboptimal network performance in identifying moving classes. So we employ two distinct heads for predicting moving labels and single-scan semantic labels separately. By explicitly supervising MOS, our method can maintain superior performance for moving object recognition. To maintain the network’s lightweight characteristics, these heads consist solely of a convolutional layer, a normalization layer, an activation function layer, and a linear layer, which are employed to further classify features with diﬀerent attributes. Finally, we can obtain point-wise motion features F′ m ∈ RM×16 and semantic features F′ s ∈ RM×32, which are utilized for the subsequent fusion to enable 4D semantic segmentation. Where 16 and 32 denotes the number of feature channel. Naturally, the motion head and semantic head also generate point-wise motion predictions F′′ m ∈ RM×3 and semantic predictions F′′ s ∈ RM×C by applying an additional linear layer and a softmax function. Note that 3 represents three diﬀerent motion classes, namely unlabeled, static, and moving, while C denotes the number of static semantic categories. Each head is supervised with a speciﬁc loss function. Further details are provided in Sec. III-F. D. Motion-Semantic Fusion Module After obtaining motion labels and single-scan semantic labels, a straightforward approach to achieve 4D semantic Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

15344 IEEE TRANSACTIONS ON AUTOMATION SCIENCE AND ENGINEERING, VOL. 22, 2025 Fig. 6. The architecture of Motion-Semantic Fusion Module. We mainly perform spatial attention and channel attention to fuse the motion features and the static semantic features. segmentation is to fuse them by checking the motion states on each semantic point. However, this fashion may yield non-smooth point segmentation. Moreover, incorrect motion predictions directly lead to false 4D semantic segmentation results. We hence propose a motion-semantic fusion module to further integrate motion features F′ m and static semantic features F′ s for achieving motion-guided 4D semantic segmen- tation. Details of this module are illustrated in Fig. 6. We build our Motion-Semantic Fusion Module upon recently advanced motion-guided attention module [42] in the ﬁeld of image processing. We extend it into 3D space and mainly utilize the 3D submanifold sparse convolution [34] as the backbone for performing spatial attention between the F′ s with F′ m as: F′ sm = F′ s ⊗ Sigmoid(3DConv1×1×1(F′ m)), (5) where ⊗ represent element-wise multiplication, 3DConv1×1×1(·) represent a 3D submanifold sparse convolution with 1×1×1 kernel size, and F′ sm ∈ RM×D are the fused motion-salient features, and D denotes the number of feature channels. We then perform channel attention for F′ sm to strengthen the responses of key attributes. Subsequently, it is element-wisely added by F′ s because the static semantic features are equally crucial for the 4D semantic segmentation. The ﬁnal F′′ sm is calculated as: F′′ sm=F′ sm ⊗ [Softmax(2DConv1×1(AvgPool(F′ sm))) · D] + F′ s, (6) where 2DConv1×1(·) and AvgPool(·) denote a 2D convolution with 1 × 1 kernel size and average pooling operation, respec- tively. 2D convolution is mainly used to quickly calculate channel attention weights, which is diﬀerent from using 3D convolution for spatial attention as mentioned earlier. Finally, we further reﬁne F′′ sm using 3D sparse convolutions and channel attention blocks [43] to generate the ﬁnal 4D semantic segmentation predictions F′′ s ∈ RM×C′, where C′ is the number of categories for 4D semantic segmentation. E. Moving Instance Reﬁnement To further enhance the accuracy of MOS, we check again the point-wise predictions within the instance bounding box and propose an instance-aware post-processing algorithm for point-level reﬁnement, combining in a bottom-up and top- down fashion. This bottom-up aims to reﬁne the results of the follow- ing second cases. Firstly, if many points within an instance are moving, then the instance is considered to be moving. Secondly, if the scene contains many moving vehicles, it is considered as a highly dynamic scene, such as the highway. Vehicles in this scene will be more easily classiﬁed as the moving class with a lower conﬁdence threshold. During the top-down step, when an instance is identiﬁed as moving, all points within the instance are determined as moving, which is natural when considering each instance as a rigid body. Besides, because motion is a continuous process, we consider an instance to be moving only when classiﬁed as a moving class in multiple observations. The details for the algorithmic process please refer to our previous conference paper [17].

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

### F. Loss Function

Due to multi-task setup, our loss function includes instance detection loss Ldet, MOS loss Lmos, SSS loss Ls sem and 4D semantic segmentation loss L4D sem. In order to achieve a balance between the magnitudes of diﬀerent loss func- tions and to expedite the convergence speed, we apply a weighted multi-task loss [44] Ltotal to supervise the training, deﬁned as: Ltotal = X i∈{det,mos,s sem,4D sem} 1 2σ2 i Li + ln � 1 + σ2 i � , (7) where σi is a learnable parameter used to represent the uncertainty of Li. Ldet is composed of instance classiﬁcation loss and bounding box regression loss. More details can be found in the CenterHead [41]. In addition, we employ the widely used weighed Cross-Entropy Loss function [22] for Lmos, Ls sem and L4D sem: L{mos,s sem,m sem}(y, ˆy) = − X αip (yi) log (p (ˆyi)) , αi = 1/ p fi, (8) where yi and ˆyi denote the ground truth and the predicted labels, respectively. fi is the frequency of the i-th class. IV. EXPERIMENTAL EVALUATION In this section, we conduct a series of experiments on SemanticKITTI [14] and nuScenes [45] datasets to demon- strate SegNet4D’s capabilities on 4D semantic segmentation (Sec. IV-A) and MOS (Sec. IV-B) and compare the perfor- mance with SOTA. Subsequently, we integrate the method into a real robotic platform (Sec. IV-C), highlighting its practical utility. Besides, we perform ablation experiments to evaluate the eﬀectiveness of the framework and the proposed modules (Sec. IV-D). Finally, we also conduct a detailed runtime analysis, demonstrating the high eﬃciency of our method (Sec. IV-E). These experimental results will substantiate our claims regarding the contributions. 1) Datasets-SemanticKITTI [14]: SemanticKITTI provides semantic labels for each individual LiDAR scan in the KITTI [46] odometry dataset, which comprises 22 sequences col- lected with a Velodyne HDL-64E LiDAR. Following previous Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

WANG et al.: SegNet4D: EFFICIENT INSTANCE-AWARE 4D SEMANTIC SEGMENTATION 15345 TABLE I 4D SEMANTIC SEGMENTATION PERFORMANCE EVALUATION ON THE SEMANTICKITTI BENCHMARK (MULTI-SCAN PHASE). “MOV.” DENOTES MOVING. THE BEST RESULTS ARE IN BOLD work [1], [28], we use the standard data split where sequences 00 to 10 are used for training (with sequence 08 for val- idation), and sequences 11 to 21 for testing. The dataset contains multiple semantic category labels, and the semantic segmentation task is oﬃcially divided into two phases. One is the single-scan phase training 19 semantic classes without distinguishing point-wise dynamic attributes. The other is the multi-scan phase, which includes 25 semantic categories that distinguish between moving and static objects. To evaluate the 4D semantic segmentation performance of our SegNet4D, we test it in the multi-scan phase. In our model, the training is supervised with 26 semantic categories, including 6 moving classes, 19 static classes, and one outlier class. For the MOS task, All the semantic categories are reorganized into two classes: moving and static [21], [26]. Due to the imbalanced distribution of moving objects between the training and test set, an additional dataset, KITTI-Road, is introduced in [22] to mitigate the impact. We follow the experimental setups described in [22] to test the MOS performance. 2) Datasets-nuScenes [45]: It consists of 1000 driving scenes collected with a 32-beam LiDAR sensor. For point cloud segmentation tasks, it is mainly used for evaluat- ing SSS with 16 static semantic classes. To achieve 4D segmentation evaluation, inspired by [13], we utilize the annotated bounding box motion attributes to generate 8 new moving categories, including moving car, moving bus, moving truck, moving construction vehicle, moving trailer, moving motorcyclist, moving bicyclist, and moving person. This is a new multi-scan phase similar to SemanticKITTI. We have released the multi-scan semantic segmentation dataset of nuScenes for the convenience of the community. For evaluating MOS, we divide all semantic categories into two classes (moving and static). 3) Implementation Details: We restrict the point cloud range in [x : ±60m, y : ±50m, z : −4m ∼ 2m] for SemanticKITTI, [x : ±50m, y : ±50m, z : −4m ∼ 2m] for nuScenes, and set g = 0.1m for encoding motion features. For 4D semantic segmentation, we set C = 20,C′ = 26, O = 3 for SemanticKITTI and C = 17,C′ = 25, O = 10 for nuScenes. The proposed model is built on the PyTorch [47] library and trained with 4 NVIDIA RTX 3090 GPUs. We set the batch size to 8 on a single GPU and train the network for a total of 80 epochs. The learning rate is initialized as 10−4 in the Adam optimizer [48] and a decay factor of 0.01 for each epoch. During the training process, we employ widely-used data augmentation techniques such as random ﬂipping, scaling, and rotation to improve model performance. 4) Evaluation Metrics: For MOS performance evaluation, we use the Intersection-over-Union (IoU) [49] of moving objects as the metric: IoU = TP TP + FP + FN, (9) where TP, FP, and FN represent the predictions of the moving class that are classiﬁed as true positive, false positive, and false negative, respectively. For 4D semantic segmentation, we use the mean Intersection-over-Union (mIoU) across all categories as the evaluation metric. A. Evaluation for 4D Semantic Segmentation We evaluate the 4D semantic segmentation performance of our approach on the SemanticKITTI multi-scan semantic segmentation benchmark and nuScenes dataset, and compare the results with LiDAR-only SOTA baselines, including (a) single-scan-based methods (stack historical LiDAR scans into a single point cloud as input for multi-scans semantic segmen- tation): KPConv [9], Cylinder3D [1]; and specially designed multi-scans semantic segmentation methods: SpSequenceNet [11], TemporalLidarSeg [12], MarS3D [13], SVQNet [30] and MemorySeg [28]. Like all methods, we only utilize the past two LiDAR scans to predict semantic labels for a fair comparison, i.e., N = 3. The quantitative results are presented in Tab. I. Our approach achieves a mIoU of 60.9% on the SemanticKITTI dataset and outperforms all methods, demonstrating its eﬀec- tiveness. For semantic class bicyclist and motorcyclist, our SegNet4D obtains a signiﬁcant improvement, indicating that the incorporation of instance information enables our model to identify these foreground points more eﬀectively. Besides, our method boasts the fastest execution speed and is the only approach capable of real-time operation on the SemanticKITTI Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

15346 IEEE TRANSACTIONS ON AUTOMATION SCIENCE AND ENGINEERING, VOL. 22, 2025 TABLE II 4D SEMANTIC SEGMENTATION PERFORMANCE EVALUATION ON THE NUSCENES DATASET. “MOV.” DENOTES MOVING Fig. 7. The qualitative results comparison between our approach and MarS3D on the nuScenes dataset. dataset, showing its highly eﬃcient for 4D LiDAR semantic segmentation. For more runtime analysis, please refer to Sec. IV-E. Additionally, we further evaluate our approach on the nuScenes datasets and compare the performance with other baselines. Note that some methods in the Tab. I is not open-source, preventing their evaluation in the nuScenes multi- scan phase. This also further highlights the contribution of our open-source release in supporting community research. As shown in Tab. II, our method consistently delivers the best performance, demonstrating its adaptability to diﬀerent types of LiDAR and scene changes. The qualitative com- parison with MarS3D, as illustrated in Fig. 7, reveals our approach’s superior ability for moving object recognition. This is also further corroborated by quantitative analyses presented in the Sec. IV-B. Additionally, our method exhibits complete segmentation for big instances, like trucks, con- trasting with Mars3D’s incomplete segmentation results. This contrast highlights the eﬀectiveness of our instance-aware design.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

### B. Evaluation for Moving Object Segmentation

We evaluate the result on the SemanticKITTI-MOS bench- mark and nuScenes dataset, and compare it with SOTA MOS methods, including (a) projection-based: LMNet [21], MotionSeg3D [22], RVMOS [2], MotionBEV [25] and MF- MOS [23]; (b) point-based: 4DMOS [26] and InsMOS [17]; as well as open-source 4D segmentation baselines: KPConv [9], SpSequenceNet [11], Cylinder3D [1] and MarS3D [13]. The quantitative comparison is presented in Tab. III. Our method achieves the best results on both the SemanticKITTI and nuScenes dataset, demonstrating its superior performance in motion segmentation. SegNet4D also shows improved per- formance compared to original InsMOS [17], indicating that semantic information is beneﬁcial for the identiﬁcation of moving objects, as it provides a vital cue for distinguishing Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

WANG et al.: SegNet4D: EFFICIENT INSTANCE-AWARE 4D SEMANTIC SEGMENTATION 15347 TABLE III MOS PERFORMANCE EVALUATION (IOU [%]) Fig. 8. Our self-developed tracked mobile platform for experiments. For perception tasks, such as segmentation or detection, there is no diﬀerence with respect to wheeled platforms. between movable and immovable classes. Additionally, our method signiﬁcantly outperforms other 4D semantic segmen- tation methods in terms of MOS performance, beneﬁting from our framework’s explicit MOS supervision during the training phase. C. Operation on Real-World Platform To substantiate the real-world utility of SegNet4D, we further simplify and accelerate the model using half-precision ﬂoating-point arithmetic and parallel motion feature encoding, subsequently integrating it into an operational robotic system. As shown in Fig. 8, our platform is equipped with a RoboSense Helios-32 LiDAR with 10 Hz sampling frequency, an Xsens MTI-300 IMU, a CMOS camera, and an industrial computer with Intel Core i7-1165G7, 16G RAM, and NVIDIA RTX 2060 GPU. In the operational phase, we utilize LiDAR and IMU data to calculate odometry poses using the FAST-LIO [50] algorithm. Our method achieves real-time operation at 15.7Hz rate on the self-developed platform, faster than the typical rota- tion LiDAR sensor frame-rate of 10Hz. We also utilize this platform to collect a dataset from the campus scene and qualitatively compare the semantic segmentation results with Cylinder3D [1] and Mars3D [13]. All methods are only trained on the nuScenes dataset and directly applied for inference on our dataset. As illustrated in Fig. 9, we can see that our SegNet4D gets the best segmentation results, demonstrating its Fig. 9. The qualitative comparison on our campus scene. Our approach can more accurately identify the drivable surfaces, persons, and manmade buildings, whereas Cylinder3D and MarS3D show a decline in performance. TABLE IV MOS GENERALIZABILITY EVALUATION ON OUR CAMPUS DATASET TABLE V ABLATION STUDIES ON THE NUSCENES VALIDATION SET. MOS: MOVING OBJECT SEGMENTATION. SSS: SINGLE-SCAN SEMANTIC SEGMEN- TATION. MANUAL MS: MANUALLY MERGING MOS AND SSS FOR MULTI-SCAN SEMANTIC SEGMENTATION. NETWORK MS: THE NETWORK’S PREDICTIONS FOR MULTI-SCAN SEMAN- TIC SEGMENTATION, I.E., THE OUTPUT OF MSFM FOR [A],[C],[D], THE OUTPUT BY ONE HEAD FOR [B] practical utility for the real platform. Additionally, we manu- ally annotate a sequence (900 frames) with moving labels to quantitatively evaluate the MOS generalization performance. From the results shown in Tab. IV, our method still possesses the best generalization ability. The above-mentioned experimental results show that Seg- Net4D can operate in real-time on the real unmanned ground platform while exhibiting superior performance in 4D seman- tic segmentation and MOS. This highlights its practical utility in enhancing robots’ environmental perception capabilities.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

### D. Ablation Study

In this section, we conduct a series of ablation experiments on our framework and MSFM module to test their eﬀec- tiveness. The results are shown in Tab. V, Here, “Instance” indicates whether instance information is integrated into the Upsample Fusion Module to achieve instance-aware seg- mentation. “One Head” means directly predicting multi-scan semantic labels using only one head, indicating an end-to-end fashion. “Two Head” means utilizing two heads (the motion head and the semantic head, i.e., our framework) to predict moving objects and single-scan semantic labels, respectively, Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

15348 IEEE TRANSACTIONS ON AUTOMATION SCIENCE AND ENGINEERING, VOL. 22, 2025 TABLE VI RUNTIME ANALYSIS. THE BEST RESULT ARE IN BOLD and ﬁnally merging their results to achieve multi-scan semantic segmentation. “Reﬁnement” refers to moving instance reﬁne- ment mentioned in Sec. III-E, and it only focuses on reﬁning the motion predictions. By comparing [A] and [C], we can see that incorporat- ing instance information can improve the accuracy of MOS and semantic segmentation, which equips the network with instance-aware segmentation capabilities, and the results sub- stantiate our second claim. In the [B] and [C], predicting multi-scan semantic labels directly from a head is even inferior to the results obtained by manually integrating outputs from the motion head and the semantic head. This illustrates the superiority of our framework in comparison to directly predict- ing multi-scan semantic labels using an end-to-end manner, thereby supporting our ﬁrst claims. The results of [C] and [D] indicate that the reﬁnement is eﬀective for improving the motion predictions, which further proves the utility of instance information. Besides, we manually merge the predictions of MOS and SSS, labeled as Manual MS in the Tab. V, and compare its results with the output of the proposed MSFM. We can see that the MSFM’s segmentation result always outperforms manual fusion, conﬁrming its eﬀectiveness in integrating motion and static semantic predictions.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

### E. Runtime Analysis

To thoroughly assess the computational eﬃciency of our proposed network, we conduct a comprehensive analysis of its inference time, parameter count, and ﬂoating-point operations (FLOPs) utilizing a single NVIDIA 3090 GPU, benchmarking against all open-source 4D semantic segmentation networks. As shown in Tab. VI, our method achieves the fastest runtime on both the SemanticKITTI and nuScenes datasets, while also exhibiting the lowest FLOPs, demonstrating its superior computational eﬃciency. Furthermore, our network comprises 35.7M parameters, indicating small memory consumption suit- able for limited onboard resources.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## Method

### V. CONCLUSION AND FUTURE WORK

In this paper, we present a novel 4D semantic segmentation method to predict both point-wise moving labels and semantic labels for LiDAR data, and operate in real-time. The frame- work decomposes the complex 4D semantic segmentation task into MOS and SSS tasks, ﬁnally merging their predictions to achieve more accurate 4D semantic segmentation. We adopt a projection-based approach to quickly obtain motion features, which signiﬁcantly reduces the computational complexity compared to 4D convolutions. To achieve instance-aware seg- mentation, we concatenate the motion features with the spatial features of the current scan, feeding them into the network for instance detection, and subsequently inject the instance features into the prediction pipeline. In addition, we design a motion-semantic fusion module to integrate the point-wise motion states and static semantic predictions, enabling motion- guided 4D semantic segmentation. Extensive experiments on multiple datasets and a real-world unmanned ground platform demonstrate the superiority of our method. The detailed run- time analysis further highlights its computational eﬃciency, conﬁrming its real-time operation feasibility across diverse LiDAR conﬁgurations. Despite its strengths, our system faces limitations, notably, BEV-based motion extraction fashion may overlook moving objects obscured in the Z-direction. Future studies may inte- grate the range images to enhance the robustness of motion feature extraction. Additionally, SegNet4D currently cannot operate on embedded GPU platforms due to limitations in 3D sparse convolution version. Subsequently, we may employ TensorRT to accelerate the model, further enhancing its eﬃ- ciency and integrating it into low-cost robot platforms. Beyond the aforementioned, future studies may exploit the instance information we introduced to broaden the network’s capabili- ties, including panoptic segmentation [37] and 4D panoptic segmentation [36]. Furthermore, studies could leverage our predicted 4D semantic labels to boost robotic autonomy, particularly in applications such as semantic SLAM [6], semantic-based navigation [3] or planning [51].

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## References

[1] X. Zhu et al., “Cylindrical and asymmetrical 3D convolution networks for LiDAR-based perception,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 10, pp. 6807–6822, Oct. 2022. [2] J. Kim, J. Woo, and S. Im, “RVMOS: Range-view moving object segmentation leveraged by semantic and motion features,” IEEE Robot. Autom. Lett., vol. 7, no. 3, pp. 8044–8051, Jul. 2022. [3] S. Felicioni, E. Burani, M. Leomanni, M. L. Fravolini, P. Valigi, and G. Costante, “Integrating occupancy grid with semantic road information for autonomous navigation in urban scenarios: A benchmark study,” in Proc. IEEE 20th Int. Conf. Autom. Sci. Eng. (CASE), Aug. 2024, pp. 2665–2671. [4] C. Shi, X. Chen, H. Lu, W. Deng, J. Xiao, and B. Dai, “RDMNet: Reliable dense matching based point cloud registration for autonomous driving,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 10, pp. 11372–11383, Oct. 2023. [5] Z. Qiao, Z. Yu, B. Jiang, H. Yin, and S. Shen, “G3Reg: Pyramid graph- based global registration using Gaussian ellipsoid model,” IEEE Trans. Autom. Sci. Eng., vol. 22, pp. 3416–3432, 2025. [6] J. Jiao et al., “Real-time metric-semantic mapping for autonomous navigation in outdoor environments,” IEEE Trans. Autom. Sci. Eng., vol. 22, pp. 5729–5740, 2025. [7] X. Chen, A. Milioto, E. Palazzolo, P. Gigu`ere, J. Behley, and C. Stachniss, “SuMa++: Eﬃcient LiDAR-based semantic SLAM,” in Proc. IEEE/RSJ Intl. Conf. Intell. Robots Syst. (IROS), Nov. 2019, pp. 4530–4537. [Online]. Available: http://www.ipb.uni-bonn.de/ wp-content/papercite-data/pdf/chen2019iros.pdf [8] F. Wang, Z. Wu, Y. Yang, W. Li, Y. Liu, and Y. Zhuang, “Real-time semantic segmentation of LiDAR point clouds on edge devices for unmanned systems,” IEEE Trans. Instrum. Meas., vol. 72, pp. 1–11, 2023. [9] H. Thomas, C. R. Qi, J.-E. Deschaud, B. Marcotegui, F. Goulette, and L. Guibas, “KPConv: Flexible and deformable convolution for point clouds,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2019, pp. 6410–6419. Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

WANG et al.: SegNet4D: EFFICIENT INSTANCE-AWARE 4D SEMANTIC SEGMENTATION 15349 [10] S. Li, X. Chen, Y. Liu, D. Dai, C. Stachniss, and J. Gall, “Multi-scale interaction for real-time LiDAR data segmentation on an embed- ded platform,” IEEE Robot. Autom. Lett., vol. 7, no. 2, pp. 738–745, Apr. 2022. [Online]. Available: https://www.ipb.uni-bonn.de/wp-content/ papercite-data/pdf/li2022ral.pdf [11] H. Shi, G. Lin, H. Wang, T.-Y. Hung, and Z. Wang, “SpSequenceNet: Semantic segmentation network on 4D point clouds,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2020, pp. 4573–4582. [Online]. Available: https://openaccess.thecvf.com/content CVPR 2020/papers/ Shi SpSequenceNet Semantic Segmentation Network on 4D Point Clouds CVPR 2020 paper.pdf [12] F. Duerr, M. Pfaller, H. Weigel, and J. Beyerer, “LiDAR-based recurrent 3D semantic segmentation with temporal memory alignment,” in Proc. Int. Conf. 3D Vis. (3DV), Nov. 2020, pp. 781–790. [Online]. Available: https://api.semanticscholar.org/CorpusID:231684481 [13] J. Liu, C. Chang, J. Liu, X. Wu, L. Ma, and X. Qi, “MarS3D: A plug-and-play motion-aware model for semantic segmentation on multi-scan 3D point clouds,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2023, pp. 9372–9381. [Online]. Avail- able: https://api.semanticscholar.org/CorpusID:259950838 [14] J. Behley et al., “SemanticKITTI: A dataset for semantic scene under- standing of LiDAR sequences,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2019, pp. 9297–9307. [15] C. Choy, J. Gwak, and S. Savarese, “4D spatio-temporal ConvNets: Minkowski convolutional neural networks,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2019, pp. 3070–3079. [16] P. Schutt, R. A. Rosu, and S. Behnke, “Abstract ﬂow for temporal semantic segmentation on the permutohedral lattice,” in Proc. Int. Conf. Robot. Autom. (ICRA), May 2022, pp. 5139–5145. [17] N. Wang, C. Shi, R. Guo, H. Lu, Z. Zheng, and X. Chen, “InsMOS: Instance-aware moving object segmentation in LiDAR data,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), Oct. 2023, pp. 7598–7605. [18] X. Chen et al., “Automatic labeling to generate training data for online LiDAR-based moving object segmentation,” IEEE Robot. Autom. Lett., vol. 7, no. 3, pp. 6107–6114, Jul. 2022. [19] P. W. Patil, K. M. Biradar, A. Dudhane, and S. Murala, “An end-to-end edge aggregation network for moving object segmentation,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2020, pp. 8146–8155. [Online]. Available: https:// openaccess.thecvf.com/content CVPR 2020/papers/Patil An End- to-End Edge Aggregation Network for Moving Object Segmentation CVPR 2020 paper.pdf [20] J. H. Giraldo, S. Javed, and T. Bouwmans, “Graph moving object segmentation,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 5, pp. 2485–2503, May 2022. [21] X. Chen et al., “Moving object segmentation in 3D LiDAR data: A learning-based approach exploiting sequential data,” IEEE Robot. Autom. Lett., vol. 6, no. 4, pp. 6529–6536, Oct. 2021. [Online]. Avail- able: http://www.ipb.uni-bonn.de/pdfs/chen2021ral-iros.pdf [22] J. Sun et al., “Eﬃcient spatial–temporal information fusion for LiDAR- based 3D moving object segmentation,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), Oct. 2022, pp. 11456–11463. [23] J. Cheng et al., “MF-MOS: A motion-focused model for mov- ing object segmentation,” in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), May 2024, pp. 12499–12505. [Online]. Available: https:// api.semanticscholar.org/CorpusID:267320275 [24] S. Mohapatra et al., “LiMoSeg: Real-time bird’s eye view based LiDAR motion segmentation,” 2021, arXiv:2111.04875. [25] B. Zhou, J. Xie, Y. Pan, J. Wu, and C. Lu, “MotionBEV: Attention-aware online LiDAR moving object segmentation with bird’s eye view based appearance and motion features,” IEEE Robot. Autom. Lett., vol. 8, no. 12, pp. 8074–8081, Dec. 2023. [26] B. Mersch, X. Chen, I. Vizzo, L. Nunes, J. Behley, and C. Stach- niss, “Receding moving object segmentation in 3D LiDAR data using sparse 4D convolutions,” IEEE Robot. Autom. Lett., vol. 7, no. 3, pp. 7503–7510, Jul. 2022. [27] T. Kreutz, M. M¨uhlh¨auser, and A. S. Guinea, “Unsupervised 4D LiDAR moving object segmentation in stationary settings with multivariate occupancy time series,” in Proc. IEEE/CVF Winter Conf. Appl. Comput. Vis. (WACV), Jan. 2023, pp. 1644–1653. [28] E. Li, S. Casas, and R. Urtasun, “MemorySeg: Online LiDAR semantic segmentation with a latent memory,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2023, pp. 745–754. [Online]. Available: https://api.semanticscholar.org/CorpusID:265019334 [29] H. Shi, J. Wei, H. Wang, F. Liu, and G. Lin, “Learning temporal variations for 4D point cloud segmentation,” Int. J. Comput. Vis., vol. 132, no. 12, pp. 5603–5617, Dec. 2024. [Online]. Available: https:// api.semanticscholar.org/CorpusID:270670906 [30] X. Chen, S. Xu, X. Zou, T. Cao, D.-Y. Yeung, and L. Fang, “SVQNet: Sparse voxel-adjacent query network for 4D spatio-temporal LiDAR semantic segmentation,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2023, pp. 8535–8544. [Online]. Available: https:// api.semanticscholar.org/CorpusID:261214641 [31] K. Yilmaz, J. Schult, A. Nekrasov, and B. Leibe, “Mask4Former: Mask transformer for 4D panoptic segmentation,” in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), May 2024, pp. 9418–9425. [32] F. Hong, L. Kong, H. Zhou, X. Zhu, H. Li, and Z. Liu, “Uniﬁed 3D and 4D panoptic segmentation via dynamic shifting networks,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 46, no. 5, pp. 3480–3495, May 2024. [33] I. Fradlin, I. Zulﬁkar, K. Yilmaz, T. Kontogianni, and B. Leibe, “Interactive4D: Interactive 4D LiDAR segmentation,” in Proc. IEEE Int. Conf. Robot. Autom. (ICRA), Oct. 2025, pp. 1–15. [34] B. Graham, M. Engelcke, and L. V. D. Maaten, “3D semantic segmentation with submanifold sparse convolutional networks,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., Jun. 2018, pp. 9224–9232. [Online]. Available: http://openaccess.thecvf.com/content cvpr 2018/papers/ Graham 3D Semantic Segmentation CVPR 2018 paper.pdf [35] X. Lai, Y. Chen, F. Lu, J. Liu, and J. Jia, “Spherical transformer for LiDAR-based 3D recognition,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2023, pp. 17545–17555. [36] M. Ayg¨un et al., “4D panoptic LiDAR segmentation,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2021, pp. 5523–5533. [37] R. Marcuzzi, L. Nunes, L. Wiesmann, J. Behley, and C. Stachniss, “Mask-based panoptic LiDAR segmentation for autonomous driving,” IEEE Robot. Autom. Lett., vol. 8, no. 2, pp. 1141–1148, Feb. 2023. [38] R. B. Rusu and S. Cousins, “3D is here: Point cloud library (PCL),” in Proc. IEEE Int. Conf. Robot. Autom., May 2011, pp. 1–4. [39] H. Hotelling, “Analysis of a complex of statistical variables into principal components,” J. Educ. Psychol., vol. 24, no. 7, pp. 498–520, Oct. 1933. [Online]. Available: https://api.semanticscholar.org/ CorpusID:144828484 [40] X. Zhang, W. Xu, C. Dong, and J. M. Dolan, “Eﬃcient L-shape ﬁtting for vehicle detection using laser scanners,” in Proc. IEEE Intell. Vehicles Symp., Jun. 2017, pp. 54–59. [41] T. Yin, X. Zhou, and P. Kr¨ahenb¨uhl, “Center-based 3D object detection and tracking,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2021, pp. 11779–11788. [42] H. Li, G. Chen, G. Li, and Y. Yu, “Motion guided attention for video salient object detection,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2019, pp. 7273–7282. [43] S. Woo, J. Park, J.-Y. Lee, and I. S. Kweon, “CBAM: Convolutional block attention module,” in Proc. Eur. Conf. Comput. Vis., Sep. 2018, pp. 3–19. [44] L. Liebel and M. K¨orner, “Auxiliary tasks in multi-task learning,” 2018, arXiv:1805.06334. [45] H. Caesar et al., “NuScenes: A multimodal dataset for autonomous driving,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2020, pp. 11618–11628. [Online]. Available: https:// api.semanticscholar.org/CorpusID:85517967 [46] A. Geiger, P. Lenz, and R. Urtasun, “Are we ready for autonomous driving? The KITTI vision benchmark suite,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., Jun. 2012, pp. 3354–3361. [Online]. Available: http://www.cvlibs.net/publications/Geiger2012CVPR.pdf [47] A. Paszke et al., “Pytorch: An imperative style, high-performance deep learning library,” in Proc. Adv. Neural Inf. Process. Syst., 2019, pp. 8026–8037. [Online]. Available: http://papers.nips.cc/paper/9015- pytorch-an-imperative-style-high-performance-deep-learning-library.pdf [48] D. Kingma and J. Ba, “Adam: A method for stochastic optimization,” 2014, arXiv:1412.6980. [49] M. Everingham, L. Van Gool, C. K. I. Williams, J. Winn, and A. Zisserman, “The Pascal visual object classes (VOC) challenge,” Int. J. Comput. Vis., vol. 88, no. 2, pp. 303–338, 2010. [Online]. Available: https://pdfs.semanticscholar.org/0ee1/ 916a0cb2dc7d3add086b5f1092c3d4beb38a.pdf [50] W. Xu, Y. Cai, D. He, J. Lin, and F. Zhang, “FAST-LIO2: Fast direct LiDAR-inertial odometry,” IEEE Trans. Robot., vol. 38, no. 4, pp. 2053–2073, Aug. 2022. Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

15350 IEEE TRANSACTIONS ON AUTOMATION SCIENCE AND ENGINEERING, VOL. 22, 2025 [51] L. Lu et al., “Semantics-aware receding horizon planner for object- centric active mapping,” IEEE Robot. Autom. Lett., vol. 9, no. 4, pp. 3838–3845, Apr. 2024. Neng Wang received the B.E. degree in automa- tion from Southwest Petroleum University, China, in 2021. He is currently pursuing the Ph.D. degree with the National University of Defense Technol- ogy (NUDT). His research interests include point cloud segmentation and semantic-based simultane- ous localization and mapping (SLAM). Ruibin Guo received the B.S. degree in communica- tion engineering, the M.S. degree in information and communication engineering, and the Ph.D. degree from the National University of Defense Technology (NUDT), in 2012, 2014, and 2019, respectively. He is currently a Lecturer with NUDT. His research interests include computer vision, simultaneous localization and mapping, and 3D reconstruction. Chenghao Shi received the B.E. degree from Nanjing University of Aeronautics and Astronautics (NUAA) and the M.E. and Ph.D. degrees in robotics from the National University of Defense Technology (NUDT), China, in 2017, 2019, and 2024, respec- tively. He is currently a Lecturer with the NUDT, China. His research interests include localization and mobile robots. Ziyue Wang received the Bachelor of Engineering degree from Nanjing University of Science and Technology (NJUST) in 2023. He is currently pursu- ing the Ph.D. degree with the National University of Defense Technology (NUDT). His research interests include uncertainty of mapping. Hui Zhang received the B.E., M.E., and Ph.D. degrees from the National University of Defense Technology, China, in 1993, 1996, and 2000, respec- tively. He became a Professor with the National University of Defense Technology in 2011. His research interests include mobile robots, simul- taneous localization and mapping, and intelligent control. Huimin Lu (Member, IEEE) received the B.E. degree in automation and the M.E. and Ph.D. degrees in control science and engineering from the National University of Defense Technology (NUDT), Chang- sha, China, in 2003, 2005, and 2010, respectively. He joined the College of Intelligence Science and Technology, NUDT, in 2010, where he is cur- rently a Professor. His research interests include mobile robotics, mainly robot vision, multi-robot coordination, and human-robot interaction. Zhiqiang Zheng received the Ph.D. degree in aerospace engineering from the University of Liege, Liege, Belgium, in 1994. He is currently a Professor with the College of Intelligent Science and Tech- nology, National University of Defense Technology, Changsha, China. His research interests include precision guidance and control and multirobot coordination control. Xieyuanli Chen (Member, IEEE) received the bachelor’s degree in electrical engineering and automation from Hunan University, China, in 2015, the master’s degree in robotics from the National University of Defense Technology, China, in 2017, and the Ph.D. degree from the Photogrammetry and Robotics Laboratory, University of Bonn. He is currently an Associate Professor with the National University of Defense Technology, China. He also serves as an Associate Editor for IEEE ROBOTICS AND AUTOMATION LETTERS. Authorized licensed use limited to: Hebei University of Technology. Downloaded on December 17,2025 at 07:34:24 UTC from IEEE Xplore.  Restrictions apply.

**详细解析 (Detailed Analysis):**

<!-- 待后续进行更详细的中文解析 -->
<!-- This section is reserved for detailed Chinese analysis -->

---

## 提取的图片 (Extracted Images)

以下是从论文中提取的所有图片，按页码分组。

Below are all images extracted from the paper, grouped by page number.

### 第 2 页 (Page 2)

**图片 1 (Image 1):**

![Page 2 Image 1](paper_images/page_02_img_1.jpeg)

**图片 2 (Image 2):**

![Page 2 Image 2](paper_images/page_02_img_2.jpeg)

**图片 3 (Image 3):**

![Page 2 Image 3](paper_images/page_02_img_3.jpeg)

**图片 4 (Image 4):**

![Page 2 Image 4](paper_images/page_02_img_4.jpeg)

**图片 5 (Image 5):**

![Page 2 Image 5](paper_images/page_02_img_5.jpeg)

### 第 3 页 (Page 3)

**图片 1 (Image 1):**

![Page 3 Image 1](paper_images/page_03_img_1.flate)

**图片 2 (Image 2):**

![Page 3 Image 2](paper_images/page_03_img_2.jpeg)

**图片 3 (Image 3):**

![Page 3 Image 3](paper_images/page_03_img_3.flate)

**图片 4 (Image 4):**

![Page 3 Image 4](paper_images/page_03_img_4.flate)

**图片 5 (Image 5):**

![Page 3 Image 5](paper_images/page_03_img_5.flate)

**图片 6 (Image 6):**

![Page 3 Image 6](paper_images/page_03_img_6.flate)

**图片 7 (Image 7):**

![Page 3 Image 7](paper_images/page_03_img_7.flate)

**图片 8 (Image 8):**

![Page 3 Image 8](paper_images/page_03_img_8.flate)

**图片 9 (Image 9):**

![Page 3 Image 9](paper_images/page_03_img_9.jpeg)

**图片 10 (Image 10):**

![Page 3 Image 10](paper_images/page_03_img_10.flate)

**图片 11 (Image 11):**

![Page 3 Image 11](paper_images/page_03_img_11.flate)

**图片 12 (Image 12):**

![Page 3 Image 12](paper_images/page_03_img_12.flate)

**图片 13 (Image 13):**

![Page 3 Image 13](paper_images/page_03_img_13.flate)

**图片 14 (Image 14):**

![Page 3 Image 14](paper_images/page_03_img_14.flate)

**图片 15 (Image 15):**

![Page 3 Image 15](paper_images/page_03_img_15.flate)

**图片 16 (Image 16):**

![Page 3 Image 16](paper_images/page_03_img_16.flate)

**图片 17 (Image 17):**

![Page 3 Image 17](paper_images/page_03_img_17.jpeg)

**图片 18 (Image 18):**

![Page 3 Image 18](paper_images/page_03_img_18.flate)

**图片 19 (Image 19):**

![Page 3 Image 19](paper_images/page_03_img_19.flate)

**图片 20 (Image 20):**

![Page 3 Image 20](paper_images/page_03_img_20.flate)

**图片 21 (Image 21):**

![Page 3 Image 21](paper_images/page_03_img_21.flate)

**图片 22 (Image 22):**

![Page 3 Image 22](paper_images/page_03_img_22.flate)

**图片 23 (Image 23):**

![Page 3 Image 23](paper_images/page_03_img_23.flate)

**图片 24 (Image 24):**

![Page 3 Image 24](paper_images/page_03_img_24.flate)

**图片 25 (Image 25):**

![Page 3 Image 25](paper_images/page_03_img_25.flate)

### 第 4 页 (Page 4)

**图片 1 (Image 1):**

![Page 4 Image 1](paper_images/page_04_img_1.flate)

**图片 2 (Image 2):**

![Page 4 Image 2](paper_images/page_04_img_2.jpeg)

**图片 3 (Image 3):**

![Page 4 Image 3](paper_images/page_04_img_3.jpeg)

**图片 4 (Image 4):**

![Page 4 Image 4](paper_images/page_04_img_4.jpeg)

**图片 5 (Image 5):**

![Page 4 Image 5](paper_images/page_04_img_5.jpeg)

**图片 6 (Image 6):**

![Page 4 Image 6](paper_images/page_04_img_6.flate)

**图片 7 (Image 7):**

![Page 4 Image 7](paper_images/page_04_img_7.flate)

**图片 8 (Image 8):**

![Page 4 Image 8](paper_images/page_04_img_8.flate)

**图片 9 (Image 9):**

![Page 4 Image 9](paper_images/page_04_img_9.flate)

**图片 10 (Image 10):**

![Page 4 Image 10](paper_images/page_04_img_10.flate)

**图片 11 (Image 11):**

![Page 4 Image 11](paper_images/page_04_img_11.flate)

**图片 12 (Image 12):**

![Page 4 Image 12](paper_images/page_04_img_12.jpeg)

**图片 13 (Image 13):**

![Page 4 Image 13](paper_images/page_04_img_13.flate)

**图片 14 (Image 14):**

![Page 4 Image 14](paper_images/page_04_img_14.jpeg)

**图片 15 (Image 15):**

![Page 4 Image 15](paper_images/page_04_img_15.flate)

**图片 16 (Image 16):**

![Page 4 Image 16](paper_images/page_04_img_16.flate)

**图片 17 (Image 17):**

![Page 4 Image 17](paper_images/page_04_img_17.flate)

**图片 18 (Image 18):**

![Page 4 Image 18](paper_images/page_04_img_18.flate)

**图片 19 (Image 19):**

![Page 4 Image 19](paper_images/page_04_img_19.flate)

**图片 20 (Image 20):**

![Page 4 Image 20](paper_images/page_04_img_20.flate)

**图片 21 (Image 21):**

![Page 4 Image 21](paper_images/page_04_img_21.flate)

**图片 22 (Image 22):**

![Page 4 Image 22](paper_images/page_04_img_22.flate)

**图片 23 (Image 23):**

![Page 4 Image 23](paper_images/page_04_img_23.flate)

**图片 24 (Image 24):**

![Page 4 Image 24](paper_images/page_04_img_24.jpeg)

**图片 25 (Image 25):**

![Page 4 Image 25](paper_images/page_04_img_25.jpeg)

**图片 26 (Image 26):**

![Page 4 Image 26](paper_images/page_04_img_26.flate)

**图片 27 (Image 27):**

![Page 4 Image 27](paper_images/page_04_img_27.flate)

**图片 28 (Image 28):**

![Page 4 Image 28](paper_images/page_04_img_28.flate)

**图片 29 (Image 29):**

![Page 4 Image 29](paper_images/page_04_img_29.jpeg)

**图片 30 (Image 30):**

![Page 4 Image 30](paper_images/page_04_img_30.flate)

**图片 31 (Image 31):**

![Page 4 Image 31](paper_images/page_04_img_31.flate)

**图片 32 (Image 32):**

![Page 4 Image 32](paper_images/page_04_img_32.flate)

### 第 5 页 (Page 5)

**图片 1 (Image 1):**

![Page 5 Image 1](paper_images/page_05_img_1.flate)

**图片 2 (Image 2):**

![Page 5 Image 2](paper_images/page_05_img_2.flate)

**图片 3 (Image 3):**

![Page 5 Image 3](paper_images/page_05_img_3.flate)

**图片 4 (Image 4):**

![Page 5 Image 4](paper_images/page_05_img_4.flate)

**图片 5 (Image 5):**

![Page 5 Image 5](paper_images/page_05_img_5.flate)

**图片 6 (Image 6):**

![Page 5 Image 6](paper_images/page_05_img_6.flate)

**图片 7 (Image 7):**

![Page 5 Image 7](paper_images/page_05_img_7.flate)

**图片 8 (Image 8):**

![Page 5 Image 8](paper_images/page_05_img_8.flate)

**图片 9 (Image 9):**

![Page 5 Image 9](paper_images/page_05_img_9.flate)

**图片 10 (Image 10):**

![Page 5 Image 10](paper_images/page_05_img_10.flate)

**图片 11 (Image 11):**

![Page 5 Image 11](paper_images/page_05_img_11.flate)

**图片 12 (Image 12):**

![Page 5 Image 12](paper_images/page_05_img_12.flate)

**图片 13 (Image 13):**

![Page 5 Image 13](paper_images/page_05_img_13.flate)

**图片 14 (Image 14):**

![Page 5 Image 14](paper_images/page_05_img_14.flate)

**图片 15 (Image 15):**

![Page 5 Image 15](paper_images/page_05_img_15.jpeg)

**图片 16 (Image 16):**

![Page 5 Image 16](paper_images/page_05_img_16.flate)

**图片 17 (Image 17):**

![Page 5 Image 17](paper_images/page_05_img_17.flate)

**图片 18 (Image 18):**

![Page 5 Image 18](paper_images/page_05_img_18.flate)

**图片 19 (Image 19):**

![Page 5 Image 19](paper_images/page_05_img_19.jpeg)

**图片 20 (Image 20):**

![Page 5 Image 20](paper_images/page_05_img_20.flate)

**图片 21 (Image 21):**

![Page 5 Image 21](paper_images/page_05_img_21.jpeg)

**图片 22 (Image 22):**

![Page 5 Image 22](paper_images/page_05_img_22.flate)

**图片 23 (Image 23):**

![Page 5 Image 23](paper_images/page_05_img_23.flate)

**图片 24 (Image 24):**

![Page 5 Image 24](paper_images/page_05_img_24.flate)

**图片 25 (Image 25):**

![Page 5 Image 25](paper_images/page_05_img_25.jpeg)

**图片 26 (Image 26):**

![Page 5 Image 26](paper_images/page_05_img_26.flate)

**图片 27 (Image 27):**

![Page 5 Image 27](paper_images/page_05_img_27.jpeg)

**图片 28 (Image 28):**

![Page 5 Image 28](paper_images/page_05_img_28.flate)

**图片 29 (Image 29):**

![Page 5 Image 29](paper_images/page_05_img_29.flate)

**图片 30 (Image 30):**

![Page 5 Image 30](paper_images/page_05_img_30.flate)

**图片 31 (Image 31):**

![Page 5 Image 31](paper_images/page_05_img_31.flate)

**图片 32 (Image 32):**

![Page 5 Image 32](paper_images/page_05_img_32.flate)

**图片 33 (Image 33):**

![Page 5 Image 33](paper_images/page_05_img_33.flate)

**图片 34 (Image 34):**

![Page 5 Image 34](paper_images/page_05_img_34.flate)

**图片 35 (Image 35):**

![Page 5 Image 35](paper_images/page_05_img_35.flate)

### 第 6 页 (Page 6)

**图片 1 (Image 1):**

![Page 6 Image 1](paper_images/page_06_img_1.flate)

**图片 2 (Image 2):**

![Page 6 Image 2](paper_images/page_06_img_2.flate)

**图片 3 (Image 3):**

![Page 6 Image 3](paper_images/page_06_img_3.flate)

**图片 4 (Image 4):**

![Page 6 Image 4](paper_images/page_06_img_4.flate)

**图片 5 (Image 5):**

![Page 6 Image 5](paper_images/page_06_img_5.flate)

**图片 6 (Image 6):**

![Page 6 Image 6](paper_images/page_06_img_6.jpeg)

**图片 7 (Image 7):**

![Page 6 Image 7](paper_images/page_06_img_7.flate)

### 第 8 页 (Page 8)

**图片 1 (Image 1):**

![Page 8 Image 1](paper_images/page_08_img_1.jpeg)

**图片 2 (Image 2):**

![Page 8 Image 2](paper_images/page_08_img_2.flate)

**图片 3 (Image 3):**

![Page 8 Image 3](paper_images/page_08_img_3.jpeg)

**图片 4 (Image 4):**

![Page 8 Image 4](paper_images/page_08_img_4.flate)

**图片 5 (Image 5):**

![Page 8 Image 5](paper_images/page_08_img_5.jpeg)

**图片 6 (Image 6):**

![Page 8 Image 6](paper_images/page_08_img_6.flate)

**图片 7 (Image 7):**

![Page 8 Image 7](paper_images/page_08_img_7.flate)

**图片 8 (Image 8):**

![Page 8 Image 8](paper_images/page_08_img_8.jpeg)

**图片 9 (Image 9):**

![Page 8 Image 9](paper_images/page_08_img_9.jpeg)

**图片 10 (Image 10):**

![Page 8 Image 10](paper_images/page_08_img_10.jpeg)

**图片 11 (Image 11):**

![Page 8 Image 11](paper_images/page_08_img_11.jpeg)

**图片 12 (Image 12):**

![Page 8 Image 12](paper_images/page_08_img_12.flate)

**图片 13 (Image 13):**

![Page 8 Image 13](paper_images/page_08_img_13.jpeg)

**图片 14 (Image 14):**

![Page 8 Image 14](paper_images/page_08_img_14.jpeg)

**图片 15 (Image 15):**

![Page 8 Image 15](paper_images/page_08_img_15.jpeg)

**图片 16 (Image 16):**

![Page 8 Image 16](paper_images/page_08_img_16.jpeg)

**图片 17 (Image 17):**

![Page 8 Image 17](paper_images/page_08_img_17.flate)

**图片 18 (Image 18):**

![Page 8 Image 18](paper_images/page_08_img_18.jpeg)

**图片 19 (Image 19):**

![Page 8 Image 19](paper_images/page_08_img_19.jpeg)

**图片 20 (Image 20):**

![Page 8 Image 20](paper_images/page_08_img_20.jpeg)

**图片 21 (Image 21):**

![Page 8 Image 21](paper_images/page_08_img_21.jpeg)

**图片 22 (Image 22):**

![Page 8 Image 22](paper_images/page_08_img_22.flate)

**图片 23 (Image 23):**

![Page 8 Image 23](paper_images/page_08_img_23.jpeg)

**图片 24 (Image 24):**

![Page 8 Image 24](paper_images/page_08_img_24.jpeg)

**图片 25 (Image 25):**

![Page 8 Image 25](paper_images/page_08_img_25.flate)

**图片 26 (Image 26):**

![Page 8 Image 26](paper_images/page_08_img_26.jpeg)

**图片 27 (Image 27):**

![Page 8 Image 27](paper_images/page_08_img_27.flate)

**图片 28 (Image 28):**

![Page 8 Image 28](paper_images/page_08_img_28.jpeg)

**图片 29 (Image 29):**

![Page 8 Image 29](paper_images/page_08_img_29.jpeg)

**图片 30 (Image 30):**

![Page 8 Image 30](paper_images/page_08_img_30.flate)

### 第 9 页 (Page 9)

**图片 1 (Image 1):**

![Page 9 Image 1](paper_images/page_09_img_1.jpeg)

**图片 2 (Image 2):**

![Page 9 Image 2](paper_images/page_09_img_2.jpeg)

**图片 3 (Image 3):**

![Page 9 Image 3](paper_images/page_09_img_3.jpeg)

**图片 4 (Image 4):**

![Page 9 Image 4](paper_images/page_09_img_4.jpeg)

**图片 5 (Image 5):**

![Page 9 Image 5](paper_images/page_09_img_5.jpeg)

**图片 6 (Image 6):**

![Page 9 Image 6](paper_images/page_09_img_6.jpeg)

**图片 7 (Image 7):**

![Page 9 Image 7](paper_images/page_09_img_7.jpeg)

**图片 8 (Image 8):**

![Page 9 Image 8](paper_images/page_09_img_8.flate)

**图片 9 (Image 9):**

![Page 9 Image 9](paper_images/page_09_img_9.flate)

**图片 10 (Image 10):**

![Page 9 Image 10](paper_images/page_09_img_10.flate)

**图片 11 (Image 11):**

![Page 9 Image 11](paper_images/page_09_img_11.jpeg)

**图片 12 (Image 12):**

![Page 9 Image 12](paper_images/page_09_img_12.jpeg)

**图片 13 (Image 13):**

![Page 9 Image 13](paper_images/page_09_img_13.jpeg)

**图片 14 (Image 14):**

![Page 9 Image 14](paper_images/page_09_img_14.jpeg)

**图片 15 (Image 15):**

![Page 9 Image 15](paper_images/page_09_img_15.jpeg)

### 第 12 页 (Page 12)

**图片 1 (Image 1):**

![Page 12 Image 1](paper_images/page_12_img_1.flate)

**图片 2 (Image 2):**

![Page 12 Image 2](paper_images/page_12_img_2.flate)

**图片 3 (Image 3):**

![Page 12 Image 3](paper_images/page_12_img_3.flate)

**图片 4 (Image 4):**

![Page 12 Image 4](paper_images/page_12_img_4.flate)

**图片 5 (Image 5):**

![Page 12 Image 5](paper_images/page_12_img_5.flate)

**图片 6 (Image 6):**

![Page 12 Image 6](paper_images/page_12_img_6.flate)

**图片 7 (Image 7):**

![Page 12 Image 7](paper_images/page_12_img_7.flate)

**图片 8 (Image 8):**

![Page 12 Image 8](paper_images/page_12_img_8.flate)

---

## 说明 (Notes)

- **提取日期 (Extraction Date):** 2026-01-28 09:05:19
- **章节数量 (Number of Sections):** 11
- **图片数量 (Number of Images):** 157

本文档由 PDF 提取工具自动生成。如需更详细的解析，请参考原始论文 PDF。

This document was automatically generated by the PDF extraction tool. For more detailed analysis, please refer to the original paper PDF.

