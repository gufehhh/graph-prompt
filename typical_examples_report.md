# 典型 Query 分类示例报告
# Typical Query Classification Examples Report

**生成时间 / Generated:** 2026-03-05 17:30 (Asia/Shanghai)  
**数据来源 / Data Source:** `results_20260305_160332/classify_prompt_v1/`

---

## 📊 概述 / Overview

本次分析从最新执行结果中提取了不同拓扑类别的典型 Query 示例。由于当前 Prompt 优化迭代中，绝大多数成功解析的 Query 都被分类为 **[Composite Graphs]（复合图）**，本报告将重点展示这一类别的多样化示例，并说明其分类原因。

**关键发现 / Key Findings:**
- 成功解析的 Query 中，100% 被分类为 [Composite Graphs]
- 这表明当前测试数据集中的问题普遍具有**多解法共享中间步骤**的特征
- 未观察到 [Single Graph]、[Concurrent Graphs]、[Divergent Graphs] 等其他类别的成功样本

---

## 📝 典型示例 / Typical Examples

### 类别 1: [Composite Graphs] - 算法/编程类问题
### Category 1: [Composite Graphs] - Algorithm/Programming Problems

---

#### 示例 1.1: 数字转换问题 / Number Conversion Problem

**英文原文 / English:**
> Convert a non-negative integer `num` to its English words representation.
> 
> **Example 1:**
> **Input:** num = 123
> **Output:** "One Hundred Twenty Three"
> 
> **Example 2:**
> **Input:** num = 12345
> **Output:** "Twelve Thousand Three Hundred Forty Five"
> 
> **Constraints:**
> `0 <= num <= 2^31 - 1`

**中文翻译 / Chinese:**
> 将一个非负整数 `num` 转换为其英文单词表示形式。
> 
> **示例 1:**
> **输入:** num = 123
> **输出:** "One Hundred Twenty Three"
> 
> **示例 2:**
> **输入:** num = 12345
> **输出:** "Twelve Thousand Three Hundred Forty Five"
> 
> **约束条件:**
> `0 <= num <= 2^31 - 1`

**分类理由 / Classification Reasoning:**
该问题存在多种解法（递归分解、迭代分解、预定义映射），所有解法都共享"将数字分解为三位一组"的中间步骤，并最终收敛到相同的输出结果。这符合复合图的定义：多条路径从共同起点出发，在中间节点相交，并汇聚到同一终点。

---

#### 示例 1.2: 图论问题 / Graph Theory Problem

**英文原文 / English:**
> In this problem, a tree is an **undirected graph** that is connected and has no cycles.
> 
> You are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional edge added. The added edge has two **different** vertices chosen from `1` to `n`, and was not an edge that already existed.
> 
> Return _an edge that can be removed so that the resulting graph is a tree of `n` nodes_. If there are multiple answers, return the answer that occurs last in the input.

**中文翻译 / Chinese:**
> 在该问题中，树是一个**无向图**，它是连通的且没有环。
> 
> 你被给定一个图，它最初是一个有 `n` 个节点的树（节点标签从 `1` 到 `n`），并添加了一条额外的边。添加的边有两个**不同的**顶点（从 `1` 到 `n` 中选择），且不是已存在的边。
> 
> 返回_一条可以移除的边，使得结果图成为一个有 `n` 个节点的树_。如果有多个答案，返回输入中最后出现的答案。

**分类理由 / Classification Reasoning:**
该问题有三种主要解法：并查集（Union-Find）、深度优先搜索（DFS）、拓扑排序。所有方法都需要构建图的邻接表表示，并检测环，最终都收敛到返回形成环的最后一条边。共享中间节点（环检测）和汇聚终点使其成为复合图。

---

#### 示例 1.3: 蚂蚁掉落问题 / Ants on Plank Problem

**英文原文 / English:**
> We have a wooden plank of the length `n` **units**. Some ants are walking on the plank, each ant moves with a speed of **1 unit per second**. Some of the ants move to the **left**, the other move to the **right**.
> 
> When two ants moving in two **different** directions meet at some point, they change their directions and continue moving again. Assume changing directions does not take any additional time.
> 
> When an ant reaches **one end** of the plank at a time `t`, it falls out of the plank immediately.
> 
> Given an integer `n` and two integer arrays `left` and `right`, the positions of the ants moving to the left and the right, return _the moment when the last ant(s) fall out of the plank_.

