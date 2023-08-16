import React from "react";

import { Card, Statistic } from "antd";

const TotalSales = (sales) => {
  const amount = sales.sales;
  const str = `$ ` + amount.toString();

  return (
    <Card bordered={false}>
      <Statistic
        title="Total Sales Amount"
        value={str}
        precision={2}
        valueStyle={{
          color: "#555e50",
        }}
      />
    </Card>
  );
};

export default TotalSales;
