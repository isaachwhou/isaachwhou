import React, { useState, useEffect } from "react";
import { Row, Col } from "antd";
import TableCard from "../components/kitchen/TableCard";
import { Spin } from "antd";

const KitchenPage = () => {
  // State to store kitchen orders
  const [kitchenOrders, setKitchenOrders] = useState([]);

  useEffect(() => {
    // Fetch kitchen orders when the component mounts
    fetchKitchenOrders();
    // Set up an interval to fetch kitchen orders every 2 seconds
    const interval = setInterval(() => {
      fetchKitchenOrders();
      console.log("fetching kitchen orders");
    }, 2000);
    // Clean up the interval when the component unmounts to prevent memory leaks
    return () => {
      clearInterval(interval);
    };
  }, []);

  // Function to generate TableCard components for each kitchen order
  const generateTableCards = () => {
    return kitchenOrders.map((order) => (
      <Col span={8} key={order.orderId}>
        <TableCard
          tableId={order.tableId}
          orderId={order.orderId}
          orderItems={order.orderItemList}
          startTime={order.startTime}
        />
      </Col>
    ));
  };

  // Function to fetch kitchen orders from the server
  async function fetchKitchenOrders() {
    const response = await fetch(
      `http://localhost:8080/waitsys/kitchen/list_all_orders_kitchen`,
      {
        method: "GET",
        headers: {
          "Content-type": "application/json",
        },
      }
    );
    const data = await response.json();
    setKitchenOrders(data);
  }

  return (
    <>
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "45px",
        }}
      >
        <h2>Kitchen Page</h2>
      </div>
      {/* Display kitchen orders if available */}
      {kitchenOrders.length > 0 ? (
        <div>
          <Row gutter={{ xs: 12, sm: 16, md: 24, lg: 32 }}>
            {generateTableCards()}
          </Row>
        </div>
      ) : (
        // Display a loading spinner while waiting for orders
        <div>
          <Spin />
          <p>Waiting for orders...</p>
        </div>
      )}
    </>
  );
};

export default KitchenPage;