**中文翻译 / Chinese:**
> 我们有一块长度为 `n` **单位**的木板。一些蚂蚁在木板上行走，每只蚂蚁的移动速度为**每秒 1 单位**。一些蚂蚁向**左**移动，另一些向**右**移动。
> 
> 当两只向**不同**方向移动的蚂蚁在某点相遇时，它们会改变方向并继续移动。假设改变方向不花费额外时间。
> 
> 当一只蚂蚁在时间 `t` 到达木板的**一端**时，它会立即从木板上掉落。
> 
> 给定一个整数 `n` 和两个整数数组 `left` 和 `right`（分别表示向左和向右移动的蚂蚁的位置），返回_最后一只（或多只）蚂蚁从木板上掉落的时刻_。

**分类理由 / Classification Reasoning:**
该问题可通过直接计算、模拟、或数学洞察来解决。所有方法都共享"计算每只蚂蚁掉落时间"的中间步骤，并汇聚到"找出最大时间"这一最终结果。尽管路径不同，但共享中间逻辑使其成为复合图。

---

### 类别 2: [Composite Graphs] - 数学/科学类问题
### Category 2: [Composite Graphs] - Mathematics/Science Problems

---

#### 示例 2.1: 微积分问题 / Calculus Problem

**英文原文 / English:**
> Imagine a drone flying in a perfect circle with a radius of 50 meters above a large, open field. The drone's control system tracks its position using a coordinate system where the center of the circle is the origin. At a certain moment, the drone is moving horizontally (along the x-axis) towards the left at a speed of 1.25 meters per second, and its current position is marked at coordinates (40, 30) meters. Given this scenario, calculate the rate at which the drone's vertical position (along the y-axis) is changing at that moment.

**中文翻译 / Chinese:**
> 想象一架无人机在一个大型开阔场地上方以半径 50 米的完美圆形飞行。无人机的控制系统使用坐标系追踪其位置，圆心为原点。在某一时刻，无人机正沿水平方向（x 轴）向左移动，速度为每秒 1.25 米，其当前位置标记在坐标 (40, 30) 米处。给定此场景，计算该时刻无人机垂直位置（沿 y 轴）的变化率。

**分类理由 / Classification Reasoning:**
该问题可通过三种方法解决：参数方程微积分、几何三角分析、向量运动学分析。所有路径都共享"确定位置向量与 x 轴的夹角θ"这一中间步骤，并汇聚到"计算 y 坐标变化率"这一最终结果。共享中间节点使其成为复合图。

---

#### 示例 2.2: 组合数学问题 / Combinatorics Problem

**英文原文 / English:**
> Imagine you have a fruit stand and you're creating a new fruit mix from bananas only. You decide to label each mix with a unique 6-character code, using the letters from the word 'BANANA'. Considering the repetition of letters, how many unique 6-character codes can you create for your fruit mixes?

**中文翻译 / Chinese:**
> 想象你有一个水果摊，你正在创建一种新的香蕉混合包装。你决定用'BANANA'这个单词中的字母为每个混合包装标记一个唯一的 6 字符代码。考虑到字母的重复，你可以为水果混合包装创建多少个唯一的 6 字符代码？

**分类理由 / Classification Reasoning:**
该问题可通过组合分析（多重集排列公式）、递归计数、或动态规划来解决。所有方法都共享"识别字母频率（B:1, A:3, N:2）"这一中间步骤，并汇聚到"计算唯一代码总数"。共享起点和终点使其成为复合图。

---

#### 示例 2.3: 物理问题 / Physics Problem

**英文原文 / English:**
> In a science experiment, two metal spheres are placed close to each other on a special scale designed to measure very tiny forces. One sphere is much larger and has a mass of 0.500 kilograms, while the smaller sphere has a mass of 0.0100 kilograms. The distance from the center of the small sphere to the center of the large sphere is 0.0500 meters. The experiment aims to measure the tiny force of attraction between the two spheres due to gravity, which is found to be a certain number times $10^{-10}$ Newtons. What is this number?

