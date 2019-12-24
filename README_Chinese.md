<li>将pFind3和MaxQuant结果取交集，作为评估的数据。（由GetSamePeptideInfo.py完成）</li>
<li>结合mgf文件以及pFind3和MaxQuant鉴定交集，将鉴定的肽段序列和mgf中质谱谱图对应在一起，便于获取对应的mz-intensity键值对，作为评估的ground truth。（由buildTargetMGF.py完成）</li>
<li>将第一步中的交集结果分别处理转换为各工具对应输入格式的文件。（由toXXXInput.py完成，其中pDeep2和Guan's work不需要转换）</li>
<li>各工具分别对数据进行强度预测：pDeep2、Guan‘s work在本地GPU环境运行；Prosit、MS2PIP在其对应的Web server上运行。</li>
<li>各工具预测后，将输出格式统一整理为msp文件。（由XXX2msp.py文件完成，其中Prosit不需要转换，Guan’s work结果输出部分由我们自己完成直接输出为msp文件）</li>
<li>对各工具的预测结果分别和ground truth数据对比，并将肽段序列、肽段长度、电荷值、PCC、强度值等信息写到文件。（考虑0值和不考虑0值两种情况，分别由perSim.py和perSimOnlymatch.py完成）</li>
<li>对各工具和ground truth数据对比后的结果分析，统计b离子、y离子、by离子的Median PCC。（考虑0值和不考虑0值两种情况，分别由ComputeMEDpersim.py和ComputeMEDpersimOnlymatch.py完成）</li>
<li>针对于PCC&gt;0.8以及PCC&gt;0.9部分所占比例进行统计。（考虑0值和不考虑0值两种情况，分别由filterMEDpersim.py和filterMEDpersimOnlymatch.py完成）</li>
<li>针对预测的峰值强度top6、8、11、15的PCC进行统计。（由ComputeTopKpeaks.py完成）</li>
