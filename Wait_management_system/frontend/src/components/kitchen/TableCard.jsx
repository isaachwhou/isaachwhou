import { Card } from "antd";
import React, { useState } from "react";
import { CheckOutlined, CloseOutlined } from "@ant-design/icons";
import { Space, Switch, Button, Popconfirm, Pagination, message } from "antd";
const { Meta } = Card;

const TableCard = ({ tableId, orderItems, orderId, startTime }) => {
  // Generate the title for the table card
  const tableTitle = "Table " + tableId.toString();

  // State to track if the order is finished
  const [isOrderFinished, setIsOrderFinished] = useState(false);

  // State to track the current page of displayed items
  const [currentPage, setCurrentPage] = useState(1);

  // Number of items to display per page
  const pageSize = 8;

  // Calculate the start and end index of displayed items on the current page
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = currentPage * pageSize;

  // Get the items to display on the current page
  const displayedItems = orderItems.slice(startIndex, endIndex);

  // Format the order start time as a string
  const timeString =
    "Order Time: " +
    new Date(startTime).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });

  // Function to handle the switch change event and update the item status
  const onChange = (checked, id) => {
    console.log(`switch to ${checked}`);
    Switch_Cooked(id);
  };

  // Function to update the status of the item as cooked
  async function Switch_Cooked(orderItemId) {
    const response = await fetch(
      `http://localhost:8080/waitsys/kitchen/modify_order_item_is_cook?orderItemId=${orderItemId}`,
      {
        method: "POST",
      }
    );
    const data = await response.json();
  }

  // Function to finish the order and update the order status
  async function Finish_Order(orderId) {
    const response = await fetch(
      `http://localhost:8080/waitsys/kitchen/modify_order_is_cook?orderId=${orderId}`,
      {
        method: "POST",
      }
    );
    const data = await response.json();
  }

  // Confirm function for finishing the order with a popconfirm
  const confirm = (id) => {
    Finish_Order(id);
    message.success("Finish Order");
    setIsOrderFinished(true);
  };

  // Cancel function for the popconfirm
  const cancel = (e) => {
    console.log(e);
  };

  return (
    <>
      {!isOrderFinished && (
        <Card
          title={tableTitle}
          style={{ height: "65vh", position: "relative", overflow: "auto" }}
          hoverable={true}
        >
          <Meta description={timeString} />
          {displayedItems.map((item) => (
            <div
              key={`item-${item.id}`}
              style={{
                display: "flex",
                marginTop: 12,
              }}
            >
              <Space size={8} key={`item-${item.id}`}>
                {item.itemName}
                <Switch
                  checkedChildren={<CheckOutlined />}
                  unCheckedChildren={<CloseOutlined />}
                  onChange={(checked) => onChange(checked, item.id)}
                  defaultChecked={item.isCook}
                />
              </Space>
            </div>
          ))}
          <div
            style={{
              position: "absolute",
              bottom: 10,
              left: "50%",
              transform: "translateX(-50%)",
            }}
          >
            {orderItems.length > pageSize && (
              <div style={{ textAlign: "center" }}>
                {/* Pagination for displayed items */}
                <Pagination
                  current={currentPage}
                  pageSize={pageSize}
                  total={orderItems.length}
                  onChange={setCurrentPage}
                  style={{ display: "inline-block", marginTop: 12 }}
                  responsive={true}
                />
              </div>
            )}
            <div style={{ textAlign: "center" }}>
              {/* Popconfirm for finishing the order */}
              <Popconfirm
                title="Finish Order?"
                description="Are you sure to Finish this order?"
                onConfirm={() => confirm(orderId)}
                onCancel={cancel}
                okText="Yes"
                cancelText="No"
              >
                <Button
                  type="primary"
                  shape="round"
                  style={{ backgroundColor: "green" }}
                >
                  Finish Order
                </Button>
              </Popconfirm>
            </div>
          </div>
        </Card>
      )}
    </>
  );
};

export default TableCard;
