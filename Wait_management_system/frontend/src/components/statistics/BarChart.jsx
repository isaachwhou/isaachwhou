import React, { useState } from "react";
import { Card, Slider, Empty } from "antd";
import { Column } from "@ant-design/plots";

const BarChart = ({ data, x, onTopValueChange }) => {
  const [inputValue, setInputValue] = useState(5);
  const [topx, setTopx] = useState(x);
  const title = `Top ${topx} Dishes by Sales Volume`;

  const onChange = (newValue) => {
    setInputValue(newValue);
    setTopx(newValue);
    onTopValueChange(newValue);
  };

  const config = {
    data,
    xField: "itemName",
    yField: "itemSaleCount",
    label: {
      position: "middle",
      style: {
        fill: "#FFFFFF",
        opacity: 0.6,
      },
    },
    xAxis: {
      label: {
        autoHide: true,
        autoRotate: true,
      },
    },
    meta: {
      itemName: {
        alias: "Dish Name",
      },
      itemSaleCount: {
        alias: "Sales Volume",
      },
    },
  };

  return (
    <Card
      title={title}
      bordered={true}
      hoverable={true}
      extra={
        <Slider
          style={{ width: 150 }}
          min={3}
          max={15}
          onChange={onChange}
          tooltip={true}
          value={typeof inputValue === "number" ? inputValue : 5}
        />
      }
    >
      {data.length > 0 ? (
        <Column {...config} />
      ) : (
        <Empty description="No order data available in this time period" />
      )}
    </Card>
  );
};

export default BarChart;
