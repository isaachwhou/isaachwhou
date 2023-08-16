import React from "react";
import { useNavigate } from "react-router-dom";
import { Button, Select, Form, Col, Row } from "antd";

import cover from "../assets/cover.webp";
import "../App.css";
import "../cooking.css";
import FryingPan from "../components/customer/FryingPan";

const SelectTable = () => {
  // initial the states.
  const navigate = useNavigate();
  const [tableNumList, setTableNumList] = React.useState();
  const [selectedTable, setSelectedTable] = React.useState();
  const [form] = Form.useForm();

  const onChange = (value) => {
    setSelectedTable(value);
  };

  // send tableId data to backend. start a compeletely new order.
  const sendFormData = async () => {
    try {
      const response = await fetch(
        `http://localhost:8080/waitsys/customer/start?tableId=${parseInt(
          selectedTable
        )}`,
        {
          method: "POST",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      const data = await response.json();
      console.log(data);
      localStorage.setItem("orderId", JSON.stringify(data.orderId));
      localStorage.setItem("tableId", JSON.stringify(data.tableId));
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // if tableId transmit successfully, nav to order page.
  const onFinish = async (values) => {
    setSelectedTable(values.tableNum);
    await sendFormData();
    console.log(selectedTable);
    navigate("/Order");
  };

  // get the table number using on filling dropdown menu.
  const fetchData = async () => {
    try {
      const response = await fetch(
        `http://localhost:8080/waitsys/customer/table/showAll`,
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );

      const data = await response.json();
      console.log(data);
      createSelectMenu(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // backend data structure formatting
  const createSelectMenu = (data) => {
    var map = [];
    for (var i = 0; i < data.length; i++) {
      const temp = {
        value: data[i],
        label: data[i],
      };
      map.push(temp);
    }

    console.log(map);
    setTableNumList(map);
  };

  return (
    <Row gutter={0} style={{ margin: -8, padding: 0, height: "100vh" }}>
      {/* Left Column: Restaurant Image */}
      <Col span={12} style={{ margin: 0, padding: 0 }}>
        <img
          src={cover} // Replace with the actual path to your restaurant image
          alt="Restaurant"
          style={{ width: "100%", height: "100vh", objectFit: "cover" }}
        />
      </Col>
      {/* Right Column: Table Selection Form */}
      <Col
        span={12}
        style={{
          margin: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <div className="title">welcome</div>
        <Form
          form={form}
          name="SelectTableForm"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 12,
          }}
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
        >
          <Form.Item
            name="tableNum"
            label="Select"
            rules={[
              {
                required: true,
                message: "Please select the table number!",
              },
            ]}
          >
            <Select
              placeholder="Table Number"
              style={{
                width: "25vh",
              }}
              options={tableNumList}
              onChange={onChange}
              onClick={fetchData}
            />
          </Form.Item>
          <Form.Item
            wrapperCol={{
              offset: 12,
              span: 7,
            }}
          >
            <Button
              type="primary"
              htmlType="submit"
              shape="round"
              style={{ backgroundColor: "grey" }}
            >
              Submit
            </Button>
          </Form.Item>
        </Form>
        <FryingPan />
      </Col>
    </Row>
  );
};

export default SelectTable;