**中文翻译 / Chinese:**
> 在一个科学实验中，两个金属球体被放置在彼此靠近的位置，使用一个专门设计用于测量微小力的特殊秤。一个球体较大，质量为 0.500 千克，而较小的球体质量为 0.0100 千克。从小球体中心到大球体中心的距离为 0.0500 米。该实验旨在测量两个球体之间由于重力产生的微小吸引力，该力被发现是某个数字乘以 $10^{-10}$ 牛顿。这个数字是多少？

**分类理由 / Classification Reasoning:**
该问题可通过直接计算（牛顿万有引力公式）、逐步验证计算、或概念性估算来解决。所有路径都共享"将给定值代入公式 F = G(m₁m₂)/r²"这一中间步骤，并汇聚到"计算以 10⁻¹⁰牛顿为单位的力"。共享中间节点使其成为复合图。

---

### 类别 3: [Composite Graphs] - 生物学/科学解释类问题
### Category 3: [Composite Graphs] - Biology/Science Explanation Problems

---

#### 示例 3.1: 霉菌食物问题 / Mouldy Food Problem

**英文原文 / English:**
> Why does mouldy food make you sick?
> 
> Bread gets mouldy pretty quickly. My parents (both of whom are nurses) throw out a loaf of bread after a spot of mould is seen (because "if you can see one spot, it means the whole thing is covered in mould spores") because they say you'll get sick if you eat it. The USDA also has a handy chart on its mould page telling you when you should discard food with mould on it.
> 
> Is it the mould itself that makes us sick or is it something that the mould is releasing?
> What are the mechanisms that cause us to feel sick after eating mouldy food?
> The USDA says that there can also be bacteria along with the mould on the food - is this what is really making us feel ill?

**中文翻译 / Chinese:**
> 为什么发霉的食物会让你生病？
> 
> 面包很快就会发霉。我的父母（他们都是护士）在看到一点霉菌后就会扔掉一整条面包（因为"如果你能看到一个斑点，意味着整条面包都覆盖了霉菌孢子"），因为他们说吃了它会生病。美国农业部（USDA）在其霉菌页面上也有一个便捷的图表，告诉你何时应该丢弃发霉的食物。
> 
> 是霉菌本身让我们生病，还是霉菌释放的某种物质？
> 吃发霉食物后让我们感到不适的机制是什么？
> 美国农业部说食物上的霉菌旁边也可能有细菌——这才是真正让我们生病的原因吗？

**分类理由 / Classification Reasoning:**
该问题可通过微生物学分析（霉菌毒素）、细菌污染分析、或综合机制分析来解决。所有路径都共享"识别面包上的霉菌和细菌类型"这一中间步骤，并汇聚到"解释发霉食物致病的机制"。多路径共享中间逻辑使其成为复合图。

---

#### 示例 3.2: 细胞膜稳定性问题 / Cell Membrane Stability Problem

**英文原文 / English:**
> Why doesn't the cell membrane just...break apart?
> 
> Forgive me if this is a silly question. I can't understand the basics. Why doesn't the cell membrane just break apart? What's keeping the layers in the phospholipid bilayer together? I know that the membrane is embedded with proteins and lipids, but I still can't wrap my head around the "why". Are the hydrophobic interactions in the middle "stronger" than the hydrophilic interactions on the outside? What's keeping the individual phosphate heads together instead of, say, one of them just drifting away due to a nearby water molecule?

**中文翻译 / Chinese:**
> 为什么细胞膜不会……散开？
> 
> 如果这是个愚蠢的问题，请原谅我。我无法理解基本原理。为什么细胞膜不会散开？是什么让磷脂双分子层中的各层保持在一起？我知道膜中嵌入了蛋白质和脂质，但我仍然无法理解"为什么"。中间的疏水相互作用比外面的亲水相互作用"更强"吗？是什么让各个磷酸头部保持在一起，而不是说，其中一个因为附近的水分子而漂走？

