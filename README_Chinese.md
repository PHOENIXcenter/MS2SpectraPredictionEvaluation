## 评估流程及对应文件：

1. 将pFind3和MaxQuant结果取交集，作为评估的数据。（由GetSamePeptideInfo.py完成）
2. 结合mgf文件以及pFind3和MaxQuant鉴定交集，将鉴定的肽段序列和mgf中质谱谱图对应在一起，便于获取对应的mz-intensity键值对，作为评估的ground truth。（由buildTargetMGF.py完成）
3. 将第一步中的交集结果分别处理转换为各工具对应输入格式的文件。（由toXXXInput.py完成，其中pDeep2和Guan's work不需要转换）
4. 各工具分别对数据进行强度预测：pDeep2、Guan‘s work在本地GPU环境运行；Prosit、MS2PIP在其对应的Web server上运行。
5. 各工具预测后，将输出格式统一整理为msp文件。（由XXX2msp.py文件完成，其中Prosit不需要转换，Guan’s work结果输出部分由我们自己完成直接输出为msp文件）
6. 对各工具的预测结果分别和ground truth数据对比，并将肽段序列、肽段长度、电荷值、PCC、强度值等信息写到文件。（考虑0值和不考虑0值两种情况，分别由perSim.py和perSimOnlymatch.py完成）
7. 对各工具和ground truth数据对比后的结果分析，统计b离子、y离子、by离子的Median PCC。（考虑0值和不考虑0值两种情况，分别由ComputeMEDpersim.py和ComputeMEDpersimOnlymatch.py完成）
8. 针对于PCC>0.8以及PCC>0.9部分所占比例进行统计。（考虑0值和不考虑0值两种情况，分别由filterMEDpersim.py和filterMEDpersimOnlymatch.py完成）
9. 针对预测的峰值强度top6、8、11、15的PCC进行统计。（由ComputeTopKpeaks.py完成）

## 评估流程外代码：
1. SpellMS2PIPresult.py ：由于MS2PIP的Web server一次最多预测10万条肽段，通过该文件将一个数据集的所有肽段结果整合到一个文件。
2. DealDataforPlot.py ：针对绘图所需，通过该文件获取所需的b离子、y离子、by离子的各项信息。

##  联系方式

  For any question, please contact [Dr. Cheng Chang](https://orcid.org/0000-0002-0361-2438)![](https://orcid.org/sites/default/files/images/orcid_16x16.png)
(Email: [changchengbio@gmail.com](mailto:changchengbio@gmail.com)).

