import React from "react";
import { Card, Empty } from "antd";
import { Pie } from "@ant-design/plots";

const PieChart = ({ data }) => {
  const config = {
    appendPadding: 5,
    data,
    angleField: "categorySalePercent",
    colorField: "categoryName",
    radius: 1,
    label: {
      type: "inner",
      offset: "-30%",
      content: ({ percent }) => `${(percent * 100).toFixed(0)}%`,
    },
    interactions: [
      {
        type: "pie-legend-active",
      },
      {
        type: "element-active",
      },
    ],
  };

  return (
    <Card
      title="Proportion of Sales by Category"
      style={{ width: "100%" }}
      itle="Card title"
      bordered={true}
      hoverable={true}
    >
      {data.length > 0 ? (
        <Pie {...config} />
      ) : (
        <Empty description="No order data available in this time period" />
      )}
    </Card>
  );
};

export default PieChart;