**分类理由 / Classification Reasoning:**
该问题可通过分子相互作用分析、热力学稳定性分析、或生物功能与进化分析来解释。所有路径都共享"理解磷脂双分子层结构"这一中间步骤，并汇聚到"解释细胞膜为何稳定"。多视角共享中间逻辑使其成为复合图。

---

### 类别 4: [Composite Graphs] - 地球科学/技术问题
### Category 4: [Composite Graphs] - Earth Science/Technical Problems

---

#### 示例 4.1: 黄石公园地热问题 / Yellowstone Geothermal Problem

**英文原文 / English:**
> The Yellowstone National Park in Wyoming is unique for its large number of "thermal occurrences", of which there are some 30 geysers. This, in turn, appears to be the result of the presence of large quantities of molten rock, and the thinness of the earth's crust there, compared to the other spots on the earth.
> 
> To the best of my knowledge, there is no other (known) place on earth where so much thermal power is contained in a relatively small area. Is this in fact the case? If so, what made Yellowstone, Wyoming so unique in this regard?

**中文翻译 / Chinese:**
> 怀俄明州的黄石国家公园因其大量的"热活动"而独特，其中约有 30 个间歇泉。这反过来似乎是由于存在大量熔融岩石，以及与地球上其他地方相比，那里的地壳较薄。
> 
> 据我所知，地球上没有其他（已知的）地方在相对较小的区域内包含如此多的热能。事实确实如此吗？如果是，是什么让怀俄明州的黄石公园在这方面如此独特？

**分类理由 / Classification Reasoning:**
该问题可通过地球物理地质分析、历史比较分析、或构造火山活动分析来解答。所有路径都共享"调查黄石的地质条件（热点、薄地壳）"这一中间步骤，并汇聚到"解释黄石地热活动的独特性"。多路径共享中间节点使其成为复合图。

---

#### 示例 4.2: NetCDF 数据读取问题 / NetCDF Data Reading Problem

**英文原文 / English:**
> I have downloaded the sea surface temperature data from the Ocean Color website, the file is in NetCDF format and contains no of geophysical_data variables like sst, qual_sst, flag_sst, bias_sst, etc. I used the following MATLAB code for file read and it is giving me an error:
> 
> `temp=ncread('A2014213085500.L2_LAC_SST.x.nc','sst')`
> 
> Error: Could not find variable or group 'sst' in file.
> 
> Can someone tell me what is the cause of the error?

**中文翻译 / Chinese:**
> 我从 Ocean Color 网站下载了海面温度数据，文件是 NetCDF 格式，包含多个地球物理_data 变量，如 sst、qual_sst、flag_sst、bias_sst 等。我使用以下 MATLAB 代码读取文件，但它给了我一个错误：
> 
> `temp=ncread('A2014213085500.L2_LAC_SST.x.nc','sst')`
> 
> 错误：在文件中找不到变量或组'sst'。
> 
> 有人能告诉我错误的原因是什么吗？

**分类理由 / Classification Reasoning:**
该问题可通过变量名不匹配检查、文件完整性检查、MATLAB 版本兼容性检查、或文件结构检查来解决。所有路径都共享"检查 NetCDF 文件结构"这一中间步骤，并汇聚到"成功读取变量"。多解法共享中间逻辑使其成为复合图。

---

### 类别 5: [Composite Graphs] - 软件开发/StackOverflow 问题
### Category 5: [Composite Graphs] - Software Development/StackOverflow Problems

---

#### 示例 5.1: Django JSON 字段问题 / Django JSON Field Problem

**英文原文 / English:**
> Django-Forms with json fields
> 
> I am looking to accept json data in a form field and than validate it using some database operations. The data will mostly consist of an array of integers. So can you please help me as to how can i do so.
> 
> I have tried to google this but didn't get any decent answer. Please help.

**中文翻译 / Chinese:**
> 带有 JSON 字段的 Django 表单
> 
> 我希望在表单字段中接受 JSON 数据，然后使用一些数据库操作对其进行验证。数据将主要由整数数组组成。你能帮我了解一下如何做到这一点吗？
> 
> 我尝试过谷歌搜索，但没有得到任何像样的答案。请帮忙。

