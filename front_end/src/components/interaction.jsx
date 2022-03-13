import React, { useState, useEffect } from 'react'
import { Select, Typography, Card, Col, Row } from 'antd'
const { Title } = Typography
const { Option } = Select
const Interaction = () => {
    const [author1, setAuthor1] = useState('')
    const [author2, setAuthor2] = useState('')
    const [res, setRes] = useState({})
    const [data, setData] = useState({})
    let mockData = {
        "data": [{'id': 1, 'author': 'Marsha'},
            {'id': 2, 'author': 'Zhang Qiuzi'}]
    }
    useEffect(()=>{
        setData(mockData)
    },[])
    const children1 = data?.data ? data['data'].map(item => <Option key={item['id']}>{item['author']}</Option>):null
    const children2 = data?.data ? data['data'].map(item => <Option key={item['id']}>{item['author']}</Option>):null
    let mockRes = {
        "data": {
            "author":[
                {
                    "name":"Paul C. DiLorenzo",
                    "affiliations": "University of California Riverside",
                    "pc": 6,
                    "cn": 29,
                    "interest": "human torso;simulated respiration;deformable part;torso simulation;human body;human trunk;breathing style;deformable body;mixed system;signature movement"
                },
                {
                    "name": "Tom Kinsella",
                    "affiliations":"",
                    "pc": 1,
                    "cn": 1,
                    "interest": "Neural Network Efficiency;Weight Investigation"
                }
            ],
            "ni": 88,
            "ini": 90
        }
    }
    useEffect(()=>{
        setRes(mockRes)
    },[author1,author2])
    const handleChange1 = (value) => {
        console.log(value)
        setAuthor1(value)
    }
    const handleChange2 = (value) => {
        console.log(value)
        setAuthor2(value)
    }
    return (<div className="page3">
        <Title>选择两个作者进行分析</Title>
        <div className="input">
            <select className="select"
                allowClear
                placeholder="Please select"
                defaultValue="Li Ming"
                onChange={handleChange1}>
                {children1}
            </select>
            <select className="select"
                allowClear
                placeholder="Please select"
                defaultValue="Jiang Shan"
                onChange={handleChange2}>
                {children2}
            </select>
        </div>
        {res.data && <div className="content">
            <Row justify="space-around" className="row">
                <Col span={8}>
                    <Card title={res.data.author[0]['name']}>
                        <div className="affiliation">所属机构：{res.data.author[0]['affiliations']}</div>
                        {`发表数量：${res.data.author[0]['pc']}
                        引用数量：${res.data.author[0]['cn']}
                        `}
                        <div className="topic">{`研究主题：${res.data.author[0]['interest']}`}</div>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title={res.data.author[1]['name']}>
                        <div className="affiliation">所属机构：{res.data.author[1]['affiliations']}</div>
                        {`发表数量：${res.data.author[1]['pc']}
                        引用数量：${res.data.author[1]['cn']}
                        `}
                        <div className="topic">{`研究主题：${res.data.author[1]['interest']}`}</div>
                    </Card>
                </Col>
            </Row>
            <Row justify="space-around" className="row">
                <Col span={8}>
                    <Card title="结构临近度指标">{res.data['ni']}</Card>
                </Col>
                <Col span={8}>
                    <Card title="主题临近度指标">{res.data['ini']}</Card>
                </Col>
            </Row>
        </div>}
    </div>)
}
export default Interaction