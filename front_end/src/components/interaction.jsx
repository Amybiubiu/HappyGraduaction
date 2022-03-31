import React, {useState, useEffect} from 'react'
import { scaleLinear } from 'd3-scale'
import {Select, Typography, Card, Col, Row} from 'antd'
import Fetch from '../fetch'

const {Title} = Typography
const {Option} = Select
const scale1 = scaleLinear()
    .domain([0, 526])
    .range([0, 100]);
const scale2 = scaleLinear()
    .domain([0, 1])
    .range([0, 100]);
const Interaction = ({option, author1, author2, onAuthorChange}) => {
    const [res, setRes] = useState({})
    const children1 = option.length ? option.map(item => <Option key={item['id']}>{item['name']}</Option>) : null
    const children2 = option.length ? option.map(item => <Option key={item['id']}>{item['name']}</Option>) : null
    let mockRes = {
        "data": {
            "author": [
                {
                    "name": "Paul C. DiLorenzo",
                    "affiliations": "University of California Riverside",
                    "pc": 6,
                    "cn": 29,
                    "interest": "human torso;simulated respiration;deformable part;torso simulation;human body;human trunk;breathing style;deformable body;mixed system;signature movement"
                },
                {
                    "name": "Tom Kinsella",
                    "affiliations": "",
                    "pc": 1,
                    "cn": 1,
                    "interest": "Neural Network Efficiency;Weight Investigation"
                }
            ],
            "dis": 88,
            "simi": 90
        }
    }
    useEffect(() => {
        if(author1 && author2) {
            const id = Number(author1) < Number(author2) ? `${author1},${author2}` : `${author2},${author1}`
            Fetch(`/analysis?id=${id}`).then(
                res => {
                    // console.log(res)
                    setRes(res)
                }
            )
        }
    }, [author1, author2])
    const handleChange1 = (value) => {
        onAuthorChange({target: 1, value: value})
    }
    const handleChange2 = (value) => {
        onAuthorChange({target: 2, value: value})
    }

    return (<div className="page3">
        <Title>选择两个作者进行分析</Title>
        <div className="input">
            <Select className="select"
                    showSearch
                    optionFilterProp="children"
                    filterOption={(input, option) =>
                        option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                    }
                    filterSort={(optionA, optionB) =>
                        optionA.children.toLowerCase().localeCompare(optionB.children.toLowerCase())
                    }
                    style={{marginRight: '2em'}}
                    allowClear
                    placeholder="Please select"
                // defaultValue="Paul C. DiLorenzo"
                    onChange={handleChange1}>
                {children1}
            </Select>
            <Select className="select"
                    showSearch
                    optionFilterProp="children"
                    filterOption={(input, option) =>
                        option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                    }
                    filterSort={(optionA, optionB) =>
                        optionA.children.toLowerCase().localeCompare(optionB.children.toLowerCase())
                    }
                    allowClear
                    placeholder="Please select"
                // defaultValue="Tom Kinsella"
                    onChange={handleChange2}>
                {children2}
            </Select>
        </div>
        {Object.values(res).length ? <div className="content">
            <Row justify="space-around" className="row">
                <Col span={8}>
                    <Card title={res.author[0]['name']}>
                        <div className="affiliation">所属机构：{res.author[0]['affiliations']}</div>
                        {`发表数量：${res.author[0]['pc']}
                        引用数量：${res.author[0]['cn']}
                        `}
                        <div className="topic">{`研究主题：${res.author[0]['interest'] ? res.author[0]['interest'] : '无数据'}`}</div>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title={res.author[1]['name']}>
                        <div className="affiliation">所属机构：{res.author[1]['affiliations']}</div>
                        {`发表数量：${res.author[1]['pc']}
                        引用数量：${res.author[1]['cn']}
                        `}
                        <div className="topic">{`研究主题：${res.author[1]['interest'] ? res.author[1]['interest'] : '无数据' }`}</div>
                    </Card>
                </Col>
            </Row>
            <Row justify="space-around" className="row">
                <Col span={8}>
                    <Card title="结构临近度指标">{Math.floor(100 - scale1(res['dis']))}</Card>
                </Col>
                <Col span={8}>
                    <Card title="主题临近度指标">{res['simi'] != -1 ? Math.floor(scale2(res['simi'])) : '无数据'}</Card>
                </Col>
            </Row>
        </div> : null}
    </div>)
}
export default Interaction