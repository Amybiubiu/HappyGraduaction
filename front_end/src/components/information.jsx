import React from 'react'
import { Typography, Divider } from 'antd';
const { Title, Paragraph, Text, Link } = Typography;

const Information = () => {
    return (<div className="page1">
        <div>
        <Title>基于学术合作网络的聚类分析</Title>
        <Title level={2}>数据集来源</Title>
        <Link href="https://lfs.aminer.cn/lab-datasets/soinf/"> Aminer 中 data Mining / Association Rules 主题的合作网络</Link>
        <Title level={2}>数据量大小</Title>
        <Paragraph>
            <ul>
                <li>节点数：689</li>
                <li>边数：1687</li>
            </ul>
        </Paragraph>
        </div>
    </div>)
}
export default Information