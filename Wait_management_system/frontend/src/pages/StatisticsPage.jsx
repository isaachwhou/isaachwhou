import React from "react";
import { Row, Col, Layout, Space, Button } from "antd";
import PieChart from "../components/statistics/PieChart";
import BarChart from "../components/statistics/BarChart";
import TotalSales from "../components/statistics/TotalSales";
import TotalPaidOrders from "../components/statistics/TotalPaidOrders";
import "../App.css";
import { useNavigate } from "react-router-dom";
const { Header, Content } = Layout;

const StatisticsPage = () => {
  const [totalSales, setTotalSales] = React.useState(0);
  const [orderNum, setOrderNum] = React.useState(0);
  const [categorySalePercent, setCategorySalePercent] = React.useState([]);
  const [topItemSale, setTopItemSale] = React.useState([]);
  const [state, setState] = React.useState(0);
  const [orderAvgCost, setOrderAvgCost] = React.useState(0);
  const [x, setX] = React.useState(5);
  const navigate = useNavigate();

  React.useEffect(() => {
    fetchAnalysisData(state, x);
  }, [state, x]);

  const fetchAnalysisData = async (state, x) => {
    const response = await fetch(
      `http://localhost:8080/waitsys/manager/analysis?state=${state}&x=${x}`,
      {
        method: "GET",
        headers: {
          "Content-type": "application/json",
        },
      }
    );
    const data = await response.json();
    console.log(data);
    setTotalSales(data.totalSale);
    setOrderNum(data.orderNum);
    setCategorySalePercent(data.categorySalePercent);
    setTopItemSale(data.topItemSale);
    setOrderAvgCost(data.orderAvgCost);
  };

  const changeTimePeriod = (buttonType) => {
    if (buttonType === "day") {
      setState(0);
    } else if (buttonType === "week") {
      setState(1);
    } else if (buttonType === "month") {
      setState(2);
    } else if (buttonType === "year") {
      setState(3);
    }
  };

  const handleChildValueChange = (newValue) => {
    setX(newValue);
  };

  const goBackToHomePage = () => {
    const targetUrl = "/manager";
    console.log("Go to home page");
    navigate(targetUrl);
  };

  return (
    <>
      <Layout>
        <Space direction="vertical">
          <Header
            style={{
              background: "#fff",
              color: "#333",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              marginLeft: -10,
              marginTop: -10,
              boxShadow: "2px 5px 12px rgba(0, 0, 0, 0.1)",
            }}
          >
            <div className="lato">
              <h1>Manager Statistics Page</h1>
            </div>
          </Header>
          <Content>
            <Row gutter={[16, 16]}>
              <Col span={24}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <Space>
                    <Button
                      type="primary"
                      onClick={() => changeTimePeriod("day")}
                    >
                      Today
                    </Button>
                    <Button
                      type="primary"
                      onClick={() => changeTimePeriod("week")}
                    >
                      7 days
                    </Button>
                    <Button
                      type="primary"
                      onClick={() => changeTimePeriod("month")}
                    >
                      This Month
                    </Button>
                    <Button
                      type="primary"
                      onClick={() => changeTimePeriod("year")}
                    >
                      This Year
                    </Button>
                  </Space>
                  <Button type="primary" onClick={() => goBackToHomePage()}>
                    Back to home page
                  </Button>
                </div>
              </Col>
              <Col span={12}>
                <TotalSales sales={totalSales} />
              </Col>
              <Col span={12}>
                <TotalPaidOrders orderNum={orderNum} avgcost={orderAvgCost} />
              </Col>
              <Col span={12}></Col>
              <Col className="gutter-row" span={12}></Col>
              <Col className="gutter-row" span={12}>
                <BarChart
                  data={topItemSale}
                  x={x}
                  onTopValueChange={handleChildValueChange}
                />
              </Col>
              <Col span={12}>
                <PieChart data={categorySalePercent} />
              </Col>
            </Row>
          </Content>
        </Space>
      </Layout>
    </>
  );
};

export default StatisticsPage;
