import * as React from "react";
import { Button, Card, Divider, message } from "antd";

const CustomerDetailedDish = ({ itemId, tableId, orderId }) => {
  // Define the state of detail dish using hooks.
  const [id, setId] = React.useState();
  const [title, setTitle] = React.useState();
  const [description, setDescription] = React.useState();
  const [ingredient, setIngredient] = React.useState();
  const [price, setPrice] = React.useState();
  const [picture, setPicture] = React.useState();

  // fetch data when itemId changes
  React.useEffect(() => {
    fetchData(itemId);
  }, [itemId]);

  // Add the dish to the current shopping cart
  const addDishMethod = () => {
    const response = fetch(
      `http://localhost:8080/waitsys/customer/order/addItem?tableId=${parseInt(
        tableId
      )}&orderId=${parseInt(orderId)}&itemId=${parseInt(itemId)}`,
      {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
      }
    )
      .then((response) => {
        if (response.status === 200) {
          message.success("Dish added successfully!");
          onClose();
        } else {
          throw new Error("Error adding dish");
        }
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  };

  // Fetch data again when id changes. it can helps us to  re-render without close and open it again.
  const fetchData = async (itemId) => {
    try {
      const response = await fetch(
        `http://localhost:8080/waitsys/manager/item/showById?itemId=${itemId}`,
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      const data = await response.json();

      // set the detail dish props.
      setId(data["itemId"]);
      setTitle(data["name"]);
      setDescription(data["description"]);
      setIngredient(data["ingredient"]);
      setPrice(data["price"]);
      setPicture(`data:image/jpeg;base64, ${data.picture}`);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    // Render detailed dish information by specifc format.
    <Card title={<strong style={{ fontSize: "24px" }}>{title}</strong>} bordered={false}>
      <img
        alt="image"
        src={picture}
        style={{ width: "100%", height: 320 }}
      />
      <div style={{ padding: "16px", textAlign: "left" }}>
        <div style={{ display: "flex", alignItems: "center" }}>
          <strong style={{ flex: "0 0 120px", marginRight: "8px" }}>Description:</strong>
          <p>{description}</p>
        </div>
        <Divider style={{ margin: "8px 0" }} />
        <div style={{ display: "flex", alignItems: "center" }}>
          <strong style={{ flex: "0 0 120px", marginRight: "8px" }}>Ingredients:</strong>
          <p>{ingredient}</p>
        </div>
        <Divider style={{ margin: "8px 0" }} />
        <div style={{ display: "flex", alignItems: "center" }}>
          <strong style={{ flex: "0 0 120px", marginRight: "8px" }}>Price:</strong>
          <p>{price}</p>
        </div>
        <Divider style={{ margin: "8px 0" }} />
        <Button onClick={() => addDishMethod()}>Add Dish</Button>
      </div>
    </Card>
  );
};

export default CustomerDetailedDish;
