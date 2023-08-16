import React, { useState } from "react";
import { List, Divider, Button, Rate, message } from "antd";
import "./CustomerRate.css";

// Rate function. Using when customer fisnish the meal.
const CustomerRate = ({ data, tableId, orderIds }) => {
  const [showThanks, setShowThanks] = useState(false); 
  
  // Need to post rate to backend with specific formatting.
  // Initalizate the data structure here. 
  const [rateList, setRateList] = useState(
    data.map((item) => ({
      itemId: item.id,
      rate: 0,
    }))
  );

  // Trigger when user finish rating.
  // Compare user given rating to the props and change it if there exist a new user rating. 
  const handleRateChange = (itemId, value) => {
    setRateList(
      rateList.map((rateItem) =>
        rateItem.itemId === itemId ? { ...rateItem, rate: value } : rateItem
      )
    );
  };

  // post rating information to the backend.
  const handleSubmit = async () => {
    try {
      const itemRatings = rateList.reduce((accumulator, { itemId, rate }) => {
        accumulator[itemId] = rate;
        return accumulator;
      }, {});
      const bodyMessage = JSON.stringify({
        tableId,
        orderIds,
        itemRatings,
      });
      const response = await fetch(
        `http://localhost:8080/waitsys/customer/order/rating`,
        {
          method: "POST",
          headers: {
            "Content-type": "application/json",
          },
          body: bodyMessage,
        }
      );
      if (response.status === 200) {
        setShowThanks(true);
        message.success("Rate Succefffully!");
      } else {
        throw new Error("Error Finish Current Order");
      }
    } catch (error) {
      console.log("Error:", error);
    }
  };

  return (
    <>
      <div>Table {tableId}</div>
      <Divider />
      <div >{showThanks ? (
        <div className="centered-message">    
        <p >Thanks for rating!</p>    
        </div>
      ) : (
        <div>
          <List
        dataSource={data}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              avatar={
                <img
                  src={`data:image/jpeg;base64, ${item.picture}`}
                  style={{ width: 50, height: 50 }}
                />
              }
              title={item.title}
            ></List.Item.Meta>
            <Rate
              allowHalf={true}
              onChange={(value) => handleRateChange(item.id, value)}
            />
          </List.Item>
        )}
      />
      </div>
      )}</div>
      <Button
        type="primary"
        onClick={handleSubmit}
        className={showThanks ? "hide-button" : ""}
      >
        {//After user submit rating, show thanks information.
        }
        Submit Rating
      </Button>
    </>
  );
};
export default CustomerRate;