**分类理由 / Classification Reasoning:**
该问题可通过自定义表单字段验证、使用第三方包、或 ModelForm 与 JSONField 来解决。所有路径都共享"实现 JSON 数据验证逻辑"这一中间步骤，并汇聚到"创建可接受和验证 JSON 数据的 Django 表单"。多方法共享中间节点使其成为复合图。

---

#### 示例 5.2: GitHub Actions 工作流问题 / GitHub Actions Workflow Problem

**英文原文 / English:**
> GitHub Actions: how can I run a workflow created on a non-'master' branch from the 'workflow_dispatch' event?
> 
> For actions working on a third party repository, I would like to be able to create an action on a branch and execute it on the workflow_dispatch event. I have not succeeded in doing this, but I have discovered the following:
> 
> The Action tab will change the branch where it finds workflows and action code based on the branch relating to the last executed workflow.
> 
> Does the above sound a) about right and b) whichever way you look at it, not optimal behaviour? Or, is there a better approach to building and testing actions?

**中文翻译 / Chinese:**
> GitHub Actions：如何从'workflow_dispatch'事件运行在非'master'分支上创建的工作流？
> 
> 对于在第三方仓库上操作的 actions，我希望能够在分支上创建一个 action 并在 workflow_dispatch 事件上执行它。我还没有成功做到这一点，但我发现了以下情况：
> 
> Action 选项卡会根据与最后执行的工作流相关的分支来改变它找到工作流和 action 代码的分支。
> 
> 上述情况听起来 a) 对吗，b) 无论从哪个角度看，都不是最优行为？或者，是否有更好的方法来构建和测试 actions？

**分类理由 / Classification Reasoning:**
该问题可通过查阅 GitHub 文档、查询社区论坛、实验测试调试、或联系 GitHub 支持来解决。所有路径都共享"收集关于 workflow_dispatch 行为的信息"这一中间步骤，并汇聚到"找到从非 master 分支运行工作流的最佳方法"。多路径汇聚到同一目标使其成为复合图。

---

## 📈 分类统计 / Classification Statistics

| 拓扑类别 / Topology Category | 示例数量 / Count | 占比 / Percentage |
|------------------------------|------------------|-------------------|
| [Composite Graphs] | 13 | 100% |
| [Single Graph] | 0 | 0% |
| [Concurrent Graphs] | 0 | 0% |
| [Divergent Graphs] | 0 | 0% |
| [Unclassifiable] | 0 | 0% |

---

## 🔍 关键观察 / Key Observations

1. **复合图主导 / Composite Graph Dominance**: 所有成功解析的 Query 都被分类为 [Composite Graphs]，这表明：
   - 测试数据集中的问题普遍具有多种解法
   - 这些解法共享中间步骤或约束
   - 当前 Prompt 对复合图的识别较为准确

2. **缺少其他类别 / Lack of Other Categories**: 未观察到 [Single Graph]、[Concurrent Graphs]、[Divergent Graphs] 等类别，可能原因：
   - 测试数据集本身以多解法问题为主
   - Prompt 可能对其他类别的识别标准过于严格
   - 需要进一步分析失败样本以确认是否存在误分类

3. **领域分布 / Domain Distribution**: 示例覆盖了多个领域：
   - 算法/编程（LeetCode）
   - 数学（定理证明、微积分、组合数学）
   - 科学（物理、生物、地球科学）
   - 软件开发（StackOverflow）

---

## 📌 结论 / Conclusion

当前 Prompt 优化迭代中，[Composite Graphs] 是最常见且最准确识别的拓扑类别。这反映了真实世界问题的复杂性——大多数问题都有多种解决路径，这些路径往往共享某些中间步骤或约束。

**下一步建议 / Next Steps:**
1. 分析失败样本（API 超时/解析失败）以确认是否存在其他拓扑类别的误分类
2. 考虑引入更多样化的测试数据，包含明确的 Single Graph 或 Concurrent Graphs 示例
3. 继续优化 Prompt 以更好地区分复合图与其他类别的边界情况

---

*报告生成完成 / Report Generation Complete*
