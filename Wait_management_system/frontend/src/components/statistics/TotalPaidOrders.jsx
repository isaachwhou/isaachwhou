import React from "react";

import { Card, Statistic } from "antd";

const gridStyle = {
  width: "50%",
  textAlign: "center",
};

const TotalPaidOrders = (orderNum, avgcost) => {
  const temp1 = orderNum.orderNum;
  const temp2 = orderNum.avgcost;
  const str = `$ ` + temp2.toString();
  return (
    <Card bordered={true}>
      <Card.Grid style={gridStyle}>
        <Statistic
          title="Total Number of Orders"
          value={temp1}
          precision={0}
          valueStyle={{
            color: "#555e50",
          }}
        />
      </Card.Grid>
      <Card.Grid style={gridStyle}>
        <Statistic
          title="Average Order Cost"
          value={str}
          precision={0}
          valueStyle={{
            color: "#555e50",
          }}
        />
      </Card.Grid>
    </Card>
  );
};

export default TotalPaidOrders;
