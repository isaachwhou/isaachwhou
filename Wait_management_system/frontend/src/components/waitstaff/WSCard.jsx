import { Card, Button, Row, Space, message, Modal, Table, Pagination } from "antd";
import {
  BellOutlined,
  DollarCircleOutlined,
  CheckOutlined,
  CoffeeOutlined,
} from "@ant-design/icons";
import { useState } from "react";
import "../../App.css";

const WSCard = ({ table }) => {
  // Destructure the table object
  const { tableId, state, needHelp, orderItemList } = table;

  // State for the popup window
  const [openPopup, setOpenPopup] = useState(false);
  const [popupData, setPopupData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const itemsPerPage = 9;

  // Filter order items to display only those that are cooked but not served
  const filteredOrderItemList = orderItemList.filter(
    (item) => item.isCook === 1 && item.isServe === 0
  );

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredOrderItemList.slice(indexOfFirstItem, indexOfLastItem);

  // Function to handle "Notify Assistance" button click
  const handleNotifyAssistance = () => {
    if (needHelp === 0) {
      message.error("Help not required");
      return;
    }
    markNeedHelp(tableId);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  // Function to mark needHelp as 1 for the table
  const markNeedHelp = (tableId) => {
    // Make a POST request to the server to mark needHelp as 1
    fetch(
      `http://localhost:8080/waitsys/waitstaff/mark_need_help?tableId=${tableId}`,
      {
        method: "POST",
      }
    )
      .then(() => {
        console.log(`Table ${tableId} request completed`);
        message.success("Request completed");
      })
      .catch((error) => {
        console.error(
          `Error marking needHelp as 0 for table ${tableId}:`,
          error
        );
      });
  };

  // Function to handle "Request Bill" button click
  const handleRequestBill = () => {
    if (state === 0 || state === 1) {
      message.error("Table not ready for bill");
      return;
    }
    confirmRequestBill(tableId);
  };

  // Function to confirm request bill for the table
  const confirmRequestBill = (tableId) => {
    // Make a POST request to the server to confirm request bill
    fetch(
      `http://localhost:8080/waitsys/waitstaff/confirm_request_bill?tableId=${tableId}`,
      {
        method: "POST",
      }
    )
      .then(() => {
        console.log(`Confirmed request bill for table ${tableId}`);
        message.success("Bill confirmed");
      })
      .catch((error) => {
        console.error(
          `Error confirming request bill for table ${tableId}:`,
          error
        );
      });
  };

  // Function to handle "Send" button click for a specific order item
  const handleSend = (orderItemId) => {
    ItemServe(orderItemId);
  };

  // Function to mark an order item as served
  const ItemServe = (orderItemId) => {
    // Make a POST request to the server to mark the order item as served
    fetch(
      `http://localhost:8080/waitsys/waitstaff/modify_order_item_is_serve?orderItemId=${orderItemId}`,
      {
        method: "POST",
      }
    )
      .then(() => {
        console.log(`itemId ${orderItemId} is served`);
        message.success("Dish served");
      })
      .catch((error) => {
        console.error(`Error posting for itemId ${orderItemId}:`, error);
      });
  };

  // Function to handle "Show Dishes" button click and fetch previous items
  const handleShowPreviousItems = () => {
    fetch(
      `http://localhost:8080/waitsys/customer/order/showAllPreviousItems?tableId=${tableId}`
    )
      .then((response) => response.json())
      .then((data) => {
        // Process the data and display the popup window
        console.log(data); // Replace with the code to process the data

        // Show the popup window
        setPopupData(data);
        setOpenPopup(true);
      })
      .catch((error) => {
        console.error("Error fetching previous items:", error);
      });
  };

  // Columns for the popup table
  const columns = [
    {
      title: "Dish",
      dataIndex: "itemName",
      key: "itemName",
    },
    {
      title: "Quantity",
      dataIndex: "itemNumber",
      key: "itemNumber",
    },
    {
      title: "Total Price",
      dataIndex: "totalPrice",
      key: "totalPrice",
    },
  ];

  return (
    <Card
      title={`Table ${tableId}`}
      style={{ width: 440, height: 400 }}
      hoverable={true}
    >
      {/* Buttons for "Notify Assistance", "Request Bill", and "Show Dishes" */}
      <Row justify="space-between" align="middle">
        <Space size={110}>
          <Button
            icon={<BellOutlined className={needHelp === 1 ? "shake" : ""} />}
            onClick={handleNotifyAssistance}
            style={{ backgroundColor: needHelp === 1 ? "yellow" : "" }}
          />
          <Button
            icon={
              <DollarCircleOutlined className={state === 2 ? "shake" : ""} />
            }
            onClick={handleRequestBill}
            style={{ backgroundColor: state === 2 ? "yellow" : "" }}
          />
          <Button onClick={handleShowPreviousItems}>Show Dishes</Button>
        </Space>
      </Row>

      {/* List of order items */}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {currentItems.map((item) => (
          <li key={item.id} style={{ display: "flex", alignItems: "center" }}>
            <span>{item.itemName}</span>
            <Space align="end" style={{ marginLeft: "auto" }}>
              {item.isCook === 1 ? (
                <CoffeeOutlined style={{ color: "#52c41a" }} />
              ) : (
                <CoffeeOutlined style={{ color: "red" }} />
              )}
              <Button
                type={item.isServe ? "primary" : ""}
                onClick={() => handleSend(item.id)}
                style={{
                  borderRadius: "50%",
                  width: "24px",
                  height: "24px",
                  border: "1px solid red",
                  backgroundColor: item.isServe ? "#52c41a" : "red",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                }}
                icon={<CheckOutlined style={{ fontSize: "12px" }} />}
              />
            </Space>
          </li>
        ))}
      </ul>

      {/* Popup modal for showing previous items */}
      <Modal
        open={openPopup}
        onCancel={() => setOpenPopup(false)}
        footer={null}
      >
        <Table
          columns={columns}
          dataSource={popupData}
          pagination={{ pageSize: 10 }}
          rowKey="itemId"
        />
      </Modal>
      <div style={{ position: "absolute", bottom: 16, left: "50%", transform: "translateX(-50%)" }}>
        <Pagination
          simple
          current={currentPage}
          pageSize={itemsPerPage}
          total={filteredOrderItemList.length}
          onChange={handlePageChange}
          style={{ textAlign: "center" }} 
        />
      </div>
    </Card>
  );
};

export default WSCard;
